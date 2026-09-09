#!/usr/bin/env python3
"""Oracle Sales History -> MySQL.

SH is the one Oracle sample whose data is not in its scripts: three small dimensions are INSERTs in
`sh_populate.sql` and the other six tables are CSVs that upstream loads with SQLcl. Those become
contract TSV and `LOAD DATA LOCAL INFILE`, so no Oracle product is needed.

Four Oracle features have no MySQL counterpart and are handled rather than ignored: range
partitioning (dropped, because InnoDB cannot combine it with the foreign keys these very tables
carry), bitmap indexes (ordinary B-trees), an Oracle Text index (InnoDB FULLTEXT) and two
materialized views (plain views). The five CREATE DIMENSION objects are dropped outright.

Record: knowledge/datasets/oracle-sh.md
"""
import csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from megasamples.sources import oracle_convert, plsql  # noqa: E402

DATABASE = "oracle_sh"
SCRIPTS = ["sh_create.sql", "sh_populate.sql"]
# table -> csv, in the order upstream loads them
CSV_TABLES = [("costs", "costs.csv"), ("customers", "customers.csv"),
              ("promotions", "promotions.csv"), ("sales", "sales.csv"),
              ("times", "times.csv"),
              ("supplementary_demographics", "supplementary_demographics.csv")]
# the container path of the read-only mount that megasamples/engines/mysql/server.py gives the build server
CONTEXT = "/context/oracle_sh"
csv.field_size_limit(1 << 20)


def to_tsv(source, dest):
    """Rewrite a CSV as MySQL's default LOAD DATA dialect: tab-separated, `\\N` for NULL.

    Oracle stores '' as NULL, so every empty field -- quoted or not -- becomes NULL rather than an
    empty string. `sales.csv` pads each line with spaces to exactly 80 characters, which would
    otherwise land in `amount_sold`, so trailing blanks are stripped from every field.
    """
    rows = 0
    with open(source, newline="", encoding="utf-8") as fh, \
            open(dest, "w", encoding="utf-8", newline="") as out:
        reader = csv.reader(fh)
        header = next(reader)
        for row in reader:
            if len(row) != len(header):
                sys.exit(f"{os.path.basename(source)} line {rows + 2}: {len(row)} fields, "
                         f"header has {len(header)}")
            fields = []
            for value in row:
                value = value.rstrip()
                if value == "":
                    fields.append("\\N")
                else:
                    fields.append(value.replace("\\", "\\\\").replace("\t", "\\t")
                                  .replace("\n", "\\n").replace("\r", "\\r"))
            out.write("\t".join(fields) + "\n")
            rows += 1
    return [c.lower() for c in header], rows


def main():
    downloads, dest = sys.argv[1], sys.argv[2]
    context = os.path.dirname(os.path.abspath(dest))

    # SH's DATE columns are verified to carry no time component, so they stay DATE: times is a
    # calendar dimension keyed by day, and a DATETIME key would read wrong and index wider.
    buckets, notes, dropped = oracle_convert.convert(downloads, SCRIPTS, date_type="DATE",
                                                    schema_prefix="sh")

    # record how many partitions each table lost, in the table's own comment
    partitions = {}
    for name in SCRIPTS:
        text = open(os.path.join(downloads, name), encoding="utf-8").read()
        for m in re.finditer(r"(?is)CREATE\s+TABLE\s+(\w+)(.*?)(?=\n\s*CREATE|\Z)", text):
            n = plsql.count_partitions(m.group(2))
            if n:
                partitions[m.group(1).lower()] = n

    loads, counts = [], {}
    for table, filename in CSV_TABLES:
        columns, rows = to_tsv(os.path.join(downloads, filename),
                               os.path.join(context, f"{table}.tsv"))
        counts[table] = rows
        loads.append(f"LOAD DATA LOCAL INFILE '{CONTEXT}/{table}.tsv' INTO TABLE `{table}`\n"
                     f"  CHARACTER SET utf8mb4 ({', '.join(f'`{c}`' for c in columns)});")

    out = [oracle_convert.header(DATABASE)]
    for phase in oracle_convert.PHASES:
        if phase == "dml":
            out.append(f"\n-- {'-' * 60}\n-- data\n")
            out += [s.rstrip(";") + ";" for s in buckets["dml"]]
            out.append(f"\n-- the six CSV tables, as contract TSV\n")
            out += loads
            continue
        if not buckets[phase]:
            continue
        out.append(f"\n-- {'-' * 60}\n-- {phase}\n")
        out += [s if s.lstrip().startswith("--") else s.rstrip(";") + ";" for s in buckets[phase]]
    if partitions:
        out.append(f"\n-- {'-' * 60}\n-- partitioning, recorded rather than reproduced\n")
        out += [f"ALTER TABLE `{t}` COMMENT = 'upstream is range-partitioned on time_id into {n} "
                f"partitions; InnoDB cannot combine partitioning with the foreign keys this table "
                f"carries, so the keys were kept and the partitioning dropped';"
                for t, n in sorted(partitions.items())]
    out.append("SET SESSION foreign_key_checks = 1;\n")
    open(dest, "w", encoding="utf-8").write("\n".join(out))

    print(f"  . translated {({k: len(v) for k, v in buckets.items() if v})}; "
          f"attached {dropped.get('column_comment_attached', 0)} of "
          f"{dropped.get('column_comment', 0)} column comments")
    print(f"  . wrote {len(CSV_TABLES)} contract TSV files, {sum(counts.values()):,} rows: "
          + ", ".join(f"{t} {n:,}" for t, n in counts.items()))
    print(f"  . dropped partitioning on {', '.join(f'{t} ({n})' for t, n in sorted(partitions.items()))}")
    for n in sorted(set(notes)):
        print(f"  . {n}")


if __name__ == "__main__":
    main()
