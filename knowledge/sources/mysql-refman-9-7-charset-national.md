---
type: Source
title: MySQL 9.7 Reference Manual - The National Character Set
description: NCHAR/NVARCHAR/NATIONAL CHAR map to utf8mb3 in 9.7 and raise a deprecation warning recommending CHARACTER SET utf8mb4.
resource: https://dev.mysql.com/doc/refman/9.7/en/charset-national.html
tags:
- mysql
- "9.7"
- nvarchar
- utf8mb3
- chinook
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/charset-national.html
  title: 12.3.7 The National Character Set
  accessed: "2026-09-02"
---

# What was read
The manual page, accessed 2026-09-02.

# Relevant excerpt
`NCHAR(10)`, `NATIONAL CHARACTER(10)` are equivalent to `CHAR(10) CHARACTER SET utf8`; `NVARCHAR(10)`, `NATIONAL VARCHAR(10)`, `NCHAR VARCHAR(10)` etc. are equivalent to `VARCHAR(10) CHARACTER SET utf8`; `N'text'` equals `_utf8'text'`. Warning raised by the server:
> NATIONAL/NCHAR/NVARCHAR implies the character set UTF8MB3, which will be replaced by UTF8MB4 in a future release. Please consider using CHAR(x) CHARACTER SET UTF8MB4 in order to be unambiguous.

# What it was used to decide
Rewrite `NVARCHAR` to `VARCHAR ... CHARACTER SET utf8mb4` for Chinook and any other script using national types ([Chinook decision](/decisions/chinook-conversion-path.md)).
