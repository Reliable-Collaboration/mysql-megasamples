"""Port a database's stored routines to PostgreSQL, deterministically, over a closed census.

MySQL's procedural SQL and PL/pgSQL are different languages. What makes a translator tractable is
that the corpus's 42 routines use a small, fixed set of constructs -- DECLARE, SET, SELECT INTO,
IF/ELSEIF, CASE, RETURN, INSERT/UPDATE/DELETE, CALL, temporary tables, two kinds of handler, LEAVE,
a transaction pair, user variables -- and every SQL statement and expression inside them goes
through the statement translator (sqltranslate.py). Anything outside the census raises Unportable,
which the port records by name; nothing is emitted on a guess.

What PostgreSQL makes of each kind of routine:
  FUNCTION                                a PL/pgSQL function; tinyint(1) results become boolean
  PROCEDURE with OUT/INOUT, no result set a PL/pgSQL procedure (OUT parameters, PostgreSQL 14+)
  PROCEDURE returning a result set        a function RETURNS TABLE(...), its columns inferred by
                                          replaying the body in a probe transaction on the build
                                          server (RETURN QUERY for the SELECT); a procedure that
                                          also has OUT parameters loses them, which is recorded,
                                          because a function cannot return both

Rules for what has no direct counterpart:
  EXIT HANDLER FOR SQLEXCEPTION BEGIN ... END  EXCEPTION WHEN OTHERS THEN ...
  EXIT HANDLER FOR NOT FOUND RETURN NULL       dropped: SELECT INTO leaves the variable NULL already
  START TRANSACTION / COMMIT / ROLLBACK        dropped: the caller's transaction, rolled back on error
  SET @user_var = expr                         PERFORM set_config('megasamples.user_var', ...)
  LEAVE label                                  RETURN
  SELECT 'literal' as a message                RAISE NOTICE
  CREATE TEMPORARY TABLE (cols, KEY (...))     CREATE TEMP TABLE with the types mapped, index apart
  ELSEIF                                       ELSIF
"""
import re

from megasamples.port import sqltranslate, typemap
from megasamples.port.model import Column


class Unportable(sqltranslate.Unportable):
    pass


# --- types ---------------------------------------------------------------------------------------
TYPE_SYNONYMS = {"integer": "int", "int4": "int", "int8": "bigint", "dec": "decimal", "numeric": "decimal",
                 "fixed": "decimal", "bool": "tinyint", "boolean": "tinyint", "character": "char"}

def column_for(mysql_type, name="_"):
    """A Column carrying just what typemap needs, from a MySQL type string such as decimal(19,4)."""
    t = mysql_type.strip().lower()
    base = re.match(r"^([a-z]+)", t).group(1)
    base = TYPE_SYNONYMS.get(base, base)
    if base == "tinyint" and t in ("bool", "boolean"):
        t = "tinyint(1)"
    m = re.search(r"\((\d+)(?:,(\d+))?\)", t)
    a = int(m.group(1)) if m else None
    b = int(m.group(2)) if m and m.group(2) else None
    return Column(name=name, data_type=base, column_type=t, nullable=True, default=None, extra="", generation=None,
                  char_len=a if base in ("char", "varchar", "binary", "varbinary") else None,
                  precision=a if base == "decimal" else None, scale=b if base == "decimal" else None,
                  fsp=a if base in ("datetime", "timestamp", "time") else None, charset=None, collation=None, ordinal=0)


def pg_type(mysql_type, boolean_for_tinyint1=False):
    if boolean_for_tinyint1 and mysql_type.strip().lower() in ("tinyint(1)", "boolean", "bool"):
        return "boolean"
    return typemap.postgres(column_for(mysql_type))


# --- lexing the body -----------------------------------------------------------------------------
def strip_comments(text):
    out, i, n, quote = [], 0, len(text), None
    while i < n:
        ch = text[i]
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            i += 1
        elif ch in ("'", '"', "`"):
            quote = ch; out.append(ch); i += 1
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2); i = n if j < 0 else j + 2; out.append(" ")
        elif text.startswith("-- ", i) or ch == "#":
            j = text.find("\n", i); i = n if j < 0 else j
        else:
            out.append(ch); i += 1
    return "".join(out)


