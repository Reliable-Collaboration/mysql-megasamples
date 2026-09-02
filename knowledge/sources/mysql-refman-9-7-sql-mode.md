---
type: Source
title: "MySQL 9.7 Reference Manual: Server SQL Modes"
description: "Default sql_mode, strict mode and LOAD DATA, ANSI_QUOTES, PIPES_AS_CONCAT, NO_BACKSLASH_ESCAPES."
resource: https://dev.mysql.com/doc/refman/9.7/en/sql-mode.html
tags: [mysql, docs, sql-mode]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/sql-mode.html
    title: "MySQL 9.7 Reference Manual: Server SQL Modes"
    accessed: 2026-09-02
    version: "MySQL 9.7 manual, section 7.1.11"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/sql-mode.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 7.1.11.

# Relevant excerpt
* Default SQL mode: ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_ENGINE_SUBSTITUTION.
* Strict mode applies to LOAD DATA and LOAD XML; within these statements rows that duplicate an existing row on a unique key are discarded with IGNORE.
* ANSI_QUOTES: treat `"` as an identifier quote (like backtick), so double-quoted literals are no longer strings. PIPES_AS_CONCAT: `||` is string concatenation. NO_BACKSLASH_ESCAPES: backslash is an ordinary character in strings and identifiers.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): converted DDL/SQL is written for the default mode (backtick identifiers, single-quoted strings, backslash escapes); ported T-SQL/PL-SQL views that rely on `||` or double-quoted identifiers are rewritten rather than served by changing sql_mode.
