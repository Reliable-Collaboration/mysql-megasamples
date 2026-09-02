---
type: Source
title: "DuckDB documentation: SQLite Extension"
description: "ATTACH 'file.db' (TYPE sqlite); type affinity mapping (integers→BIGINT, text→VARCHAR, blob/unspecified→BLOB), sqlite_all_varchar override; read/write; single writer."
resource: https://duckdb.org/docs/current/core_extensions/sqlite
tags: [duckdb, sqlite, extension]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://duckdb.org/docs/current/core_extensions/sqlite
    title: "DuckDB documentation: SQLite Extension"
    accessed: "2026-09-02"
    version: "docs 'current' (DuckDB 1.5.5), read 2026-09-02"
---

# What was read
https://duckdb.org/docs/current/core_extensions/sqlite, accessed 2026-09-02; version: docs 'current' (DuckDB 1.5.5), read 2026-09-02.

# Relevant excerpt
* `INSTALL sqlite; LOAD sqlite;`; `ATTACH 'sakila.db' (TYPE sqlite); USE sakila;`; the CLI can open a SQLite file directly (`duckdb sakila.db`).
* Types follow "SQLite's type affinity rules with a few extensions": integer affinity → BIGINT, text → VARCHAR, blob/unspecified → BLOB; `SET GLOBAL sqlite_all_varchar = true;` forces VARCHAR when values do not match the declared affinity.
* Read/write support (SELECT, INSERT, UPDATE, DELETE, CREATE TABLE, ALTER TABLE, COPY, transactions); "Only a single thread or process can write to the database at one time."

# What it was used to decide
[DuckDB record](/tools/duckdb.md): SQLite-distributed datasets (Chinook, Northwind-SQLite ports) are read with this extension; `sqlite_all_varchar` plus explicit casts handles SQLite's untyped columns.
