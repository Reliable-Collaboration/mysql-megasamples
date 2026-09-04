#!/usr/bin/env python3
"""Translate a T-SQL routine body -- procedure, function or trigger -- into a MySQL one.

Why this is hand-written rather than delegated. `sqlglot` is already in this project's stack and is
the obvious candidate, so it was tried on the simplest routine in AdventureWorks, a twelve-line
scalar function. It dropped the `RETURNS int` type, turned `IF (@ret IS NULL) SET @ret = 0` into an
**empty string**, and parsed `RETURN @ret` as a column alias -- while printing `Unsupported If block
syntax` and emitting confident-looking output anyway. Its own record says it: "SQLGlot is a
transpiler, not a validator." For statements it is used and useful; for procedural bodies it is
worse than nothing, because the failure is silent.

What makes a hand-written translator tractable here is that the census is small and closed. Across
the 47 routines in AdventureWorks, AdventureWorks DW, Northwind and pubs there are **no** WHILE
loops, no cursors, no table variables, no dynamic SQL, no MERGE and no GOTO -- the constructs that
make general T-SQL translation hard. What is left is eleven mechanical rewrites over 1,276 lines.
WideWorldImporters is the opposite case and is mostly refused rather than translated: 57 of its 72
routines are SQL Server feature configuration, SSIS ETL or the randomised data generator, and a
procedure whose body is `ALTER TABLE ... ADD COLUMNSTORE INDEX` has no MySQL meaning to translate to.

Two conventions this makes visible rather than hidden:

* `@Local` becomes `v_local` and `@Param` becomes `p_param`. T-SQL's sigil keeps variables and
  columns apart; MySQL has no sigil, so a local named `Name` inside a routine that also selects a
  `Name` column resolves to the column. The prefix restores the separation.
* MySQL requires every DECLARE at the top of its block, before any statement; T-SQL scatters them.
  Declarations are hoisted, and an initialiser that cannot move with them is left behind as a SET.

Anything not in the census raises `Unportable`, which the caller reports as a dropped object with a
stated reason. Nothing is emitted on a guess.
"""
import re

# ------------------------------------------------------------------ refusals

class Unportable(Exception):
    """Raised with the reason a routine is not translated, for the caller to report."""


BLOCKERS = [
    (r"(?i)\bRETURNS\s+@\w+\s+TABLE\b",
     "returns a table; MySQL has no table-valued functions"),
    (r"(?i)\bON\s+(DATABASE|ALL\s+SERVER)\b",
     "is a DDL trigger (ON DATABASE), which MySQL has no equivalent for"),
    (r"(?i)\bERROR_(NUMBER|MESSAGE|SEVERITY|STATE|LINE|PROCEDURE)\s*\(",
     "calls SQL Server's ERROR_*() functions, which have no MySQL equivalent"),
    (r"(?i)\bXACT_STATE\s*\(", "calls XACT_STATE(), which has no MySQL equivalent"),
    (r"(?i)\bDECLARE\s+\w+\s+CURSOR\b", "uses a cursor"),
    (r"(?i)\bDECLARE\s+@\w+\s+TABLE\b", "declares a table variable"),
    (r"(?i)\b(sp_executesql|EXEC(UTE)?\s*\(\s*@)", "builds dynamic SQL"),
    (r"(?i)\bMERGE\b\s+", "uses MERGE, which MySQL has no equivalent for"),
    (r"(?i)\bREADONLY\b", "takes a table-valued parameter, which MySQL has no equivalent for"),
    (r"(?i)\bOPENJSON\b", "uses OPENJSON"),
    (r"(?i)\bFOR\s+(JSON|XML)\b", "uses FOR JSON/FOR XML"),
    (r"(?i)\bsys\.\w+", "reads SQL Server's catalogue views"),
    (r"(?i)\b(ALTER|CREATE|DROP)\s+(TABLE|INDEX|DATABASE|SEQUENCE|SCHEMA|LOGIN|USER|ROLE)\b",
     "changes the schema: SQL Server feature configuration, not business logic"),
    (r"(?i)\bOUTPUT\s+(INSERTED|DELETED)\.", "uses the OUTPUT clause"),
    (r"(?i)\bNEXT\s+VALUE\s+FOR\b", "draws from a SEQUENCE, which became AUTO_INCREMENT here"),
    (r"(?i)\.(query|value|nodes|exist|modify)\s*\(", "calls an XML method"),
    (r"(?i)\b(GETANCESTOR|GETDESCENDANT|ISDESCENDANTOF)\s*\(",
     "calls a hierarchyid method; the decoded *_path columns are the MySQL equivalent"),
]


