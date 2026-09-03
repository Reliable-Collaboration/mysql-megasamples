#!/usr/bin/env python3
"""An Oracle to MySQL translator for the oracle-samples/db-sample-schemas install scripts.

The scripts are plain SQL*Plus: `;`-terminated statements, `REM`/`PROMPT` directives, `CREATE
SEQUENCE`, `COMMENT ON`, identity columns and Oracle type names. As in the T-SQL translator, every
transformation runs on a scanner that tracks string literals so that data is never rewritten.

Type mapping follows knowledge/datasets/oracle-hr.md and oracle-co.md:
  NUMBER(p,s) -> DECIMAL(p,s)      NUMBER(p) -> the narrowest integer that holds p digits
  NUMBER      -> INT               (the sample schemas only use it for small integer keys; the
                                    converter asserts integrality when it emits data)
  VARCHAR2(n [CHAR|BYTE]) -> VARCHAR(n)     CHAR(n) -> CHAR(n)
  DATE -> DATETIME                 (an Oracle DATE carries a time component)
  TIMESTAMP[(p)] -> DATETIME(6)    CLOB -> LONGTEXT       BLOB -> LONGBLOB
"""
import re

SKIP_LINE = re.compile(r"(?i)^\s*(rem\b|prompt\b|set\s+\w+|@|--|/\s*$)")


PLSQL_START = re.compile(r"(?i)^\s*create\s+(or\s+replace\s+)?(procedure|function|trigger|package|type)\b")


ASSIGNMENT = re.compile(r"(?is)^[ \t]*(\w+)\s*:=\s*(.*?);\s*$", re.M)


def _eval_concat(expr):
    """Evaluate a PL/SQL concatenation of string literals and chr(n) calls to one Python string."""
    parts, out = split_top_level(expr, "|"), []
    # split_top_level splits on a single '|', so rejoin the empty halves of each '||'
    merged = [p for p in parts if p.strip()]
    for part in merged:
        part = part.strip()
        m = re.fullmatch(r"(?i)chr\s*\(\s*(\d+)\s*\)", part)
        if m:
            out.append(chr(int(m.group(1)))); continue
        if part.startswith("'") and part.endswith("'"):
            out.append(part[1:-1].replace("''", "'")); continue
        return None                       # anything else is not a constant expression
    return "".join(out)


def resolve_variables(sql):
    """Inline PL/SQL variables that are assigned a constant expression.

    The CO populate script exceeds SQL*Plus's line limit for one JSON document and works around it
    with `prod_details := '...' || chr(10) || '...';` followed by a reference to the variable. The
    value has to be inlined or the row cannot be written at all.
    """
    values = {}
    def capture(m):
        value = _eval_concat(m.group(2))
        if value is None:
            return m.group(0)
        values[m.group(1)] = value
        return ""                          # the assignment itself has no MySQL equivalent
    sql = ASSIGNMENT.sub(capture, sql)
    for name, value in values.items():
        literal = "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"
        sql = re.sub(rf"(?<![\w.]){re.escape(name)}(?![\w])", literal, sql)
    return sql


def split_statements(sql):
    """Split a SQL*Plus script into statements.

    PL/SQL units (`CREATE OR REPLACE PROCEDURE ...`) are terminated by a line containing only `/`
    and are extracted whole, because their bodies contain `;` of their own and splitting on that
    would shred them. The rest is split on `;` outside string literals, and the anonymous
    `BEGIN`/`END` wrapper the populate scripts put around their inserts is discarded so each insert
    stands as its own statement.
    """
    units, plain, lines, i = [], [], sql.split("\n"), 0
    while i < len(lines):
        if PLSQL_START.match(lines[i]):
            block = []
            while i < len(lines) and lines[i].strip() != "/":
                block.append(lines[i]); i += 1
            i += 1
            units.append("\n".join(block))
            continue
        plain.append(lines[i]); i += 1
    return units + _split_on_semicolons("\n".join(plain))