BLOCK_END_WORDS = ("if", "case", "loop", "while", "repeat")
STATEMENT_STARTERS = (None, ";", "then", "else", "begin", "do", ":")


def tokens(text):
    """(position, kind, value) for words, quoted strings and single punctuation characters."""
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1; continue
        if ch in ("'", '"', "`"):
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2; continue
                if text[j] == ch:
                    if j + 1 < n and text[j + 1] == ch:      # a doubled quote inside the string
                        j += 2; continue
                    break
                j += 1
            yield i, "string", text[i:j + 1]; i = j + 1; continue
        if ch.isalpha() or ch == "_" or ch == "@":
            j = i + 1
            while j < n and (text[j].isalnum() or text[j] in "_@"):
                j += 1
            yield i, "word", text[i:j].lower(); i = j; continue
        yield i, "punct", ch; i += 1


def scan(text):
    """Every token with the block depth before it. A block opens at BEGIN, at CASE (statement or
    expression, both close with END), and at IF/WHILE/LOOP/REPEAT when they start a statement --
    so IF(x, a, b), DROP TABLE IF EXISTS and REPEAT('0', n) are not blocks; it closes at END, whose
    trailing IF/CASE/LOOP/WHILE/REPEAT is part of the closer."""
    depth, prev, skip_next = 0, None, False
    for pos, kind, value in tokens(text):
        if skip_next:
            skip_next = False
            if kind == "word" and value in BLOCK_END_WORDS:
                prev = value; continue
        yield pos, kind, value, depth
        if kind == "word":
            if value == "end":
                depth -= 1; skip_next = True
            elif value in ("begin", "case"):
                depth += 1
            elif value in ("if", "while", "loop", "repeat") and prev in STATEMENT_STARTERS:
                depth += 1
        prev = value if kind != "string" else "'"


def split_statements(text):
    """Top-level statements, with IF/CASE/BEGIN/WHILE/LOOP/REPEAT blocks kept whole."""
    out, start = [], 0
    for pos, kind, value, depth in scan(text):
        if kind == "punct" and value == ";" and depth == 0:
            out.append(text[start:pos].strip()); start = pos + 1
    tail = text[start:].strip()
    if tail:
        out.append(tail)
    return [s for s in out if s]


def split_branches(body):
    """The branches of an IF body: [(None, then_statements), (cond, elseif_statements)..., (None, else)]."""
    marks = [(pos, value) for pos, kind, value, depth in scan(body)
             if kind == "word" and depth == 0 and value in ("elseif", "else")]
    out, start, cond = [], 0, None
    for pos, w in marks:
        out.append((cond, body[start:pos]))
        if w == "else":
            cond, start = None, pos + 4
        else:
            m = re.match(r"(?is)elseif\s+(.+?)\s+then\s", body[pos:])
            if not m:
                raise Unportable("ELSEIF without THEN")
            cond, start = m.group(1), pos + m.end()
    out.append((cond, body[start:]))
    return out