def refuse(sql):
    """The first reason this body cannot be translated, or None."""
    bare = blank_literals(sql)
    for pattern, reason in BLOCKERS:
        if re.search(pattern, bare):
            return reason
    return None


# ------------------------------------------------------------------ scanning

def blank_literals(sql):
    """`sql` with string bodies, bracketed identifiers and comments blanked, same length.

    Keyword scanning has to ignore them: AdventureWorks' routines are full of comments that name
    the very constructs being searched for, and `PRINT 'ROLLBACK the transaction'` is not a
    rollback.
    """
    out, i, n = list(sql), 0, len(sql)
    while i < n:
        c = sql[i]
        if c == "'":
            j = i + 1
            while j < n:
                if sql[j] == "'":
                    if j + 1 < n and sql[j + 1] == "'":
                        j += 2; continue
                    break
                j += 1
            for k in range(i + 1, min(j, n)):
                out[k] = " "
            i = j + 1
        elif c == "[":
            j = sql.find("]", i)
            j = n if j < 0 else j
            for k in range(i + 1, j):
                out[k] = " "
            i = j + 1
        elif sql.startswith("--", i):
            j = sql.find("\n", i)
            j = n if j < 0 else j
            for k in range(i, j):
                out[k] = " "
            i = j
        elif sql.startswith("/*", i):
            j = sql.find("*/", i)
            j = n + 2 if j < 0 else j
            for k in range(i, min(j + 2, n)):
                out[k] = " "
            i = j + 2
        else:
            i += 1
    return "".join(out)


def blank_strings(sql):
    """`sql` with only string bodies blanked -- comments stay, because a caller may be looking
    for one."""
    out, i, n = list(sql), 0, len(sql)
    while i < n:
        if sql[i] != "'":
            i += 1
            continue
        j = i + 1
        while j < n:
            if sql[j] == "'":
                if j + 1 < n and sql[j + 1] == "'":
                    j += 2
                    continue
                break
            j += 1
        for k in range(i + 1, min(j, n)):
            out[k] = " "
        i = j + 1
    return "".join(out)


WORD = re.compile(r"\w+")
# a statement may begin without a preceding semicolon: T-SQL does not require one
STARTERS = ("SELECT", "INSERT", "UPDATE", "DELETE", "SET", "DECLARE", "IF", "ELSE", "BEGIN", "END",
            "WHILE", "RETURN", "EXEC", "EXECUTE", "PRINT", "RAISERROR", "THROW", "COMMIT",
            "ROLLBACK", "WITH", "TRUNCATE", "GOTO", "BREAK", "CONTINUE", "USE")


def word_at(bare, i):
    m = WORD.match(bare, i)
    return m.group(0).upper() if m else None


def skip_space(bare, i, end):
    while i < end and bare[i].isspace():
        i += 1
    return i


# ------------------------------------------------------------------ parsing
# Nodes: ("block", [node]) ("if", cond, then, else|None) ("while", cond, node)
#        ("try", [node], [node]) ("stmt", text)

# keywords that may legitimately begin a line *inside* a statement rather than starting a new one
CONTINUATION = {"INSERT": {"SELECT", "VALUES", "EXEC", "EXECUTE", "WITH"},
                "UPDATE": {"SET"}, "DELETE": set(), "WITH": {"SELECT", "INSERT", "UPDATE", "DELETE"},
                "SELECT": set(), "MERGE": {"WHEN", "USING"}}


def at_line_start(sql, i):
    """True if only whitespace separates position i from the previous newline."""
    j = i - 1
    while j >= 0 and sql[j] in " \t":
        j -= 1
    return j < 0 or sql[j] == "\n"


def parse_statements(sql, bare, i, end, stop_words=("END",)):
    nodes = []
    while True:
        i = skip_space(bare, i, end)
        while i < end and bare[i] == ";":
            i = skip_space(bare, i + 1, end)
        if i >= end:
            return nodes, i
        if word_at(bare, i) in stop_words:
            return nodes, i
        node, i = parse_one(sql, bare, i, end)
        if node is not None:
            nodes.append(node)


