#!/usr/bin/env python3
"""A small T-SQL to MySQL translator for the Microsoft sample scripts (Northwind, pubs).

These scripts are SQL Server 2000 era: `GO` batch separators, `"Quoted Identifiers"`, types written
as `"int"`, `IDENTITY (1,1)`, `PRIMARY KEY CLUSTERED`, `dbo.` prefixes and `INSERT "T" VALUES(...)`
without INTO. Everything here works on a token scanner that tracks single-quoted string literals, so
no transformation can reach into data: the scripts contain apostrophes, commas, capital letters and
words like `int` inside customer names.

What it does NOT attempt: rewriting T-SQL procedural bodies. Objects whose body uses constructs with
no mechanical MySQL equivalent are reported by name so the caller can decide to port or drop them.
"""
import hashlib
import re

from ddlutil import inline_identity_pk

TYPE_MAP = {
    "int": "INT", "smallint": "SMALLINT", "bigint": "BIGINT",
    # SQL Server tinyint is UNSIGNED 0..255; MySQL's plain TINYINT is signed -128..127, so an
    # unqualified mapping silently rejects any value above 127 (pubs.jobs.min_lvl hits this).
    "tinyint": "TINYINT UNSIGNED",
    "bit": "TINYINT(1)", "money": "DECIMAL(19,4)", "smallmoney": "DECIMAL(10,4)",
    "datetime": "DATETIME", "smalldatetime": "DATETIME", "float": "DOUBLE", "real": "FLOAT",
    "ntext": "TEXT", "text": "TEXT", "image": "MEDIUMBLOB", "uniqueidentifier": "CHAR(36)",
    "sysname": "VARCHAR(128)", "xml": "TEXT", "date": "DATE", "time": "TIME",
    "datetime2": "DATETIME(6)", "datetimeoffset": "DATETIME(6)", "hierarchyid": "VARCHAR(255)",
}
SIZED = {"nvarchar": "VARCHAR", "varchar": "VARCHAR", "nchar": "CHAR", "char": "CHAR",
         "decimal": "DECIMAL", "numeric": "DECIMAL", "binary": "BINARY", "varbinary": "VARBINARY"}

SKIP_BATCH = re.compile(
    r"^\s*(if\s+exists|set\s+(nocount|dateformat|quoted_identifier|ansi_nulls|rowcount)\b"
    r"|set\s+identity_insert|use\s+|go\s*$|--"
    # server maintenance and messaging with no MySQL equivalent; the pipeline runs its own
    # ANALYZE TABLE after loading, so UPDATE STATISTICS is redundant rather than lost
    r"|update\s+statistics\b|dbcc\b|raiserror\b|print\b|checkpoint\b"
    r"|exec(ute)?\s+sp_|create\s+type\b)", re.I)


MAX_IDENT = 64          # MySQL's limit; SQL Server allows 128


def ident(name):
    """Upstream identifier -> MySQL identifier: lower case, spaces to underscores.

    A name over MySQL's 64-character limit is truncated and given a hash of the full original, so
    the result is deterministic across builds and two long names that share a prefix stay distinct.
    AdventureWorks LT has a six-column index whose name runs to 82 characters.
    """
    out = name.strip().lower().replace(" ", "_")
    if len(out) > MAX_IDENT:
        digest = hashlib.sha256(out.encode()).hexdigest()[:8]
        out = out[:MAX_IDENT - 9] + "_" + digest
    return out


def split_batches(sql):
    """Split on a line that is only GO (the batch separator), never inside a string literal."""
    out, cur, i, n, in_str = [], [], 0, len(sql), False
    for line in sql.splitlines():
        stripped = line.strip()
        if not in_str and re.fullmatch(r"(?i)go", stripped):
            out.append("\n".join(cur)); cur = []
            continue
        cur.append(line)
        # track unterminated string literals across lines
        q = 0
        j = 0
        while j < len(line):
            if line[j] == "'":
                if j + 1 < len(line) and line[j + 1] == "'":
                    j += 2; continue
                q += 1
            j += 1
        if q % 2:
            in_str = not in_str
    if cur:
        out.append("\n".join(cur))
    return [b for b in out if b.strip()]


STMT_START = re.compile(
    r"(?i)^\s*(create|insert|alter|update|delete|drop|exec(ute)?|grant|use|set|if|begin)\b")
ROUTINE_START = re.compile(r"(?i)^\s*create\s+(view|proc(edure)?|function|trigger)\b")


def split_statements(batch):
    """Split one batch into statements. T-SQL separates them by nothing but a newline, so a new
    statement begins at a line that starts with a statement keyword outside any string literal.
    A view or routine body is never split: its lines are part of one definition."""
    lines, in_str = batch.split("\n"), False
    lead = re.sub(r"(?s)^\s*(?:/\*.*?\*/|--[^\n]*\n)\s*", "", batch)
    if ROUTINE_START.match(lead):
        return [batch]
    out, cur = [], []
    for line in lines:
        if not in_str and STMT_START.match(line) and cur and any(c.strip() for c in cur):
            out.append("\n".join(cur)); cur = []
        cur.append(line)
        quotes = 0
        j = 0
        while j < len(line):
            if line[j] == "'":
                if j + 1 < len(line) and line[j + 1] == "'":
                    j += 2; continue
                quotes += 1
            j += 1
        if quotes % 2:
            in_str = not in_str
    if cur:
        out.append("\n".join(cur))
    return [st for st in out if st.strip()]


