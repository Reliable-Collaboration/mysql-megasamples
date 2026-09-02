---
type: Source
title: "MySQL 9.7 Reference Manual: Invisible Columns"
description: "INVISIBLE columns are hidden from SELECT * but loadable by name; a table needs at least one visible column; mysqldump includes them."
resource: https://dev.mysql.com/doc/refman/9.7/en/invisible-columns.html
tags: [mysql, docs, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/invisible-columns.html
    title: "MySQL 9.7 Reference Manual: Invisible Columns"
    accessed: "2026-09-02"
    version: "MySQL 9.7 manual, section 15.1.25.10"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/invisible-columns.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 15.1.25.10.

# Relevant excerpt
* `CREATE TABLE t1 (i INT, j DATE INVISIBLE)`; `ALTER TABLE t1 ALTER COLUMN j SET VISIBLE;`; "A table must have at least one visible column."
* INSERT without naming an invisible column gives it its implicit default; `SELECT *` omits it unless named explicitly.
* mysqldump includes invisible columns in dumped definitions and data.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): used for the surrogate `my_row_id`-style keys that MySQL Shell's `createInvisiblePKs` adds to PK-less tables, and as the mechanism for provenance columns (`_source_row`) that must not disturb `SELECT *` demos.