def parse_one(sql, bare, i, end):
    kw = word_at(bare, i)
    if kw == "BEGIN":
        nxt = word_at(bare, skip_space(bare, i + 5, end))
        if nxt == "TRY":
            j = skip_space(bare, i + 5, end) + 3
            body, j = parse_statements(sql, bare, j, end, stop_words=("END",))
            j = skip_space(bare, j + 3, end)          # END
            if word_at(bare, j) == "TRY":
                j = skip_space(bare, j + 3, end)
            if word_at(bare, j) != "BEGIN":
                raise Unportable("BEGIN TRY without a matching BEGIN CATCH")
            j = skip_space(bare, j + 5, end)
            if word_at(bare, j) != "CATCH":
                raise Unportable("BEGIN TRY without a matching BEGIN CATCH")
            j += 5
            handler, j = parse_statements(sql, bare, j, end, stop_words=("END",))
            j = skip_space(bare, j + 3, end)
            if word_at(bare, j) == "CATCH":
                j += 5
            return ("try", body, handler), j
        if nxt in ("TRANSACTION", "TRAN"):
            return consume_simple(sql, bare, i, end)
        body, j = parse_statements(sql, bare, i + 5, end, stop_words=("END",))
        if word_at(bare, j) != "END":
            raise Unportable("a BEGIN block is not closed")
        return ("block", body), j + 3
    if kw == "IF":
        j = i + 2
        cond_start = j
        j = condition_end(sql, bare, j, end)
        cond = sql[cond_start:j].strip()
        then_node, j = parse_one(sql, bare, skip_space(bare, j, end), end)
        j = skip_space(bare, j, end)
        while j < end and bare[j] == ";":
            j = skip_space(bare, j + 1, end)
        else_node = None
        if word_at(bare, j) == "ELSE":
            else_node, j = parse_one(sql, bare, skip_space(bare, j + 4, end), end)
        return ("if", cond, then_node, else_node), j
    if kw == "WHILE":
        j = condition_end(sql, bare, i + 5, end)
        cond = sql[i + 5:j].strip()
        body, j = parse_one(sql, bare, skip_space(bare, j, end), end)
        return ("while", cond, body), j
    return consume_simple(sql, bare, i, end)


def condition_end(sql, bare, i, end):
    """Where an IF/WHILE condition stops: the first statement keyword at paren depth 0."""
    depth, j = 0, skip_space(bare, i, end)
    while j < end:
        c = bare[j]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif depth == 0 and c.isalpha() and (j == 0 or not (bare[j - 1].isalnum() or bare[j - 1] == "_")):
            w = word_at(bare, j)
            if w in STARTERS and w not in ("NOT", "EXISTS"):
                return j
        elif depth == 0 and c == ";":
            return j
        j += 1
    return end


def consume_simple(sql, bare, i, end):
    """One plain statement: to the next `;` at depth 0, or to a line-starting keyword.

    `CASE ... END` has to be counted. It is an expression whose parts -- ELSE, END -- are also
    statement keywords, and without tracking it a `SET @x = CASE ... ELSE ... END` was cut into
    three statements at the ELSE and the END.
    """
    first = word_at(bare, i)
    allowed = CONTINUATION.get(first, set())
    depth, case, j = 0, 0, i
    while j < end:
        c = bare[j]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == ";" and depth == 0 and case == 0:
            return ("stmt", sql[i:j].strip()), j + 1
        elif (c.isalpha() or c == "_") and not (j and (bare[j - 1].isalnum() or bare[j - 1] == "_")):
            w = word_at(bare, j)
            if w == "CASE":
                case += 1
            elif w == "END" and case:
                case -= 1
                j += 3
                continue
            elif depth == 0 and case == 0 and j > i and at_line_start(bare, j) \
                    and w in STARTERS and w not in allowed:
                return ("stmt", sql[i:j].strip()), j
        j += 1
    return ("stmt", sql[i:end].strip()), end


# ------------------------------------------------------------------ emitting

SYSTEM_VARS = [(r"(?i)@@ROWCOUNT\b", "ROW_COUNT()"),
               (r"(?i)@@IDENTITY\b", "LAST_INSERT_ID()"),
               (r"(?i)\bSCOPE_IDENTITY\s*\(\s*\)", "LAST_INSERT_ID()"),
               (r"(?i)@@TRANCOUNT\b", "0"),
               (r"(?i)@@ERROR\b", "0")]

BUILTINS = [(r"(?i)\bREPLICATE\s*\(", "REPEAT("), (r"(?i)\bDATALENGTH\s*\(", "LENGTH("),
            (r"(?i)\bNEWID\s*\(\s*\)", "UUID()"), (r"(?i)\bSTUFF\s*\(", "INSERT("),
            (r"(?i)\bSQUARE\s*\(", "POW2_("), (r"(?i)\bCEILING\s*\(", "CEIL(")]

