---
type: Source
title: "MySQL 9.7 Reference Manual: CHECK Constraints"
description: CHECK syntax, disallowed expressions, ENFORCED/NOT ENFORCED, and behaviour under LOAD DATA ... IGNORE.
resource: https://dev.mysql.com/doc/refman/9.7/en/create-table-check-constraints.html
tags:
- mysql
- docs
- constraints
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/create-table-check-constraints.html
  title: "MySQL 9.7 Reference Manual: CHECK Constraints"
  accessed: "2026-09-02"
  version: MySQL 9.7 manual, section 15.1.25.6
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/create-table-check-constraints.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 15.1.25.6.

# Relevant excerpt
* Syntax `[CONSTRAINT [symbol]] CHECK (expr) [[NOT] ENFORCED]`.
* Not permitted: nondeterministic functions (CONNECTION_ID(), CURRENT_USER(), NOW() ...), subqueries, stored and loadable functions, stored program parameters, variables, AUTO_INCREMENT columns, columns in other tables, foreign key referential actions.
* Evaluated for INSERT, UPDATE, REPLACE, LOAD DATA and LOAD XML; "If a constraint evaluates to FALSE, an error occurs"; with INSERT IGNORE / UPDATE IGNORE / LOAD DATA ... IGNORE / LOAD XML ... IGNORE a warning occurs and "the insert or update for any offending row is skipped".
* NOT ENFORCED creates the constraint without enforcing it.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): CHECK constraints are added in `constraints.sql` after loading ([indexing strategy](/decisions/indexing-strategy.md)); constraints referencing functions MySQL lacks are ported as `NOT ENFORCED` with a comment or dropped, per dataset record.
