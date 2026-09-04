#!/usr/bin/env python3
"""TPC-DS -> MySQL, generated rather than downloaded.

  convert.py <out.sql> [--sf 1]

The same shape as TPC-H's converter and the same licence position: nothing TPC-authored is
committed, and both the rows and the 99 query texts are produced into the staging directory at build
time.

One difference worth stating. TPC-H's DDL is written out by hand from `dss.ddl`, because DuckDB's
generator infers types that would change the reference answers. TPC-DS's does not need that: the
extension already emits the specification's types -- `DECIMAL(7,2)` for money, `DECIMAL(5,2)` for
rates, `DATE`, `BIGINT` surrogate keys -- so the DDL is derived from what was generated and the
column list can never drift out of step with the data. What is *not* generated is the keys: dsdgen
declares no constraints at all, so primary keys come from the specification and are checked against
the data before they are declared.

Record: knowledge/datasets/tpc-ds.md
"""
import os, re, sys

import duckdb

DATABASE = "tpcds"
# The specification's primary keys. Fact tables are composite; dimensions are their surrogate key.
PRIMARY_KEYS = {
    "call_center": ["cc_call_center_sk"], "catalog_page": ["cp_catalog_page_sk"],
    "catalog_returns": ["cr_item_sk", "cr_order_number"],
    "catalog_sales": ["cs_item_sk", "cs_order_number"],
    "customer": ["c_customer_sk"], "customer_address": ["ca_address_sk"],
    "customer_demographics": ["cd_demo_sk"], "date_dim": ["d_date_sk"],
    "household_demographics": ["hd_demo_sk"], "income_band": ["ib_income_band_sk"],
    "inventory": ["inv_date_sk", "inv_item_sk", "inv_warehouse_sk"],
    "item": ["i_item_sk"], "promotion": ["p_promo_sk"], "reason": ["r_reason_sk"],
    "ship_mode": ["sm_ship_mode_sk"], "store": ["s_store_sk"],
    "store_returns": ["sr_item_sk", "sr_ticket_number"],
    "store_sales": ["ss_item_sk", "ss_ticket_number"], "time_dim": ["t_time_sk"],
    "warehouse": ["w_warehouse_sk"], "web_page": ["wp_web_page_sk"],
    "web_returns": ["wr_item_sk", "wr_order_number"],
    "web_sales": ["ws_item_sk", "ws_order_number"], "web_site": ["web_site_sk"],
}
# dimensions before facts, so the load never inserts a child before its parent
LOAD_ORDER = ["date_dim", "time_dim", "customer_address", "customer_demographics",
              "household_demographics", "income_band", "item", "reason", "ship_mode", "warehouse",
              "call_center", "catalog_page", "promotion", "store", "web_page", "web_site",
              "customer", "inventory", "store_sales", "store_returns", "catalog_sales",
              "catalog_returns", "web_sales", "web_returns"]
