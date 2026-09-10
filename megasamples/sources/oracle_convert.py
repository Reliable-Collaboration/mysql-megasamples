#!/usr/bin/env python3
"""Shared converter for the Oracle sample schemas (HR, CO).

Both are SQL*Plus install scripts with the same shape, so the phase ordering, the dropped
constructs and the reporting are identical; only the database name and file list differ.
Decision: knowledge/decisions/oracle-conversion-path.md
"""
import os, re, sys
from megasamples.sources import plsql  # noqa: E402

# comments come after views: some of them describe a view rather than a base table
PHASES = ("table", "dml", "index", "constraint", "view", "comment", "routine")


def header(database):
    return f"""-- Oracle {database} sample schema, translated by megasamples/sources/oracle_convert.py.
-- Upstream: oracle-samples/db-sample-schemas (MIT). See datasets/{database}/LICENSE.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{database}`;
CREATE DATABASE `{database}` DEFAULT CHARACTER SET utf8mb4;
USE `{database}`;
"""


def convert(downloads, files, date_type="DATETIME", schema_prefix=None):
    buckets = {k: [] for k in PHASES}
    notes, dropped = [], {"sequence": 0, "column_comment": 0}
    primary_keys = {}
    identity_pk = {}     # table -> column already made PRIMARY KEY inline with its identity
    base_tables = set()  # only a base table can carry a MySQL table comment
    json_cols = set()    # columns the schema marks IS JSON, possibly in a separate ALTER TABLE
    sources = {f: plsql.resolve_variables(open(os.path.join(downloads, f), encoding="utf-8").read())
               for f in files}
    # collected before any table is written: MySQL can only set a column comment as part of the
    # column definition, so they have to be known while the CREATE TABLE is being built
    column_comments = {}
    for text in sources.values():
        for m in re.finditer(r"(?is)COMMENT\s+ON\s+COLUMN\s+(?:\w+\.)?(\w+)\.(\w+)\s+IS\s+"
                             r"'((?:[^']|'')*)'", text):
            column_comments.setdefault(m.group(1).lower(), {})[m.group(2).lower()] = \
                m.group(3).replace("''", "'")
    for text in sources.values():          # pre-scan: an IS JSON check can be in another file
        json_cols |= plsql.json_columns(text)
    for filename in files:
        text = sources[filename]
        for raw in plsql.split_statements(text):
            kind, statement = plsql.classify(raw)
            if schema_prefix:
                statement = plsql.strip_schema_prefix(statement, schema_prefix)
            if kind in ("empty", "other", "skip"):
                continue
            if kind == "sequence":
                dropped["sequence"] += 1
                continue
            if kind == "dimension":
                # CREATE DIMENSION declares hierarchies for query rewrite; MySQL has no equivalent
                # and the hierarchies are implicit in the *_id columns anyway
                dropped["dimension"] = dropped.get("dimension", 0) + 1
                continue
            if kind == "comment":
                m = re.match(r"(?is)^comment\s+on\s+table\s+(\w+)\s+is\s+('(?:[^']|'')*')", statement)
                if m and m.group(1).lower() in base_tables:
                    buckets["comment"].append(f"ALTER TABLE `{m.group(1).lower()}` COMMENT = {m.group(2)}")
                elif m:
                    # the target is a view; MySQL views cannot carry a table comment
                    dropped["view_comment"] = dropped.get("view_comment", 0) + 1
                else:
                    dropped["column_comment"] += 1     # counted here, attached to the column above
                    target = re.match(r"(?is)^comment\s+on\s+column\s+(?:\w+\.)?(\w+)\.", statement)
                    if target and target.group(1).lower() not in base_tables:
                        # a view column: MySQL views carry neither table nor column comments
                        dropped["view_column_comment"] = dropped.get("view_column_comment", 0) + 1
                continue
            statement = plsql.convert_values(statement)
            if kind == "view":
                blockers = plsql.view_blockers(statement)
                if blockers:
                    name = re.search(r"(?i)view\s+(\w+)", statement)
                    label = (name.group(1).lower() if name else "view")
                    notes.append(f"unported view {label}")
                    buckets["view"].append(
                        f"-- UNPORTED VIEW `{label}`: the body uses\n"
                        + "".join(f"--   - {b}\n" for b in blockers)
                        + "--   Upstream text:\n"
                        + "".join(f"--   {l}\n" for l in statement.split("\n")))
                    continue
                statement = plsql.convert_view(plsql.convert_types(
                    plsql.convert_materialized_view(statement), date_type))
            if kind in ("table", "constraint", "index"):
                statement = plsql.convert_ddl(plsql.convert_types(statement, date_type), json_cols)
                plsql.collect_primary_keys(statement, primary_keys)
                if kind == "constraint":
                    statement = plsql.convert_alter(statement, primary_keys)
                if kind == "table":
                    tname = re.search(r"(?i)CREATE\s+TABLE\s+(\w+)", statement)
                    if tname:
                        base_tables.add(tname.group(1).lower())
                    statement, identity = plsql.inline_identity_pk(statement)
                    if identity:
                        identity_pk[identity[0]] = identity[1]
                    statement, n = attach_column_comments(statement, column_comments)
                    dropped["column_comment_attached"] = dropped.get(
                        "column_comment_attached", 0) + n
            if kind == "routine":
                name = re.search(r"(?i)(procedure|function|trigger)\s+(\w+)", statement)
                label = f"{name.group(1).lower()} {name.group(2).lower()}" if name else "routine"
                notes.append(f"unported {label}")
                buckets["routine"].append(
                    f"-- UNPORTED {label.upper()}: PL/SQL body (DECLARE/EXCEPTION/RAISE_APPLICATION_ERROR)\n"
                    f"--   has no mechanical MySQL translation; the record names the intended\n"
                    f"--   equivalent if it is wanted. Upstream text:\n"
                    + "".join(f"--   {l}\n" for l in statement.split("\n")))
                continue
            # the identity is declared inline, so Oracle's separate MODIFY ... AS IDENTITY
            # (which MySQL cannot express as a MODIFY without restating the column type) is moot
            if re.match(r"(?is)^\s*ALTER\s+TABLE\s+\w+\s+MODIFY\s+\w+\s+AUTO_INCREMENT\s*$", statement):
                dropped["identity_alter"] = dropped.get("identity_alter", 0) + 1
                continue
            # the identity column already carries its PRIMARY KEY from the CREATE TABLE
            dup = re.match(r"(?is)^\s*ALTER\s+TABLE\s+(\w+)\s+ADD\s+CONSTRAINT\s+\w+\s+"
                           r"PRIMARY\s+KEY\s*\(\s*(\w+)\s*\)\s*$", statement)
            if dup and identity_pk.get(dup.group(1).lower()) == dup.group(2).lower():
                dropped["duplicate_pk"] = dropped.get("duplicate_pk", 0) + 1
                continue
            # a clause that reduced to nothing (an IS JSON check, say) leaves a bare ADD behind
            if re.match(r"(?is)^\s*ALTER\s+TABLE\s+\S+\s+ADD\s*$", statement):
                dropped["empty_clause"] = dropped.get("empty_clause", 0) + 1
                continue
            buckets[kind].append(statement)
    # An Oracle materialized view is a table and can be indexed; the MySQL view it becomes cannot.
    views = {m.group(1).lower() for sql in buckets["view"]
             for m in [re.search(r"(?i)CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+)?VIEW\s+(\w+)",
                                 sql)] if m}
    on_view = re.compile(r"(?is)^\s*CREATE\s+(?:UNIQUE\s+|FULLTEXT\s+)?INDEX\s+\w+\s+ON\s+(\w+)")
    kept = []
    for sql in buckets["index"]:
        m = on_view.match(sql)
        if m and m.group(1).lower() in views:
            dropped["index_on_view"] = dropped.get("index_on_view", 0) + 1
            continue
        kept.append(sql)
    buckets["index"] = kept
    buckets["table"], retyped = align_foreign_key_types(buckets["table"], buckets["constraint"])
    notes += [f"retyped {c}" for c in retyped]
    return buckets, notes, dropped


