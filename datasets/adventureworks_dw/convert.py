#!/usr/bin/env python3
"""AdventureWorks DW (2025 edition) -> MySQL.

The same install-script shape as the OLTP database and the same reader (`scripts/bulkinsert.py`),
but a far simpler schema: one `dbo` schema so nothing is prefixed, one terminator family (`|` and a
newline), no computed columns and none of SQL Server's exotic types -- the only awkward ones are four
`varbinary` photo columns and a single `xml`.

Record: knowledge/datasets/adventureworks-dw.md
"""
import os, re, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import tsql, tsqlbody, ddlutil, bulkinsert  # noqa: E402

DATABASE = "adventureworks_dw"
CONTEXT = "/context/adventureworks_dw"
SCRIPT = "instawdbdw.sql"
# one schema, so its tables are unprefixed (knowledge/decisions/schema-to-database-mapping.md)
SCHEMAS = {"dbo": ""}
# SQL Server's own logging table; the naming decision drops it, as it does for the OLTP database
DROP_TABLES = {"databaselog"}
# The upstream version row is built from SERVERPROPERTY(), which does not exist here. Same treatment
# as the OLTP database: the version the 2025 edition reports, and the script's own "Updated" date,
# which is also the commit date of the pinned artifact.
BUILD_VERSION = ("INSERT INTO `adventureworksdwbuildversion` (`dbversion`, `versiondate`)\n"
                 "VALUES ('17.0.1000.3', '2025-11-14 00:00:00');")


def main():
    src, dest, mapfile = sys.argv[1], sys.argv[2], sys.argv[3]
    context = os.path.dirname(os.path.abspath(dest))
    z = zipfile.ZipFile(src)
    script = z.read(SCRIPT).decode("utf-8-sig")

    statements, name_map, notes = tsql.translate(script, keep_objects=True, schemas=SCHEMAS)

    buckets = {k: [] for k in ("table", "index", "constraint", "view", "procedure", "function",
                               "trigger", "dml")}
    columns, unported, deferred_routines = {}, [], set()
    # the routine bodies are translated by scripts/tsqlbody.py; anything it refuses is named here
    # with its reason, and a view that calls a refused routine is dropped below
    udts = dict(tsql.collect_tsql_types(script))
    routines, refused, routine_notes = tsqlbody.port(statements, udts)
    unported += refused
    deferred_routines = {r.split(":")[0].split()[-1].lower() for r in refused}
    for st in statements:
        kind, sql = st["kind"], st["sql"]
        if kind in ("procedure", "function", "trigger"):
            continue
        blockers = tsql.xml_blockers(sql) if kind == "view" else []
        if blockers:
            name = re.search(r"(?i)view\s+`?(\w+)`?", sql)
            unported.append(f"view {name.group(1).lower() if name else '?'}: "
                            f"uses {', '.join(blockers)}")
            continue
        if kind == "table":
            name = re.search(r"(?is)^\s*CREATE\s+TABLE\s+`([^`]+)`", sql).group(1)
            if name in DROP_TABLES:
                continue
            columns[name] = ddlutil.columns_of(sql)
        if kind in buckets:
            buckets[kind].append(sql)
        elif kind == "other" and re.match(r"(?i)^\s*create\s+(unique\s+)?index", sql.strip()):
            buckets["index"].append(sql)

    loads, loaded = [], {}
    for schema, table, filename, field, row in bulkinsert.statements(script):
        table = f"{SCHEMAS[schema]}{table}"
        if table not in columns:
            sys.exit(f"{filename} loads `{table}`, which the script does not create")
        loaded[table] = write_tsv(z, filename, field, row, table, columns[table], context)
        names = ", ".join(f"`{c}`" for c in columns[table])
        loads.append(f"LOAD DATA LOCAL INFILE '{CONTEXT}/{table}.tsv' INTO TABLE `{table}`\n"
                     f"  CHARACTER SET utf8mb4 ({names});")

    buckets["table"] = [t for t in buckets["table"]
                        if re.search(r"(?is)^\s*CREATE\s+TABLE\s+`([^`]+)`", t).group(1)
                        not in DROP_TABLES]
    # a view that calls a routine we did not port cannot be created; it comes back with V-02
    kept_views = []
    for sql in buckets["view"]:
        # the call site is backticked by the identifier scan: `udfbuildiso8601date` (...)
        used = sorted(r for r in deferred_routines
                      if re.search(rf"(?i)\b{re.escape(r)}`?\s*\(", sql))
        if used:
            name = re.search(r"(?i)view\s+`?(\w+)`?", sql)
            unported.append(f"view {name.group(1).lower() if name else '?'}: calls "
                            f"{', '.join(used)}, which is not ported yet (task V-02)")
            continue
        kept_views.append(sql)
    buckets["view"] = kept_views

    empty = sorted(set(columns) - set(loaded))
    out = [f"""-- AdventureWorks DW (2025 edition), translated by datasets/{DATABASE}/convert.py.
-- Upstream: microsoft/sql-server-samples (MIT). See datasets/{DATABASE}/LICENSE.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{DATABASE}`;
CREATE DATABASE `{DATABASE}` DEFAULT CHARACTER SET utf8mb4;
USE `{DATABASE}`;
"""]
    out += [tsql.terminate(sql) for sql in buckets["table"]]
    out.append(f"\n-- {'-' * 60}\n-- data\n")
    for sql in buckets["dml"]:
        out.append(BUILD_VERSION if "SERVERPROPERTY" in sql.upper() else tsql.terminate(sql))
    out += loads
    for phase in ("index", "constraint"):
        if buckets[phase]:
            out.append(f"\n-- {'-' * 60}\n-- {phase}\n")
            out += [tsql.terminate(sql) for sql in buckets[phase]]
    # routines before views: vTimeSeries calls udfBuildISO8601Date, and MySQL resolves a function
    # name when the view is created, not when it is queried
    if routines:
        out.append(f"\n-- {'-' * 60}\n-- routines\n")
        out.append(routines)
    if buckets["view"]:
        out.append(f"\n-- {'-' * 60}\n-- view\n")
        out += [tsql.terminate(sql) for sql in buckets["view"]]
    out.append("SET SESSION foreign_key_checks = 1;\n")
    open(dest, "w", encoding="utf-8").write("\n".join(out))
    with open(mapfile, "w", encoding="utf-8") as fh:
        fh.write(f"# Generated by datasets/{DATABASE}/convert.py.\n")
        for old, new in sorted(name_map.items()):
            fh.write(f"{old}: {new}\n")

    print(f"  . translated {len(buckets['table'])} tables, {len(buckets['index'])} indexes, "
          f"{len(buckets['view'])} views, "
          f"{routines.count('CREATE ')} routines")
    for n in routine_notes:
        print(f"  . note {n}")
    print(f"  . wrote {len(loaded)} TSV files, {sum(loaded.values()):,} rows")
    if empty:
        print(f"  . created with no data file upstream: {', '.join(empty)}")
    for u in unported:
        print(f"  . unported {u}")


def write_tsv(z, filename, field, row, table, table_columns, context):
    text = z.read(filename).decode("utf-8")
    written = 0
    with open(os.path.join(context, f"{table}.tsv"), "w", encoding="utf-8", newline="") as out:
        for fields in bulkinsert.rows(text, field, row, len(table_columns), filename, table):
            out.write("\t".join(bulkinsert.tsv_value(v) for v in fields) + "\n")
            written += 1
    return written


if __name__ == "__main__":
    main()
