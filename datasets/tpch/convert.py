#!/usr/bin/env python3
"""TPC-H -> MySQL, generated rather than downloaded.

  convert.py <out.sql> [--sf 1]

No TPC data is shipped by this project and none is committed: the rows are produced on the machine
that builds them, by DuckDB's `tpch` extension (a port of dbgen 2.17.3). The same goes for the 22
query texts, which are written into the staging directory at build time rather than into the
repository -- the conservative reading of the TPC EULA, adopted because it costs nothing here
(knowledge/questions/tpc-eula-generated-data-redistribution.md,
knowledge/questions/tpc-query-text-redistribution.md).

The DDL is written from the specification's `dss.ddl` rather than inferred from DuckDB, because the
types are load-bearing: the reference answers are decimal sums, and letting a generator choose
DOUBLE would change them in the last places.

Record: knowledge/datasets/tpc-h.md
"""
import os, re, sys

import duckdb

DATABASE = "tpch"
# The eight tables in dss.ddl order -- which is also load order, parents before children.
TABLES = [
    ("region", [("r_regionkey", "INT NOT NULL"), ("r_name", "CHAR(25) NOT NULL"),
                ("r_comment", "VARCHAR(152)")], ["r_regionkey"]),
    ("nation", [("n_nationkey", "INT NOT NULL"), ("n_name", "CHAR(25) NOT NULL"),
                ("n_regionkey", "INT NOT NULL"), ("n_comment", "VARCHAR(152)")], ["n_nationkey"]),
    ("supplier", [("s_suppkey", "INT NOT NULL"), ("s_name", "CHAR(25) NOT NULL"),
                  ("s_address", "VARCHAR(40) NOT NULL"), ("s_nationkey", "INT NOT NULL"),
                  ("s_phone", "CHAR(15) NOT NULL"), ("s_acctbal", "DECIMAL(15,2) NOT NULL"),
                  ("s_comment", "VARCHAR(101) NOT NULL")], ["s_suppkey"]),
    ("part", [("p_partkey", "INT NOT NULL"), ("p_name", "VARCHAR(55) NOT NULL"),
              ("p_mfgr", "CHAR(25) NOT NULL"), ("p_brand", "CHAR(10) NOT NULL"),
              ("p_type", "VARCHAR(25) NOT NULL"), ("p_size", "INT NOT NULL"),
              ("p_container", "CHAR(10) NOT NULL"), ("p_retailprice", "DECIMAL(15,2) NOT NULL"),
              ("p_comment", "VARCHAR(23) NOT NULL")], ["p_partkey"]),
    ("partsupp", [("ps_partkey", "INT NOT NULL"), ("ps_suppkey", "INT NOT NULL"),
                  ("ps_availqty", "INT NOT NULL"), ("ps_supplycost", "DECIMAL(15,2) NOT NULL"),
                  ("ps_comment", "VARCHAR(199) NOT NULL")], ["ps_partkey", "ps_suppkey"]),
    ("customer", [("c_custkey", "INT NOT NULL"), ("c_name", "VARCHAR(25) NOT NULL"),
                  ("c_address", "VARCHAR(40) NOT NULL"), ("c_nationkey", "INT NOT NULL"),
                  ("c_phone", "CHAR(15) NOT NULL"), ("c_acctbal", "DECIMAL(15,2) NOT NULL"),
                  ("c_mktsegment", "CHAR(10) NOT NULL"),
                  ("c_comment", "VARCHAR(117) NOT NULL")], ["c_custkey"]),
    ("orders", [("o_orderkey", "BIGINT NOT NULL"), ("o_custkey", "INT NOT NULL"),
                ("o_orderstatus", "CHAR(1) NOT NULL"), ("o_totalprice", "DECIMAL(15,2) NOT NULL"),
                ("o_orderdate", "DATE NOT NULL"), ("o_orderpriority", "CHAR(15) NOT NULL"),
                ("o_clerk", "CHAR(15) NOT NULL"), ("o_shippriority", "INT NOT NULL"),
                ("o_comment", "VARCHAR(79) NOT NULL")], ["o_orderkey"]),
    ("lineitem", [("l_orderkey", "BIGINT NOT NULL"), ("l_partkey", "INT NOT NULL"),
                  ("l_suppkey", "INT NOT NULL"), ("l_linenumber", "INT NOT NULL"),
                  ("l_quantity", "DECIMAL(15,2) NOT NULL"),
                  ("l_extendedprice", "DECIMAL(15,2) NOT NULL"),
                  ("l_discount", "DECIMAL(15,2) NOT NULL"), ("l_tax", "DECIMAL(15,2) NOT NULL"),
                  ("l_returnflag", "CHAR(1) NOT NULL"), ("l_linestatus", "CHAR(1) NOT NULL"),
                  ("l_shipdate", "DATE NOT NULL"), ("l_commitdate", "DATE NOT NULL"),
                  ("l_receiptdate", "DATE NOT NULL"), ("l_shipinstruct", "CHAR(25) NOT NULL"),
                  ("l_shipmode", "CHAR(10) NOT NULL"), ("l_comment", "VARCHAR(44) NOT NULL")],
     ["l_orderkey", "l_linenumber"]),
]
# dss.ri
FOREIGN_KEYS = [
    ("nation", "n_regionkey", "region", "r_regionkey"),
    ("supplier", "s_nationkey", "nation", "n_nationkey"),
    ("customer", "c_nationkey", "nation", "n_nationkey"),
    ("partsupp", "ps_partkey", "part", "p_partkey"),
    ("partsupp", "ps_suppkey", "supplier", "s_suppkey"),
    ("orders", "o_custkey", "customer", "c_custkey"),
    ("lineitem", "l_orderkey", "orders", "o_orderkey"),
    ("lineitem", "l_partkey", "part", "p_partkey"),
    ("lineitem", "l_suppkey", "supplier", "s_suppkey"),
]
INDEXES = [
    ("lineitem", "ix_lineitem_part_supp", ["l_partkey", "l_suppkey"]),
    ("lineitem", "ix_lineitem_suppkey", ["l_suppkey"]),
    ("lineitem", "ix_lineitem_shipdate", ["l_shipdate"]),
    ("orders", "ix_orders_custkey", ["o_custkey"]),
    ("orders", "ix_orders_orderdate", ["o_orderdate"]),
    ("partsupp", "ix_partsupp_suppkey", ["ps_suppkey"]),
    ("customer", "ix_customer_nationkey", ["c_nationkey"]),
    ("supplier", "ix_supplier_nationkey", ["s_nationkey"]),
    ("nation", "ix_nation_regionkey", ["n_regionkey"]),
]

