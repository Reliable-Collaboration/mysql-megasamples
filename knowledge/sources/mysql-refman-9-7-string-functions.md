---
type: Source
title: MySQL 9.7 Reference Manual — String Functions (SUBSTR/SUBSTRING forms)
description: SUBSTR() is a synonym for SUBSTRING(); the SUBSTRING(str FROM pos FOR len) standard form is supported.
resource: https://dev.mysql.com/doc/refman/9.7/en/string-functions.html
tags: [mysql, sql-syntax]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/string-functions.html
    title: String Functions and Operators
    accessed: "2026-09-02"
---
# What was read
* https://dev.mysql.com/doc/refman/9.7/en/string-functions.html, “String Functions and Operators”, accessed 2026-09-02

# Relevant excerpt
* "SUBSTR() is a synonym for SUBSTRING()."; forms `SUBSTRING(str, pos)`, `SUBSTRING(str FROM pos)`, `SUBSTRING(str, pos, len)`, `SUBSTRING(str FROM pos FOR len)`.

# What it was used to decide
TPC-H Q22 (`substring(c_phone from 1 for 2)`) and TPC-DS substr() queries need no rewrite — [TPC-H](/datasets/tpc-h.md), [TPC-DS](/datasets/tpc-ds.md).