# --- the translator ------------------------------------------------------------------------------
class Translator:
    def __init__(self, routine, database, extra):
        self.r, self.db, self.extra = routine, database, extra
        self.names = sqltranslate.names_of(database)
        self.schema = database.name
        self.declares = []          # PL/pgSQL DECLARE lines
        self.notes = []             # what was changed and why
        self.result_sets = 0        # bare SELECTs (a procedure returning rows)
        self.handler = None         # EXCEPTION block lines
        self.variables = {p[1].lower() for p in routine.params}
        self.var_types = {p[1]: pg_type(p[2]) for p in routine.params}
        self.temp_tables = []       # statements that create temp tables, for the result-type probe
        self.select_for_probe = None

    def expr(self, text, condition=False):
        return sqltranslate.translate(f"SELECT {text}", "postgres", self.schema, self.extra,
                                      self.names, self.variables, condition=condition)[len("SELECT "):]

    def sql(self, text):
        return sqltranslate.translate(text, "postgres", self.schema, self.extra, self.names, self.variables)

    def statements(self, text, out, depth=1):
        pad = "  " * depth
        for st in split_statements(text):
            low = st.lower()
            if re.match(r"^declare\s+(exit|continue)\s+handler", low):
                self.handler_of(st); continue
            if low.startswith("declare "):
                self.declare(st); continue
            m = re.match(r"(?is)^set\s+@(\w+)\s*=\s*(.+)$", st)
            if m:
                out.append(f"{pad}PERFORM set_config('megasamples.{m.group(1)}', ({self.expr(m.group(2))})::text, false);")
                self.notes.append(f"SET @{m.group(1)} became set_config('megasamples.{m.group(1)}')")
                continue
            m = re.match(r"(?is)^set\s+(\w+)\s*=\s*(.+)$", st)
            if m:
                out.append(f"{pad}{m.group(1)} := {self.expr(m.group(2))};"); continue
            m = re.match(r"(?is)^return\s+(.+)$", st)
            if m:
                out.append(f"{pad}RETURN {self.expr(m.group(1))};"); continue
            m = re.match(r"(?is)^if\s+(.+?)\s+then\s+(.*)\s*end\s+if$", st)
            if m:
                self.if_block(m.group(1), m.group(2), out, depth); continue
            m = re.match(r"(?is)^leave\s+\w+$", st)
            if m:
                out.append(f"{pad}RETURN;"); continue
            if low in ("start transaction", "commit", "rollback", "begin"):
                self.notes.append(f"{st.upper()} dropped: the procedure runs in the caller's transaction, rolled back on error")
                continue
            m = re.match(r"(?is)^call\s+`?(\w+)`?\s*\((.*)\)$", st)
            if m:
                args = self.expr(m.group(2)) if m.group(2).strip() else ""
                out.append(f'{pad}CALL "{m.group(1)}"({args});'); continue
            m = re.match(r"(?is)^create\s+temporary\s+table\s+`?(\w+)`?\s*\((.*)\)$", st)
            if m:
                self.temp_table(m.group(1), m.group(2), out, pad); continue
            m = re.match(r"(?is)^drop\s+table\s+(if\s+exists\s+)?`?(\w+)`?$", st)
            if m:
                out.append(f'{pad}DROP TABLE {"IF EXISTS " if m.group(1) else ""}{m.group(2).lower()};'); continue
            if re.match(r"(?is)^(insert|update|delete)\b", st):
                out.append(pad + self.sql(st) + ";"); continue
            if re.match(r"(?is)^(select|with)\b", st):
                self.select(st, out, pad); continue
            raise Unportable(f"statement outside the census: {st[:50]!r}")

    def declare(self, st):
        m = re.match(r"(?is)^declare\s+([\w,\s]+?)\s+([a-z]+(?:\s*\([\d,\s]+\))?(?:\s+unsigned)?)\s*(?:default\s+(.+))?$", st)
        if not m:
            raise Unportable(f"DECLARE not understood: {st[:50]!r}")
        names = [n.strip() for n in m.group(1).split(",")]
        ptype = pg_type(m.group(2))
        default = f" := {self.expr(m.group(3))}" if m.group(3) else ""
        for n in names:
            self.declares.append(f"  {n} {ptype}{default};")
            self.variables.add(n.lower())
            self.var_types[n] = ptype

    def handler_of(self, st):
        m = re.match(r"(?is)^declare\s+exit\s+handler\s+for\s+not\s+found\s+return\s+null$", st)
        if m:
            self.notes.append("EXIT HANDLER FOR NOT FOUND RETURN NULL dropped: SELECT INTO leaves the variable NULL")
            return
        m = re.match(r"(?is)^declare\s+exit\s+handler\s+for\s+sqlexception\s+begin\s+(.*)\s*end$", st)
        if m:
            lines = []
            self.statements(m.group(1), lines, depth=2)
            self.handler = lines or ["    NULL;"]
            return
        raise Unportable(f"handler outside the census: {st[:50]!r}")

    def if_block(self, cond, body, out, depth):
        pad = "  " * depth
        branches = split_branches(body)          # [(condition | None, statements)]
        first = True
        for c, b in branches:
            if first:
                out.append(f"{pad}IF {self.expr(cond, condition=True)} THEN"); first = False
            elif c is None:
                out.append(f"{pad}ELSE")
            else:
                out.append(f"{pad}ELSIF {self.expr(c, condition=True)} THEN")
            n = len(out)
            self.statements(b, out, depth + 1)
            if len(out) == n:
                out.append(f"{pad}  NULL;")
        out.append(f"{pad}END IF;")

    def temp_table(self, name, cols, out, pad):
        columns, keys = [], []
        for part in _split_top(cols, ","):
            p = part.strip()
            m = re.match(r"(?is)^(?:key|index)\s*\(([^)]*)\)$", p)
            if m:
                keys.append([c.strip().strip("`") for c in m.group(1).split(",")]); continue
            m = re.match(r"(?is)^(?:primary\s+key)\s*\(([^)]*)\)$", p)
            if m:
                columns.append(f"PRIMARY KEY ({', '.join(c.strip().strip(chr(96)).lower() for c in m.group(1).split(','))})"); continue
            m = re.match(r"(?is)^`?(\w+)`?\s+([a-z]+(?:\s*\([\d,\s]+\))?(?:\s+unsigned)?)(.*)$", p)
            if not m:
                raise Unportable(f"temporary table column not understood: {p[:40]!r}")
            tail = m.group(3)
            attrs = (" NOT NULL" if re.search(r"(?i)\bnot\s+null\b", tail) else "") + (" PRIMARY KEY" if re.search(r"(?i)\bprimary\s+key\b", tail) else "")
            columns.append(f'{m.group(1).lower()} {pg_type(m.group(2))}{attrs}')
        # unquoted and lower-cased, like every reference to it after PostgreSQL's folding
        name = name.lower()
        stmt = f'CREATE TEMP TABLE {name} ({", ".join(columns)});'
        out.append(pad + stmt)
        self.temp_tables.append(stmt)
        for i, k in enumerate(keys):
            idx = f'CREATE INDEX {name}_key{i + 1} ON {name} ({", ".join(c.lower() for c in k)});'
            out.append(pad + idx)
            self.temp_tables.append(idx)

    def select(self, st, out, pad):
        # SELECT ... INTO variables, with the INTO anywhere MySQL allows it
        m = re.search(r"(?is)\binto\s+((?:\w+\s*,\s*)*\w+)\s*(?=\bfrom\b|$)", st)
        if m and all(v.strip().lower() in self.variables for v in m.group(1).split(",")):
            targets = ", ".join(v.strip() for v in m.group(1).split(","))
            query = self.sql((st[:m.start()] + " " + st[m.end():]).strip())
            out.append(f"{pad}{query} INTO {targets};")
            return
        # a literal message, in a routine that returns rows: a notice
        m = re.match(r"(?is)^select\s+'((?:[^']|'')*)'$", st)
        if m:
            out.append(f"{pad}RAISE NOTICE '%', '{m.group(1)}';")
            self.notes.append(f"SELECT '{m.group(1)[:30]}' became RAISE NOTICE")
            return
        # a result set
        query = self.sql(st)
        if re.search(r"(?is)\bwith\b", query[:10]) and not re.search(r"(?is)\bwith\s+recursive\b", query[:20]):
            name = re.match(r"(?is)^with\s+\"?(\w+)\"?", query)
            if name and re.search(r'(?i)\bfrom\s+"?' + re.escape(name.group(1)) + r'"?\b', query[query.lower().find(" as "):]):
                query = "WITH RECURSIVE" + query[4:]
        self.result_sets += 1
        if self.select_for_probe is None:
            self.select_for_probe = query
        out.append(f"{pad}RETURN QUERY {query};")

    def probe_select(self):
        """The result-set SELECT with every variable replaced by a typed NULL, for `\\gdesc`."""
        text = self.select_for_probe
        for name, ptype in sorted(self.var_types.items(), key=lambda kv: -len(kv[0])):
            text = re.sub(rf"(?<![\w\"]){re.escape(name)}(?![\w\"])", f"(NULL::{ptype})", text, flags=re.I)
        return text