def scan_replace(sql, on_dquote=None, on_word=None):
    """Walk sql outside string literals and comments, rewriting quoted names and bare words.

    `on_dquote` is called with (name, in_type_position). A quoted token sits in type position when
    the previous emitted token was itself an identifier, which is how a column definition reads:
    `[Col] [Type]`. Deciding by name alone is not enough -- AdventureWorks has a column named
    NameStyle whose type is also NameStyle, and treating the first one as a type eats the name.
    """
    out, i, n = [], 0, len(sql)
    prev_ident = False
    while i < n:
        ch = sql[i]
        if ch == "'":                                  # string literal: copy verbatim
            out.append(ch); i += 1
            while i < n:
                if sql[i] == "'":
                    if i + 1 < n and sql[i + 1] == "'":
                        out.append("''"); i += 2; continue
                    out.append("'"); i += 1; break
                out.append(sql[i]); i += 1
            continue
        if ch == "`":                                  # already-emitted MySQL identifier: copy
            end = sql.find("`", i + 1)
            if end > 0:
                out.append(sql[i:end + 1]); i = end + 1; continue
        if sql.startswith("--", i):                    # line comment
            end = sql.find("\n", i); end = n if end < 0 else end
            out.append(sql[i:end]); i = end; continue
        if sql.startswith("/*", i):
            end = sql.find("*/", i + 2); end = n if end < 0 else end + 2
            out.append(sql[i:end]); i = end; continue
        if ch in '"[' and on_dquote:                   # "quoted" or [bracketed] identifier
            end = sql.find('"' if ch == '"' else "]", i + 1)
            if end > 0:
                emitted = on_dquote(sql[i + 1:end], prev_ident)
                out.append(emitted)
                prev_ident = emitted.endswith("`")
                i = end + 1
                continue
        if on_word and (ch.isalpha() or ch == "_"):    # bare word
            m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", sql[i:])
            word = m.group(0)
            out.append(on_word(word)); i += len(word); prev_ident = False; continue
        if not ch.isspace():
            prev_ident = False
        out.append(ch); i += 1
    return "".join(out)


CAST_TYPES = {"money": "DECIMAL(19,4)", "smallmoney": "DECIMAL(10,4)", "int": "SIGNED",
              "bigint": "SIGNED", "smallint": "SIGNED", "tinyint": "SIGNED", "bit": "SIGNED",
              "float": "DOUBLE", "real": "DOUBLE", "datetime": "DATETIME", "date": "DATE",
              "varchar": "CHAR", "nvarchar": "CHAR", "char": "CHAR", "nchar": "CHAR"}


def _cast_type(tsql_type):
    """Map a T-SQL type used as a CONVERT/CAST target to a MySQL CAST target type.

    MySQL's CAST accepts a much shorter list of types than a column declaration does: VARCHAR is not
    among them, so a character target of any width becomes CHAR(n)."""
    t = tsql_type.strip()
    m = re.match(r"(?i)^(n?(?:var)?char)\s*\(\s*(\d+)\s*\)$", t)
    if m:
        return f"CHAR({m.group(2)})"
    m = re.match(r"(?i)^(decimal|numeric)\s*\((\s*\d+\s*(?:,\s*\d+\s*)?)\)$", t)
    if m:
        return f"DECIMAL({m.group(2).replace(' ', '')})"
    return CAST_TYPES.get(t.lower(), t.upper())


def convert_tsql_convert(sql):
    """`CONVERT(type, expr)` -> `CAST(expr AS type)`.

    The argument list is parsed with balanced-paren scanning rather than split on the first comma,
    because the type itself may contain one (`CONVERT(decimal(14,2), x)`)."""
    out, i, n = [], 0, len(sql)
    while i < n:
        m = re.compile(r"(?i)(?<![A-Za-z0-9_])CONVERT\s*\(").match(sql, i)
        if not m:
            out.append(sql[i]); i += 1; continue
        j, depth = m.end(), 1
        while j < n and depth:                       # find the matching close paren
            if sql[j] == "(": depth += 1
            elif sql[j] == ")": depth -= 1
            j += 1
        args = sql[m.end():j - 1]
        # first argument is a type: a word plus an optional balanced (...) group
        tm = re.match(r"(?i)\s*([A-Za-z_][A-Za-z0-9_]*\s*(?:\([^()]*\))?)\s*,", args)
        if not tm:
            out.append(sql[i:j]); i = j; continue
        expr = args[tm.end():]
        out.append(f"CAST({convert_tsql_convert(expr)} AS {_cast_type(tm.group(1))})")
        i = j
    return "".join(out)


LIKE_CLASS = re.compile(r"(?i)\bLIKE\s+'((?:[^']|'')*)'")


