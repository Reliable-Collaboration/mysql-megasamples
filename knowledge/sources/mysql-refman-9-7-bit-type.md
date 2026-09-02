---
type: Source
title: "MySQL 9.7 Reference Manual: Bit-Value Type - BIT"
description: "BIT(M) with M 1..64, b'value' literals, left zero padding."
resource: https://dev.mysql.com/doc/refman/9.7/en/bit-type.html
tags: [mysql, docs, numeric]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/bit-type.html
    title: "MySQL 9.7 Reference Manual: Bit-Value Type - BIT"
    accessed: 2026-09-02
    version: "MySQL 9.7 manual, section 13.1.5"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/bit-type.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 13.1.5.

# Relevant excerpt
* "M can range from 1 to 64"; bit literals `b'111'` (7), `b'10000000'` (128); values shorter than M are padded on the left with zeros.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): SQL Server `bit` is mapped to `TINYINT(1)`/`BOOLEAN` rather than `BIT(1)` so that LOAD DATA text `0`/`1` and DuckDB's `mysql_bit1_as_boolean` behave predictably.
