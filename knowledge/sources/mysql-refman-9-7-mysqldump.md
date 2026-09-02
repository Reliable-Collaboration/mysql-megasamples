---
type: Source
title: "MySQL 9.7 Reference Manual: mysqldump"
description: "mysqldump options that matter for exports and re-imports, its utf8mb4 default, and the manual's pointer to MySQL Shell dump utilities."
resource: https://dev.mysql.com/doc/refman/9.7/en/mysqldump.html
tags: [mysql, docs, mysqldump]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/mysqldump.html
    title: "MySQL 9.7 Reference Manual: mysqldump"
    accessed: "2026-09-02"
    version: "MySQL 9.7 manual, section 6.5.4"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/mysqldump.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 6.5.4.

# Relevant excerpt
* "The mysqldump client utility performs logical backups, producing a set of SQL statements that can be executed to reproduce the original database object definitions and table data."
* `--default-character-set` default `utf8mb4`; `--single-transaction`; `--set-gtid-purged` (OFF/ON/AUTO/COMMENTED, default AUTO); `--tab=path` writes a `.sql` DDL file and a `.txt` tab-separated data file per table and requires `secure_file_priv` plus the FILE privilege; `--fields-terminated-by` etc. have the same meaning as LOAD DATA clauses; `--no-data`; `--hex-blob` (BINARY, VARBINARY, BLOB, BIT and spatial columns as hex); `--routines`, `--triggers`, `--events`; `--extended-insert` on by default via `--opt`; `--column-statistics`.
* Tip on the page: "Consider using the MySQL Shell dump utilities, which provide parallel dumping with multiple threads, file compression, and progress information display ..."

# What it was used to decide
[LOAD DATA tool record](/tools/load-data-infile.md): mysqldump `--tab` is the fallback exporter; `--hex-blob` is required whenever binary or spatial columns are round-tripped through SQL text.
