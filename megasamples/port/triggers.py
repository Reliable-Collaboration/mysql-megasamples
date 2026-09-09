"""Port a database's triggers, and the ON UPDATE CURRENT_TIMESTAMP columns, to PostgreSQL and SQLite.

MySQL trigger bodies in this corpus are one of two shapes -- a single `SET NEW.col = expr`, or a
BEGIN ... END block of DML statements and IF ... THEN ... END IF blocks -- and every expression in
them goes through the statement translator. What each target does with them:

PostgreSQL  a trigger function in PL/pgSQL (`NEW.col := expr;`, IF blocks as they are, DML as
            translated, RETURN NEW/OLD) and a CREATE TRIGGER with the same timing and event.
SQLite      a trigger whose body is DML. A BEFORE trigger that assigns NEW.col becomes an AFTER
            trigger updating the row by rowid, since SQLite triggers cannot modify NEW; a body that
            is one IF around DML becomes a WHEN clause; an IF among other statements has its
            condition pushed into that statement's WHERE. A BEFORE INSERT that assigns a primary-key
            column is Unportable: the row must carry the key before any SQLite trigger can run.

ON UPDATE CURRENT_TIMESTAMP is emulated on both targets with a trigger that fires only when some
other column of the row changes and the timestamp column was not set explicitly -- MySQL's rule.
"""
import re

from megasamples.port import sqltranslate
from megasamples.port.ddl import short_name

NAMES = {}          # database name -> sqltranslate.names_of(database), set by render()


class Unportable(sqltranslate.Unportable):
    pass


# --- parsing the MySQL body ----------------------------------------------------------------------
def _split_statements(text):
    """Top-level statements of a body, respecting strings and IF ... END IF nesting."""
    out, buf, depth, quote, i = [], [], 0, None, 0
    low = text.lower()
    while i < len(text):
        ch = text[i]
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in ("'", '"', "`"):
            quote = ch; buf.append(ch); i += 1; continue
        if re.match(r"\bif\b", low[i:i + 3]) and (i == 0 or not low[i - 1].isalnum()) and not low[i - 4:i].endswith("end "):
            depth += 1
        if low.startswith("end if", i) and (i == 0 or not low[i - 1].isalnum()):
            depth -= 1
        if ch == ";" and depth == 0:
            out.append("".join(buf).strip()); buf = []; i += 1; continue
        buf.append(ch); i += 1
    tail = "".join(buf).strip()
    if tail:
        out.append(tail)
    return [s for s in out if s]


def parse_body(body):
    """[statement] where a statement is ('set', col, expr) | ('if', cond, [statements]) | ('dml', sql)."""
    text = body.strip()
    if re.match(r"(?is)^begin\b", text):
        text = re.sub(r"(?is)^begin\b", "", text, count=1)
        text = re.sub(r"(?is)\bend\s*;?\s*$", "", text, count=1)
    out = []
    for st in _split_statements(text):
        m = re.match(r"(?is)^set\s+new\.`?(\w+)`?\s*=\s*(.+)$", st)
        if m:
            out.append(("set", m.group(1), m.group(2).strip())); continue
        m = re.match(r"(?is)^if\s+(.+?)\s+then\s+(.+?)\s*end\s+if$", st)
        if m:
            out.append(("if", m.group(1).strip(), parse_body(m.group(2)))); continue
        if re.match(r"(?is)^(insert|update|delete)\b", st):
            out.append(("dml", st)); continue
        raise Unportable(f"trigger statement not understood: {st[:60]!r}")
    return out


def _expr(expr, dialect, schema, condition=False):
    """A MySQL expression -> the dialect, through the statement translator."""
    return sqltranslate.translate(f"SELECT {expr}", dialect, schema, names=NAMES.get(schema),
                                  condition=condition)[len("SELECT "):]


def _rowvars(sql, dialect):
    """NEW/OLD references as the target writes them."""
    if dialect == "postgres":
        return re.sub(r'"(new|old)"\.', lambda m: m.group(1).upper() + ".", sql, flags=re.I)
    return re.sub(r'"(new|old)"\.', lambda m: m.group(1).upper() + ".", sql, flags=re.I)


# --- PostgreSQL -----------------------------------------------------------------------------------
def _pg_statements(statements, dialect, schema, out):
    for st in statements:
        if st[0] == "set":
            out.append(f'  NEW."{st[1]}" := {_rowvars(_expr(st[2], "postgres", schema), "postgres")};')
        elif st[0] == "if":
            out.append(f'  IF {_rowvars(_expr(st[1], "postgres", schema, condition=True), "postgres")} THEN')
            _pg_statements(st[2], dialect, schema, out)
            out.append("  END IF;")
        else:
            out.append("  " + _rowvars(sqltranslate.translate(st[1], "postgres", schema, names=NAMES.get(schema)), "postgres") + ";")


def postgres_trigger(trigger, schema):
    statements = parse_body(trigger.body)
    lines = []
    _pg_statements(statements, "postgres", schema, lines)
    fn = short_name(f"{trigger.table}_{trigger.name}_fn")
    returns = "RETURN OLD;" if trigger.event == "DELETE" else "RETURN NEW;"
    body = "\n".join(lines)
    return [f'CREATE FUNCTION "{fn}"() RETURNS trigger LANGUAGE plpgsql AS $$\nBEGIN\n{body}\n  {returns}\nEND $$;',
            f'CREATE TRIGGER "{short_name(trigger.name)}" {trigger.timing} {trigger.event} ON "{trigger.table}" '
            f'FOR EACH ROW EXECUTE FUNCTION "{fn}"();']