VAR = re.compile(r"@(\w+)")


def rename_vars(sql, params):
    """`@Local` -> `v_local`, `@Param` -> `p_param`, outside string literals.

    MySQL has no sigil, so a routine local called `Name` inside a query that also selects a `Name`
    column resolves to the column. The prefix keeps them apart, and makes the origin of every
    identifier in the translated body visible.
    """
    for pattern, repl in SYSTEM_VARS:
        sql = re.sub(pattern, repl, sql)
    bare, out, last = blank_literals(sql), [], 0
    for m in VAR.finditer(bare):
        name = m.group(1)
        prefix = "p_" if name.lower() in params else "v_"
        out.append(sql[last:m.start()])
        out.append(prefix + name.lower())
        last = m.end()
    out.append(sql[last:])
    text = "".join(out)
    for pattern, repl in BUILTINS:
        text = re.sub(pattern, repl, text)
    return text


DECLARE_ONE = re.compile(r"(?is)^\s*DECLARE\s+(.*)$")
SET_ASSIGN = re.compile(r"(?is)^\s*SET\s+([\w.]+)\s*=\s*(.+)$")
SELECT_ASSIGN = re.compile(r"(?is)^\s*SELECT\s+(.+)$")
ASSIGN_ITEM = re.compile(r"(?is)^\s*(v_\w+|p_\w+)\s*=\s*(.+)$")


def split_commas(text):
    parts, depth, item = [], 0, []
    bare = blank_literals(text)
    for i, ch in enumerate(text):
        b = bare[i]
        if b == "(":
            depth += 1
        elif b == ")":
            depth -= 1
        if b == "," and depth == 0:
            parts.append("".join(item)); item = []
        else:
            item.append(ch)
    if item:
        parts.append("".join(item))
    return [p.strip() for p in parts if p.strip()]


class Routine:
    """Accumulates the declarations, handlers and notes while a body is emitted."""

    def __init__(self, kind, params, label, stringy=()):
        self.kind, self.params, self.label = kind, params, label
        self.declares, self.handlers, self.notes = [], [], []
        self.stringy = set(stringy)
        self.udts = {}
        self.rowcount = None

    def expr(self, text):
        """One expression, with T-SQL's overloaded `+` resolved against the declared types."""
        import tsql
        return tsql.convert_concat(text.strip(), self.stringy)


def emit_nodes(nodes, r, indent="  "):
    return [line for node in nodes for line in emit(node, r, indent)]


def emit(node, r, indent):
    tag = node[0]
    if tag == "block":
        return emit_nodes(node[1], r, indent)
    if tag == "if":
        _, cond, then_node, else_node = node
        out = [f"{indent}IF {cond.strip()} THEN"]
        out += emit(then_node, r, indent + "  ")
        if else_node is not None:
            out.append(f"{indent}ELSE")
            out += emit(else_node, r, indent + "  ")
        out.append(f"{indent}END IF;")
        return out
    if tag == "while":
        _, cond, body = node
        return ([f"{indent}WHILE {cond.strip()} DO"] + emit(body, r, indent + "  ")
                + [f"{indent}END WHILE;"])
    if tag == "try":
        _, body, handler = node
        inner = emit_nodes(handler, r, "    ")
        if inner:
            r.handlers.append("  DECLARE EXIT HANDLER FOR SQLEXCEPTION\n  BEGIN\n"
                              + "\n".join(inner) + "\n  END;")
            r.notes.append("BEGIN TRY/END CATCH became an EXIT handler, which leaves the whole "
                           "routine where T-SQL would continue after END CATCH")
        return emit_nodes(body, r, indent)
    return emit_stmt(node[1], r, indent)


def terminate(text, indent=""):
    """Append the statement terminator, before any trailing line comment rather than after it.

    `SET @DealerDiscount = 0.60  -- 60% of list price` with a `;` stuck on the end is a statement
    that has been commented out, and the next one runs on into it.
    """
    # blank_literals also blanks comments, which is exactly what must stay visible here
    bare = blank_strings(text)
    tail = bare.rfind("--")
    if tail >= 0 and "\n" not in bare[tail:]:
        return f"{indent}{text[:tail].rstrip()}; {text[tail:].rstrip()}"
    return f"{indent}{text.rstrip()};"


OPTION_HINT = re.compile(r"(?is)\s+OPTION\s*\((?:[^()]|\([^()]*\))*\)\s*$")


