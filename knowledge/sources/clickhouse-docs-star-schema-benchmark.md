---
type: Source
title: ClickHouse docs — Star Schema Benchmark (SSB, 2009) example dataset
description: A complete worked SSB setup (dbgen flags, table DDL, all 13 queries) used as the community reference for column types and query text.
resource: https://clickhouse.com/docs/getting-started/example-datasets/star-schema
tags: [ssb, clickhouse]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/ClickHouse/clickhouse-docs/main/docs/getting-started/example-datasets/star-schema.md
    title: star-schema.md (source of the rendered page; the clickhouse.com URL returned HTTP 530 during this session)
    accessed: "2026-09-02"
---

# What was read
The full markdown source (16 KB).

# Relevant excerpt
* Generator: `git clone https://github.com/vadimtk/ssb-dbgen.git && cd ssb-dbgen && make`; "with -s 100, 600 million rows are generated"; `./dbgen -s 1000 -T c`, `-T l`, `-T p`, `-T s`, `-T d`.
* DDL (ClickHouse types): customer (C_CUSTKEY UInt32, C_NAME, C_ADDRESS String, C_CITY/C_NATION/C_REGION LowCardinality(String), C_PHONE String, C_MKTSEGMENT); lineorder (LO_ORDERKEY UInt32, LO_LINENUMBER UInt8, LO_CUSTKEY/LO_PARTKEY/LO_SUPPKEY UInt32, LO_ORDERDATE Date, LO_ORDERPRIORITY, LO_SHIPPRIORITY UInt8, LO_QUANTITY UInt8, LO_EXTENDEDPRICE UInt32, LO_ORDTOTALPRICE UInt32, LO_DISCOUNT UInt8, LO_REVENUE UInt32, LO_SUPPLYCOST UInt32, LO_TAX UInt8, LO_COMMITDATE Date, LO_SHIPMODE); part (P_PARTKEY UInt32, P_NAME, P_MFGR, P_CATEGORY, P_BRAND, P_COLOR, P_TYPE, P_SIZE UInt8, P_CONTAINER); supplier; date (D_DATEKEY Date, D_DATE FixedString(18), D_DAYOFWEEK, D_MONTH, D_YEAR UInt16, D_YEARMONTHNUM UInt32, D_YEARMONTH FixedString(7), D_DAYNUMINWEEK/… UInt8, D_SELLINGSEASON String, four UInt8 flags). Import: `clickhouse-client --query "INSERT INTO customer FORMAT CSV" < customer.tbl`.
* Optional denormalised `lineorder_flat` (joins all dimensions).
* All 13 queries in standard SQL, e.g. Q1.1 `SELECT sum(LO_EXTENDEDPRICE * LO_DISCOUNT) AS REVENUE FROM lineorder, date WHERE LO_ORDERDATE = D_DATEKEY AND D_YEAR = 1993 AND LO_DISCOUNT BETWEEN 1 AND 3 AND LO_QUANTITY < 25;`; Q2.1 (P_CATEGORY = 'MFGR#12', S_REGION = 'AMERICA', GROUP BY D_YEAR, P_BRAND); Q3.1 (C_REGION = 'ASIA' AND S_REGION = 'ASIA', D_YEAR 1992–1997, ORDER BY D_YEAR ASC, REVENUE DESC); Q3.4 (`D_YEARMONTH = 'Dec1997'`); Q4.1 (sum(LO_REVENUE - LO_SUPPLYCOST) AS PROFIT, C_REGION/S_REGION 'AMERICA', P_MFGR IN ('MFGR#1','MFGR#2')); Q4.3 (`P_CATEGORY = 'MFGR#14'`, `S_NATION = 'UNITED STATES'`).

# What it was used to decide
[SSB dataset](/datasets/ssb.md) DDL types and query text (the 13 queries are plain SQL-92 and run unchanged on MySQL — **Inferred**, to be verified in execution).
