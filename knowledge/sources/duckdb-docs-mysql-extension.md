---
type: Source
title: DuckDB documentation — MySQL extension (ATTACH a MySQL database)
description: DuckDB can attach a MySQL server and insert into its tables directly, an alternative to writing .tbl files.
resource: https://duckdb.org/docs/current/core_extensions/mysql.html
tags: [duckdb, mysql, extension]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://duckdb.org/docs/current/core_extensions/mysql.html
    title: MySQL Extension
    accessed: "2026-09-02"
---

# What was read
Installation, ATTACH, writing, settings sections.

# Relevant excerpt
* `INSTALL mysql;` (autoloads on first use; `LOAD mysql;` to force).
* `ATTACH 'host=localhost user=root port=0 database=mysql' AS mysqldb (TYPE mysql);` — connection string keys: host, port, database, user, password, socket, SSL parameters; defaults fall back to MYSQL_HOST, MYSQL_USER, MYSQL_PWD environment variables.
* Writes: `CREATE TABLE mysql_db.tbl (...)`, `INSERT INTO mysql_db.tbl VALUES (...)`, `COPY mysql_db.tbl FROM 'data.parquet'`.
* Settings: mysql_bit1_as_boolean (true), mysql_tinyint1_as_boolean (true), mysql_enable_filter_pushdown (true). Supported MySQL versions are not stated.

# What it was used to decide
Listed as the alternative load path in [DuckDB extensions tool record](/tools/duckdb-tpch-tpcds-extensions.md); the primary path stays LOAD DATA from files because bulk-insert throughput through the extension is unverified (open question there).