def emit_stmt(text, r, indent):
    stripped = OPTION_HINT.sub("", text.strip().rstrip(";").strip()).strip()
    if not stripped:
        return []
    head = (WORD.match(blank_literals(stripped)) or re.match("", "")).group(0).upper() \
        if WORD.match(blank_literals(stripped)) else ""

    if head == "DECLARE":
        for item in split_commas(DECLARE_ONE.match(stripped).group(1)):
            m = re.match(r"(?is)^(v_\w+|p_\w+)\s+(.+?)(?:\s*=\s*(.+))?$", item)
            if not m:
                raise Unportable(f"cannot read the declaration `{item[:40]}`")
            name, decl_type, init = m.group(1), m.group(2).strip(), m.group(3)
            declared = mysql_type(decl_type, r.udts)
            r.declares.append(f"  DECLARE {name} {declared};")
            if declared.lower().startswith(CHAR_TYPES):
                r.stringy.add(name.lower())
            if init:
                # the initialiser cannot travel with the declaration: it may depend on a value
                # computed further down, so it stays where it was, as an assignment
                return [terminate(f"SET {name} = {r.expr(init)}", indent)]
        return []
    if head == "SET":
        if re.match(r"(?i)^SET\s+(NOCOUNT|XACT_ABORT|ANSI_|QUOTED_|ARITHABORT|CONCAT_)", stripped):
            return []
        rowcount = re.match(r"(?i)^SET\s+ROWCOUNT\s+(\d+)$", stripped)
        if rowcount:
            r.rowcount = int(rowcount.group(1))
            r.notes.append(f"SET ROWCOUNT {r.rowcount} became a LIMIT on the statement it governed")
            return []
        m = SET_ASSIGN.match(stripped)
        if m:
            return [terminate(f"SET {m.group(1)} = {r.expr(m.group(2))}", indent)]
        raise Unportable(f"cannot read `{stripped[:40]}`")
    if head == "SELECT":
        assigns, rest = select_assignment(stripped)
        if assigns is not None:
            names = ", ".join(n for n, _ in assigns)
            exprs = ", ".join(e for _, e in assigns)
            if rest:
                return [terminate(f"SELECT {exprs} INTO {names}{rest}", indent)]
            return [f"{indent}SET {names} = {exprs};" if len(assigns) == 1 else
                    f"{indent}SELECT {exprs} INTO {names};"]
        if r.rowcount and not re.search(r"(?i)\bLIMIT\b", blank_literals(stripped)):
            stripped, r.rowcount = f"{stripped} LIMIT {r.rowcount}", None
        return [terminate(stripped, indent)]
    if head == "RETURN":
        value = unwrap(stripped[6:].strip())
        if r.kind == "function":
            return [terminate(f"RETURN {r.expr(value)}", indent) if value
                    else f"{indent}RETURN NULL;"]
        return [f"{indent}LEAVE {r.label};"]
    if head == "PRINT":
        r.notes.append("dropped a PRINT: MySQL has no statement that writes to the client log")
        return []
    if head in ("RAISERROR", "THROW"):
        message = first_string(stripped) or "error raised by the original T-SQL"
        return [f"{indent}SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = {message};"]
    if head in ("BEGIN", "COMMIT", "ROLLBACK"):
        if r.kind != "procedure":
            raise Unportable("controls a transaction, which MySQL forbids inside a "
                             f"{r.kind} (error 1422)")
        return [f"{indent}{'START TRANSACTION' if head == 'BEGIN' else head};"]
    if head in ("EXEC", "EXECUTE"):
        call = re.sub(r"(?i)^EXEC(UTE)?\s+", "", stripped)
        name = call.split()[0] if call.split() else ""
        args = call[len(name):].strip()
        return [f"{indent}CALL {name}({args});"]
    if head in ("BREAK", "CONTINUE"):
        return [f"{indent}{'LEAVE' if head == 'BREAK' else 'ITERATE'} {r.label};"]
    if head in ("GOTO", "USE", "TRUNCATE"):
        raise Unportable(f"uses {head}")
    return [terminate(stripped, indent)]


def unwrap(expr):
    """Drop one redundant outer paren pair, and only if it really is a pair.

    `expr.strip("()")` strips characters rather than a pair, which quietly removes the closing paren
    of `STR_TO_DATE('20030701', '%Y%m%d')` and leaves an unbalanced expression.
    """
    e = expr.strip()
    while e.startswith("(") and e.endswith(")"):
        depth = 0
        for i, ch in enumerate(blank_literals(e)):
            depth += {"(": 1, ")": -1}.get(ch, 0)
            if depth == 0 and i < len(e) - 1:
                return e
        e = e[1:-1].strip()
    return e