def _split_on_semicolons(sql):
    out, cur, i, n = [], [], 0, len(sql)
    while i < n:
        ch = sql[i]
        if ch == "'":
            cur.append(ch); i += 1
            while i < n:
                if sql[i] == "'":
                    if i + 1 < n and sql[i + 1] == "'":
                        cur.append("''"); i += 2; continue
                    cur.append("'"); i += 1; break
                cur.append(sql[i]); i += 1
            continue
        if sql.startswith("--", i):
            end = sql.find("\n", i); end = n if end < 0 else end
            cur.append(sql[i:end]); i = end; continue
        if sql.startswith("/*", i):
            end = sql.find("*/", i + 2); end = n if end < 0 else end + 2
            cur.append(sql[i:end]); i = end; continue
        if ch == ";":
            out.append("".join(cur)); cur = []; i += 1; continue
        cur.append(ch); i += 1
    if "".join(cur).strip():
        out.append("".join(cur))
    return [x.strip() for x in out if x.strip()]


def strip_directives(statement):
    """Remove SQL*Plus directives, then the anonymous PL/SQL block wrapper.

    The populate scripts read `REM ... / Prompt ... / BEGIN / INSERT ...;`, so the wrapper only
    becomes visible once the directive lines are gone -- stripping it first silently loses the
    first row of every table."""
    body = "\n".join(l for l in statement.split("\n") if not SKIP_LINE.match(l))
    body = re.sub(r"(?is)^\s*(BEGIN|DECLARE)\b\s*", "", body)
    body = re.sub(r"(?is)\s*\bEND\s*$", "", body)
    return body


def convert_types(sql):
    def number(m):
        precision, scale = m.group(1), m.group(2)
        if scale:
            return f"DECIMAL({precision},{scale.strip()})"
        p = int(precision)
        if p <= 2: return "TINYINT"
        if p <= 4: return "SMALLINT"
        if p <= 9: return "INT"
        return "BIGINT"
    sql = re.sub(r"(?i)\bNUMBER\s*\(\s*(\d+)\s*(?:,\s*(-?\d+)\s*)?\)", number, sql)
    sql = re.sub(r"(?i)\bNUMBER\b(?!\s*\()", "INT", sql)
    sql = re.sub(r"(?i)\bVARCHAR2\s*\(\s*(\d+)\s*(?:CHAR|BYTE)?\s*\)", r"VARCHAR(\1)", sql)
    sql = re.sub(r"(?i)\bNVARCHAR2\s*\(\s*(\d+)\s*\)", r"VARCHAR(\1)", sql)
    sql = re.sub(r"(?i)\bTIMESTAMP\s*(?:\(\s*\d+\s*\))?(\s+WITH(\s+LOCAL)?\s+TIME\s+ZONE)?", "DATETIME(6)", sql)
    sql = re.sub(r"(?i)\bCLOB\b", "LONGTEXT", sql)
    sql = re.sub(r"(?i)\bBLOB\b", "LONGBLOB", sql)
    sql = re.sub(r"(?i)\bDATE\b(?!\s*\()", "DATETIME", sql)
    return sql


def json_columns(sql):
    """Columns the schema declares as JSON via a CHECK constraint, wherever that check appears.

    The check is often a separate ALTER TABLE, so it has to be collected from the whole script
    before any CREATE TABLE is rewritten."""
    return {c.lower() for c in re.findall(r"(?is)CHECK\s*\(\s*(\w+)\s+IS\s+JSON", sql)}


def convert_ddl(sql, json_cols=()):
    """Oracle-specific DDL spellings that MySQL states differently."""
    # a named column-level NOT NULL: MySQL cannot name it
    sql = re.sub(r"(?is)\bCONSTRAINT\s+\w+\s+(NOT\s+NULL)", r"\1", sql)
    # identity columns
    sql = re.sub(r"(?is)\bGENERATED\s+(?:BY\s+DEFAULT\s+)?(?:ON\s+NULL\s+)?(?:ALWAYS\s+)?AS\s+IDENTITY"
                 r"(\s*\([^)]*\))?", "AUTO_INCREMENT", sql)
    # An Oracle "CHECK (col IS JSON)" on a BLOB/CLOB column is how the schema declares a JSON
    # document. MySQL has a real JSON type, so retype the column and drop the check -- leaving it
    # as LONGBLOB would make every JSON function fail with "CHARACTER SET 'binary'".
    for col in set(re.findall(r"(?is)CHECK\s*\(\s*(\w+)\s+IS\s+JSON", sql)) | set(json_cols):
        sql = re.sub(rf"(?im)^(\s*,?\s*{re.escape(col)}\s+)(LONGBLOB|LONGTEXT|BLOB|CLOB)\b", r"\1JSON", sql)
    sql = re.sub(r"(?is),?\s*(?:CONSTRAINT\s+\w+\s+)?CHECK\s*\(\s*\w+\s+IS\s+JSON[^)]*\)", "", sql)
    # a trailing ENABLE on a constraint clause; anchored so it cannot eat text elsewhere
    sql = re.sub(r"(?i)\s+ENABLE(?=\s*[,)\n;]|\s*$)", "", sql)
    sql = re.sub(r"(?i)\s+USING\s+INDEX\b", "", sql)
    sql = re.sub(r"(?i)\s+ORGANIZATION\s+INDEX\b", "", sql)
    return sql


