---
type: Open Question
title: How does DuckDB's MySQL extension physically write rows, and is it fast enough to skip CSV?
description: The docs never say whether writes are batched INSERTs or LOAD DATA; this decides whether the loader needs a CSV intermediate at all.
resource: /questions/duckdb-mysql-write-throughput.md
tags:
- duckdb
- mysql
- performance
status: draft
trust: open
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://duckdb.org/docs/current/core_extensions/mysql.html
  title: MySQL Extension - DuckDB documentation
  accessed: "2026-09-02"
---

# Question
The DuckDB MySQL extension page documents `CREATE TABLE`, `INSERT INTO` and `COPY ... FROM` against an attached MySQL database, but says nothing about how rows reach the server: batched multi-row `INSERT` statements, prepared-statement batches, or `LOAD DATA LOCAL INFILE`. It also has no limitations section and quotes no throughput figures.

This matters because the plan's conversion path for the large tabular datasets is Parquet/CSV -> DuckDB -> **CSV** -> `LOAD DATA LOCAL INFILE`. If the extension already uses `LOAD DATA` internally, the CSV intermediate and its disk cost can be dropped and the pipeline becomes a single `CREATE TABLE mysqldb.trips AS SELECT ... FROM read_parquet(...)`.

# Cheapest experiment
On the builder, with a throwaway MySQL 9.7 container:

```sql
SET GLOBAL general_log = 'ON';           -- on the MySQL side
-- in duckdb:
INSTALL mysql; LOAD mysql;
SET mysql_debug_show_queries = true;
ATTACH 'host=127.0.0.1 user=root password=... database=t' AS m (TYPE mysql);
CREATE TABLE m.probe AS SELECT * FROM read_parquet('green_tripdata_2025-01.parquet');
```

Then read the general log: it shows verbatim whether the server received `INSERT INTO ... VALUES (...),(...)` batches or a `LOAD DATA LOCAL INFILE`. Time the same 48,326-row load both ways (extension vs `COPY TO` CSV + `LOAD DATA`) and compare. Cost: a few minutes on a machine that already builds the image; `mysql_debug_show_queries` makes it self-documenting.

# Provisional answer used by the plan
**Inferred:** treat the extension as row-protocol `INSERT`s and keep the CSV + `LOAD DATA` path for anything over ~1 million rows; use the extension directly for dimension tables (265 taxi zones, 434 IUCR codes, ~19k airports).

# Resolves
Records that depend on the answer:
* [large-tabular-conversion-path.md](/decisions/large-tabular-conversion-path.md)
* [duckdb-generator-fidelity.md](/questions/duckdb-generator-fidelity.md)
* [duckdb-mysql-extension-docs.md](/sources/duckdb-mysql-extension-docs.md)
* [duckdb.md](/tools/duckdb.md)
