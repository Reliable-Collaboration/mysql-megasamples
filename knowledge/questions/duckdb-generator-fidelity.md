---
type: Open Question
title: Do DuckDB's dbgen/dsdgen ports produce byte-identical rows to the C tools, and how fast is ATTACH-mysql insert versus LOAD DATA?
description: The chosen generator path relies on DuckDB's ports; identity with the reference C output and the NULL/DECIMAL/CHAR export behaviour are unverified.
resource: /questions/duckdb-generator-fidelity.md
tags: [question, duckdb, tpc-h, tpc-ds]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://github.com/duckdb/duckdb/tree/main/extension/tpch
    accessed: "2026-09-02"
  - resource: https://duckdb.org/docs/current/core_extensions/mysql.html
    accessed: "2026-09-02"
---

# Question
1. Are `COPY … (DELIMITER '|', HEADER false)` exports of `dbgen(sf=1)` identical (after stripping the trailing pipe) to tpch-kit `dbgen -s 1` `.tbl` files? Same for `dsdgen(sf=1)` vs tpcds-kit `dsdgen -SCALE 1 -TERMINATE N`.
2. How does DuckDB render NULL (`NULLSTR` default), DECIMAL(15,2) (trailing zeros), and does it quote any TPC-H/TPC-DS string (`|` or `"` inside values)?
3. Is `INSERT INTO m.lineitem SELECT * FROM lineitem` through the mysql extension competitive with `LOAD DATA LOCAL INFILE` for 6 M rows?

# Cheapest experiment
In the loader image: generate SF 0.01 and SF 1 both ways; `sort | cmp` per table; `grep -c '"'` on exports; time both load paths for lineitem at SF 1 into the `mysql-build` service; run Q1–Q22 / Q1–Q99 and compare with `tpch_answers()`/`tpcds_answers()`. Record results in [TPC-H](/datasets/tpc-h.md) and [TPC-DS](/datasets/tpc-ds.md) "Tests and expected values".

# Resolves
[tpch-generator-path](/decisions/tpch-generator-path.md) and [tpcds-generator-path](/decisions/tpcds-generator-path.md) (pending → accepted or superseded).

# Related
Item 3 overlaps [duckdb-mysql-write-throughput](/questions/duckdb-mysql-write-throughput.md) (another agent's record); run that experiment once and reuse its numbers here.
