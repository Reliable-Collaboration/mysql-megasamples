---
type: Source
title: "MySQL Shell 9.7: Parallel Table Import Utility (util.importTable)"
description: "util.importTable(): LOAD DATA LOCAL INFILE in parallel chunks; dialects, columns/decodeColumns, threads, bytesPerChunk, skipRows, characterSet, compression, globs; requires local_infile=ON."
resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-parallel-table.html
tags:
- mysql-shell
- import
- load-data
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:41:13Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:41:13Z"
sources:
- resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-parallel-table.html
  title: "MySQL Shell 9.7: Parallel Table Import Utility (util.importTable)"
  accessed: "2026-09-02"
  version: MySQL Shell 9.7 manual, section 12.4
---

# What was read
https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-parallel-table.html, accessed 2026-09-02; version: MySQL Shell 9.7 manual, section 12.4.

# Relevant excerpt
> "The parallel table import utility uses LOAD DATA LOCAL INFILE statements to upload data, so the local_infile system variable must be set to ON on the target server." (`SET GLOBAL local_infile = 1;`)
> "The utility analyzes an input data file, distributes it into chunks, and uploads the chunks to the target MySQL server using parallel connections. The utility is capable of completing a large data import many times faster than a standard single-threaded upload using a LOAD DATA statement."
* Dialects: `default` (LF, TAB, no enclosure, `\` escape), `csv` (CRLF, `,`, `"` optionally enclosed, `\`), `csv-unix` (LF, `,`, `"` always enclosed, `\`), `tsv` (CRLF, TAB, `"` optionally enclosed, `\`), `json` (LF-separated documents, no escape). Overridable: `linesTerminatedBy`, `fieldsTerminatedBy`, `fieldsEnclosedBy`, `fieldsOptionallyEnclosed`, `fieldsEscapedBy`.
* `columns`: array of column names in file order; integers capture fields as user variables (`@1`); `decodeColumns`: dictionary assigning captured variables/expressions to target columns "in the same way as the SET clause of a LOAD DATA statement" (example `{'sum': '@1 + @2', 'power': 'POW(@1, @2)'}`).
* `threads` default max 8, actual `min{max{1, threads}, chunks}`; `bytesPerChunk` default 50M, minimum 131072 bytes, not available for multi-file lists; `maxRate` per thread; `skipRows` (applies to every file in a list); `characterSet` (default `character_set_database`; `binary` = no conversion); `replaceDuplicates` (default false); `showProgress`; `sessionInitSql` (example `["SET SESSION sql_log_bin=0;", "SET SESSION innodb_ddl_threads=8,"]`).
* Compressed `.gz`/`.zst` inputs are accepted (detected by extension) but "cannot be distributed into chunks"; parallelism then comes from uploading multiple files at once. Multiple files and `*`/`?` wildcards are supported and all land in one table.
* `maxBytesPerTransaction` and `onDuplicateKey` are not documented on this page.

# What it was used to decide
[MySQL Shell utilities](/tools/mysql-shell-utilities.md): the primary bulk loader for CSV/TSV produced by converters; `decodeColumns` replaces `LOAD DATA ... SET` transformations.
