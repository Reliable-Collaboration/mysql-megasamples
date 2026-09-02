---
type: Source
title: eyalroz/ssb-dbgen (unified, CMake-built Star Schema Benchmark data generator)
description: Read README, CMakeLists.txt options, doc/ssb.ddl, doc/ssb.ri, src/driver.c header, repository listing and metadata; no LICENSE file exists.
resource: https://github.com/eyalroz/ssb-dbgen
tags: [ssb, dbgen, github]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/eyalroz/ssb-dbgen/master/README.md
    title: README.md
    accessed: 2026-09-02
    version: master @ ae1e254aa4d603d8ef1f44078e5abed011634b23 (2025-04-26, latest commit); GitHub license null; no tags; 38 stars
  - resource: https://raw.githubusercontent.com/eyalroz/ssb-dbgen/master/CMakeLists.txt
    title: CMakeLists.txt
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/eyalroz/ssb-dbgen/master/doc/ssb.ddl
    title: doc/ssb.ddl (+ doc/ssb.ri)
    accessed: 2026-09-02
---

# What was read
Root: .gitignore, .travis.yml, CMakeLists.txt, README.md, dists.dss, doc/ (TPCH_BUGS, TPCH_CHANGES, TPCH_HISTORY, TPCH_PORTING_NOTES, TPCH_README, ssb.ddl, ssb.ri, tpch.ddl, tpch.ri), src/ (bm_utils.c, build.c, config.h.in, driver.c, dss.h, dsstypes.h, load_stub.c, permute.c, print.c, qgen.c, rnd.c, shared.h, speed_seed.c, text.c, tpcd.h, varsub.c ...). **No LICENSE, EULA or COPYING file**; src/driver.c header is "/* @(#)driver.c 2.1.8.4 */ /* main driver for dss benchmark */" with no license text; doc/TPCH_README has no license lines.

# Relevant excerpt
* README: "The ssb-dbgen utility is based on the TPC-H benchmark's data generation utility, also named dbgen ... the original code of its own dbgen was forked from an older, now out-of-date version of TPC-H dbgen"; "This effort is an attempt to unify all of those disparate repositories"; build "cmake -B ./build && cmake --build ./build"; options table: DATABASE (INFORMIX, DB2, TDAT, SQLSERVER, SYBASE; default DB2; affects qgen only), **EOL_HANDLING** (ON omits the separator after the last column; default OFF → trailing pipe), CSV_OUTPUT_FORMAT (default OFF), WORKLOAD (SSB/TPCH, default SSB), **YMD_DASH_DATE** (ON → YYYY-MM-DD, default OFF → YYYYMMDD). Invocation "dbgen -b /path/to/dists.dss -v -s 10 ... will have, for example, 300,000 lines in customer.tbl" (so 30,000 at SF=1) with sample rows `1|Customer#000000001|j5JsirBM9P|MOROCCO  0|MOROCCO|AFRICA|25-989-741-2988|BUILDING|`. Differences from TPC-H: NATION/REGION removed, PARTSUPP removed, ORDERS denormalised into LINEORDER, DATE added, "refreshing is only applied to LINEORDER".
* doc/ssb.ddl: `part (p_partkey INTEGER NOT NULL, p_name VARCHAR(22), p_mfgr VARCHAR(6), p_category VARCHAR(7), p_brand1 VARCHAR(9), p_color VARCHAR(11), p_type VARCHAR(25), p_size INTEGER, p_container VARCHAR(10))`; `supplier (s_suppkey, s_name VARCHAR(25), s_address VARCHAR(25), s_city VARCHAR(10), s_nation VARCHAR(15), s_region VARCHAR(12), s_phone VARCHAR(15))`; `customer (c_custkey, c_name VARCHAR(25), c_address VARCHAR(25), c_city VARCHAR(10), c_nation VARCHAR(15), c_region VARCHAR(12), c_phone VARCHAR(15), c_mktsegment VARCHAR(10))`; `date (d_datekey INTEGER, d_date VARCHAR(19), d_dayofweek VARCHAR(10), d_month VARCHAR(10), d_year INTEGER, d_yearmonthnum INTEGER, d_yearmonth VARCHAR(8), d_daynuminweek, d_daynuminmonth, d_daynuminyear, d_monthnuminyear, d_weeknuminyear INTEGER, d_sellingseason VARCHAR(13), d_lastdayinweekfl, d_lastdayinmonthfl, d_holidayfl, d_weekdayfl VARCHAR(1))`; `lineorder (lo_orderkey, lo_linenumber, lo_custkey, lo_partkey, lo_suppkey, lo_orderdate INTEGER, lo_orderpriority VARCHAR(15), lo_shippriority VARCHAR(1), lo_quantity, lo_extendedprice, lo_ordertotalprice, lo_discount, lo_revenue, lo_supplycost, lo_tax, lo_commitdate INTEGER, lo_shipmode VARCHAR(10))` — all NOT NULL except p_mfgr.
* doc/ssb.ri: PKs on date_(d_datekey), supplier, customer, part, and `lineorder ADD PRIMARY KEY (lo_orderkey)` (**inconsistent with the paper's compound key and with the DDL's table name `date`** — the RI file says `date_`); FKs lo_orderdate/lo_commitdate → date_, lo_suppkey, lo_custkey, lo_partkey.

# What it was used to decide
[ssb-dbgen tool record](/tools/ssb-dbgen.md); [SSB dataset](/datasets/ssb.md); [SSB generator decision](/decisions/ssb-generator-path.md).
