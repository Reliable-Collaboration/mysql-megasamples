---
type: Source
title: "DuckDB documentation: CSV Import (data/csv/overview)"
description: read_csv with sniffer auto-detection and the parameter table (delim, quote, escape, header, nullstr, encoding utf-8/utf-16/latin-1, dateformat, timestampformat, columns/types, sample_size 20480, ignore_errors, store_rejects, all_varchar, compression auto, strict_mode, max_line_size).
resource: https://duckdb.org/docs/current/data/csv/overview
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
- resource: https://duckdb.org/docs/current/data/csv/overview
  title: "DuckDB documentation: CSV Import (data/csv/overview)"
  accessed: "2026-09-02"
  version: docs 'current' (DuckDB 1.5.5), read 2026-09-02
---

# What was read
https://duckdb.org/docs/current/data/csv/overview, accessed 2026-09-02; version: docs 'current' (DuckDB 1.5.5), read 2026-09-02.

# Relevant excerpt
> "The DuckDB CSV reader can automatically infer which configuration flags to use by analyzing the CSV file using the CSV sniffer." (`auto_detect` default true).
* Parameters and defaults: `delim`/`sep` `,` (up to 4 bytes); `quote` `"`; `escape` `"`; `header` false (auto-detected); `nullstr`/`null` empty (may be a list); `encoding` utf-8 (UTF-8, UTF-16, Latin-1 supported); `dateformat`/`timestampformat` empty; `columns` (struct of name→type) and `types`/`dtypes` (by position or name); `sample_size` 20480; `skip` 0; `compression` auto (none, gzip, zstd — "detected automatically from the file extension (e.g., t.csv.gz will use gzip)"); `ignore_errors` false; `store_rejects` false; `all_varchar` false; `strict_mode` true; `max_line_size` 2000000.

# What it was used to decide
[DuckDB record](/tools/duckdb.md): converters read upstream CSV with explicit `columns=`/`types=` after inspecting `sniff_csv`, `encoding='latin-1'` for legacy files, and `store_rejects=true` to log bad rows into the dataset record.