def like_pattern_to_regexp(pattern):
    """Translate a T-SQL LIKE pattern that uses [character classes] into a MySQL REGEXP.

    MySQL's LIKE has no character classes, so `LIKE '[0-9][0-9][0-9]-...'` silently matches nothing
    and a CHECK built on it would wrongly reject every row."""
    out, i, n = ["^"], 0, len(pattern)
    while i < n:
        ch = pattern[i]
        if ch == "[":
            end = pattern.find("]", i)
            if end > 0:
                out.append(pattern[i:end + 1]); i = end + 1
                # collapse an immediately repeated identical class into a {n} quantifier
                continue
        if ch == "%":
            out.append(".*")
        elif ch == "_":
            out.append(".")
        elif ch in ".^$*+?()|{}\\":
            out.append("\\" + ch)
        else:
            out.append(ch)
        i += 1
    out.append("$")
    return "".join(out)


def convert_like_classes(sql):
    """Rewrite only those LIKE patterns that actually use a character class."""
    def repl(m):
        pattern = m.group(1)
        if "[" not in pattern:
            return m.group(0)
        return "REGEXP '" + like_pattern_to_regexp(pattern) + "'"
    return LIKE_CLASS.sub(repl, sql)


NULLABILITY = re.compile(r"(?i)\s*\b(NOT\s+NULL|NULL)\s*$")


def split_alias(definition):
    """`nvarchar(50) NULL` -> ('VARCHAR(50)', 'NULL'), with the base type already mapped to MySQL."""
    definition = convert_types(definition.strip().rstrip(";").strip())
    m = NULLABILITY.search(definition)
    if not m:
        return definition, ""
    return definition[:m.start()].strip(), " ".join(m.group(1).split()).upper()


DECLARED_PK = re.compile(r"(?is)ALTER\s+TABLE\s+(?:\[?\w+\]?\s*\.\s*)*\[?(\w+)\]?\s+"
                         r"(?:WITH\s+\w+\s+)?ADD\s+(?:CONSTRAINT\s+\[?\w+\]?\s+)?"
                         r"PRIMARY\s+KEY[^(]*\(([^)]*)\)")


def collect_declared_pks(sql):
    """Primary keys the script adds with ALTER TABLE, as {table: [column, ...]}.

    An identity column has to be keyed the moment it is declared, and what key it should get depends
    on the primary key that arrives later, so that has to be known before the tables are emitted.
    """
    pks = {}
    for m in DECLARED_PK.finditer(sql):
        columns = [c.lower() for c in re.findall(r"\[?(\w+)\]?", m.group(2))
                   if c.upper() not in ("ASC", "DESC")]
        pks[ident(m.group(1))] = columns
    return pks


def collect_tsql_types(sql):
    """`CREATE TYPE [dbo].[Name] FROM nvarchar(50) NULL` -> {name: ('VARCHAR(50)', 'NULL')}."""
    types = {}
    for m in re.finditer(r"(?im)^\s*CREATE\s+TYPE\s+(?:\[?\w+\]?\s*\.\s*)?\[?(\w+)\]?\s+FROM\s+([^;\n]+)", sql):
        types[m.group(1).lower()] = split_alias(m.group(2))
    return types


