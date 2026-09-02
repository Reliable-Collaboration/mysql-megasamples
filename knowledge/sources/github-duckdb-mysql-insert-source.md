---
type: Source
title: "duckdb/duckdb-mysql src/storage/mysql_insert.cpp (write path)"
description: "The extension inserts by generating multi-row `INSERT INTO schema.table (cols) VALUES (...), (...)` statements, flushing whenever the accumulated VALUES text reaches 8000 bytes (INSERT_FLUSH_SIZE), with a final flush in Finalize; values are cast to VARCHAR and quoted."
resource: https://raw.githubusercontent.com/duckdb/duckdb-mysql/main/src/storage/mysql_insert.cpp
tags: [duckdb, mysql, extension, source]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://raw.githubusercontent.com/duckdb/duckdb-mysql/main/src/storage/mysql_insert.cpp
    title: "duckdb/duckdb-mysql src/storage/mysql_insert.cpp (write path)"
    accessed: 2026-09-02
    version: "main branch, read 2026-09-02; repo MIT, last push 2026-08-28"
---

# What was read
https://raw.githubusercontent.com/duckdb/duckdb-mysql/main/src/storage/mysql_insert.cpp, accessed 2026-09-02; version: main branch, read 2026-09-02; repo MIT, last push 2026-08-28.

# Relevant excerpt
* `GetBaseInsertQuery()`: `query += "INSERT INTO "; ... query += " VALUES ";` with the schema, table and optional column list written through `MySQLUtils::WriteIdentifier`.
* `MySQLInsert::Sink()`: `static constexpr const idx_t INSERT_FLUSH_SIZE = 8000;` — every input chunk is cast to VARCHAR (`VectorOperations::Cast`, blobs via `MySQLCastBlob`), each row appended as `(v1, v2, ...)` (NULL as `NULL`, strings through `MySQLUtils::WriteLiteral`), and `if (gstate.insert_values.size() >= INSERT_FLUSH_SIZE) { con.Execute(gstate.base_insert_query + gstate.insert_values); gstate.insert_values = string(); }`.
* `MySQLInsert::Finalize()` executes the remaining buffered VALUES. No use of LOAD DATA anywhere in `src/storage/` (files: mysql_catalog*, mysql_connection_pool, mysql_execute_query, mysql_index*, mysql_insert, mysql_optimizer, mysql_schema*, mysql_table*, mysql_transaction).

# What it was used to decide
[DuckDB record](/tools/duckdb.md): quantifies why the extension is not a bulk loader — roughly 8 KB of SQL text per round trip, one statement per ~8 KB, versus LOAD DATA's 50 MB chunks in util.importTable.