def select_assignment(stmt):
    """`SELECT @a = x, @b = y FROM ...` -> ([(a, x), (b, y)], ' FROM ...'), else (None, None)."""
    body = SELECT_ASSIGN.match(stmt).group(1)
    bare, depth, cut = blank_literals(body), 0, len(body)
    for i, ch in enumerate(bare):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif depth == 0 and ch.isalpha() and (i == 0 or not (bare[i - 1].isalnum() or bare[i - 1] == "_")):
            if word_at(bare, i) in ("FROM", "WHERE", "ORDER", "GROUP", "HAVING"):
                cut = i
                break
    items = split_commas(body[:cut])
    pairs = []
    for item in items:
        m = ASSIGN_ITEM.match(item)
        if not m:
            return None, None
        pairs.append((m.group(1), m.group(2).strip()))
    return (pairs, " " + body[cut:].strip()) if pairs else (None, None)


def first_string(text):
    m = re.search(r"'((?:[^']|'')*)'", text)
    return f"'{m.group(1)}'" if m else None


def wrap(statements):
    """Routine definitions, ready to stream into the client.

    Their bodies are full of semicolons, and the `mysql` client ends a statement at the first one
    unless the delimiter is changed -- which shows up as a syntax error pointing at an empty string
    somewhere in the middle of the routine.
    """
    if not statements:
        return ""
    return ("DELIMITER $$\n" + "\n".join(s.rstrip().rstrip(";") + "$$\n" for s in statements)
            + "DELIMITER ;\n")


# ------------------------------------------------------------------ the header, and the whole job

PARAM = re.compile(r"(?is)@(\w+)\s+([\w()\[\]., ]+?)\s*(?:=\s*([^,]+?))?\s*(OUTPUT|OUT)?\s*(?:,|$)")
TRIGGER_ON = re.compile(r"(?is)\bON\s+`?([\w.]+)`?")
TRIGGER_EVENTS = re.compile(r"(?is)\b(AFTER|FOR|INSTEAD\s+OF)\s+((?:INSERT|UPDATE|DELETE)"
                            r"(?:\s*,\s*(?:INSERT|UPDATE|DELETE))*)")
RETURNS = re.compile(r"(?is)\bRETURNS\s+([\w()\[\]`., ]+?)\s*(?:WITH\b|AS\b|$)")
CHAR_TYPES = ("char", "varchar", "nchar", "nvarchar", "text", "ntext", "sysname")


def mysql_type(text, udts=None):
    """`[int]` or `` `int` `` -> `int`; `[nvarchar](50)` -> `varchar(50)`.

    Types reach here bracketed from the source and backticked from tsql.py, which cannot tell a
    type from an identifier in a routine header -- nothing there marks the token as a type the way
    a column declaration does.
    """
    t = text.replace("[", "").replace("]", "").replace("`", "").strip()
    if udts and t.lower() in udts:
        # collect_tsql_types and collect_udts disagree about their value shape: one returns the
        # type, the other (type, nullability)
        alias = udts[t.lower()]
        t = alias[0] if isinstance(alias, tuple) else alias
    else:
        import tsql
        base = re.match(r"(?i)^(\w+)", t)
        if base and base.group(1).lower() in tsql.TYPE_MAP:
            t = tsql.TYPE_MAP[base.group(1).lower()] + t[base.end():]
    t = re.sub(r"(?i)^n(char|varchar|text)", r"\1", t)
    t = re.sub(r"(?i)^(text|ntext)$", "LONGTEXT", t)
    t = re.sub(r"(?i)^money$", "DECIMAL(19,4)", t)
    t = re.sub(r"(?i)^smallmoney$", "DECIMAL(10,4)", t)
    t = re.sub(r"(?i)^bit$", "TINYINT(1)", t)
    t = re.sub(r"(?i)^(datetime2|smalldatetime)(\(\d+\))?$", "DATETIME(3)", t)
    # T-SQL datetime keeps milliseconds and the routines rely on it: ufnGetAccountingEndDate is
    # `DATEADD(ms, -2, ...)`, which a MySQL DATETIME with no fractional digits rounds straight back
    # up to the next day. Columns stay DATETIME; only routine types widen.
    t = re.sub(r"(?i)^datetime$", "DATETIME(3)", t)
    t = re.sub(r"(?i)^uniqueidentifier$", "CHAR(36)", t)
    return re.sub(r"(?i)^n?varchar\s*\(\s*max\s*\)$", "LONGTEXT", t)


