#!/usr/bin/env python3
"""Star Schema Benchmark -> MySQL, generated in the loader image rather than downloaded.

  convert.py <out.sql> [--sf 1]

SSB's generator is a fork of TPC-H's dbgen: no fork carries a LICENSE file and the sources keep the
TPC SCCS ids, so the TPC EULA governs it as a modified dbgen. It is therefore cloned and compiled
inside `engines/mysql/loader.Dockerfile` at build time and never vendored here, and its output is never
shipped -- the same position as TPC-H and TPC-DS.

The generator is built with `EOL_HANDLING=ON` (no trailing pipe, so MySQL sees the real column count)
and `YMD_DASH_DATE=ON` (dates as `1992-01-01` rather than the integer `19920101`). Both are build
options rather than post-processing, which is why the `.tbl` files load with no rewriting at all.

The schema is the paper's, not `doc/ssb.ri`: that file names the date table `date_` and puts a
single-column primary key on lineorder, and both contradict the DDL beside it.

Record: knowledge/datasets/ssb.md
"""
import os, subprocess, sys

DATABASE = "ssb"
IMAGE = os.environ.get("LOADER_IMAGE", "sql-megasamples-loader:dev")
TABLES = {
    "customer": ([("c_custkey", "INT NOT NULL"), ("c_name", "VARCHAR(25) NOT NULL"),
                  ("c_address", "VARCHAR(25) NOT NULL"), ("c_city", "CHAR(10) NOT NULL"),
                  ("c_nation", "CHAR(15) NOT NULL"), ("c_region", "CHAR(12) NOT NULL"),
                  ("c_phone", "CHAR(15) NOT NULL"), ("c_mktsegment", "CHAR(10) NOT NULL")],
                 ["c_custkey"]),
    "part": ([("p_partkey", "INT NOT NULL"), ("p_name", "VARCHAR(22) NOT NULL"),
              ("p_mfgr", "CHAR(6) NOT NULL"), ("p_category", "CHAR(7) NOT NULL"),
              ("p_brand1", "CHAR(9) NOT NULL"), ("p_color", "VARCHAR(11) NOT NULL"),
              ("p_type", "VARCHAR(25) NOT NULL"), ("p_size", "INT NOT NULL"),
              ("p_container", "CHAR(10) NOT NULL")], ["p_partkey"]),
    "supplier": ([("s_suppkey", "INT NOT NULL"), ("s_name", "CHAR(25) NOT NULL"),
                  ("s_address", "VARCHAR(25) NOT NULL"), ("s_city", "CHAR(10) NOT NULL"),
                  ("s_nation", "CHAR(15) NOT NULL"), ("s_region", "CHAR(12) NOT NULL"),
                  ("s_phone", "CHAR(15) NOT NULL")], ["s_suppkey"]),
    "date": ([("d_datekey", "DATE NOT NULL"), ("d_date", "CHAR(18) NOT NULL"),
              ("d_dayofweek", "CHAR(9) NOT NULL"), ("d_month", "CHAR(9) NOT NULL"),
              ("d_year", "INT NOT NULL"), ("d_yearmonthnum", "INT NOT NULL"),
              ("d_yearmonth", "CHAR(7) NOT NULL"), ("d_daynuminweek", "INT NOT NULL"),
              ("d_daynuminmonth", "INT NOT NULL"), ("d_daynuminyear", "INT NOT NULL"),
              ("d_monthnuminyear", "INT NOT NULL"), ("d_weeknuminyear", "INT NOT NULL"),
              ("d_sellingseason", "CHAR(12) NOT NULL"), ("d_lastdayinweekfl", "CHAR(1) NOT NULL"),
              ("d_lastdayinmonthfl", "CHAR(1) NOT NULL"), ("d_holidayfl", "CHAR(1) NOT NULL"),
              ("d_weekdayfl", "CHAR(1) NOT NULL")], ["d_datekey"]),
    "lineorder": ([("lo_orderkey", "INT NOT NULL"), ("lo_linenumber", "INT NOT NULL"),
                   ("lo_custkey", "INT NOT NULL"), ("lo_partkey", "INT NOT NULL"),
                   ("lo_suppkey", "INT NOT NULL"), ("lo_orderdate", "DATE NOT NULL"),
                   ("lo_orderpriority", "CHAR(15) NOT NULL"),
                   ("lo_shippriority", "CHAR(1) NOT NULL"), ("lo_quantity", "INT NOT NULL"),
                   ("lo_extendedprice", "INT NOT NULL"), ("lo_ordtotalprice", "INT NOT NULL"),
                   ("lo_discount", "INT NOT NULL"), ("lo_revenue", "INT NOT NULL"),
                   ("lo_supplycost", "INT NOT NULL"), ("lo_tax", "INT NOT NULL"),
                   ("lo_commitdate", "DATE NOT NULL"), ("lo_shipmode", "CHAR(10) NOT NULL")],
                  ["lo_orderkey", "lo_linenumber"]),
}
ORDER = ["customer", "part", "supplier", "date", "lineorder"]
FOREIGN_KEYS = [("lineorder", "lo_custkey", "customer", "c_custkey"),
                ("lineorder", "lo_partkey", "part", "p_partkey"),
                ("lineorder", "lo_suppkey", "supplier", "s_suppkey"),
                ("lineorder", "lo_orderdate", "date", "d_datekey")]
