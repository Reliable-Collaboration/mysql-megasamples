#!/usr/bin/env python3
"""AdventureWorks OLTP -> MySQL.

The 2025 edition of the install script plus its 69 UTF-8 CSVs, with no SQL Server involved. The five
schemas fold into table-name prefixes (`person_address`, `sales_salesorderheader`) per the naming
decision; `dbo` tables stay unprefixed and SQL Server's own logging tables are dropped.

Three SQL Server types have no MySQL equivalent and are decoded here rather than stored opaquely:
`hierarchyid` keeps its raw bytes and gains a materialised path column, `geography` becomes a
`POINT SRID 4326`, and `xml` becomes text. See knowledge/sources/mysql-9-7-srid-4326-axis-order-probe.md
for how both binary formats were verified.

Record: knowledge/datasets/adventureworks-oltp.md
"""
import csv, os, re, struct, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import tsql, tsqlbody, hierarchyid, ddlutil, bulkinsert  # noqa: E402

DATABASE = "adventureworks"
SCRIPT = "instawdb.sql"
CONTEXT = "/context/adventureworks"      # the read-only mount scripts/db.py gives the build server
# every schema in the script, and the prefix its tables take
SCHEMAS = {"person": "person_", "humanresources": "humanresources_", "production": "production_",
           "purchasing": "purchasing_", "sales": "sales_", "dbo": ""}
# SQL Server's own logging tables; the naming decision drops them
DROP_TABLES = {"databaselog", "errorlog"}
# The upstream AWBuildVersion row is built from SERVERPROPERTY() and GETDATE(), neither of which
# exists here and the second of which would not be reproducible anyway. The version is the one the
# 2025 edition reports; the dates are the script's own "Updated" date, which is also the commit date
# of the pinned artifact.
BUILD_VERSION = ("INSERT INTO `awbuildversion` (`database_version`, `versiondate`, `modifieddate`)\n"
                 "VALUES ('17.0.1000.3', '2025-11-14 00:00:00', '2025-11-14 00:00:00');")

# T-SQL infers a computed column's type; MySQL makes you declare it. Types are the upstream ones.
COMPUTED_TYPES = {
    "purchasing_purchaseorderdetail.linetotal": "DECIMAL(38,6)",
    "purchasing_purchaseorderdetail.stockedqty": "DECIMAL(38,6)",
    "purchasing_purchaseorderheader.totaldue": "DECIMAL(19,4)",
    "sales_salesorderdetail.linetotal": "DECIMAL(38,6)",
    "sales_salesorderheader.totaldue": "DECIMAL(19,4)",
    "production_workorder.stockedqty": "DECIMAL(38,6)",
    "sales_salesorderheader.salesordernumber": "VARCHAR(25)",
    "sales_customer.accountnumber": "VARCHAR(10)",
    "humanresources_employee.organizationlevel": "SMALLINT",
    "production_document.documentlevel": "SMALLINT",
}
# MySQL will not generate a column that reads an AUTO_INCREMENT column, and it has no hierarchyid,
# so these four are ordinary columns whose values come from the data files.
MATERIALIZE = {"sales_salesorderheader.salesordernumber", "sales_customer.accountnumber",
               "humanresources_employee.organizationlevel", "production_document.documentlevel"}
# hierarchyid columns: kept as raw bytes, with a decoded path column added beside them
HIERARCHY = {"humanresources_employee.organizationnode", "production_document.documentnode",
             "production_productdocument.documentnode"}
GEOGRAPHY = {"person_address.spatiallocation"}

csv.field_size_limit(1 << 24)


def decode_point(hexstr):
    """SQL Server geography point -> (latitude, longitude); see the probe record."""
    raw = bytes.fromhex(hexstr)
    if len(raw) != 22:
        raise SystemExit(f"geography value is {len(raw)} bytes, only 22-byte points are handled")
    srid, version, flags = struct.unpack_from("<I", raw, 0)[0], raw[4], raw[5]
    if (srid, version, flags) != (4326, 1, 0x0C):
        raise SystemExit(f"unexpected geography header srid={srid} version={version} flags={flags:#x}")
    return struct.unpack_from("<dd", raw, 6)


PATH_COLUMN = re.compile(r"(?im)^(\s*)`(\w+)`(\s+VARBINARY\(892\))")