COLUMN_DEF = re.compile(r"(?im)^(\s*)(\w+)(\s+)([A-Za-z_]+(?:\s*\(\s*\d+\s*(?:,\s*-?\d+\s*)?\))?)")
FK_CLAUSE = re.compile(r"(?is)FOREIGN\s+KEY\s*\(\s*(\w+)\s*\)\s*REFERENCES\s+(\w+)\s*\(\s*(\w+)\s*\)")
NOT_A_COLUMN = re.compile(r"(?i)^\s*(CONSTRAINT|PRIMARY|FOREIGN|UNIQUE|CHECK|KEY|INDEX)\b")


def attach_column_comments(create_table, comments):
    """Put `COMMENT '...'` on each column of a translated CREATE TABLE.

    MySQL has no standalone COMMENT ON COLUMN: a comment can only be set as part of a full column
    definition, which is why this happens while the table is being written rather than afterwards.
    """
    table = re.search(r"(?i)CREATE\s+TABLE\s+(\w+)", create_table)
    if not table:
        return create_table, 0
    wanted = comments.get(table.group(1).lower())
    if not wanted:
        return create_table, 0
    open_paren = create_table.index("(")
    close_paren = create_table.rindex(")")
    items, attached = [], 0
    for item in plsql.split_top_level(create_table[open_paren + 1:close_paren]):
        m = COLUMN_DEF.match(item.strip("\n"))
        if m and not NOT_A_COLUMN.match(item) and m.group(2).lower() in wanted:
            text = wanted[m.group(2).lower()][:1024].replace("\\", "\\\\").replace("'", "''")
            item = item.rstrip() + f" COMMENT '{text}'"
            attached += 1
        items.append(item)
    # split_top_level strips its items, so put the line breaks back rather than emitting one
    # very long line per table
    body = ",\n   ".join(item.strip() for item in items)
    return (create_table[:open_paren + 1] + "\n   " + body + "\n" + create_table[close_paren:],
            attached)