def column_tail(sql, pos):
    """The rest of the column definition starting at pos: up to the comma that ends it."""
    depth = 0
    for i in range(pos, len(sql)):
        ch = sql[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            if depth == 0:
                return sql[pos:i]
            depth -= 1
        elif ch == "," and depth == 0:
            return sql[pos:i]
    return sql[pos:]


def split_top(text, sep):
    """Split at `sep` where it is outside both parentheses and string literals."""
    parts, depth, start, i, n = [], 0, 0, 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "'":
            i += 1
            while i < n:
                if text[i] == "'":
                    if i + 1 < n and text[i + 1] == "'":
                        i += 2; continue
                    break
                i += 1
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == sep and depth == 0:
            parts.append(text[start:i]); start = i + 1
        i += 1
    parts.append(text[start:])
    return parts


def has_top_literal(text):
    """True when a string literal appears at the top nesting level, so a `+` here concatenates."""
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "'" and depth == 0:
            return True
    return False


def top_groups(text):
    """(open, close) index pairs of the outermost parenthesised groups, ignoring literals."""
    groups, depth, start, i, n = [], 0, None, 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "'":
            i += 1
            while i < n and text[i] != "'":
                i += 1
        elif ch == "(":
            if depth == 0:
                start = i
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                groups.append((start, i))
        i += 1
    return groups


def convert_concat(expr):
    """T-SQL overloads `+` for string concatenation; MySQL's `+` is always arithmetic.

    An operand tells the two apart: `N'SO' + CONVERT(...)` has a string literal at the top level of
    the expression and concatenates, while `[SubTotal] + [TaxAmt]` does not and stays as it is.
    Left alone, `'SO' + 71774` would silently evaluate to 71774 in MySQL rather than 'SO71774'.
    """
    parts = split_top(expr, "+")
    if len(parts) > 1 and any(has_top_literal(p) for p in parts):
        return "CONCAT(" + ", ".join(convert_concat(p.strip()) for p in parts) + ")"
    out, i = [], 0
    for start, end in top_groups(expr):
        out.append(expr[i:start + 1])
        out.append(", ".join(convert_concat(a.strip()) for a in split_top(expr[start + 1:end], ",")))
        out.append(")")
        i = end + 1
    out.append(expr[i:])
    return "".join(out)


COMPUTED = re.compile(r"(?i)(?:^|,)\s*`(\w+)`\s+AS\s+")


def convert_computed(body, computed_types, materialize=()):
    """`[LineTotal] AS ISNULL(...)` -> `` `linetotal` DECIMAL(38,6) AS (IFNULL(...)) STORED ``.

    T-SQL infers a computed column's type; MySQL requires one to be declared, so the caller supplies
    it per `table.column` from the dataset record. Returns the body and the generated column names,
    which the caller must leave out of INSERT column lists.

    A column named in `materialize` becomes an ordinary column instead, for expressions MySQL will
    not generate -- it rejects a generated column that reads an AUTO_INCREMENT column. Its value
    then has to come from the data, so it stays in the INSERT column list.
    """
    table = re.search(r"(?is)^\s*CREATE\s+TABLE\s+`([^`]+)`", body)
    if not table:
        return body, []
    generated, out, pos = [], [], 0
    for m in COMPUTED.finditer(body):
        column = m.group(1)
        key = f"{table.group(1)}.{column}".lower()
        if key not in computed_types:
            raise SystemExit(f"computed column {key} has no declared MySQL type")
        expression = column_tail(body, m.end()).strip()
        out.append(body[pos:m.start(1) - 1])
        pos = m.end() + len(column_tail(body, m.end()))
        if key in materialize:
            out.append(f"`{column}` {computed_types[key]}")
            continue
        # N'x' is a national-character literal; MySQL's utf8mb4 columns make the prefix redundant
        expression = re.sub(r"(?<![A-Za-z0-9_])N'", "'", expression)
        expression = convert_concat(convert_functions(convert_tsql_convert(expression)))
        out.append(f"`{column}` {computed_types[key]} AS ({expression}) STORED")
        generated.append(column)
    out.append(body[pos:])
    return "".join(out), generated


def expand_alias_types(sql, types):
    """Replace a user-defined type used as a column type with its base definition.

    T-SQL lets the column override the alias's nullability, so the alias only supplies NULL/NOT NULL
    when the column declares none. Emitting both produces `VARCHAR(50) NULL NOT NULL`, which MySQL
    rejects -- AdventureWorks LT's [Name] alias hits this on nearly every table.
    """
    for name, (base, nullability) in types.items():
        def repl(m, base=base, nullability=nullability):
            tail = column_tail(sql, m.end())
            if nullability and not re.search(r"(?i)\bNULL\b", tail):
                return f"{m.group(1)}{base} {nullability}"
            return m.group(1) + base
        sql = re.sub(rf"(?i)(`\w+`\s+)(?:`dbo`\s*\.\s*)?{name}(?![A-Za-z0-9_(])", repl, sql)
    return sql


def collect_udts(sql):
    """`execute sp_addtype name, 'basetype', 'NOT NULL'` -> {name: ('BASETYPE', 'NOT NULL')}."""
    udts = {}
    for m in re.finditer(r"(?im)^\s*exec(?:ute)?\s+sp_addtype\s+(\w+)\s*,\s*'([^']+)'\s*(?:,\s*'([^']*)')?", sql):
        name, base, nullability = m.group(1), m.group(2), (m.group(3) or "")
        udts[name.lower()] = split_alias(f"{base.strip()} {nullability.strip()}".strip())
    return udts


def convert_functions(sql):
    """Map SQL Server built-ins to their MySQL equivalents.

    CURRENT_TIMESTAMP is used rather than NOW() because it is also legal in a DEFAULT clause, which
    is where getdate() most often appears."""
    sql = re.sub(r"(?i)\bGETDATE\s*\(\s*\)", "CURRENT_TIMESTAMP", sql)
    sql = re.sub(r"(?i)\bGETUTCDATE\s*\(\s*\)", "UTC_TIMESTAMP", sql)
    sql = re.sub(r"(?i)\bISNULL\s*\(", "IFNULL(", sql)
    sql = re.sub(r"(?i)\bLEN\s*\(", "CHAR_LENGTH(", sql)
    return sql


CTE_HEAD = re.compile(r"(?i)\bWITH\s+(`?\w+`?)\s*(?:\([^()]*\))?\s+AS\s*\(")


def convert_recursive_cte(sql):
    """MySQL needs WITH RECURSIVE where T-SQL just writes WITH.

    Without it a self-referencing CTE fails with "table doesn't exist" on its own name, which is how
    AdventureWorks LT's vGetAllCategories reads the product category tree.
    """
    m = CTE_HEAD.search(sql)
    if not m:
        return sql
    name, depth, i = m.group(1).strip("`"), 1, m.end()
    while i < len(sql) and depth:
        depth += {"(": 1, ")": -1}.get(sql[i], 0)
        i += 1
    if not re.search(rf"(?i)\b{re.escape(name)}\b", sql[m.end():i - 1]):
        return sql
    return sql[:m.start()] + re.sub(r"(?i)^WITH\b", "WITH RECURSIVE", sql[m.start():], count=1)


XML_VALUE = re.compile(r"(?is)(`?\w+`?)\.value\s*\(\s*N?'((?:[^']|'')*)'\s*,\s*'([^']*)'\s*\)")
XML_METHOD = re.compile(r"(?i)`?\w+`?\.(query|exist|nodes|modify)\s*\(")
DECLARE_NS = re.compile(r'(?is)\s*declare\s+namespace\s+[\w-]+\s*=\s*"[^"]*"\s*;')


def convert_xml_value(sql):
    """SQL Server's `col.value('xquery', 'type')` -> MySQL's `ExtractValue(col, 'xpath')`.

    MySQL has no XQuery and its XPath subset has no namespace support -- `local-name()` is not in the
    grammar. It does match a prefixed element name literally, though, and AdventureWorks' catalog
    documents use the same prefixes the queries declare (p1, wm, wf, html), so dropping the
    `declare namespace` preamble and keeping the path as written selects the same nodes. The
    `(path)[1]` form becomes `path[1]`, which MySQL's grammar does accept, and a sized result type
    becomes a CAST so the column is truncated the way SQL Server truncates it.
    """
    bad = XML_METHOD.search(sql)
    if bad:
        raise SystemExit(f"XML method .{bad.group(1)}() has no MySQL equivalent")

    def one(m):
        column, xquery, result = m.group(1), m.group(2), m.group(3).strip()
        path = DECLARE_NS.sub("", xquery).strip()
        outer = re.match(r"^\((.*)\)(\[\d+\])$", path, re.S)
        if outer:
            path = outer.group(1).strip() + outer.group(2)
        path = " ".join(path.split())
        expression = f"ExtractValue({column}, '{path}')"
        size = re.match(r"(?i)^n?(?:var)?char\s*\(\s*(\d+)\s*\)$", result)
        return f"CAST({expression} AS CHAR({size.group(1)}))" if size else expression

    return XML_VALUE.sub(one, sql)


INLINE_REF = re.compile(r"(?i)\s+REFERENCES\s+(`?\w+`?)\s*\(\s*(`?\w+`?)\s*\)")


def hoist_inline_references(create_table):
    """Turn column-level `REFERENCES t(c)` into table-level FOREIGN KEY clauses.

    MySQL "parses but ignores inline REFERENCES specifications" (they are accepted and then do
    nothing), so a script that declares all of its foreign keys inline -- as pubs does, with ten of
    them and no ALTER TABLE at all -- would produce a database with no foreign keys whatsoever.
    """
    lines, hoisted = create_table.split("\n"), []
    for idx, line in enumerate(lines):
        m = INLINE_REF.search(line)
        if not m:
            continue
        col = re.match(r"\s*(`?[\w ]+?`?)\s+\S", line)
        if not col:
            continue
        lines[idx] = INLINE_REF.sub("", line)
        hoisted.append(f"\tFOREIGN KEY ({col.group(1)}) REFERENCES {m.group(1)} ({m.group(2)})")
    if not hoisted:
        return create_table, 0
    body = "\n".join(lines)
    close = body.rfind(")")
    head = body[:close].rstrip().rstrip(",")
    return head + ",\n" + ",\n".join(hoisted) + "\n" + body[close:], len(hoisted)


def strip_money_literals(sql):
    """T-SQL writes money literals as `$20.00`; MySQL reads that as an identifier.

    Applied only outside string literals, so a dollar sign inside data is preserved."""
    out, i, n = [], 0, len(sql)
    while i < n:
        ch = sql[i]
        if ch == "'":
            out.append(ch); i += 1
            while i < n:
                if sql[i] == "'":
                    if i + 1 < n and sql[i + 1] == "'":
                        out.append("''"); i += 2; continue
                    out.append("'"); i += 1; break
                out.append(sql[i]); i += 1
            continue
        if ch == "$" and i + 1 < n and (sql[i + 1].isdigit() or sql[i + 1] in "-."):
            i += 1; continue                      # drop the currency prefix, keep the number
        out.append(ch); i += 1
    return "".join(out)


COL_LINE = re.compile(r"^\s*(`[^`]+`|\w+)\s+(?=[A-Za-z])")
NOT_A_COLUMN = re.compile(r"(?i)^\s*(constraint|primary|foreign|unique|check|key|index)\b")


def parse_columns(create_table):
    """Return (all column names, the AUTO_INCREMENT column or None) for a CREATE TABLE statement."""
    open_paren = create_table.find("(")
    if open_paren < 0:
        return [], None
    cols, identity = [], None
    for line in create_table[open_paren + 1:].split("\n"):
        if NOT_A_COLUMN.match(line):
            continue
        m = COL_LINE.match(line)
        if not m:
            continue
        name = m.group(1)
        cols.append(name)
        if re.search(r"(?i)\bAUTO_INCREMENT\b", line):
            identity = name
    return cols, identity


def add_column_list(insert_sql, columns, identity):
    """T-SQL omits an identity column from `INSERT ... VALUES`; MySQL needs the count to match."""
    listed = [c for c in columns if c != identity]
    return re.sub(r"(?i)^(\s*INSERT\s+INTO\s+(?:`[^`]+`|\w+))(\s+VALUES\b)",
                  lambda m: f"{m.group(1)} ({', '.join(listed)}){m.group(2)}", insert_sql, count=1)


def normalize_comments(sql):
    """MySQL needs whitespace after `--` to treat it as a comment; T-SQL does not.

    An upstream line like `--ORDER BY City` is a comment in SQL Server and a syntax error in MySQL.
    Only whole lines are rewritten, so data is never touched."""
    out = []
    for line in sql.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("--") and len(stripped) > 2 and stripped[2] not in " \t-":
            indent = line[:len(line) - len(stripped)]
            out.append(f"{indent}-- {stripped[2:]}")
        else:
            out.append(line)
    return "\n".join(out)


def terminate(sql):
    """Append the statement terminator after the last line of code, not after a trailing comment.

    Several batches end with an explanatory `-- comment` line; putting the semicolon there comments
    it out and silently merges the statement with the next one."""
    lines = normalize_comments(sql).rstrip().split("\n")
    last = max((i for i, l in enumerate(lines)
                if l.strip() and not l.strip().startswith("--")), default=len(lines) - 1)
    lines[last] = lines[last].rstrip().rstrip(";") + ";"
    return "\n".join(lines) + "\n"


def strip_schemas(sql, schemas=("dbo",)):
    """Remove a schema prefix in either T-SQL quoting style.

    MySQL has no schema level below the database, so a prefix either disappears (a single-schema
    dataset such as AdventureWorks LT, where SalesLT and dbo do not collide) or is folded into the
    table name by the caller. Left in place it becomes a database reference and the load fails with
    "Unknown database".
    """
    for schema in schemas:
        sql = re.sub(rf'(?i)(["\[]?)\b{re.escape(schema)}\1?["\]]?\s*\.\s*', "", sql)
    return sql


def convert_types(sql):
    """Map SQL Server column types. Types may appear double-quoted (`"int"`), already unquoted here."""
    # SQL Server's MAX length (2 GB) has no size argument in MySQL; LONGTEXT/LONGBLOB are the
    # closest equivalents. AdventureWorks LT uses varbinary(max) for product photos.
    sql = re.sub(r"(?i)\b(?:n?varchar|n?text)\s*\(\s*max\s*\)", "LONGTEXT", sql)
    sql = re.sub(r"(?i)\b(?:var)?binary\s*\(\s*max\s*\)", "LONGBLOB", sql)
    # MySQL has no XML type. A typed XML column names its schema collection, which goes with it.
    sql = re.sub(r"(?i)\bxml\s*\(\s*`?[\w.`]+`?\s*\)", "LONGTEXT", sql)

    def sized(m):
        return f"{SIZED[m.group(1).lower()]}({m.group(2)})"
    sql = re.sub(r"(?i)\b(" + "|".join(SIZED) + r")\s*\(\s*([0-9]+(?:\s*,\s*[0-9]+)?)\s*\)", sized, sql)
    for src, dst in TYPE_MAP.items():
        sql = re.sub(rf"(?i)(?<![A-Za-z0-9_`]){src}(?![A-Za-z0-9_(])", dst, sql)
    # bare nvarchar/nchar with no length
    sql = re.sub(r"(?i)(?<![A-Za-z0-9_`])nvarchar(?![A-Za-z0-9_(])", "VARCHAR(255)", sql)
    sql = re.sub(r"(?i)(?<![A-Za-z0-9_`])nchar(?![A-Za-z0-9_(])", "CHAR(1)", sql)
    return sql


DATE_MDY = re.compile(r"'(\d{1,2})/(\d{1,2})/(\d{2}|\d{4})'")


def convert_dates_mdy(sql):
    """Rewrite `'MM/DD/YYYY'` literals to ISO, as `SET DATEFORMAT mdy` in the script requires.

    This is the one transformation that deliberately reaches inside string literals, so the pattern
    is anchored to a whole quoted value in exactly that shape: a phone number or address containing
    a slash cannot match, and MySQL cannot parse the mdy form at all."""
    def iso(m):
        month, day, year = int(m.group(1)), int(m.group(2)), m.group(3)
        if len(year) == 2:
            # SQL Server's default two-digit year cutoff is 2049: 00-49 -> 20xx, 50-99 -> 19xx
            year = f"20{year}" if int(year) <= 49 else f"19{year}"
        return f"'{year}-{month:02d}-{day:02d}'"
    return DATE_MDY.sub(iso, sql)


def translate(sql, drop_checks=(), keep_objects=True, dateformat=None, schemas=("dbo",),
              computed_types=None, materialize=()):
    """Return (statements, name_map, notes). `drop_checks` names CHECK constraints to omit."""
    name_map, notes, statements = {}, [], []
    identity_pk = {}     # table -> column that already carries PRIMARY KEY with its identity
    udts = collect_udts(sql)
    declared_pk = collect_declared_pks(sql)
    tsql_types = collect_tsql_types(sql)

    if tsql_types:
        notes.append(f"expanded CREATE TYPE aliases: {', '.join(sorted(tsql_types))}")
    if udts:
        notes.append(f"expanded user-defined types: {', '.join(sorted(udts))}")
    tables = {}          # lower-cased upstream table name -> MySQL identifier
    table_columns = {}   # lower-cased table name -> (columns, identity column)

    # a double-quoted or bracketed token naming a type is a type, not an identifier -- including
    # the script's own CREATE TYPE aliases, which are collected before the scan for this reason
    TYPE_WORDS = set(TYPE_MAP) | set(SIZED) | set(tsql_types)

    def dq(name, in_type_position=False):
        if in_type_position and name.strip().lower() in TYPE_WORDS:
            return name.strip().lower()      # `[Col] [int]`: the second token is the type
        mapped = ident(name)
        if name != mapped:
            name_map[name] = mapped
        return f"`{mapped}`"

    for batch in split_batches(sql):
      for batch in split_statements(batch):
        head = batch.strip()
        if SKIP_BATCH.match(head) or not re.sub(r"(?s)/\*.*?\*/|--[^\n]*", "", head).strip():
            continue
        if re.match(r"(?i)^\s*alter\s+table\s+.*\b(no)?check\s+constraint\s+all", head, re.S):
            continue                                    # constraint disabling has no MySQL analogue
        body = strip_schemas(batch, schemas)
        # classify on the first real statement: several batches open with a block comment
        lead = re.sub(r"(?s)^\s*(?:/\*.*?\*/|--[^\n]*\n)\s*", "", body)
        kind = "other"
        if re.match(r"(?i)^\s*create\s+table", lead): kind = "table"
        elif re.match(r"(?i)^\s*create\s+view", lead): kind = "view"
        elif re.match(r"(?i)^\s*create\s+proc", lead): kind = "procedure"
        elif re.match(r"(?i)^\s*create\s+trigger", lead): kind = "trigger"
        elif re.match(r"(?i)^\s*create\s+function", lead): kind = "function"
        elif re.match(r"(?i)^\s*alter\s+table", lead): kind = "constraint"
        elif re.match(r"(?i)^\s*(insert|update|delete)", lead): kind = "dml"

        body = scan_replace(body, on_dquote=dq)
        if kind == "table":
            m = re.search(r"(?i)CREATE\s+TABLE\s+(?:`([^`]+)`|(\w+))", body)
            if m:
                tname = m.group(1) or m.group(2)
                tables[tname.lower()] = tname
        if kind in ("view", "procedure", "constraint", "dml"):
            # bare (unquoted) references to a table must be lower-cased too
            body = scan_replace(body, on_word=lambda w: f"`{tables[w.lower()]}`" if w.lower() in tables else w)
        # filegroup placement and index-organisation keywords have no MySQL equivalent, and they
        # appear on CREATE INDEX as well as on tables and constraints
        body = re.sub(r"(?i)\s+ON\s+`primary`", "", body)
        body = re.sub(r"(?i)\b(?:NON)?CLUSTERED\s+(?=INDEX\b)", "", body)
        body = re.sub(r"(?i)\b(PRIMARY\s+KEY|UNIQUE)\s+(?:NON)?CLUSTERED", r"\1", body)
        if kind in ("table", "constraint"):
            body = convert_types(body)
            body = re.sub(r"(?i)\bIDENTITY\s*\(\s*\d+\s*,\s*\d+\s*\)", "AUTO_INCREMENT", body)
            body = re.sub(r"(?i)\bAUTO_INCREMENT\s+(NOT\s+NULL|NULL)", r"\1 AUTO_INCREMENT", body)
            body = re.sub(r"(?i)\bWITH\s+(?:NO)?CHECK\b(?!\s+OPTION)", "", body)
            # T-SQL parenthesises column defaults and lets them be named constraints;
            # MySQL supports neither: CONSTRAINT `df_x` DEFAULT (0) -> DEFAULT 0
            body = re.sub(r"(?i)\bDEFAULT\s*\(\s*([^()]+?)\s*\)", r"DEFAULT \1", body)
            body = re.sub(r"(?i)\bCONSTRAINT\s+`[^`]+`\s+(?=DEFAULT\b)", "", body)
            # MySQL cannot name a column-level PRIMARY KEY/UNIQUE constraint
            body = re.sub(r"(?i)\bCONSTRAINT\s+`?\w+`?\s+(?=(PRIMARY\s+KEY|UNIQUE)\b)", "", body)
            body = expand_alias_types(body, udts)          # sp_addtype (pubs)
            body = expand_alias_types(body, tsql_types)    # CREATE TYPE ... FROM (AdventureWorks)
            body = convert_like_classes(body)
            body = convert_functions(body)
            if kind == "table":
                body, generated = convert_computed(body, computed_types or {}, materialize)
                # AdventureWorks LT's scripts end several column lists with a trailing comma
                body = re.sub(r",(\s*\)\s*;?)$", r"\1", body.rstrip())
                # only now does IDENTITY(1,1) exist as AUTO_INCREMENT
                body, identity = inline_identity_pk(body, declared_pk)
                if identity:
                    identity_pk[identity[0]] = identity[1]
                body, n_fk = hoist_inline_references(body)
                if n_fk:
                    notes.append(f"hoisted {n_fk} inline REFERENCES to table-level FOREIGN KEYs")
            body = re.sub(r"(?i)\bNOT\s+FOR\s+REPLICATION\b", "", body)
            body = re.sub(r"(?i)\s+\bROWGUIDCOL\b", "", body)          # a marker attribute only
            # NEWID()/NEWSEQUENTIALID() defaults: the data files supply every rowguid, and MySQL
            # cannot default a CHAR column to a generated UUID anyway
            body = re.sub(r"(?i)\s+DEFAULT\s*\(?\s*NEWSEQUENTIALID\s*\(\s*\)\s*\)?", "", body)
            body = re.sub(r"(?i)\s+DEFAULT\s*\(?\s*NEWID\s*\(\s*\)\s*\)?", "", body)
            for name in drop_checks:                     # CHECKs MySQL cannot express
                body = re.sub(rf"(?is),?\s*CONSTRAINT\s+`{re.escape(ident(name))}`\s+CHECK\s*\((?:[^()]|\([^()]*\))*\)",
                              "", body)
                notes.append(f"dropped CHECK {name}")
        if kind == "dml":
            if dateformat == "mdy":
                body = convert_dates_mdy(body)
            body = strip_money_literals(body)
            body = re.sub(r"(?i)^\s*INSERT\s+(?!INTO)", "INSERT INTO ", body, count=1)
            body = re.sub(r"(?i)\n\s*INSERT\s+(?!INTO)", "\nINSERT INTO ", body)
            tm = re.match(r"(?i)\s*INSERT\s+INTO\s+(?:`([^`]+)`|(\w+))\s+VALUES\b", body)
            if tm:
                key = (tm.group(1) or tm.group(2)).lower()
                cols, identity = table_columns.get(key, ([], None))
                if identity:
                    body = add_column_list(body, cols, identity)
        if kind == "table":
            m = re.search(r"(?i)CREATE\s+TABLE\s+(?:`([^`]+)`|(\w+))", body)
            if m:
                table_columns[(m.group(1) or m.group(2)).lower()] = parse_columns(body)
        if kind == "constraint":
            # T-SQL takes several clauses under one ADD; MySQL wants ADD on each of them. Splitting
            # them also lets a primary key already declared with an identity column be dropped on
            # its own, without losing the other clauses of the same statement.
            head = re.match(r"(?is)^(\s*ALTER\s+TABLE\s+`?(\w+)`?\s+)ADD\s+(.*?);?\s*$", body.strip())
            if head:
                clauses = []
                for clause in split_top(head.group(3), ","):
                    clause = clause.strip()
                    dup = re.match(r"(?is)^(?:CONSTRAINT\s+`?\w+`?\s+)?PRIMARY\s+KEY\s*"
                                   r"\(\s*`?(\w+)`?\s*\)$", clause)
                    if dup and identity_pk.get(head.group(2).lower()) == dup.group(1).lower():
                        notes.append("dropped a PRIMARY KEY already declared with its identity column")
                        continue
                    clauses.append(clause)
                if not clauses:
                    continue
                body = head.group(1) + ", ".join("ADD " + c for c in clauses)
        if kind == "view":
            # view attributes: SCHEMABINDING ties a view to its tables' schema, VIEW_METADATA
            # changes what the client driver reports. Neither has a MySQL equivalent.
            body = re.sub(r"(?i)\s+WITH\s+(SCHEMABINDING|VIEW_METADATA|ENCRYPTION)"
                          r"(\s*,\s*(SCHEMABINDING|VIEW_METADATA|ENCRYPTION))*", "", body)
        if kind in ("view", "procedure", "trigger"):
            body = convert_functions(convert_tsql_convert(convert_xml_value(body)))
            body = convert_recursive_cte(body)
        if kind in ("view", "procedure") and not keep_objects:
            notes.append(f"skipped {kind}")
            continue
        statements.append({"kind": kind, "sql": body.strip(),
                           "generated": generated if kind == "table" else []})
    # SQL Server can index a view; MySQL has no materialised views, so those indexes go away
    views = {m.group(1) for st in statements if st["kind"] == "view"
             for m in [re.search(r"(?is)^\s*CREATE\s+VIEW\s+`([^`]+)`", st["sql"])] if m}
    on_view = re.compile(r"(?is)^\s*CREATE\s+(?:UNIQUE\s+)?INDEX\s+`[^`]+`\s+ON\s+`([^`]+)`")
    kept = []
    for st in statements:
        m = on_view.match(st["sql"])
        if m and m.group(1) in views:
            notes.append(f"dropped an index on view {m.group(1)}: MySQL has no indexed views")
            continue
        kept.append(st)
    return kept, name_map, notes
