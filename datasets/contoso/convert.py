#!/usr/bin/env python3
"""Contoso V2 -> MySQL, at whatever scale is asked for.

  convert.py <downloads> <out.sql>              100 k orders -> `contoso`      (core)
  convert.py <downloads> <out.sql> --size 1m    1 M orders   -> `contoso_1m`   (extended)
  convert.py <downloads> <out.sql> --size 10m   10 M orders  -> `contoso_10m`  (extended)

The larger sets are separate databases, not appends: they are the same eight tables at a different
scale, so there is nothing to add to an existing one.

The data ships as a 7-zip archive of eight header-bearing CSVs, read here with py7zr so the build
needs no system 7-zip. The types come from SQLBI's own SQL Server DDL, pinned at generator release
2.0.1, rather than being guessed from the data; the converter checks each CSV header against the
DDL's column order before writing a row, because the load is positional.

Record: knowledge/datasets/contoso.md
"""
import csv, io, os, re, sys

import py7zr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import tsql, ddlutil  # noqa: E402

DDL = ["CreateTablesCommon.sql", "CreateTablesSales.sql", "CreateTablesOrders.sql"]
csv.field_size_limit(1 << 24)


def main():
    downloads, dest = sys.argv[1], sys.argv[2]
    size = "100k"
    if "--size" in sys.argv[3:]:
        size = sys.argv[sys.argv.index("--size") + 1]
    database = "contoso" if size == "100k" else f"contoso_{size}"
    archive = f"csv-{size}.7z"
    context = os.path.dirname(os.path.abspath(dest))
    inside = f"/context/{os.path.basename(context)}"

    script = "\nGO\n".join(open(os.path.join(downloads, f), encoding="utf-8-sig").read()
                           for f in DDL)
    # one schema, so its objects are unprefixed (knowledge/decisions/schema-to-database-mapping.md)
    # SQLBI's DDL omits the comma before each table's PRIMARY KEY constraint
    statements, name_map, notes = tsql.translate(script, keep_objects=True, schemas={"data": ""},
                                                 fix_missing_commas=True)

    tables, columns = [], {}
    for st in statements:
        if st["kind"] != "table":
            continue
        name = re.search(r"(?is)^\s*CREATE\s+TABLE\s+`([^`]+)`", st["sql"]).group(1)
        tables.append((name, st["sql"]))
        columns[name] = ddlutil.columns_of(st["sql"])

    with py7zr.SevenZipFile(os.path.join(downloads, archive)) as archive:
        archive.extractall(path=context)

    loads, counts = [], {}
    for name, _ in tables:
        source = os.path.join(context, f"{name}.csv")
        if not os.path.exists(source):
            sys.exit(f"{name}: no {name}.csv in {archive}")
        counts[name] = to_tsv(source, os.path.join(context, f"{name}.tsv"), columns[name], name)
        os.remove(source)
        names = ", ".join(f"`{c}`" for c in columns[name])
        loads.append(f"LOAD DATA LOCAL INFILE '{inside}/{name}.tsv' INTO TABLE `{name}`\n"
                     f"  CHARACTER SET utf8mb4 ({names});")

    out = [f"""-- Contoso V2 ({size} orders), translated by datasets/contoso/convert.py from SQLBI's
-- ready-to-use CSV set and its SQL Server DDL (MIT). See datasets/contoso/LICENSE.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{database}`;
CREATE DATABASE `{database}` DEFAULT CHARACTER SET utf8mb4;
USE `{database}`;
"""]
    out += [tsql.terminate(sql) for _, sql in tables]
    out.append(f"\n-- {'-' * 60}\n-- data\n")
    out += loads
    for st in statements:
        if st["kind"] in ("index", "constraint") or (
                st["kind"] == "other" and re.match(r"(?i)^\s*create\s+(unique\s+)?index",
                                                   st["sql"].strip())):
            out.append(tsql.terminate(st["sql"]))
    out.append("SET SESSION foreign_key_checks = 1;\n")
    open(dest, "w", encoding="utf-8").write("\n".join(out))

    print(f"  . translated {len(tables)} tables from SQLBI's SQL Server DDL")
    print(f"  . wrote {len(counts)} contract TSV files, {sum(counts.values()):,} rows: "
          + ", ".join(f"{t} {n:,}" for t, n in counts.items()))
    for n in sorted(set(notes)):
        print(f"  . {n}")


def to_tsv(source, dest, table_columns, table):
    """CSV -> the LOAD DATA default dialect, checking the header against the DDL's column order."""
    rows = 0
    with open(source, newline="", encoding="utf-8-sig") as fh, \
            open(dest, "w", encoding="utf-8", newline="") as out:
        reader = csv.reader(fh)
        header = [h.strip().lower() for h in next(reader)]
        if header != [c.lower() for c in table_columns]:
            sys.exit(f"{table}: CSV header does not match the DDL\n"
                     f"  csv {header}\n  ddl {[c.lower() for c in table_columns]}")
        for row in reader:
            if len(row) != len(header):
                sys.exit(f"{table} line {rows + 2}: {len(row)} fields, header has {len(header)}")
            out.write("\t".join(
                "\\N" if v == "" else v.replace("\\", "\\\\").replace("\t", "\\t")
                .replace("\n", "\\n").replace("\r", "\\r") for v in row) + "\n")
            rows += 1
    return rows


if __name__ == "__main__":
    main()