def add_path_columns(create_table):
    """Give every hierarchyid column a decoded-path column beside it.

    The raw bytes are kept so nothing is lost -- `scripts/hierarchyid.py` round-trips them -- but
    they are unusable as they stand, so the path SQL Server would print is materialised next to them.
    """
    table = re.search(r"(?is)CREATE\s+TABLE\s+`([^`]+)`", create_table)

    def add(m):
        if f"{table.group(1)}.{m.group(2)}".lower() not in HIERARCHY:
            return m.group(0)
        return (f"{m.group(1)}`{m.group(2)}`{m.group(3)},\n"
                f"{m.group(1)}`{m.group(2)}_path` VARCHAR(300)")

    return PATH_COLUMN.sub(add, create_table) if table else create_table


def main():
    src, dest, mapfile = sys.argv[1], sys.argv[2], sys.argv[3]
    context = os.path.dirname(os.path.abspath(dest))
    z = zipfile.ZipFile(src)
    script = z.read(SCRIPT).decode("utf-8-sig")

    statements, name_map, notes = tsql.translate(
        script, keep_objects=True, schemas=SCHEMAS,
        computed_types=COMPUTED_TYPES, materialize=MATERIALIZE)

    udts = dict(tsql.collect_tsql_types(script))
    udts.update({k: (v[0] if isinstance(v, tuple) else v)
                 for k, v in tsql.collect_udts(script).items()})
    routines, refused, routine_notes = tsqlbody.port(statements, udts)

    buckets = {k: [] for k in ("table", "index", "constraint", "view", "procedure", "function",
                               "trigger", "dml")}
    columns, generated, dropped_tables, unported = {}, {}, [], list(refused)
    for st in statements:
        kind, sql = st["kind"], st["sql"]
        if kind == "table":
            sql = add_path_columns(sql)
        if kind in ("procedure", "function", "trigger"):
            continue                 # translated in one pass by scripts/tsqlbody.py, below
        blockers = tsql.xml_blockers(sql) if kind == "view" else []
        if blockers:
            name = re.search(r"(?i)(view|procedure|function|trigger)\s+`?([\w.]+)`?", sql)
            unported.append(f"{name.group(1).lower()} {name.group(2).lower()}: "
                            f"uses {', '.join(blockers)}" if name else f"object uses {blockers}")
            continue
        if kind == "table":
            name = re.search(r"(?is)^\s*CREATE\s+TABLE\s+`([^`]+)`", sql).group(1)
            if name in DROP_TABLES:
                dropped_tables.append(name)
                continue
            columns[name] = ddlutil.columns_of(sql)
            generated[name] = set(st["generated"])
        if kind in buckets:
            buckets[kind].append(sql)
        elif kind == "other" and re.match(r"(?i)^\s*create\s+(unique\s+)?index", sql.strip()):
            buckets["index"].append(sql)

    # a statement that mentions a dropped table goes with it
    for phase, items in buckets.items():
        buckets[phase] = [s for s in items
                          if not any(re.search(rf"`{t}`", s) for t in dropped_tables)]

    loads, loaded = [], {}
    for schema, table_name, filename, field, row in bulkinsert.statements(script):
        table = f"{SCHEMAS[schema]}{table_name}"
        if table in DROP_TABLES:
            continue
        loaded[table] = write_tsv(z, filename, field, row, table, columns[table],
                                  generated[table], context)
        targets, sets = [], []
        # the decoded-path columns are written as part of their hierarchyid column's pair, so they
        # are not listed again on their own
        paths = {f"{c}_path" for c in columns[table] if f"{table}.{c}".lower() in HIERARCHY}
        for c in columns[table]:
            if c in generated[table] or c in paths:
                continue
            key = f"{table}.{c}".lower()
            if key in HIERARCHY:
                # the raw bytes go in as hex, and the decoded path follows in its own field
                targets += [f"@hex_{c}", f"`{c}_path`"]
                sets.append(f"`{c}` = UNHEX(@hex_{c})")
            elif key in GEOGRAPHY:
                targets.append(f"@wkt_{c}")
                sets.append(f"`{c}` = ST_GeomFromText(@wkt_{c}, 4326)")
            else:
                targets.append(f"`{c}`")
        clause = ("\n  SET " + ", ".join(sets)) if sets else ""
        loads.append(f"LOAD DATA LOCAL INFILE '{CONTEXT}/{table}.tsv' INTO TABLE `{table}`\n"
                     f"  CHARACTER SET utf8mb4 ({', '.join(targets)}){clause};")

    out = [f"""-- AdventureWorks OLTP (2025 edition), translated by datasets/{DATABASE}/convert.py.
-- Upstream: microsoft/sql-server-samples (MIT). See datasets/{DATABASE}/LICENSE.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{DATABASE}`;
CREATE DATABASE `{DATABASE}` DEFAULT CHARACTER SET utf8mb4;
USE `{DATABASE}`;
"""]
    for sql in buckets["table"]:
        out.append(tsql.terminate(sql))
    out.append(f"\n-- {'-' * 60}\n-- data\n")
    for sql in buckets["dml"]:
        if "SERVERPROPERTY" in sql.upper():
            out.append(BUILD_VERSION)
            continue
        out.append(tsql.terminate(sql))
    out += loads
    for phase in ("index", "constraint"):
        if buckets[phase]:
            out.append(f"\n-- {'-' * 60}\n-- {phase}\n")
            out += [tsql.terminate(s) for s in buckets[phase]]
    # routines before views: a view may call a function, and MySQL resolves the name at CREATE time
    if routines:
        out.append(f"\n-- {'-' * 60}\n-- routines\n")
        out.append(routines)
    if buckets["view"]:
        out.append(f"\n-- {'-' * 60}\n-- view\n")
        out += [tsql.terminate(s) for s in buckets["view"]]
    out.append("SET SESSION foreign_key_checks = 1;\n")
    open(dest, "w", encoding="utf-8").write("\n".join(out))
    with open(mapfile, "w", encoding="utf-8") as fh:
        fh.write("# Generated by datasets/adventureworks/convert.py.\n")
        for old, new in sorted(name_map.items()):
            fh.write(f"{old}: {new}\n")

    print(f"  . translated {len(buckets['table'])} tables, {len(buckets['index'])} indexes, "
          f"{len(buckets['view'])} views, {routines.count('CREATE ')} routines")
    print(f"  . wrote {len(loaded)} TSV files, {sum(loaded.values()):,} rows")
    print(f"  . dropped SQL Server logging tables: {', '.join(dropped_tables)}")
    for u in unported:
        print(f"  . unported {u}")
    for n in sorted(set(notes)):
        print(f"  . {n}")


