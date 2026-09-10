"""Translate one MySQL statement or expression into PostgreSQL or SQLite, deterministically.

sqlglot parses MySQL and renders the target dialect; a fixed list of rewrite rules covers what it
leaves alone or gets wrong for this corpus, and a per-dialect allowlist of functions turns anything
unknown into `Unportable` rather than into output that might not mean the same thing. Every rule is
named here and covered by a test; nothing is rewritten by pattern-matching text where the AST will
do.

Rules (both dialects unless noted):
  qualifiers   `db`.`table` of the current database becomes `table`; another database is Unportable
  extractvalue EXTRACTVALUE(x, '/a/b[1]') -> PostgreSQL array_to_string(xpath('/*[local-name()=...]/text()',
               CAST(x AS xml)), ''), namespace-agnostic as MySQL's prefix matching is; SQLite Unportable
  charset cast CAST(x AS CHAR CHARACTER SET ...) / CONVERT(x USING ...) -> CAST(x AS text)
  char(n) cast CAST(x AS CHAR(n)) -> PostgreSQL varchar(n) (MySQL's CHAR cast does not pad), SQLite TEXT
  group_concat GROUP_CONCAT(x [ORDER BY ...] [SEPARATOR s]) -> string_agg(x, s ORDER BY ...) /
               group_concat(x, s ORDER BY ...) (SQLite 3.44+)
  rollup       GROUP BY a, b WITH ROLLUP -> PostgreSQL GROUP BY ROLLUP (a, b); SQLite Unportable
  to_days      TO_DAYS(a) - TO_DAYS(b) -> PostgreSQL (CAST(a AS date) - CAST(b AS date))
  float        a FLOAT column inside arithmetic -> CAST(col AS double precision) on PostgreSQL, and a
               CAST(... AS DECIMAL) over it goes through text, so the rounding is MySQL's
  predicate    a comparison in a select list -> CAST(... AS int) on PostgreSQL (MySQL has no boolean)
  convert      CONVERT(binary_col USING utf8mb4) -> convert_from(col, 'UTF8') on PostgreSQL
  date literal '19970101' against a date-time column -> '1997-01-01' (SQLite: '1997-01-01 00:00:00')
  JSON_TABLE   NESTED PATH -> PostgreSQL JSON_TABLE; SQLite LEFT JOIN json_each(...)
  now          SYSDATE()/NOW() -> PostgreSQL now(), SQLite CURRENT_TIMESTAMP; LAST_INSERT_ID() ->
               lastval() / last_insert_rowid()
  n-literal    N'x' -> 'x'
  json_table   JSON_TABLE(x, '$' COLUMNS (NESTED PATH '$.p[*]' COLUMNS (c type PATH '$.k', ...))) t
               -> PostgreSQL JSON_TABLE over CAST(x AS jsonb); SQLite json_each(x, '$.p') with
               json_extract(t.value, '$.k') for each column reference
"""
import re

import sqlglot
from sqlglot import exp

PG_FUNCTIONS = {
    "convert_from",
    "coalesce", "count", "sum", "avg", "min", "max", "round", "upper", "lower", "length", "substring", "substr",
    "concat", "string_agg", "cast", "extract", "date_trunc", "to_char", "to_date", "now", "lastval", "repeat",
    "xpath", "array_to_string", "grouping", "abs", "ceil", "ceiling", "floor", "trim", "ltrim", "rtrim", "replace",
    "left", "right", "position", "nullif", "greatest", "least", "date_part", "current_date", "current_timestamp",
    "row_number", "rank", "dense_rank", "json_table", "date", "mod", "power", "sqrt", "exp", "ln", "log",
    "char_length", "character_length", "octet_length", "initcap", "lpad", "rpad", "reverse", "strpos",
    "make_date", "make_interval", "justify_days", "age", "localtimestamp",
}
SQLITE_FUNCTIONS = {
    "coalesce", "count", "sum", "avg", "min", "max", "round", "upper", "lower", "length", "substr", "substring",
    "group_concat", "cast", "iif", "strftime", "date", "datetime", "julianday", "abs", "trim", "ltrim", "rtrim",
    "replace", "nullif", "json_extract", "json_each", "last_insert_rowid", "current_timestamp", "current_date",
    "total", "instr", "printf", "format", "hex", "typeof", "row_number", "rank", "dense_rank", "ifnull", "quote",
    "unicode", "char", "random", "zeroblob", "likely", "unlikely", "time", "unixepoch", "changes",
}