def table_columns(create_table):
    """{column: declared type} for one translated CREATE TABLE."""
    body = create_table[create_table.index("(") + 1:create_table.rindex(")")]
    columns = {}
    for item in plsql.split_top_level(body):
        if NOT_A_COLUMN.match(item):
            continue
        m = COLUMN_DEF.match(item.strip("\n"))
        if m:
            columns[m.group(2).lower()] = " ".join(m.group(4).split())
    return columns


def align_foreign_key_types(tables, constraints):
    """Give each foreign key column the type of the key it references.

    Oracle does not care that `sales.channel_id` is NUMBER(1) while `channels.channel_id` is an
    unconstrained NUMBER; MySQL refuses the foreign key unless both sides have the same type. The
    referenced side wins, because it is the key. Returns the rewritten tables and what changed.
    """
    named = {}
    for i, sql in enumerate(tables):
        m = re.search(r"(?i)CREATE\s+TABLE\s+(\w+)", sql)
        if m:
            named[m.group(1).lower()] = i
    types = {t: table_columns(tables[i]) for t, i in named.items()}
    keys = [(re.search(r"(?i)CREATE\s+TABLE\s+(\w+)", sql).group(1).lower(), fk)
            for sql in tables for fk in FK_CLAUSE.findall(sql)]
    keys += [(re.search(r"(?i)ALTER\s+TABLE\s+(\w+)", sql).group(1).lower(), fk)
             for sql in constraints if re.search(r"(?i)ALTER\s+TABLE\s+(\w+)", sql)
             for fk in FK_CLAUSE.findall(sql)]
    changed = []
    for child, (column, parent, parent_column) in keys:
        want = types.get(parent, {}).get(parent_column.lower())
        have = types.get(child, {}).get(column.lower())
        if not want or not have or want == have:
            continue
        def retype(m, column=column, want=want):
            if m.group(2).lower() != column.lower():
                return m.group(0)
            return f"{m.group(1)}{m.group(2)}{m.group(3)}{want}"
        tables[named[child]] = COLUMN_DEF.sub(retype, tables[named[child]])
        types[child][column.lower()] = want
        changed.append(f"{child}.{column} {have} -> {want} (matches {parent}.{parent_column})")
    return tables, changed


def run(downloads, dest, database, files):
    buckets, notes, dropped = convert(downloads, files)
    out = [header(database)]
    for phase in PHASES:
        if not buckets[phase]:
            continue
        out.append(f"\n-- {'-' * 60}\n-- {phase}\n")
        for statement in buckets[phase]:
            out.append(statement if statement.lstrip().startswith("--") else statement.rstrip(";") + ";")
    out.append("SET SESSION foreign_key_checks = 1;\n")
    open(dest, "w", encoding="utf-8").write("\n".join(out))
    counts = {k: len(v) for k, v in buckets.items() if v}
    attached = dropped.pop("column_comment_attached", 0)
    total = dropped.pop("column_comment", 0)
    print(f"  . translated {counts}" + ("; dropped " + ", ".join(
        f"{n} {k.replace('_', ' ')}(s)" for k, n in sorted(dropped.items()) if n) if any(
        dropped.values()) else ""))
    on_views = dropped.pop("view_column_comment", 0)
    if total:
        why = f" (the other {on_views} name view columns, which MySQL cannot comment)" if on_views else ""
        print(f"  . attached {attached} of {total} column comments to their columns{why}")
    for n in sorted(set(notes)):
        print(f"  . {n}")