def write_tsv(z, filename, field, row, table, table_columns, generated_columns, context):
    """Rewrite one upstream CSV as contract TSV, decoding the columns MySQL has no type for."""
    text = z.read(filename).decode("utf-8")
    # the decoded-path columns are ours, not the data file's, so they are not counted when reading
    source_columns = [c for c in table_columns
                      if f"{table}.{c[:-5]}".lower() not in HIERARCHY or not c.endswith("_path")]
    keep = [i for i, c in enumerate(source_columns) if c not in generated_columns]
    hierarchy = {i: f"{table}.{c}".lower() in HIERARCHY for i, c in enumerate(source_columns)}
    geography = {i: f"{table}.{c}".lower() in GEOGRAPHY for i, c in enumerate(source_columns)}
    written = 0
    with open(os.path.join(context, f"{table}.tsv"), "w", encoding="utf-8", newline="") as out:
        for fields in bulkinsert.rows(text, field, row, len(source_columns), filename, table):
            values = []
            for i in keep:
                value = fields[i]
                if value == "\x00":
                    value = ""
                if hierarchy[i]:
                    # the hex as written, then the decoded path. The root node's hierarchyid is the
                    # *empty* binary, not a missing value, so these two fields never become NULL.
                    values.append(bulkinsert.escape(value))
                    values.append(bulkinsert.escape(hierarchyid.decode(bytes.fromhex(value))))
                    continue
                if geography[i] and value:
                    lat, lon = decode_point(value)
                    value = f"POINT({lat} {lon})"
                values.append(bulkinsert.tsv_value(value))
            out.write("\t".join(values) + "\n")
            written += 1
    return written


if __name__ == "__main__":
    main()