class Unportable(Exception):
    """The statement uses something the target cannot express; the message says what."""


def _strip_qualifiers(node, schema):
    if isinstance(node, exp.Table) and node.db:
        if node.db.lower() != schema.lower():
            raise Unportable(f"references database {node.db}")
        node.set("db", None)
    if isinstance(node, exp.Column) and node.db:
        if node.db.lower() != schema.lower():
            raise Unportable(f"references database {node.db}")
        node.set("db", None)
    return node


def _xpath_local(path):
    """'/p1:A/p1:B[1]' -> '/*[local-name()=\\'A\\']/*[local-name()=\\'B\\'][1]': MySQL matches the
    prefixed names literally, so the namespace-agnostic form means the same thing."""
    steps = []
    for step in path.strip("/").split("/"):
        m = re.match(r"^(?:[A-Za-z_][\w.-]*:)?([A-Za-z_][\w.-]*)(\[\d+\])?$", step)
        if not m:
            raise Unportable(f"XPath step {step!r} is not an element step")
        steps.append(f"*[local-name()='{m.group(1)}']{m.group(2) or ''}")
    return "/" + "/".join(steps)


def _to_days_operand(node):
    """The argument of a TO_DAYS(x), which sqlglot's MySQL parser expands into
    (DATEDIFF(CAST(x AS DATE), CAST('0000-01-01' AS DATE), DAY) + 1); None for anything else."""
    while isinstance(node, exp.Paren):
        node = node.this
    if not (isinstance(node, exp.Add) and isinstance(node.expression, exp.Literal) and node.expression.this == "1"):
        return None
    dd = node.this
    if not isinstance(dd, exp.DateDiff):
        return None
    origin = dd.expression
    if not (isinstance(origin, (exp.Cast, exp.TsOrDsToDate)) and isinstance(origin.this, exp.Literal)
            and origin.this.this == "0000-01-01"):
        return None
    x = dd.this
    return x.this if isinstance(x, (exp.TsOrDsToDate, exp.Cast)) else x


def _rewrite(node, dialect, schema):
    node = _strip_qualifiers(node, schema)
    if isinstance(node, exp.Dot) and isinstance(node.expression, exp.Func):
        # `db`.`func`(args): the database's own routine, called unqualified on the target
        if node.this.name.lower() != schema.lower():
            raise Unportable(f"calls a routine of database {node.this.name}")
        node = node.expression
    if isinstance(node, exp.Anonymous) and isinstance(node.this, exp.Identifier):
        node.set("this", node.this.name.lower())     # a quoted, upper-cased call would not resolve
    if isinstance(node, exp.Anonymous):
        name = node.name.lower()
        if name == "extractvalue":
            if dialect != "postgres":
                raise Unportable("EXTRACTVALUE: SQLite has no XML functions")
            col, path = node.expressions
            if not isinstance(path, exp.Literal):
                raise Unportable("EXTRACTVALUE with a non-literal path")
            xp = _xpath_local(path.this) + "/text()"
            col = col.transform(lambda n: _strip_qualifiers(n, schema))
            return exp.Anonymous(this="array_to_string", expressions=[
                exp.Anonymous(this="xpath", expressions=[exp.Literal.string(xp),
                                                        exp.Cast(this=col, to=exp.DataType.build("xml", udt=True))]),
                exp.Literal.string("")])
        if name == "sysdate":
            return exp.Anonymous(this="now", expressions=[]) if dialect == "postgres" else exp.CurrentTimestamp()
        if name == "last_insert_id":
            return exp.Anonymous(this="lastval" if dialect == "postgres" else "last_insert_rowid", expressions=[])
        if name == "to_days":
            raise Unportable("TO_DAYS outside a TO_DAYS(a) - TO_DAYS(b) difference")
    if isinstance(node, exp.CurrentTimestamp) or (isinstance(node, exp.Anonymous) and node.name.lower() == "now"):
        return exp.Anonymous(this="now", expressions=[]) if dialect == "postgres" else exp.CurrentTimestamp()
    if isinstance(node, exp.Sub):
        a, b = _to_days_operand(node.this), _to_days_operand(node.expression)
        if a is not None and b is not None:
            if dialect == "postgres":
                return exp.Paren(this=exp.Sub(this=exp.Cast(this=a, to=exp.DataType.build("date")),
                                              expression=exp.Cast(this=b, to=exp.DataType.build("date"))))
            return exp.Cast(this=exp.Sub(this=exp.Anonymous(this="julianday", expressions=[a]),
                                         expression=exp.Anonymous(this="julianday", expressions=[b])),
                            to=exp.DataType.build("int"))
    if isinstance(node, exp.DateDiff) and _to_days_operand(exp.Paren(this=exp.Add(this=node, expression=exp.Literal.number(1)))) is not None:
        raise Unportable("TO_DAYS outside a TO_DAYS(a) - TO_DAYS(b) difference")
    if isinstance(node, exp.Cast):
        # the target type is changed in place: a new Cast node would end the walk, and the
        # expression being cast may itself hold something to rewrite
        dt = node.to
        if dt.this == exp.DataType.Type.CHARACTER_SET:
            node.set("to", exp.DataType.build("text"))      # CAST(x AS CHAR CHARACTER SET ...), CONVERT(x USING ...)
        elif dt.this in (exp.DataType.Type.CHAR, exp.DataType.Type.NCHAR):
            size = next((e for e in dt.expressions if isinstance(e, exp.DataTypeParam)), None)
            if size is None or dialect == "sqlite":
                node.set("to", exp.DataType.build("text"))
            else:
                node.set("to", exp.DataType.build(f"varchar({size.this})"))
        return node
    if isinstance(node, exp.GroupConcat) and dialect == "sqlite":
        inner = node.this.this if isinstance(node.this, exp.Order) else node.this
        if isinstance(inner, exp.Distinct) and (node.args.get("separator") is not None or isinstance(node.this, exp.Order)):
            raise Unportable("SQLite group_concat cannot combine DISTINCT with a separator or an ORDER BY")
    if isinstance(node, exp.Introducer):
        return node.expression                       # _utf8mb4'x' is just 'x' on the target
    if isinstance(node, exp.National):
        return exp.Literal.string(node.name)
    if isinstance(node, exp.Join) and not node.args.get("on") and not node.args.get("using") \
            and not node.args.get("kind") and not node.args.get("side"):
        node.set("kind", "CROSS")                    # a comma join inside parentheses: CROSS JOIN everywhere
    return node


