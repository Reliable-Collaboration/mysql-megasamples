#!/usr/bin/env python3
"""Shared converter for the Oracle sample schemas (HR, CO).

Both are SQL*Plus install scripts with the same shape, so the phase ordering, the dropped
constructs and the reporting are identical; only the database name and file list differ.
Decision: knowledge/decisions/oracle-conversion-path.md
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import plsql  # noqa: E402

# comments come after views: some of them describe a view rather than a base table
PHASES = ("table", "dml", "index", "constraint", "view", "comment", "routine")


def header(database):
    return f"""-- Oracle {database} sample schema, translated by scripts/oracle_convert.py.
-- Upstream: oracle-samples/db-sample-schemas (MIT). See datasets/{database}/LICENSE.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{database}`;
CREATE DATABASE `{database}` DEFAULT CHARACTER SET utf8mb4;
USE `{database}`;
"""


def convert(downloads, files):
    buckets = {k: [] for k in PHASES}
    notes, dropped = [], {"sequence": 0, "column_comment": 0}
    primary_keys = {}
    identity_pk = {}     # table -> column already made PRIMARY KEY inline with its identity
    base_tables = set()  # only a base table can carry a MySQL table comment
    json_cols = set()    # columns the schema marks IS JSON, possibly in a separate ALTER TABLE
    sources = {f: plsql.resolve_variables(open(os.path.join(downloads, f), encoding="utf-8").read())
               for f in files}
    for text in sources.values():          # pre-scan: an IS JSON check can be in another file
        json_cols |= plsql.json_columns(text)
    for filename in files:
        text = sources[filename]
        for raw in plsql.split_statements(text):
            kind, statement = plsql.classify(raw)
            if kind in ("empty", "other", "skip"):
                continue
            if kind == "sequence":
                dropped["sequence"] += 1
                continue
            if kind == "comment":
                m = re.match(r"(?is)^comment\s+on\s+table\s+(\w+)\s+is\s+('(?:[^']|'')*')", statement)
                if m and m.group(1).lower() in base_tables:
                    buckets["comment"].append(f"ALTER TABLE `{m.group(1).lower()}` COMMENT = {m.group(2)}")
                elif m:
                    # the target is a view; MySQL views cannot carry a table comment
                    dropped["view_comment"] = dropped.get("view_comment", 0) + 1
                else:
                    dropped["column_comment"] += 1     # MySQL needs the full column definition
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
                statement = plsql.convert_view(plsql.convert_types(statement))
            if kind in ("table", "constraint", "index"):
                statement = plsql.convert_ddl(plsql.convert_types(statement), json_cols)
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
    return buckets, notes, dropped


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
    print(f"  . translated {counts}; dropped {dropped['sequence']} sequence(s) "
          f"and {dropped['column_comment']} column comment(s)")
    for n in sorted(set(notes)):
        print(f"  . {n}")

