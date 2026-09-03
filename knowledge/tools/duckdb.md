---
type: Tool
title: DuckDB (Parquet/CSV reader and MySQL writer)
description: Single-binary analytical engine used to read TLC Parquet and the bike/BTS CSVs, reshape them, and emit MySQL-ready CSV; its MySQL extension can also write straight into MySQL.
resource: https://duckdb.org/docs/stable/core_extensions/mysql
tags:
- tool
- duckdb
- parquet
- etl
status: draft
trust: inferred
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://duckdb.org/docs/current/core_extensions/mysql.html
  title: MySQL Extension - DuckDB documentation
  accessed: "2026-09-02"
- resource: /sources/duckdb-mysql-extension-docs.md
  title: What the MySQL extension docs actually say
  accessed: "2026-09-02"
- resource: /sources/nyc-tlc-parquet-footer-inspection.md
  title: Parquet files DuckDB would have to read
  accessed: "2026-09-02"
stale_after: "2027-03-01"
---

# Facts
A single-binary in-process OLAP engine that reads Parquet, CSV and zipped CSV natively and can `ATTACH` a MySQL database through a first-party extension. For this group of datasets it is the only tool that reads the TLC Parquet files without standing up Spark or a Python data stack.

**Verified from the documentation** (see [the source record](/sources/duckdb-mysql-extension-docs.md)):
* `INSTALL mysql; LOAD mysql;` then `ATTACH 'host=... user=... port=0 database=...' AS mysqldb (TYPE mysql);`, with `READ_ONLY` available to prevent writes.
* Writes are ordinary SQL: `CREATE TABLE mysqldb.tbl (...)`, `INSERT INTO mysqldb.tbl SELECT ...`, `COPY mysqldb.tbl FROM 'data.parquet'`, `UPDATE`, `DELETE`.
* Reads go to MySQL at query time (no local copy).
* Settings named on the page: `mysql_bit1_as_boolean` (true), `mysql_tinyint1_as_boolean` (true), `mysql_debug_show_queries` (false), a filter-pushdown toggle, `mysql_pool_size`.
* "The DDL statements are not transactional in MySQL." `mysql_clear_cache()` refreshes cached schema metadata.

**Not stated anywhere on that page:** whether writes are sent as batched multi-row `INSERT`s or via `LOAD DATA LOCAL INFILE`; any throughput number; any limitations section; the DuckDB version the page documents. See [the open question](/questions/duckdb-mysql-write-throughput.md).

## Why it matters here
* **NYC TLC:** the source is Parquet with `TIMESTAMP_MICROS`, and the yearly type drift (`passenger_count` INT64 vs DOUBLE, `airport_fee` vs `Airport_fee`) is exactly what `read_parquet([...], union_by_name := true)` plus explicit casts is for. `COPY (SELECT ...) TO 'x.csv' (FORMAT CSV, HEADER)` then feeds `LOAD DATA`.
* **Citi Bike / Divvy / BTS:** `read_csv` with an explicit `columns` map handles the quoted/unquoted era differences, the `"0659"` HHMM strings and the BTS trailing comma without a bespoke parser.

## Verified behaviour
Nothing about DuckDB's runtime behaviour was executed in this session. **This machine has no `duckdb` binary and no `duckdb`, `pyarrow` or `pandas` Python module** (checked 2026-09-02: `which duckdb` -> not found; `import duckdb` / `import pyarrow` / `import pandas` -> `ModuleNotFoundError`). Everything below is **Inferred:** and must be confirmed by the executor.

* **Inferred:** for multi-hundred-million-row loads, `INSERT ... SELECT` across the MySQL extension will be slower than writing CSV and using `LOAD DATA LOCAL INFILE`, because the latter is MySQL's documented bulk path and avoids per-row protocol overhead. The plan therefore uses DuckDB as a **reader/reshaper emitting CSV**, not as the writer, and treats the MySQL extension as a convenience for small dimension tables (taxi zones, IUCR codes, `L_AIRPORT`).
* **Inferred:** DuckDB's `TIMESTAMP` maps cleanly to MySQL `DATETIME(6)`; the TLC values are local wall-clock (`isAdjustedToUTC=false`), so no timezone conversion must be applied.
* **Inferred:** memory use is bounded by row-group size; the TLC yellow files have 1-4 row groups and the HVFHV file 22, so a `--memory-limit` will be needed on small builders for the 537 MB HVFHV file.

# Limits
* The MySQL extension's write path (INSERT batching versus LOAD DATA) is undocumented; throughput for multi-million-row tables is an [open question](/questions/duckdb-mysql-write-throughput.md), so the plan keeps a CSV intermediate and `util.importTable` for large tables.
* No SSB generator; the `tpch`/`tpcds` generators embed TPC code under the TPC EULA ([record](/tools/duckdb-tpch-tpcds-extensions.md)).
* Extension binaries are fetched at `INSTALL` time and must be pinned to the DuckDB release in `uv.lock`.

# Alternatives considered
* **pyarrow / pandas** - would work for Parquet but adds a Python dependency chain to the loader image and needs hand-written type-drift handling. No pyarrow record is written in this bundle because nothing about pyarrow was verified in this session; if the executor chooses it, create `tools/pyarrow.md` then.
* **MySQL Shell `util.importTable`** - the right tool for the final CSV -> MySQL step (parallel, `LOAD DATA`-based); covered by whoever owns `tools/mysql-shell-utilities.md`.

# Version to pin
Unpinned. The loader image must install a specific DuckDB release and record it; the `mysql` extension version is tied to the DuckDB version and is fetched at `INSTALL` time from the extension repository, which is a **network dependency at build time** to note in the build design.
