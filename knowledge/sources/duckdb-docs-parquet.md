---
type: Source
title: "DuckDB documentation: Reading and Writing Parquet Files"
description: "read_parquet with globs and lists, hive partitioning auto-detect, compression codecs snappy/zstd/lz4/brotli/uncompressed, COPY ... (FORMAT parquet) options."
resource: https://duckdb.org/docs/current/data/parquet/overview
tags: [duckdb, parquet]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://duckdb.org/docs/current/data/parquet/overview
    title: "DuckDB documentation: Reading and Writing Parquet Files"
    accessed: "2026-09-02"
    version: "docs 'current' (DuckDB 1.5.5), read 2026-09-02"
---

# What was read
https://duckdb.org/docs/current/data/parquet/overview, accessed 2026-09-02; version: docs 'current' (DuckDB 1.5.5), read 2026-09-02.

# Relevant excerpt
* `SELECT * FROM read_parquet('test.parquet');`, `FROM 'test/*.parquet'`, `read_parquet(['folder1/*.parquet', 'folder2/*.parquet'])`; `hive_partitioning` auto-detected.
* Codecs shown: snappy (default), zstd, lz4/lz4_raw, brotli, uncompressed; `COPY (SELECT * FROM tbl) TO 'result-snappy.parquet' (FORMAT parquet);` with COMPRESSION, COMPRESSION_LEVEL, ROW_GROUP_SIZE, PARQUET_VERSION. Feature coverage is referenced to the Apache Parquet implementation-status page.

# What it was used to decide
[DuckDB record](/tools/duckdb.md): Parquet-distributed datasets (NYC TLC) are read directly by month with globs.
