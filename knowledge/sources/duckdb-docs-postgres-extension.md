---
type: Source
title: "DuckDB documentation: PostgreSQL Extension"
description: "ATTACH TYPE postgres / READ_ONLY / SCHEMA; COPY to and from PostgreSQL uses the binary wire encoding; COPY FROM DATABASE; settings pg_use_binary_copy, pg_pages_per_task, pg_use_ctid_scan, pg_array_as_varchar."
resource: https://duckdb.org/docs/current/core_extensions/postgres/overview
tags: [duckdb, postgresql, extension]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://duckdb.org/docs/current/core_extensions/postgres/overview
    title: "DuckDB documentation: PostgreSQL Extension"
    accessed: 2026-09-02
    version: "docs 'current' (DuckDB 1.5.5), read 2026-09-02"
---

# What was read
https://duckdb.org/docs/current/core_extensions/postgres/overview, accessed 2026-09-02; version: docs 'current' (DuckDB 1.5.5), read 2026-09-02.

# Relevant excerpt
* `ATTACH 'dbname=postgres user=postgres host=127.0.0.1' AS db (TYPE postgres, READ_ONLY);` / `(TYPE postgres, SCHEMA 'public')`.
* `COPY postgres_db.tbl TO 'data.parquet'; COPY postgres_db.tbl FROM 'data.parquet';` — "These copies use PostgreSQL binary wire encoding."; `COPY 'data.parquet' TO 'pg.bin' WITH (FORMAT postgres_binary);`; `COPY FROM DATABASE postgres_db TO my_duckdb_db;`.
* Settings: `pg_use_binary_copy` "Whether or not to use BINARY copy to read data"; `pg_use_ctid_scan` "Whether or not to parallelize scanning using table ctids"; `pg_pages_per_task`; `pg_array_as_varchar`.

# What it was used to decide
[DuckDB record](/tools/duckdb.md): if a dataset is only available as a PostgreSQL dump, DuckDB reads it from a throwaway PostgreSQL container with binary COPY and writes CSV for MySQL; contrasts with the MySQL extension, whose write path is plain INSERT.
