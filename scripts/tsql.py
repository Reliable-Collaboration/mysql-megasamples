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
import re

TYPE_MAP = {
    "int": "INT", "smallint": "SMALLINT", "bigint": "BIGINT",
    # SQL Server tinyint is UNSIGNED 0..255; MySQL's plain TINYINT is signed -128..127, so an
    # unqualified mapping silently rejects any value above 127 (pubs.jobs.min_lvl hits this).
    "tinyint": "TINYINT UNSIGNED",
    "bit": "TINYINT(1)", "money": "DECIMAL(19,4)", "smallmoney": "DECIMAL(10,4)",
    "datetime": "DATETIME", "smalldatetime": "DATETIME", "float": "DOUBLE", "real": "FLOAT",
    "ntext": "TEXT", "text": "TEXT", "image": "MEDIUMBLOB", "uniqueidentifier": "BINARY(16)",
}
SIZED = {"nvarchar": "VARCHAR", "varchar": "VARCHAR", "nchar": "CHAR", "char": "CHAR",
         "decimal": "DECIMAL", "numeric": "DECIMAL", "binary": "BINARY", "varbinary": "VARBINARY"}

SKIP_BATCH = re.compile(
    r"^\s*(if\s+exists|set\s+(nocount|dateformat|quoted_identifier|ansi_nulls|rowcount)\b"
    r"|set\s+identity_insert|use\s+|go\s*$|--"
    # server maintenance and messaging with no MySQL equivalent; the pipeline runs its own
    # ANALYZE TABLE after loading, so UPDATE STATISTICS is redundant rather than lost
    r"|update\s+statistics\b|dbcc\b|raiserror\b|print\b|checkpoint\b"
    r"|exec(ute)?\s+sp_)", re.I)


def ident(name):
    """Upstream identifier -> MySQL identifier: lower case, spaces to underscores."""
    return name.strip().lower().replace(" ", "_")


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
    """Walk sql outside string literals and comments, rewriting double-quoted names and bare words."""
    out, i, n = [], 0, len(sql)
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
        if ch == '"' and on_dquote:                    # "quoted" identifier
            end = sql.find('"', i + 1)
            if end > 0:
                out.append(on_dquote(sql[i + 1:end])); i = end + 1; continue
        if ch == "[" and on_dquote:                    # [bracketed] identifier (the other T-SQL style)
            end = sql.find("]", i + 1)
            if end > 0:
                out.append(on_dquote(sql[i + 1:end])); i = end + 1; continue
        if on_word and (ch.isalpha() or ch == "_"):    # bare word
            m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", sql[i:])
            word = m.group(0)
            out.append(on_word(word)); i += len(word); continue
        out.append(ch); i += 1
    return "".join(out)


CAST_TYPES = {"money": "DECIMAL(19,4)", "smallmoney": "DECIMAL(10,4)", "int": "SIGNED",
              "bigint": "SIGNED", "smallint": "SIGNED", "tinyint": "SIGNED", "bit": "SIGNED",
              "float": "DOUBLE", "real": "DOUBLE", "datetime": "DATETIME", "date": "DATE"}


def _cast_type(tsql_type):
    """Map a T-SQL type used as a CONVERT/CAST target to a MySQL CAST target type."""
    t = tsql_type.strip()
    m = re.match(r"(?i)^(n?varchar)\s*\(\s*(\d+)\s*\)$", t)
    if m:
        return f"VARCHAR({m.group(2)})"
    m = re.match(r"(?i)^(n?char)\s*\(\s*(\d+)\s*\)$", t)
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


def collect_udts(sql):
    """`execute sp_addtype name, 'basetype', 'NOT NULL'` -> {name: 'BASETYPE NOT NULL'}."""
    udts = {}
    for m in re.finditer(r"(?im)^\s*exec(?:ute)?\s+sp_addtype\s+(\w+)\s*,\s*'([^']+)'\s*(?:,\s*'([^']*)')?", sql):
        name, base, nullability = m.group(1), m.group(2), (m.group(3) or "")
        udts[name.lower()] = f"{base.strip()} {nullability.strip()}".strip()
    return udts


def expand_udts(sql, udts):
    """Replace a user-defined type used as a column type with its base type."""
    for name, expansion in udts.items():
        sql = re.sub(rf"(?i)(`\w+`\s+){name}(?![A-Za-z0-9_(])", rf"\g<1>{expansion}", sql)
    return sql