INDEXES = [("lineorder", ["lo_orderdate"]), ("lineorder", ["lo_partkey"]),
           ("lineorder", ["lo_suppkey"]), ("lineorder", ["lo_custkey"]),
           ("lineorder", ["lo_discount", "lo_quantity"]),
           ("part", ["p_brand1"]), ("part", ["p_category"]), ("part", ["p_mfgr"]),
           ("customer", ["c_region"]), ("customer", ["c_nation"]), ("customer", ["c_city"]),
           ("supplier", ["s_region"]), ("supplier", ["s_nation"]), ("supplier", ["s_city"]),
           ("date", ["d_year"]), ("date", ["d_yearmonth"]), ("date", ["d_yearmonthnum"])]
DISCLAIMER = ("The Star Schema Benchmark is derived from TPC-H. This is NOT a TPC result and any "
              "measurement taken against it is not comparable to a published TPC result.")


def generate(context, sf):
    """Run the generator inside the loader image; nothing is compiled or installed on the host."""
    if all(os.path.exists(os.path.join(context, f"{t}.tbl")) for t in ORDER):
        return "reused the .tbl files already in the staging directory"
    cmd = ["docker", "run", "--rm", "-v", f"{os.path.abspath(context)}:/work", IMAGE,
           "sh", "-c", f"cd /work && ssb-dbgen -b /opt/dists.dss -s {sf:g} -f -q"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0 or not os.path.exists(os.path.join(context, "lineorder.tbl")):
        sys.exit(f"ssb-dbgen failed in {IMAGE}: {(p.stderr or p.stdout)[-400:]}\n"
                 f"Build the loader image first: "
                 f"make loader-image")
    return f"generated in {IMAGE}"


def main():
    dest = sys.argv[1]
    sf = float(sys.argv[sys.argv.index("--sf") + 1]) if "--sf" in sys.argv[2:] else 1.0
    context = os.path.dirname(os.path.abspath(dest))
    inside = f"/context/{os.path.basename(context)}"
    os.makedirs(context, exist_ok=True)
    how = generate(context, sf)

    ddl, loads, counts = [], [], {}
    for table in ORDER:
        columns, pk = TABLES[table]
        path = os.path.join(context, f"{table}.tbl")
        with open(path, "rb") as fh:
            counts[table] = sum(1 for _ in fh)
        first = open(path, encoding="utf-8", errors="replace").readline().rstrip("\n")
        if len(first.split("|")) != len(columns):
            sys.exit(f"{table}.tbl has {len(first.split('|'))} fields, the schema declares "
                     f"{len(columns)} -- was the generator built with EOL_HANDLING=ON?")
        body = ",\n".join(f"  `{c}` {t}" for c, t in columns)
        keys = ", ".join(f"`{c}`" for c in pk)
        ddl.append(f"CREATE TABLE `{table}` (\n{body},\n  PRIMARY KEY ({keys})\n) ENGINE=InnoDB "
                   f"DEFAULT CHARSET=utf8mb4;")
        names = ", ".join(f"`{c}`" for c, _ in columns)
        loads.append(f"LOAD DATA LOCAL INFILE '{inside}/{table}.tbl' INTO TABLE `{table}`\n"
                     f"  CHARACTER SET utf8mb4 FIELDS TERMINATED BY '|' ESCAPED BY ''\n"
                     f"  ({names});")

    later = [f"ALTER TABLE `{t}` ADD KEY `ix_{t}_{'_'.join(c.split('_', 1)[-1] for c in cols)}` "
             f"({', '.join(f'`{c}`' for c in cols)});" for t, cols in INDEXES]
    later += [f"ALTER TABLE `{t}` ADD CONSTRAINT `fk_{t}_{c}` FOREIGN KEY (`{c}`) "
              f"REFERENCES `{rt}` (`{rc}`);" for t, c, rt, rc in FOREIGN_KEYS]

    sql = f"""-- Star Schema Benchmark at scale factor {sf:g}, prepared by datasets/{DATABASE}/convert.py.
-- The generator is compiled in engines/mysql/loader.Dockerfile and its output is never shipped.
--
-- {DISCLAIMER}
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{DATABASE}`;
CREATE DATABASE `{DATABASE}` DEFAULT CHARACTER SET utf8mb4;
USE `{DATABASE}`;

{chr(10).join(ddl)}

-- {'-' * 60}
-- data

{chr(10).join(loads)}

-- {'-' * 60}
-- indexes and referential integrity

{chr(10).join(later)}

SET SESSION foreign_key_checks = 1;
"""
    open(dest, "w", encoding="utf-8").write(sql)
    print(f"  . {how}")
    print(f"  . scale factor {sf:g}: {sum(counts.values()):,} rows -> "
          + ", ".join(f"{t} {counts[t]:,}" for t in ORDER))
    print(f"  . {len(later)} indexes and foreign keys")


if __name__ == "__main__":
    main()
