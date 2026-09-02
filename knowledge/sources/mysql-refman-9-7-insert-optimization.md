---
type: Source
title: "MySQL 9.7 Reference Manual: Optimizing INSERT Statements"
description: "LOAD DATA is usually 20 times faster than INSERT; multi-row INSERT; bulk_insert_buffer_size applies to nonempty tables (MyISAM context)."
resource: https://dev.mysql.com/doc/refman/9.7/en/insert-optimization.html
tags: [mysql, docs, performance]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/insert-optimization.html
    title: "MySQL 9.7 Reference Manual: Optimizing INSERT Statements"
    accessed: 2026-09-02
    version: "MySQL 9.7 manual, section 10.2.5.1"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/insert-optimization.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 10.2.5.1.

# Relevant excerpt
* "When loading a table from a text file, use LOAD DATA. This is usually 20 times faster than using INSERT statements."
* "If you are inserting many rows from the same client at the same time, use INSERT statements with multiple VALUES lists to insert several rows at a time. This is considerably faster (many times faster in some cases) than using separate single-row INSERT statements."
* "If you are adding data to a nonempty table, you can tune the bulk_insert_buffer_size variable to make data insertion even faster." (links to the InnoDB and MyISAM bulk-loading sections).

# What it was used to decide
[LOAD DATA tool record](/tools/load-data-infile.md): justification for converting every dataset to LOAD DATA input instead of INSERT scripts; [DuckDB record](/tools/duckdb.md): why the DuckDB MySQL extension's INSERT path is not the bulk loader.