def convert_functions(sql):
    """Map SQL Server built-ins to their MySQL equivalents.

    CURRENT_TIMESTAMP is used rather than NOW() because it is also legal in a DEFAULT clause, which
    is where getdate() most often appears."""
    sql = re.sub(r"(?i)\bGETDATE\s*\(\s*\)", "CURRENT_TIMESTAMP", sql)
    sql = re.sub(r"(?i)\bGETUTCDATE\s*\(\s*\)", "UTC_TIMESTAMP", sql)
    sql = re.sub(r"(?i)\bISNULL\s*\(", "IFNULL(", sql)
    sql = re.sub(r"(?i)\bLEN\s*\(", "CHAR_LENGTH(", sql)
    return sql


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


def strip_dbo(sql):
    """Remove the dbo schema prefix in either quoting style."""
    return re.sub(r'(?i)(["\[]?)\bdbo\1?["\]]?\s*\.\s*', "", sql)


def convert_types(sql):
    """Map SQL Server column types. Types may appear double-quoted (`"int"`), already unquoted here."""
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


def translate(sql, drop_checks=(), keep_objects=True, dateformat=None):
    """Return (statements, name_map, notes). `drop_checks` names CHECK constraints to omit."""
    name_map, notes, statements = {}, [], []
    udts = collect_udts(sql)
    if udts:
        notes.append(f"expanded user-defined types: {', '.join(sorted(udts))}")
    tables = {}          # lower-cased upstream table name -> MySQL identifier
    table_columns = {}   # lower-cased table name -> (columns, identity column)

    TYPE_WORDS = set(TYPE_MAP) | set(SIZED)

    def dq(name):
        if name.strip().lower() in TYPE_WORDS:
            return name.strip().lower()      # `"int"` is a type name, not an identifier
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
        body = strip_dbo(batch)
        # classify on the first real statement: several batches open with a block comment
        lead = re.sub(r"(?s)^\s*(?:/\*.*?\*/|--[^\n]*\n)\s*", "", body)
        kind = "other"
        if re.match(r"(?i)^\s*create\s+table", lead): kind = "table"
        elif re.match(r"(?i)^\s*create\s+view", lead): kind = "view"
        elif re.match(r"(?i)^\s*create\s+proc", lead): kind = "procedure"
        elif re.match(r"(?i)^\s*create\s+trigger", lead): kind = "trigger"
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
        if kind in ("table", "constraint"):
            body = convert_types(body)
            body = re.sub(r"(?i)\bIDENTITY\s*\(\s*\d+\s*,\s*\d+\s*\)", "AUTO_INCREMENT", body)
            body = re.sub(r"(?i)\bAUTO_INCREMENT\s+(NOT\s+NULL|NULL)", r"\1 AUTO_INCREMENT", body)
            body = re.sub(r"(?i)\b(PRIMARY\s+KEY|UNIQUE)\s+(CLUSTERED|NONCLUSTERED)", r"\1", body)
            body = re.sub(r"(?i)\bWITH\s+NOCHECK\b", "", body)
            body = re.sub(r"(?i)\s+ON\s+`primary`", "", body)      # filegroup placement
            # T-SQL parenthesises column defaults and lets them be named constraints;
            # MySQL supports neither: CONSTRAINT `df_x` DEFAULT (0) -> DEFAULT 0
            body = re.sub(r"(?i)\bDEFAULT\s*\(\s*([^()]+?)\s*\)", r"DEFAULT \1", body)
            body = re.sub(r"(?i)\bCONSTRAINT\s+`[^`]+`\s+(?=DEFAULT\b)", "", body)
            # MySQL cannot name a column-level PRIMARY KEY/UNIQUE constraint
            body = re.sub(r"(?i)\bCONSTRAINT\s+`?\w+`?\s+(?=(PRIMARY\s+KEY|UNIQUE)\b)", "", body)
            body = expand_udts(body, udts)
            body = convert_like_classes(body)
            body = convert_functions(body)
            if kind == "table":
                body, n_fk = hoist_inline_references(body)
                if n_fk:
                    notes.append(f"hoisted {n_fk} inline REFERENCES to table-level FOREIGN KEYs")
            body = re.sub(r"(?i)\bNOT\s+FOR\s+REPLICATION\b", "", body)
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
        if kind in ("view", "procedure", "trigger"):
            body = convert_functions(convert_tsql_convert(body))
        if kind in ("view", "procedure") and not keep_objects:
            notes.append(f"skipped {kind}")
            continue
        statements.append({"kind": kind, "sql": body.strip()})
    return statements, name_map, notes
