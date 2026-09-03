---
type: Source
title: "DuckDB documentation: CSV Auto Detection and sniff_csv"
description: The sniffer detects dialect, header and types from 20,480 sample rows; sniff_csv returns Delimiter, Quote, Escape, NewLineDelimiter, HasHeader, Columns, DateFormat, TimestampFormat and a Prompt; sample_size = -1 reads the whole file.
resource: https://duckdb.org/docs/current/data/csv/auto_detection
tags:
- duckdb
- csv
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:41:13Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:41:13Z"
sources:
- resource: https://duckdb.org/docs/current/data/csv/auto_detection
  title: "DuckDB documentation: CSV Auto Detection and sniff_csv"
  accessed: "2026-09-02"
  version: docs 'current' (DuckDB 1.5.5), read 2026-09-02
---

# What was read
https://duckdb.org/docs/current/data/csv/auto_detection, accessed 2026-09-02; version: docs 'current' (DuckDB 1.5.5), read 2026-09-02.

# Relevant excerpt
> "CSV files are not self-describing and come in many different dialects." The sniffer detects the dialect (delimiter, quoting rule, escape), column types and header presence.
* `FROM sniff_csv('my_file.csv');` / `FROM sniff_csv('my_file.csv', sample_size = 1000);` returns Delimiter, Quote, Escape, NewLineDelimiter, HasHeader, Columns (with types), DateFormat, TimestampFormat and a ready-to-use Prompt.
* Default sample 20,480 rows; `sample_size = -1` reads the entire file; individual options override detection (`read_csv('file.csv', delim = '|')`); candidate types are NULL, BOOLEAN, temporal, numeric, VARCHAR fallback; ISO 8601 preferred for dates.

# What it was used to decide
[DuckDB record](/tools/duckdb.md): every CSV-sourced dataset record stores the `sniff_csv(..., sample_size = -1)` Prompt as the reproducible reader definition.
