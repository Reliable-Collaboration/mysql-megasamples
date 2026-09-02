---
type: Source
title: "MySQL 9.7 Reference Manual: CREATE TABLE and Generated Columns"
description: Generated column syntax, VIRTUAL default, expression restrictions, DEFAULT-only assignment, indexability.
resource: https://dev.mysql.com/doc/refman/9.7/en/create-table-generated-columns.html
tags:
- mysql
- docs
- generated-columns
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/create-table-generated-columns.html
  title: "MySQL 9.7 Reference Manual: CREATE TABLE and Generated Columns"
  accessed: "2026-09-02"
  version: MySQL 9.7 manual, section 15.1.25.8
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/create-table-generated-columns.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 15.1.25.8.

# Relevant excerpt
* Syntax `col_name data_type [GENERATED ALWAYS] AS (expr) [VIRTUAL | STORED] [NOT NULL | NULL] [UNIQUE [KEY]] [[PRIMARY] KEY] [COMMENT 'string']`; default VIRTUAL.
* Permitted: literals, deterministic built-in functions and operators, earlier-defined generated columns, any base column. Not permitted: stored/loadable functions, stored program parameters, variables, subqueries, AUTO_INCREMENT on the generated column or as a base column.
* For INSERT/REPLACE/UPDATE "the only permitted value is DEFAULT" (or omit the column).
* STORED generated columns can be indexed including PRIMARY KEY; VIRTUAL generated columns support secondary indexes only (InnoDB).

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): SQL Server computed columns and Oracle virtual columns port to generated columns only when the expression is deterministic and uses functions MySQL has; the loader column list must omit generated columns.