def body_split(sql):
    """(header, body) -- the body starts at the first depth-0 BEGIN, else after the last AS."""
    bare, depth, begins, ases = blank_literals(sql), 0, [], []
    for i, ch in enumerate(bare):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif depth == 0 and (ch.isalpha()) and (i == 0 or not (bare[i - 1].isalnum() or bare[i - 1] == "_")):
            w = word_at(bare, i)
            if w == "BEGIN":
                begins.append(i)
            elif w == "AS":
                ases.append(i)
    if begins:
        cut = begins[0]
        return sql[:cut], sql[cut:]
    if ases:
        # the *first* AS, not the last: a body with no BEGIN can still contain `AS` as a column
        # alias, and Northwind's Ten Most Expensive Products selects
        # `ProductName AS TenMostExpensiveProducts` -- splitting there threw away the SELECT
        return sql[:ases[0]], sql[ases[0] + 2:]
    raise Unportable("cannot find where the routine body begins")


def parameter_region(header, kind):
    """The text holding the parameter list: the parenthesised form or the bare one.

    Both spellings occur in the same script -- `CREATE FUNCTION x(@a int)` and
    `CREATE PROCEDURE y @a int, @b int AS` -- and the name may be bracketed, quoted or bare.
    """
    after = re.sub(r"(?is)^\s*CREATE\s+\w+\s+(?:`[^`]+`|\[[^\]]+\](?:\.\[[^\]]+\])?|[\w.]+)",
                   "", header, count=1)
    bare, i = blank_literals(after), 0
    i = skip_space(bare, 0, len(bare))
    if i < len(bare) and bare[i] == "(":
        depth, j = 0, i
        while j < len(bare):
            if bare[j] == "(":
                depth += 1
            elif bare[j] == ")":
                depth -= 1
                if depth == 0:
                    return after[i + 1:j]
            j += 1
        raise Unportable("the parameter list is not closed")
    stop = len(after)
    for m in re.finditer(r"(?is)\b(RETURNS|AS|ON|WITH)\b", bare):
        stop = m.start()
        break
    return after[:stop]


PARAM_ITEM = re.compile(r"(?is)^\s*@(\w+)\s+(.+?)\s*(?:=\s*(.+?))?\s*(OUTPUT|OUT)?\s*$")


def parameters(header, kind, udts=None):
    """[(name, MySQL type, had a default, is OUT)] in declaration order."""
    out = []
    for item in split_commas(parameter_region(header, kind)):
        m = PARAM_ITEM.match(item)
        if not m:
            raise Unportable(f"cannot read the parameter `{item[:40]}`")
        out.append((m.group(1), mysql_type(m.group(2), udts), m.group(3) is not None,
                    bool(m.group(4))))
    return out


def translate(sql, name, udts=None):
    """One T-SQL routine -> a list of MySQL CREATE statements, plus notes.

    `udts` maps the script's own CREATE TYPE aliases to their MySQL types; a routine header carries
    them unexpanded because nothing there marks the token as a type.

    Raises Unportable with a reason the caller should report rather than emitting a guess.
    """
    reason = refuse(sql)
    if reason:
        raise Unportable(reason)
    kind = re.match(r"(?is)\s*CREATE\s+(PROCEDURE|PROC|FUNCTION|TRIGGER)", sql)
    if not kind:
        raise Unportable("not a routine")
    kind = {"PROC": "procedure"}.get(kind.group(1).upper(), kind.group(1).lower())
    header, body = body_split(sql)
    header = re.sub(r"(?i)\bWITH\s+(SCHEMABINDING|ENCRYPTION|EXECUTE\s+AS\s+\w+)"
                    r"(\s*,\s*\w+)*", " ", header)

    if kind == "trigger":
        return trigger(sql, header, body, name)
    params = parameters(header, kind, udts)

    param_names = {p.lower() for p, _, _, _ in params}
    label = "proc_body"
    stringy = {f"p_{p.lower()}" for p, t, _, _ in params if t.lower().startswith(CHAR_TYPES)}
    r = Routine(kind, param_names, label, stringy)
    r.udts = udts or {}
    renamed = rename_vars(body, param_names)
    bare = blank_literals(renamed)
    nodes, _ = parse_statements(renamed, bare, 0, len(renamed), stop_words=())
    lines = emit_nodes(nodes, r)
    if any(p[2] for p in params):
        r.notes.append("a parameter had a default; MySQL has none, so callers must pass every one")

    signature = ", ".join(
        f"{('OUT' if is_out else 'IN') if kind == 'procedure' else ''} p_{p.lower()} {t}".strip()
        for p, t, _, is_out in params)
    head = [f"CREATE {kind.upper()} `{name}`({signature})"]
    if kind == "function":
        m = RETURNS.search(blank_literals(header))
        if not m:
            raise Unportable("no RETURNS type")
        head.append(f"RETURNS {mysql_type(header[m.start(1):m.end(1)], udts)}")
        head.append("NOT DETERMINISTIC READS SQL DATA" if re.search(r"(?i)\bFROM\b", bare)
                    else "DETERMINISTIC NO SQL")
        head.append("SQL SECURITY INVOKER")
    else:
        head.append("SQL SECURITY INVOKER")
    opener = f"{label}: BEGIN" if kind == "procedure" and any("LEAVE" in l for l in lines) else "BEGIN"
    sql_out = "\n".join(head) + "\n" + opener + "\n" + "\n".join(
        r.declares + r.handlers + lines) + "\nEND"
    return [sql_out], r.notes


