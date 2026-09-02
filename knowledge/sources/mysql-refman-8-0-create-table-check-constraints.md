---
type: Source
title: "MySQL 8.0 Reference Manual: CHECK Constraints (8.0.16 history)"
description: "Before 8.0.16 CHECK constraints were parsed and ignored; from 8.0.16 they are enforced for all storage engines."
resource: https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html
tags: [mysql, docs, constraints, history]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html
    title: "MySQL 8.0 Reference Manual: CHECK Constraints (8.0.16 history)"
    accessed: "2026-09-02"
    version: "MySQL 8.0 manual, section 15.1.20.6"
---

# What was read
https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html, accessed 2026-09-02; version: MySQL 8.0 manual, section 15.1.20.6.

# Relevant excerpt
> "Prior to MySQL 8.0.16, CREATE TABLE permits only the following limited version of table CHECK constraint syntax, which is parsed and ignored: CHECK (expr)"
> "As of MySQL 8.0.16, CREATE TABLE permits the core features of table and column CHECK constraints, for all storage engines."

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): any third-party MySQL port of a sample database written for 5.x/8.0.15 may carry CHECK clauses that were silently ignored then and are enforced now; loads that fail on such constraints are a known upstream-script hazard.