def _group_concat_placeholders(tree, dialect):
    """GROUP_CONCAT(x ORDER BY y SEPARATOR s) on SQLite: sqlglot drops the ORDER BY, so each such call
    is replaced by a placeholder and rendered by hand as group_concat(x, s ORDER BY y), the form
    SQLite 3.44 and later accept. Returns {placeholder: rendered}."""
    rendered = {}
    counter = [0]

    def swap(node):
        if isinstance(node, exp.GroupConcat) and isinstance(node.this, exp.Order):
            order = node.this
            expr_sql = order.this.sql(dialect=dialect)
            order_sql = ", ".join(o.sql(dialect=dialect) for o in order.expressions)
            sep = node.args.get("separator")
            sep_sql = sep.sql(dialect=dialect) if sep is not None else "','"
            counter[0] += 1
            key = f"__group_concat_{counter[0]}__"
            rendered[key] = f"group_concat({expr_sql}, {sep_sql} ORDER BY {order_sql})"
            return exp.Anonymous(this=key, expressions=[])
        return node

    return tree.transform(swap), rendered


TYPE_NAMES = {"decimal", "numeric", "varchar", "char", "character", "varying", "text", "int", "integer", "bigint",
              "smallint", "real", "double", "float", "date", "timestamp", "time", "interval", "xml", "jsonb", "json",
              "boolean", "precision", "bytea", "blob", "signed", "unsigned", "nchar", "nvarchar", "datetime"}
KEYWORDS_BEFORE_PAREN = {
    "in", "values", "exists", "rollup", "cube", "over", "filter", "join", "from", "and", "or", "not", "on", "where",
    "select", "then", "else", "when", "by", "as", "any", "all", "interval", "using", "with", "grouping", "sets",
    "distinct", "into", "insert", "update", "delete", "having", "limit", "offset", "union", "except", "intersect",
    "between", "like", "is", "case", "end", "partition", "order", "group", "cross", "inner", "left", "right", "outer",
    "columns", "path", "nested", "table", "view", "primary", "key", "unique", "references", "check", "constraint",
    "default", "create", "temp", "temporary", "index", "returning", "set", "lateral", "recursive", "array",
}
CALL_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")