LISTAGG = re.compile(r"(?is)\bLISTAGG\s*\(")


def convert_listagg(sql):
    """`LISTAGG(expr, sep [ON OVERFLOW ...]) WITHIN GROUP (ORDER BY x)` -> GROUP_CONCAT.

    MySQL truncates GROUP_CONCAT at group_concat_max_len (1024 by default) where Oracle's ON
    OVERFLOW clause makes the truncation explicit, so the view carries a comment saying so.
    """
    while True:
        m = LISTAGG.search(sql)
        if not m:
            return sql
        depth, j, n = 1, m.end(), len(sql)
        while j < n and depth:
            if sql[j] == "'":
                j += 1
                while j < n and sql[j] != "'":
                    j += 1
            elif sql[j] == "(":
                depth += 1
            elif sql[j] == ")":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        args = sql[m.end():j]
        rest = sql[j + 1:]
        args = re.sub(r"(?is)\s+ON\s+OVERFLOW\s+(TRUNCATE|ERROR).*$", "", args).strip()
        parts = split_top_level(args)
        expr = parts[0] if parts else args
        sep = parts[1].strip() if len(parts) > 1 else "','"
        order = ""
        w = re.match(r"(?is)\s*WITHIN\s+GROUP\s*\(\s*(ORDER\s+BY\s.*?)\)", rest)
        if w:
            order = " " + w.group(1).strip()
            rest = rest[w.end():]
        sql = sql[:m.start()] + f"GROUP_CONCAT({expr}{order} SEPARATOR {sep})" + rest


BUILTINS = ("sum count avg min max round trunc abs coalesce nvl decode substr instr length lower upper "
            "to_char cast extract greatest least mod power sqrt concat replace trim ltrim rtrim "
            "group_concat json_object json_arrayagg row_number rank dense_rank listagg").split()


def close_function_spaces(sql):
    """Remove the space between a built-in function name and its opening parenthesis.

    Oracle accepts `SUM (x)`; MySQL, without IGNORE_SPACE in sql_mode, reads that as a reference to
    a stored function named SUM and fails with "FUNCTION db.SUM does not exist".
    """
    for fn in BUILTINS:
        sql = re.sub(rf"(?i)(?<![\w.]){fn}\s+\(", f"{fn}(", sql)
    return sql


def convert_view(sql):
    """Oracle view clauses MySQL does not have. WITH READ ONLY is implicit for a join view."""
    sql = re.sub(r"(?is)\s+WITH\s+READ\s+ONLY\s*$", "", sql)
    sql = re.sub(r"(?is)\s+WITH\s+CHECK\s+OPTION\s*(CONSTRAINT\s+\w+)?\s*$", " WITH CHECK OPTION", sql)
    sql = re.sub(r"(?i)^CREATE\s+OR\s+REPLACE\s+", "CREATE ", sql)
    return close_function_spaces(convert_listagg(sql))


def view_blockers(sql):
    """Oracle view constructs with no MySQL equivalent, reported rather than mistranslated."""
    blockers = []
    if re.search(r"(?is)\bGROUPING\s+SETS\b", sql):
        blockers.append("GROUPING SETS, which MySQL 9.7 parses but rejects at execution "
                        "(ERROR 3889, a HeatWave-only feature verified at P-02); WITH ROLLUP is "
                        "the portable form but produces a different row set")
    if re.search(r"(?is)\bCONNECT\s+BY\b|\bSTART\s+WITH\b", sql):
        blockers.append("CONNECT BY hierarchical query, which MySQL spells as a recursive CTE")
    if re.search(r"(?is)\bMODEL\b\s+", sql):
        blockers.append("the MODEL clause, which MySQL has no equivalent for")
    return blockers