def postgres_on_update(table, column, columns):
    fn = short_name(f"{table}_{column}_on_update_fn")
    return [f'CREATE FUNCTION "{fn}"() RETURNS trigger LANGUAGE plpgsql AS $$\nBEGIN\n'
            f'  IF NEW."{column}" IS NOT DISTINCT FROM OLD."{column}" THEN NEW."{column}" := CURRENT_TIMESTAMP; END IF;\n'
            f'  RETURN NEW;\nEND $$;',
            f'CREATE TRIGGER "{short_name(f"{table}_{column}_on_update")}" BEFORE UPDATE ON "{table}" FOR EACH ROW '
            f'WHEN (OLD.* IS DISTINCT FROM NEW.*) EXECUTE FUNCTION "{fn}"();']


# --- SQLite ---------------------------------------------------------------------------------------
def _push_condition(sql, cond):
    """DML with a WHEN condition folded into it, for an IF among other statements."""
    low = sql.lower()
    if low.startswith("insert"):
        raise Unportable("an IF around an INSERT among other statements")
    if " where " in low:
        i = low.rfind(" where ")
        return sql[:i] + f" WHERE ({sql[i + 7:]}) AND ({cond})"
    return f"{sql} WHERE ({cond})"


def sqlite_trigger(trigger, table_model, schema):
    statements = parse_body(trigger.body)
    pk = {c for c, _ in (table_model.primary_key.columns if table_model.primary_key else [])}
    body, when = [], None
    timing, event = trigger.timing, trigger.event
    sets = [st for st in statements if st[0] == "set"] + [s for st in statements if st[0] == "if" for s in st[2] if s[0] == "set"]
    if sets:
        if event == "INSERT" and any(st[1] in pk for st in sets):
            raise Unportable(f"assigns primary-key column {[st[1] for st in sets if st[1] in pk][0]} before insert; "
                             "a SQLite trigger cannot modify NEW and the row must carry its key first")
        timing = "AFTER"                      # SQLite triggers cannot modify NEW: update the row afterwards
    if len(statements) == 1 and statements[0][0] == "if":
        when = _rowvars(_expr(statements[0][1], "sqlite", schema), "sqlite")
        statements = statements[1][2] if False else statements[0][2]
    for st in statements:
        if st[0] == "set":
            body.append(f'  UPDATE "{trigger.table}" SET "{st[1]}" = {_rowvars(_expr(st[2], "sqlite", schema), "sqlite")} '
                        f'WHERE rowid = NEW.rowid;')
        elif st[0] == "if":
            cond = _rowvars(_expr(st[1], "sqlite", schema), "sqlite")
            for inner in st[2]:
                if inner[0] == "set":
                    body.append(f'  UPDATE "{trigger.table}" SET "{inner[1]}" = {_rowvars(_expr(inner[2], "sqlite", schema), "sqlite")} '
                                f'WHERE rowid = NEW.rowid AND ({cond});')
                elif inner[0] == "dml":
                    body.append("  " + _push_condition(_rowvars(sqltranslate.translate(inner[1], "sqlite", schema, names=NAMES.get(schema)), "sqlite"), cond) + ";")
                else:
                    raise Unportable("an IF nested inside an IF")
        else:
            body.append("  " + _rowvars(sqltranslate.translate(st[1], "sqlite", schema, names=NAMES.get(schema)), "sqlite") + ";")
    when_clause = f"\nWHEN {when}" if when else ""
    return [f'CREATE TRIGGER "{trigger.name}" {timing} {event} ON "{trigger.table}" FOR EACH ROW{when_clause}\nBEGIN\n'
            + "\n".join(body) + "\nEND;"]


def sqlite_on_update(table, column, columns):
    others = [c for c in columns if c != column]
    changed = " OR ".join(f'NEW."{c}" IS NOT OLD."{c}"' for c in others) or "0"
    return [f'CREATE TRIGGER "{table}_{column}_on_update" AFTER UPDATE ON "{table}" FOR EACH ROW\n'
            f'WHEN NEW."{column}" IS OLD."{column}" AND ({changed})\nBEGIN\n'
            f'  UPDATE "{table}" SET "{column}" = CURRENT_TIMESTAMP WHERE rowid = NEW.rowid;\nEND;']


# --- the port -------------------------------------------------------------------------------------
def insert_defaults(database):
    """{(table, column): "CURRENT_TIMESTAMP"} for every column a BEFORE INSERT trigger sets to the
    current time: what a SQLite column needs as its default, since the trigger can only run after."""
    out = {}
    for tr in database.triggers:
        if tr.timing != "BEFORE" or tr.event != "INSERT":
            continue
        try:
            statements = parse_body(tr.body)
        except Unportable:
            continue
        for st in statements:
            if st[0] == "set" and st[2].strip().lower() in ("now()", "current_timestamp", "current_timestamp()", "sysdate()"):
                out[(tr.table, st[1])] = "CURRENT_TIMESTAMP"
    return out


def render(database, dialect):
    """([statements], dropped) for every trigger and every ON UPDATE CURRENT_TIMESTAMP column."""
    statements, dropped = [], []
    NAMES[database.name] = sqltranslate.names_of(database)
    tables = {t.name: t for t in database.tables}
    for t in database.tables:
        for c in t.columns:
            if c.on_update_now:
                cols = [x.name for x in t.columns]
                statements += (postgres_on_update(t.name, c.name, cols) if dialect == "postgres"
                               else sqlite_on_update(t.name, c.name, cols))
    for tr in database.triggers:
        try:
            if dialect == "postgres":
                statements += postgres_trigger(tr, database.name)
            else:
                statements += sqlite_trigger(tr, tables[tr.table], database.name)
        except sqltranslate.Unportable as exc:
            dropped.append(f"trigger {tr.name}: {exc}")
    return statements, dropped