def _check_functions(sql, dialect, extra=()):
    """Every name followed by '(' in the rendered SQL must be a function the dialect has (or one of
    the database's own routines); anything else is Unportable rather than a guess."""
    allowed = (PG_FUNCTIONS if dialect == "postgres" else SQLITE_FUNCTIONS) | {e.lower() for e in extra}
    text = re.sub(r"'(?:[^']|'')*'", "''", sql)                     # string literals cannot hide a call
    text = re.sub(r'"(?:[^"]|"")*"', '""', text)                    # nor can quoted identifiers
    text = re.sub(r"(?i)\binto\s+[A-Za-z_][A-Za-z0-9_]*\s*\(", "INTO (", text)   # INSERT INTO t (cols) is not a call
    names = {m.group(1).lower() for m in CALL_RE.finditer(text)}
    unknown = sorted(n for n in names if n not in allowed and n not in KEYWORDS_BEFORE_PAREN and n not in TYPE_NAMES
                     and not n.startswith("__group_concat_"))
    if unknown:
        raise Unportable(f"{dialect} has no function(s) {', '.join(unknown)}")


JSON_TABLE_RE = re.compile(
    r"json_table\(\s*(?P<src>`?\w+`?(?:\.`?\w+`?)?)\s*,\s*'\$'\s*columns\s*\(\s*nested\s+path\s*'(?P<path>[^']+)\[\*\]'\s*"
    r"columns\s*\((?P<cols>(?:[^()]|\([^()]*\))*)\)\s*\)\s*\)\s*(?:as\s+)?`?(?P<alias>\w+)`?", re.I)
JSON_COL_RE = re.compile(r"`?(?P<name>\w+)`?\s+(?P<type>\w+(?:\(\d+\))?)(?:\s+character\s+set\s+\w+)?\s+path\s+'(?P<key>[^']+)'", re.I)


def _json_table(sql, dialect):
    """The one JSON_TABLE shape the corpus uses, rewritten before parsing because sqlglot cannot
    read MySQL's form. Returns (sql, alias_columns) where alias_columns says which column references
    SQLite has to rewrite into json_extract calls."""
    m = JSON_TABLE_RE.search(sql)
    if not m:
        return sql, None
    src, path, alias = m.group("src"), m.group("path"), m.group("alias")
    cols = [(c.group("name"), c.group("type"), c.group("key")) for c in JSON_COL_RE.finditer(m.group("cols"))]
    if not cols:
        raise Unportable("JSON_TABLE without recognisable columns")
    if dialect == "postgres":
        coldefs = ", ".join(f'"{n}" {t.replace("varchar", "varchar")} PATH \'{k}\'' for n, t, k in cols)
        repl = (f"JSON_TABLE(CAST({src} AS jsonb), '$' COLUMNS (NESTED PATH '{path}[*]' COLUMNS ({coldefs}))) AS {alias}")
        return sql[:m.start()] + repl + sql[m.end():], None
    # NESTED PATH keeps the parent row, with NULLs, when the array is empty: a LEFT JOIN, not a CROSS JOIN
    head = sql[:m.start()]
    if re.search(r"(?is)\bjoin\s*$", head):
        head = re.sub(r"(?is)\b(?:inner\s+|cross\s+)?join\s*$", "LEFT JOIN ", head)
    elif re.search(r",\s*$", head):
        head = re.sub(r",\s*$", " LEFT JOIN ", head)
    else:
        raise Unportable("JSON_TABLE not joined to its source row")
    repl = f"json_each({src}, '{path}') AS {alias} ON 1 = 1"
    return head + repl + sql[m.end():], (alias, cols)


AGGREGATES = (exp.AggFunc,)


def _has_aggregate(node):
    return any(isinstance(n, exp.AggFunc) for n in node.walk())


