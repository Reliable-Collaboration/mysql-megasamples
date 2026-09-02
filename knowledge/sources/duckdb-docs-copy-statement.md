---
type: Source
title: DuckDB documentation — COPY statement (CSV export options)
description: Options for writing DuckDB tables to delimited files that MySQL LOAD DATA can read.
resource: https://duckdb.org/docs/current/sql/statements/copy.html
tags:
- duckdb
- csv
- export
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://duckdb.org/docs/current/sql/statements/copy.html
  title: COPY Statement
  accessed: "2026-09-02"
---

# What was read
The COPY ... TO section and the CSV option table.

# Relevant excerpt
* Form: `COPY lineitem TO 'lineitem.csv' (FORMAT csv, DELIMITER '|', HEADER false);`
* Defaults: DELIMITER `,`; HEADER `true`; QUOTE `"`. PREFIX/SUFFIX options require HEADER false.

# What it was used to decide
Export path from DuckDB-generated tables to pipe-delimited files in [DuckDB extensions tool record](/tools/duckdb-tpch-tpcds-extensions.md).