def unwrap_call(sql, function):
    """Replace `function(expr)` with `expr`, matching the closing paren by depth."""
    pattern = re.compile(r"(?i)(?<![\w.])" + re.escape(function).replace(r"\.", r"\s*\.\s*") + r"\s*\(")
    while True:
        m = pattern.search(sql)
        if not m:
            return sql
        depth, j, n = 1, m.end(), len(sql)
        while j < n and depth:
            if sql[j] == "'":                      # skip string literals when counting parens
                j += 1
                while j < n:
                    if sql[j] == "'":
                        if j + 1 < n and sql[j + 1] == "'":
                            j += 2; continue
                        break
                    j += 1
            elif sql[j] == "(":
                depth += 1
            elif sql[j] == ")":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        sql = sql[:m.start()] + sql[m.end():j].strip() + sql[j + 1:]


def convert_values(sql):
    """Oracle value constructors that MySQL spells as plain literals."""
    # TO_DATE('01-JAN-2020','DD-MON-YYYY') and TO_TIMESTAMP(...) -> the literal, normalised
    def to_date(m):
        return "'" + oracle_date_literal(m.group(1), m.group(2)) + "'"
    sql = re.sub(r"(?is)\bTO_(?:DATE|TIMESTAMP)\s*\(\s*'([^']*)'\s*,\s*'([^']*)'\s*\)", to_date, sql)
    # UTL_RAW.CAST_TO_RAW(x) wraps a JSON document; MySQL takes the value directly. The whole
    # call is replaced with its argument -- stripping only the prefix would leave its closing
    # paren behind and break the statement.
    sql = unwrap_call(sql, "UTL_RAW.CAST_TO_RAW")
    sql = re.sub(r"(?is)\bSYSDATE\b", "CURRENT_TIMESTAMP", sql)
    return sql