# Secondary indexes on the fact tables' foreign keys and the dimensions' filter columns. dsdgen
# declares none, and without them MySQL cannot finish half the 99 queries in a minute at SF 1 --
# 51 of them timed out before these were added. The set is derived from what the queries filter and
# join on, not from a rule of thumb.
INDEXES = {
    "store_sales": [["ss_sold_date_sk"], ["ss_item_sk"], ["ss_customer_sk"], ["ss_store_sk"],
                    ["ss_promo_sk"], ["ss_cdemo_sk"], ["ss_hdemo_sk"], ["ss_addr_sk"]],
    "store_returns": [["sr_returned_date_sk"], ["sr_item_sk"], ["sr_customer_sk"],
                      ["sr_store_sk"], ["sr_reason_sk"]],
    "catalog_sales": [["cs_sold_date_sk"], ["cs_item_sk"], ["cs_bill_customer_sk"],
                      ["cs_bill_addr_sk"], ["cs_ship_addr_sk"], ["cs_call_center_sk"],
                      ["cs_warehouse_sk"], ["cs_promo_sk"], ["cs_bill_cdemo_sk"]],
    "catalog_returns": [["cr_returned_date_sk"], ["cr_item_sk"], ["cr_returning_customer_sk"],
                        ["cr_call_center_sk"], ["cr_catalog_page_sk"]],
    "web_sales": [["ws_sold_date_sk"], ["ws_item_sk"], ["ws_bill_customer_sk"],
                  ["ws_ship_addr_sk"], ["ws_web_site_sk"], ["ws_warehouse_sk"],
                  ["ws_promo_sk"], ["ws_ship_customer_sk"]],
    "web_returns": [["wr_returned_date_sk"], ["wr_item_sk"], ["wr_returning_customer_sk"],
                    ["wr_web_page_sk"]],
    "inventory": [["inv_item_sk"], ["inv_warehouse_sk"]],
    "date_dim": [["d_date"], ["d_year"], ["d_month_seq"], ["d_week_seq"], ["d_qoy"],
                 ["d_year", "d_moy"]],
    "item": [["i_item_id"], ["i_category"], ["i_brand"], ["i_manufact_id"], ["i_manager_id"],
             ["i_class"]],
    "customer": [["c_current_addr_sk"], ["c_current_cdemo_sk"], ["c_current_hdemo_sk"],
                 ["c_customer_id"], ["c_birth_month"]],
    "customer_address": [["ca_state"], ["ca_city"], ["ca_zip"], ["ca_county"],
                         ["ca_gmt_offset"]],
    "customer_demographics": [["cd_gender", "cd_marital_status", "cd_education_status"],
                              ["cd_demo_sk", "cd_dep_count"]],
    "household_demographics": [["hd_income_band_sk"], ["hd_buy_potential"]],
    "store": [["s_state"], ["s_county"], ["s_store_id"], ["s_gmt_offset"]],
    "promotion": [["p_channel_email", "p_channel_event"]],
    "time_dim": [["t_hour"], ["t_meal_time"]],
    "web_page": [["wp_char_count"]],
    "warehouse": [["w_warehouse_name"]],
    "call_center": [["cc_call_center_id"]],
}

DISCLAIMER = ("This data is derived from the TPC-DS benchmark specification. It is NOT a TPC-DS "
              "result and any measurement taken against it is not comparable to a published "
              "TPC-DS result.")


def mysql_type(duck):
    """DuckDB's generated type -> MySQL's. The money and rate decimals pass through unchanged."""
    t = duck.upper()
    if t.startswith("DECIMAL"):
        return t
    return {"BIGINT": "BIGINT", "INTEGER": "INT", "DATE": "DATE", "VARCHAR": "VARCHAR(255)"}[t]


def patch(sql):
    """dsdgen's SQL dialect -> MySQL. Each rule is here because a query failed without it."""
    out = sql
    out = re.sub(r"(?i)\b(\w+)\s*\+\s*(\d+)\s+days?\b", r"DATE_ADD(\1, INTERVAL \2 DAY)", out)
    out = re.sub(r"(?i)interval\s+'(\d+)'\s+(day|month|year)\s*(\(\d+\))?",
                 lambda m: f"INTERVAL {m.group(1)} {m.group(2).upper()}", out)
    out = re.sub(r"::\s*DECIMAL\s*\(\s*\d+\s*,\s*\d+\s*\)", "", out)
    out = re.sub(r"(?i)\bstddev_samp\b", "STDDEV_SAMP", out)
    return out.strip().rstrip(";")