def _postgres_select_rules(tree, predicates_as_int=True):
    """Three rules for what MySQL accepts and PostgreSQL does not:
    * string_agg(DISTINCT x, sep ORDER BY y) needs y in the argument list; the order becomes x itself
      (for this corpus x starts with y, so the order is the same);
    * a bare column used as a condition (tinyint acting as boolean) becomes col <> 0;
    * a grouped SELECT may name non-aggregated columns that MySQL accepts as functionally dependent;
      they are added to GROUP BY, which does not change the result they were dependent in."""
    def fix(node):
        if isinstance(node, exp.GroupConcat) and isinstance(node.this, exp.Order) and isinstance(node.this.this, exp.Distinct):
            arg = node.this.this.expressions[0]
            ordered = [o.this for o in node.this.expressions]
            if any(o.sql() != arg.sql() for o in ordered):
                node.this.set("expressions", [exp.Ordered(this=arg.copy(), desc=node.this.expressions[0].args.get("desc"))])
        if isinstance(node, exp.If) and isinstance(node.this, exp.Column):
            node.set("this", exp.NEQ(this=node.this, expression=exp.Literal.number(0)))
        if isinstance(node, (exp.And, exp.Or)):
            for side in ("this", "expression"):
                if isinstance(node.args.get(side), exp.Column):
                    node.set(side, exp.NEQ(this=node.args[side], expression=exp.Literal.number(0)))
        if isinstance(node, exp.Where) and isinstance(node.this, exp.Column):
            node.set("this", exp.NEQ(this=node.this, expression=exp.Literal.number(0)))
        if isinstance(node, exp.Select) and predicates_as_int:
            # MySQL has no boolean type: a comparison in the select list is an integer 1/0
            for i, e in enumerate(node.expressions):
                inner = e.this if isinstance(e, exp.Alias) else e
                while isinstance(inner, exp.Paren):
                    inner = inner.this
                if isinstance(inner, PREDICATES):
                    cast = exp.Cast(this=inner.copy(), to=exp.DataType.build("int"))
                    if isinstance(e, exp.Alias):
                        e.set("this", cast)
                    else:
                        node.expressions[i] = cast
        if isinstance(node, exp.Select) and node.args.get("group") and not node.args["group"].args.get("rollup"):
            group = node.args["group"]
            present = {g.sql() for g in group.expressions}
            aliases = {e.alias.lower() for e in node.expressions if isinstance(e, exp.Alias)}
            candidates = [e.this if isinstance(e, exp.Alias) else e for e in node.expressions]
            if node.args.get("order"):
                candidates += [o.this for o in node.args["order"].expressions]
            for inner in candidates:
                if isinstance(inner, exp.Literal) or _has_aggregate(inner):
                    continue
                if isinstance(inner, exp.Column) and not inner.table and inner.name.lower() in aliases:
                    continue                      # ORDER BY an output alias (of an aggregate, typically)
                if inner.sql() not in present:
                    group.append("expressions", inner.copy())
                    present.add(inner.sql())
        return node
    return tree.transform(fix)


def names_of(database):
    """The real spelling of every table and column, by lower-cased name, for resolving the unquoted
    identifiers a hand-written body uses: MySQL matches them case-insensitively, PostgreSQL folds
    them to lower case, and the ported schema keeps the original case in quotes."""
    tables, columns, per_table, types = {}, {}, {}, {}
    if isinstance(database, dict):                   # a port's model.json
        table_list = [(t["name"], [(c["name"], c["data_type"]) for c in t["columns"]]) for t in database["tables"]]
        view_list = [(v["name"], [(c[0], c[1]) for c in v["columns"]]) for v in database.get("views", [])]
    else:
        table_list = [(t.name, [(c.name, c.data_type) for c in t.columns]) for t in database.tables]
        view_list = [(v.name, [(c[0], c[1]) for c in v.columns]) for v in database.views]
    for name, cols in table_list + view_list:
        tables[name.lower()] = name
        per_table[name.lower()] = {c.lower(): c for c, _ in cols}
        types[name.lower()] = {c.lower(): t.lower() for c, t in cols}
        for c, _ in cols:
            columns.setdefault(c.lower(), set()).add(c)
    return {"tables": tables, "columns": columns, "per_table": per_table, "types": types}


ARITHMETIC = (exp.Add, exp.Sub, exp.Mul, exp.Div, exp.Mod, exp.Neg, exp.Sum, exp.Avg)
BINARY_TYPES = ("binary", "varbinary", "tinyblob", "blob", "mediumblob", "longblob")
PREDICATES = (exp.EQ, exp.NEQ, exp.GT, exp.GTE, exp.LT, exp.LTE, exp.And, exp.Or, exp.Not, exp.Is,
              exp.Like, exp.In, exp.Between, exp.Exists, exp.NullSafeEQ, exp.NullSafeNEQ)