DISCLAIMER = ("This data is derived from the TPC-H benchmark specification. It is NOT a TPC-H "
              "result and any measurement taken against it is not comparable to a published "
              "TPC-H result.")


def patch(sql):
    """dbgen's SQL dialect -> MySQL. Small and enumerated, because each rewrite changes a result."""
    out = sql
    # `interval '90' day (3)` and its siblings; MySQL wants INTERVAL 90 DAY
    out = re.sub(r"(?i)interval\s+'(\d+)'\s+(day|month|year)\s*(\(\d+\))?",
                 lambda m: f"INTERVAL {m.group(1)} {m.group(2).upper()}", out)
    out = re.sub(r"(?i)\bdate\s+'(\d{4}-\d{2}-\d{2})'", r"DATE '\1'", out)
    # DuckDB writes `x::type`; MySQL has no cast operator
    out = re.sub(r"::\s*DECIMAL\s*\(\s*\d+\s*,\s*(\d+)\s*\)", "", out)
    return out.strip().rstrip(";")


def main():
    dest = sys.argv[1]
    sf = 1.0
    if "--sf" in sys.argv[2:]:
        sf = float(sys.argv[sys.argv.index("--sf") + 1])
    context = os.path.dirname(os.path.abspath(dest))
    inside = f"/context/{os.path.basename(context)}"
    queries_dir = os.path.join(context, "queries")
    os.makedirs(queries_dir, exist_ok=True)

    con = duckdb.connect()
    con.execute("INSTALL tpch; LOAD tpch;")
    con.execute(f"CALL dbgen(sf={sf});")

    counts, loads = {}, []
    for table, columns, _ in TABLES:
        path = os.path.join(context, f"{table}.tbl")
        con.execute(f"COPY {table} TO '{path}' (FORMAT csv, DELIMITER '|', HEADER false, "
                    "QUOTE '', ESCAPE '', NULLSTR '')")
        counts[table] = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        names = ", ".join(f"`{c}`" for c, _ in columns)
        loads.append(f"LOAD DATA LOCAL INFILE '{inside}/{table}.tbl' INTO TABLE `{table}`\n"
                     f"  CHARACTER SET utf8mb4 FIELDS TERMINATED BY '|' ESCAPED BY ''\n"
                     f"  ({names});")

    written = 0
    for nr, text in con.execute("SELECT query_nr, query FROM tpch_queries() ORDER BY query_nr").fetchall():
        with open(os.path.join(queries_dir, f"q{nr:02d}.sql"), "w", encoding="utf-8") as fh:
            fh.write(f"-- TPC-H query {nr}, generated at build time and not committed.\n"
                     f"-- {DISCLAIMER}\n{patch(text)};\n")
        written += 1

    ddl = []
    for table, columns, pk in TABLES:
        body = ",\n".join(f"  `{c}` {t}" for c, t in columns)
        keys = ", ".join(f"`{c}`" for c in pk)
        ddl.append(f"CREATE TABLE `{table}` (\n{body},\n  PRIMARY KEY ({keys})\n"
                   f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;")
    later = [f"ALTER TABLE `{t}` ADD KEY `{n}` ({', '.join(f'`{c}`' for c in cols)});"
             for t, n, cols in INDEXES]
    later += [f"ALTER TABLE `{t}` ADD CONSTRAINT `fk_{t}_{c}` FOREIGN KEY (`{c}`) "
              f"REFERENCES `{rt}` (`{rc}`);" for t, c, rt, rc in FOREIGN_KEYS]

    sql = f"""-- TPC-H at scale factor {sf:g}, generated by datasets/{DATABASE}/convert.py using
-- DuckDB's tpch extension. No TPC data is shipped or committed by this project.
--
-- {DISCLAIMER}
--
-- utf8mb4_bin: the reference answers order strings by byte value, and a case-insensitive
-- collation reorders ties in several queries.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{DATABASE}`;
CREATE DATABASE `{DATABASE}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
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
    print(f"  . scale factor {sf:g}: {sum(counts.values()):,} rows -> "
          + ", ".join(f"{t} {n:,}" for t, n in counts.items()))
    print(f"  . {written} query texts written to {os.path.basename(queries_dir)}/ "
          f"(generated at build time, never committed)")


if __name__ == "__main__":
    main()