def main():
    dest = sys.argv[1]
    sf = float(sys.argv[sys.argv.index("--sf") + 1]) if "--sf" in sys.argv[2:] else 1.0
    context = os.path.dirname(os.path.abspath(dest))
    inside = f"/context/{os.path.basename(context)}"
    queries_dir = os.path.join(context, "queries")
    os.makedirs(queries_dir, exist_ok=True)

    con = duckdb.connect()
    con.execute("INSTALL tpcds; LOAD tpcds;")
    con.execute(f"CALL dsdgen(sf={sf});")

    tables = [t for (t,) in con.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='main' "
        "ORDER BY table_name").fetchall()]
    missing = set(tables) ^ set(LOAD_ORDER)
    if missing:
        sys.exit(f"the generator's table set changed: {sorted(missing)}")

    ddl, loads, counts, demoted = [], [], {}, []
    for table in LOAD_ORDER:
        columns = [(r[0], mysql_type(r[1])) for r in con.execute(f'DESCRIBE "{table}"').fetchall()]
        counts[table] = con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        pk = PRIMARY_KEYS[table]
        # dsdgen declares no constraints, so the key is checked before it is trusted: a NULL or a
        # duplicate in a key column makes the PRIMARY KEY a lie and the load would fail on it
        nulls = con.execute(f'SELECT COUNT(*) FROM "{table}" WHERE '
                            + " OR ".join(f'"{c}" IS NULL' for c in pk)).fetchone()[0]
        distinct = con.execute(f'SELECT COUNT(*) FROM (SELECT DISTINCT '
                               + ", ".join(f'"{c}"' for c in pk)
                               + f' FROM "{table}")').fetchone()[0]
        keyed = nulls == 0 and distinct == counts[table]
        if not keyed and counts[table]:
            demoted.append(f"{table}: {nulls} NULL and {counts[table] - distinct} duplicate key "
                           f"rows, so ({', '.join(pk)}) is a plain index here")
        body = ",\n".join(
            f"  `{c}` {t}{' NOT NULL' if keyed and c in pk else ''}" for c, t in columns)
        key = ", ".join(f"`{c}`" for c in pk)
        ddl.append(f"CREATE TABLE `{table}` (\n{body},\n"
                   f"  {'PRIMARY KEY' if keyed else 'KEY `ix_' + table + '_pk`'} ({key})\n"
                   f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;")
        path = os.path.join(context, f"{table}.dat")
        con.execute(f"COPY \"{table}\" TO '{path}' (FORMAT csv, DELIMITER '|', HEADER false, "
                    "QUOTE '', ESCAPE '', NULLSTR '')")
        names = ", ".join(f"@{c}" for c, _ in columns)
        sets = ", ".join(f"`{c}` = NULLIF(@{c}, '')" for c, _ in columns)
        loads.append(f"LOAD DATA LOCAL INFILE '{inside}/{table}.dat' INTO TABLE `{table}`\n"
                     f"  CHARACTER SET utf8mb4 FIELDS TERMINATED BY '|' ESCAPED BY ''\n"
                     f"  ({names}) SET {sets};")

    written = 0
    for nr, text in con.execute(
            "SELECT query_nr, query FROM tpcds_queries() ORDER BY query_nr").fetchall():
        with open(os.path.join(queries_dir, f"q{nr:02d}.sql"), "w", encoding="utf-8") as fh:
            fh.write(f"-- TPC-DS query {nr}, generated at build time and not committed.\n"
                     f"-- {DISCLAIMER}\n{patch(text)};\n")
        written += 1

    secondary = []
    for table in LOAD_ORDER:
        for cols in INDEXES.get(table, []):
            name = "ix_" + table + "_" + "_".join(c.split("_", 1)[-1] for c in cols)
            keys = ", ".join(f"`{c}`" for c in cols)
            secondary.append(f"ALTER TABLE `{table}` ADD KEY `{name[:60]}` ({keys});")

    sql = f"""-- TPC-DS at scale factor {sf:g}, generated by datasets/{DATABASE}/convert.py using
-- DuckDB's tpcds extension. No TPC data is shipped or committed by this project.
--
-- {DISCLAIMER}
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{DATABASE}`;
CREATE DATABASE `{DATABASE}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
USE `{DATABASE}`;

{chr(10).join(ddl)}

-- {'-' * 60}
-- data. An empty field is NULL, not the empty string: dsdgen leaves optional foreign keys and
-- measures blank, and TPC-DS queries test them with IS NULL.

{chr(10).join(loads)}

-- {'-' * 60}
-- secondary indexes, built after the load

{chr(10).join(secondary)}

SET SESSION foreign_key_checks = 1;
"""
    open(dest, "w", encoding="utf-8").write(sql)
    print(f"  . scale factor {sf:g}: {len(LOAD_ORDER)} tables, {sum(counts.values()):,} rows")
    print("  . " + ", ".join(f"{t} {counts[t]:,}" for t in
                             sorted(counts, key=counts.get, reverse=True)[:5]) + ", ...")
    print(f"  . {written} query texts written to queries/ (generated, never committed)")
    print(f"  . {len(secondary)} secondary indexes")
    for d in demoted:
        print(f"  . {d}")


if __name__ == "__main__":
    main()