def _split_top(text, sep):
    out, buf, depth, quote = [], [], 0, None
    for ch in text:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"', "`"):
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            out.append("".join(buf)); buf = []
        else:
            buf.append(ch)
    out.append("".join(buf))
    return out


class NotProbed(Exception):
    """A procedure returns rows and its result columns have not been measured yet."""


def translate_routine(routine, database, result_columns, probe=None):
    """(statement, notes). A procedure that returns rows needs its result columns: from
    `result_columns[name]` when recorded, else from `probe(translator)` on a PostgreSQL server."""
    extra = [r.name for r in database.routines]
    tr = Translator(routine, database, extra)
    body = strip_comments(routine.body).strip()
    body = re.sub(r"(?is)^\w+\s*:\s*", "", body)                     # a leading label: `proc: BEGIN`
    body = re.sub(r"(?is)^begin\b", "", body, count=1)
    body = re.sub(r"(?is)\bend\s*$", "", body, count=1)
    lines = []
    tr.statements(body, lines)

    params = [(mode, name, pg_type(mtype)) for mode, name, mtype in routine.params]
    directive = ""
    if routine.kind == "FUNCTION":
        returns = pg_type(routine.returns, boolean_for_tinyint1=True)
        volatility = ("IMMUTABLE" if routine.deterministic and routine.data_access == "NO SQL"
                      else "STABLE" if routine.data_access == "READS SQL DATA" else "VOLATILE")
        sig = ", ".join(f"{n} {t}" for m, n, t in params)
        head = f'CREATE FUNCTION "{routine.name}"({sig}) RETURNS {returns} LANGUAGE plpgsql {volatility} AS $body$'
    elif tr.result_sets:
        outs = [p for p in params if p[0] in ("OUT", "INOUT")]
        if outs:
            tr.notes.append("OUT parameter(s) " + ", ".join(p[1] for p in outs) +
                            " omitted: a function returning rows cannot also return them; the count equals the rows returned")
            for p in outs:                                              # assignments to the omitted OUTs go
                lines = [l for l in lines if not re.match(rf"\s*{re.escape(p[1])}\s*:=", l)
                         and not re.search(rf"\bINTO {re.escape(p[1])};", l)]
        ins = [p for p in params if p[0] == "IN"]
        if routine.name in result_columns:
            cols = result_columns[routine.name]
        elif probe is not None:
            cols = result_columns[routine.name] = probe(tr)
        else:
            raise NotProbed(routine.name)
        sig = ", ".join(f"{n} {t}" for m, n, t in ins)
        table = ", ".join(f'"{c}" {t}' for c, t in cols)
        head = f'CREATE FUNCTION "{routine.name}"({sig}) RETURNS TABLE({table}) LANGUAGE plpgsql AS $body$'
        # the TABLE columns are variables to PL/pgSQL, and would shadow the columns they are named after
        directive = "#variable_conflict use_column\n"
    else:
        sig = ", ".join(f"{m} {n} {t}" for m, n, t in params)
        head = f'CREATE PROCEDURE "{routine.name}"({sig}) LANGUAGE plpgsql AS $body$'
    declare = "DECLARE\n" + "\n".join(tr.declares) + "\n" if tr.declares else ""
    body_text = "\n".join(lines) if lines else "  NULL;"
    exception = ("EXCEPTION WHEN OTHERS THEN\n" + "\n".join(tr.handler) + "\n") if tr.handler else ""
    statement = f"{head}\n{directive}{declare}BEGIN\n{body_text}\n{exception}END $body$;"
    return statement, tr.notes


def render(database, result_columns, probe=None):
    """([statements], dropped, {routine: [notes]}) for PostgreSQL. Functions come first, so a
    procedure's result set can call them; `result_columns` is filled in by the probe when given."""
    statements, dropped, notes = [], [], {}
    order = sorted(database.routines, key=lambda r: (r.kind != "FUNCTION", r.name))
    for r in order:
        try:
            stmt, n = translate_routine(r, database, result_columns, probe)
        except sqltranslate.Unportable as exc:
            dropped.append(f"{r.kind.lower()} {r.name}: {exc}")
            continue
        statements.append(stmt)
        if n:
            notes[r.name] = n
    return statements, dropped, notes