def trigger(sql, header, body, name):
    """T-SQL fires one trigger for several events; MySQL needs one per event, per row."""
    masked = blank_literals(header)
    on, ev = TRIGGER_ON.search(masked), TRIGGER_EVENTS.search(masked)
    if not on or not ev:
        raise Unportable("cannot read the trigger's table or events")
    timing = "BEFORE" if ev.group(1).upper().startswith("INSTEAD") else "AFTER"
    if timing == "BEFORE":
        raise Unportable("INSTEAD OF triggers have no MySQL equivalent")
    events = [e.strip().upper() for e in ev.group(2).split(",")]
    bare_body = blank_literals(body)
    if re.search(r"(?i)\b(inserted|deleted)\b", bare_body):
        # a row trigger sees one row; a body that joins or aggregates over the pseudo-tables is
        # making a statement-level claim that NEW/OLD cannot express
        if re.search(r"(?i)\b(JOIN|GROUP\s+BY|COUNT\s*\(|SUM\s*\(|FROM\s+(inserted|deleted)\s*,)",
                     bare_body):
            raise Unportable("the body aggregates over the inserted/deleted pseudo-tables, which "
                             "a MySQL row trigger cannot express")
    out, notes = [], []
    for event in events:
        r = Routine("trigger", set(), "trg_body")
        text = rename_vars(body, set())
        text = re.sub(r"(?i)\binserted\b\.", "NEW.", text)
        text = re.sub(r"(?i)\bdeleted\b\.", "OLD.", text)
        nodes, _ = parse_statements(text, blank_literals(text), 0, len(text), stop_words=())
        lines = emit_nodes(nodes, r)
        suffix = f"_{event.lower()[:3]}" if len(events) > 1 else ""
        table = header[on.start(1):on.end(1)].replace("[", "").replace("]", "").replace("`", "")
        opener = "trg_body: BEGIN" if any("LEAVE trg_body" in l for l in lines) else "BEGIN"
        out.append(f"CREATE TRIGGER `{name}{suffix}` {timing} {event} ON `{table}`\n"
                   f"FOR EACH ROW\n{opener}\n"
                   + "\n".join(r.declares + r.handlers + lines) + "\nEND")
        notes = r.notes
    if len(events) > 1:
        notes.append(f"one T-SQL trigger for {', '.join(events)} became {len(events)} MySQL "
                     f"triggers, one per event")
    return out, notes


def port(statements, udts=None, task="V-02"):
    """Translate every routine in a converter's statement list.

    Returns (sql, unported, notes): `sql` is ready to stream into the client, delimiter and all;
    `unported` names each object that was refused and why, in the form the converters already use
    for anything they drop. Nothing is emitted on a guess -- a refusal is the only other outcome.
    """
    out, unported, notes = [], [], []
    for st in statements:
        if st["kind"] not in ("procedure", "function", "trigger"):
            continue
        m = re.search(r"(?i)(procedure|function|trigger)\s+`?([\w.]+)`?", st["sql"])
        kind, name = (m.group(1).lower(), m.group(2)) if m else (st["kind"], "?")
        try:
            created, made = translate(st["sql"], name, udts)
        except Unportable as exc:
            unported.append(f"{kind} {name}: {exc}")
            continue
        except Exception as exc:                       # a translator bug, not a source problem
            unported.append(f"{kind} {name}: the translator failed ({type(exc).__name__}: {exc})")
            continue
        out += created
        notes += [f"{name}: {n}" for n in made]
    return wrap(out), unported, notes