COMPARISONS = (exp.EQ, exp.NEQ, exp.GT, exp.GTE, exp.LT, exp.LTE, exp.Between)
COMPACT_DATETIME = re.compile(r"^(\d{4})(\d{2})(\d{2})(?:(\d{2})(\d{2})(\d{2}))?$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _column_type(node, names, scope):
    """The MySQL data type of a resolved column reference, or None."""
    if not isinstance(node, exp.Column):
        return None
    qualifier = node.args.get("table")
    tables = [scope.get(qualifier.name.lower()) or qualifier.name.lower()] if isinstance(qualifier, exp.Identifier) else list(scope.values())
    found = {names["types"].get(t, {}).get(node.name.lower()) for t in tables} - {None}
    return next(iter(found)) if len(found) == 1 else None


def _typed_rules(tree, names, scope, dialect):
    """What the engines do differently with the same expression, put right where a column's type
    says so:
    * MySQL evaluates a FLOAT operand in double precision; PostgreSQL in single. The column is cast
      to double precision inside arithmetic and sums, so the digits come out the same;
    * a date-time column compared with a compact literal ('19970101'): MySQL reads it as a date,
      SQLite compares text and PostgreSQL reads it too; it becomes ISO, and on SQLite, where a
      DATETIME is text, a date-only literal gets midnight appended so the comparison is the same."""
    def has_float(node):
        return any(_column_type(c, names, scope) in ("float", "double") for c in node.find_all(exp.Column))

    def fix(node):
        if dialect == "postgres" and isinstance(node, ARITHMETIC):
            for key in ("this", "expression"):
                child = node.args.get(key)
                if _column_type(child, names, scope) == "float":
                    node.set(key, exp.Cast(this=child, to=exp.DataType.build("double precision", dialect="postgres")))
        if (dialect == "postgres" and isinstance(node, exp.Cast) and node.to.this == exp.DataType.Type.CHARACTER_SET
                and _column_type(node.this, names, scope) in BINARY_TYPES):
            # CONVERT(binary_col USING utf8mb4) reads the bytes as text; bytea::text would render them as hex
            return exp.Anonymous(this="convert_from", expressions=[node.this, exp.Literal.string("UTF8")])
        if (dialect == "postgres" and isinstance(node, exp.Cast) and node.to.this == exp.DataType.Type.DECIMAL
                and not isinstance(node.this, exp.Cast) and has_float(node.this)):
            # PostgreSQL turns a double into a numeric through a 15-digit rendering, so
            # 7.764749999999999 becomes 7.7648 at four places where MySQL, converting the exact
            # value, gives 7.7647; the shortest-exact text form (PostgreSQL 12+) converts as MySQL does
            node.set("this", exp.Cast(this=node.this, to=exp.DataType.build("text")))
        if isinstance(node, COMPARISONS):
            sides = [node.this, node.expression] + ([node.args["low"], node.args["high"]] if isinstance(node, exp.Between) else [])
            col_type = next((t for t in (_column_type(s, names, scope) for s in sides) if t in ("date", "datetime", "timestamp")), None)
            if col_type:
                for key in ("this", "expression", "low", "high"):
                    lit = node.args.get(key)
                    if isinstance(lit, exp.Literal) and lit.is_string:
                        node.set(key, exp.Literal.string(_date_literal(lit.this, col_type, dialect)))
        return node
    return tree.transform(fix)


def _date_literal(text, col_type, dialect):
    m = COMPACT_DATETIME.match(text)
    if m:
        y, mo, da, h, mi, s = m.groups()
        text = f"{y}-{mo}-{da}" + (f" {h}:{mi}:{s}" if h else "")
    if dialect == "sqlite" and col_type in ("datetime", "timestamp") and ISO_DATE.match(text):
        text += " 00:00:00"
    return text


def _resolve_identifiers(tree, names, exclude):
    """Unquoted table and column names -> their real spelling, quoted. Names in `exclude` (a
    routine's variables) and names the model does not know (aliases, temporary tables) stay as
    written, and fold the same way everywhere they appear."""
    exclude = {e.lower() for e in exclude}

    def fix(ident, real):
        if real is not None and real != ident.name or not ident.quoted:
            ident.set("this", real)
            ident.set("quoted", True)

    # the statement's own tables, by alias or name, narrow an ambiguous spelling down
    scope, in_scope = {}, {}
    for node in tree.find_all(exp.Table):
        ident = node.this
        if not isinstance(ident, exp.Identifier):
            continue
        real = names["tables"].get(ident.name.lower())
        if real and not ident.quoted:
            fix(ident, real)
        if real:
            key = (node.alias or ident.name).lower()
            scope[key] = real.lower()
            for low, spelled in names["per_table"][real.lower()].items():
                in_scope.setdefault(low, set()).add(spelled)
    for node in tree.find_all(exp.Column):
        ident = node.this
        if not isinstance(ident, exp.Identifier) or ident.quoted or ident.name.lower() in exclude:
            continue
        qualifier = node.args.get("table")
        real = None
        if isinstance(qualifier, exp.Identifier):
            table = scope.get(qualifier.name.lower()) or qualifier.name.lower()
            per = names["per_table"].get(table)
            if per:
                real = per.get(ident.name.lower())
                if not qualifier.quoted and qualifier.name.lower() in names["tables"] and qualifier.name.lower() not in scope:
                    fix(qualifier, names["tables"][qualifier.name.lower()])
        if real is None:
            for pool in (in_scope, names["columns"]):
                spellings = pool.get(ident.name.lower())
                if spellings and len(spellings) == 1:
                    real = next(iter(spellings)); break
        if real:
            fix(ident, real)
    for node in tree.find_all(exp.Schema):                    # INSERT INTO t (col, ...)
        target = node.this
        per = names["per_table"].get(target.name.lower()) if isinstance(target, exp.Table) else None
        for ident in node.expressions:
            if isinstance(ident, exp.Identifier) and not ident.quoted:
                real = (per or {}).get(ident.name.lower())
                if real:
                    fix(ident, real)
    return tree, scope


def translate(sql, dialect, schema, extra=(), names=None, exclude=(), condition=False):
    """One MySQL statement -> the dialect. Raises Unportable with the reason when it cannot.
    `extra` names functions the target will have (the database's own routines, ported first);
    `names` (names_of) resolves unquoted identifiers to their real spelling, except `exclude`;
    `condition` says the SELECT wraps an expression a routine or trigger tests (IF, WHEN), which
    must stay boolean on PostgreSQL rather than becoming MySQL's integer."""
    if dialect not in ("postgres", "sqlite"):
        raise ValueError(dialect)
    sql, json_cols = _json_table(sql, dialect)
    try:
        tree = sqlglot.parse_one(sql, read="mysql")
    except Exception as exc:  # noqa: BLE001 - the message is the diagnosis
        raise Unportable(f"cannot parse: {str(exc).splitlines()[0][:120]}")
    if names:
        tree, scope = _resolve_identifiers(tree, names, exclude)
        tree = _typed_rules(tree, names, scope, dialect)
    # GROUP_CONCAT's ORDER BY must survive: remember it before the generic rewrite
    concats = {}
    for n in tree.find_all(exp.GroupConcat):
        order = n.this if isinstance(n.this, exp.Order) else None
        concats[id(n)] = order
    rollup = any(isinstance(g, exp.Group) and g.args.get("rollup") for g in tree.find_all(exp.Group))
    tree = tree.transform(lambda n: _rewrite(n, dialect, schema))
    if dialect == "postgres":
        tree = _postgres_select_rules(tree, predicates_as_int=not condition)
    if json_cols and dialect == "sqlite":
        alias, cols = json_cols
        by_name = {n.lower(): k for n, _t, k in cols}
        def cols_to_json(node):
            if isinstance(node, exp.Column) and node.table and node.table.lower() == alias.lower() and node.name.lower() in by_name:
                return exp.Anonymous(this="json_extract", expressions=[exp.column("value", table=alias), exp.Literal.string(by_name[node.name.lower()])])
            return node
        tree = tree.transform(cols_to_json)
    placeholders = {}
    if dialect == "sqlite":
        tree, placeholders = _group_concat_placeholders(tree, dialect)
    out = tree.sql(dialect=dialect)
    for key, text in placeholders.items():
        out = re.sub(re.escape(key) + r"\(\)", lambda m: text, out, flags=re.I)
    _check_functions(out, dialect, extra)
    if rollup:
        if dialect != "postgres":
            raise Unportable("GROUP BY ... WITH ROLLUP: SQLite has no ROLLUP")
        out = re.sub(r"GROUP BY (.+?) WITH ROLLUP", lambda m: f"GROUP BY ROLLUP ({m.group(1)})", out)
    return out
