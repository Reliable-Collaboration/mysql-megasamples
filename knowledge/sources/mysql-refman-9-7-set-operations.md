---
type: Source
title: MySQL 9.7 Reference Manual — Set Operations with UNION, INTERSECT, and EXCEPT
description: Confirms UNION/INTERSECT/EXCEPT, ALL/DISTINCT, and INTERSECT precedence in the target version.
resource: https://dev.mysql.com/doc/refman/9.7/en/set-operations.html
tags: [mysql, sql-syntax]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/set-operations.html
    title: Set Operations with UNION, INTERSECT, and EXCEPT
    accessed: 2026-09-02
---

# Relevant excerpt (verbatim)
* "MySQL supports UNION, INTERSECT, and EXCEPT."
* "Each of these set operators supports an ALL modifier."; DISTINCT is the default.
* "INTERSECT is evaluated before UNION or EXCEPT."

# What it was used to decide
[TPC-DS dataset](/datasets/tpc-ds.md).
