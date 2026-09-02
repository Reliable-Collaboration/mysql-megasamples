---
type: Source
title: DuckDB MySQL extension documentation
description: What the DuckDB docs state about attaching to MySQL and writing into it; notably they do not describe the bulk-insert mechanism.
resource: https://duckdb.org/docs/stable/core_extensions/mysql
tags: [duckdb, mysql, tool]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://duckdb.org/docs/current/core_extensions/mysql.html
    title: MySQL Extension - DuckDB documentation
    accessed: 2026-09-02
    version: docs "current" channel; the page did not print a version number
stale_after: 2027-03-01
---

# What was read
`https://duckdb.org/docs/current/core_extensions/mysql.html`, read twice on 2026-09-02. `curl` against `https://duckdb.org/docs/stable/core_extensions/mysql` and `.../mysql.html` returns only a 50-byte client-side redirect stub, so the page was read through WebFetch.

# Relevant excerpt

**Install / load**
```sql
INSTALL mysql;
LOAD mysql;
```

**Attach**
```sql
ATTACH 'host=localhost user=root port=0 database=mysql' AS mysqldb (TYPE mysql);
```
Connection-string keys with defaults and environment fallbacks: `database` (NULL / `MYSQL_DATABASE`), `host` (localhost / `MYSQL_HOST`), `password` (empty / `MYSQL_PWD`), `port` (0 / `MYSQL_TCP_PORT`), `socket` (NULL / `MYSQL_UNIX_PORT`), `user` (current user / `MYSQL_USER`), `ssl_mode` (preferred).

**Reading**
> "The tables in the MySQL database can be read as if they were normal DuckDB tables, but the underlying data is read directly from MySQL at query time."

**Writing**
> "In addition to reading data from MySQL, create tables, ingest data into MySQL and make other modifications to a MySQL database using standard SQL queries."
```sql
CREATE TABLE mysql_db.tbl (id INTEGER, name VARCHAR);
INSERT INTO mysql_db.tbl VALUES (42, 'DuckDB');
COPY mysql_db.tbl FROM 'data.parquet';
UPDATE mysql_db.tbl SET name = 'value' WHERE id = 42;
DELETE FROM mysql_db.tbl WHERE id = 42;
```
> "Note that if modifications are not desired, `ATTACH` can be run with the `READ_ONLY` property which prevents making modifications to the underlying database."

**Transactions** - `BEGIN; INSERT ...; ROLLBACK;` is supported, but: "The DDL statements are not transactional in MySQL."

**Schema cache**
> "To avoid having to continuously fetch schema data from MySQL, DuckDB keeps schema information cached. If changes are made to the schema through a different connection to the MySQL instance, such as new columns being added to a table, the cached schema information might be outdated. In this case, the function `mysql_clear_cache` can be executed to clear the internal caches."

**Settings** named on the page: `mysql_bit1_as_boolean` (default true), `mysql_tinyint1_as_boolean` (default true), `mysql_debug_show_queries` (default false), a filter-pushdown toggle (reported as `mysql_enable_filter_pushdown` in one reading and `mysql_experimental_filter_pushdown` in another - **the exact current name was not pinned**), and `mysql_pool_size` (derived from CPU count). The settings table has roughly 14 rows.

**Not present on the page:** any "Limitations" section, any statement of how rows are physically transmitted on write (batched multi-row `INSERT` vs `LOAD DATA LOCAL INFILE`), any throughput figure, and any explicit DuckDB version number.

# What it was used to decide
[DuckDB](/tools/duckdb.md) and [the large-tabular conversion path decision](/decisions/large-tabular-conversion-path.md); the unspecified write mechanism is [an open question](/questions/duckdb-mysql-write-throughput.md).