MONTHS = {m: i + 1 for i, m in enumerate(
    ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"])}


TOKENS = [("YYYY", r"(?P<Y>\d{4})"), ("RRRR", r"(?P<Y>\d{4})"), ("MON", r"(?P<b>[A-Za-z]{3})"),
          ("MONTH", r"(?P<B>[A-Za-z]+)"), ("DD", r"(?P<d>\d{1,2})"), ("MM", r"(?P<m>\d{1,2})"),
          ("HH24", r"(?P<H>\d{1,2})"), ("HH", r"(?P<H>\d{1,2})"), ("MI", r"(?P<M>\d{1,2})"),
          ("SS", r"(?P<S>\d{1,2})"), ("YY", r"(?P<y>\d{2})"), ("RR", r"(?P<y>\d{2})")]


def mask_to_regex(mask):
    """Compile an Oracle date format mask into a regex with named groups."""
    pattern, i, m = "", 0, mask.upper()
    while i < len(m):
        for token, group in TOKENS:
            if m.startswith(token, i):
                pattern += group; i += len(token); break
        else:
            if m.startswith("FF", i):                 # FF or FFn: fractional seconds
                i += 2
                while i < len(m) and m[i].isdigit():
                    i += 1
                pattern += r"(?P<f>\d*)"
            else:
                pattern += re.escape(mask[i]); i += 1
    return re.compile("^" + pattern + "$")


def oracle_date_literal(value, mask):
    """Normalise an Oracle date/timestamp literal to ISO, driven by its format mask.

    Guessing the layout from the value is not safe: `01-02-2020` is 1 February under `dd-MM-yyyy`
    and 2 January under `MM-dd-yyyy`, and both masks appear in these schemas.
    """
    v = value.strip()
    match = mask_to_regex(mask).match(v)
    if not match:
        return v                                       # leave it alone rather than corrupt it
    g = match.groupdict()
    year = g.get("Y")
    if not year and g.get("y"):
        year = f"20{g['y']}" if int(g["y"]) <= 49 else f"19{g['y']}"
    month = g.get("m") or (MONTHS.get((g.get("b") or "").upper()) if g.get("b") else None)
    if month is None and g.get("B"):
        month = MONTHS.get(g["B"][:3].upper())
    day = g.get("d") or "1"
    time = f"{int(g.get('H') or 0):02d}:{int(g.get('M') or 0):02d}:{int(g.get('S') or 0):02d}"
    frac = (g.get("f") or "")[:6]                      # MySQL keeps at most 6 fractional digits
    return f"{year}-{int(month):02d}-{int(day):02d} {time}" + (f".{frac}" if frac else "")


def split_top_level(text, sep=","):
    """Split on `sep` at paren depth zero, outside string literals."""
    parts, cur, depth, i, n = [], [], 0, 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "'":
            cur.append(ch); i += 1
            while i < n:
                if text[i] == "'":
                    if i + 1 < n and text[i + 1] == "'":
                        cur.append("''"); i += 2; continue
                    cur.append("'"); i += 1; break
                cur.append(text[i]); i += 1
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(cur)); cur = []; i += 1; continue
        cur.append(ch); i += 1
    if "".join(cur).strip():
        parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def collect_primary_keys(statement, primary_keys):
    """Record each table's primary key columns, from either a CREATE TABLE or an ALTER TABLE."""
    table = re.search(r"(?i)^\s*(?:CREATE\s+TABLE|ALTER\s+TABLE)\s+(\w+)", statement)
    pk = re.search(r"(?i)PRIMARY\s+KEY\s*\(([^)]*)\)", statement)
    if table and pk:
        primary_keys.setdefault(table.group(1).lower(),
                                [c.strip() for c in pk.group(1).split(",")])


IDENTITY_COL = re.compile(r"(?im)^\s*,?\s*(\w+)\s+([A-Za-z]+(?:\s*\([^)]*\))?(?:\s+UNSIGNED)?)\s+AUTO_INCREMENT")


def inline_identity_pk(create_table):
    """Give an identity column its PRIMARY KEY inline, and report which key that makes redundant.

    MySQL requires an AUTO_INCREMENT column to be a key the moment it is declared, but these schemas
    add the primary key afterwards with ALTER TABLE. Deferring the AUTO_INCREMENT instead does not
    work either: the rows are inserted with NULL in that column (Oracle's `GENERATED BY DEFAULT ON
    NULL` generates the value), so the later ALTER fails on NULLs. Declaring it inline keeps the
    generation working during the load; the matching ALTER is then dropped as a duplicate.
    """
    table = re.search(r"(?i)CREATE\s+TABLE\s+(\w+)", create_table)
    if not table or "AUTO_INCREMENT" not in create_table.upper():
        return create_table, None
    col = IDENTITY_COL.search(create_table)
    if not col:
        return create_table, None
    close = create_table.rfind(")")
    head = create_table[:close].rstrip().rstrip(",")
    return (head + f",\n  PRIMARY KEY ({col.group(1)})\n" + create_table[close:],
            (table.group(1).lower(), col.group(1).lower()))


def convert_alter(statement, primary_keys):
    """Oracle's `ALTER TABLE t ADD ( c1, c2 )` -> MySQL's `ALTER TABLE t ADD c1, ADD c2`, and fill
    in a REFERENCES column list where Oracle let it default to the target's primary key."""
    m = re.match(r"(?is)^(\s*ALTER\s+TABLE\s+\w+\s*)ADD\s*\((.*)\)\s*$", statement)
    if m:
        clauses = split_top_level(m.group(2))
        statement = m.group(1) + ", ".join("ADD " + c for c in clauses)

    def fill(ref):
        table = ref.group(1)
        cols = primary_keys.get(table.lower())
        return f"REFERENCES {table} ({', '.join(cols)})" if cols else ref.group(0)
    # REFERENCES t   (no column list) -- legal in Oracle, rejected by MySQL
    statement = re.sub(r"(?i)\bREFERENCES\s+(\w+)\s*(?![\s(]*\()", fill, statement)
    return statement


def classify(statement):
    s = strip_directives(statement).strip()
    # MySQL has no constraint enable/disable; these statements have no equivalent at all
    if re.match(r"(?is)^alter\s+table\s+\w+\s+(disable|enable)\s+constraint", s):
        return "skip", s
    for pattern, kind in [(r"(?i)^create\s+table", "table"),
                          (r"(?i)^create\s+(unique\s+)?index", "index"),
                          (r"(?i)^create\s+sequence", "sequence"),
                          (r"(?i)^create\s+(or\s+replace\s+)?view", "view"),
                          (r"(?i)^create\s+(or\s+replace\s+)?(procedure|function|trigger|package)", "routine"),
                          (r"(?i)^alter\s+table", "constraint"),
                          (r"(?i)^comment\s+on", "comment"),
                          (r"(?i)^insert\s+into", "dml")]:
        if re.match(pattern, s):
            return kind, s
    return ("empty" if not s else "other"), s
