---
type: Source
title: MySQL 9.7 Reference Manual — Fractional Seconds in Time Values
description: DATETIME/TIMESTAMP carry at most 6 fractional digits; extra digits are rounded by default, truncated under TIME_TRUNCATE_FRACTIONAL.
resource: https://dev.mysql.com/doc/refman/9.7/en/fractional-seconds.html
tags:
- mysql
- datetime
- type-mapping
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/fractional-seconds.html
  title: Fractional Seconds in Time Values
  accessed: "2026-09-02"
---

# What was read
The manual page, 2026-09-02.

# Relevant excerpt
* MySQL "has fractional seconds support for `TIME`, `DATETIME`, and `TIMESTAMP` values, with up to microseconds (6 digits) precision"; `fsp` range 0–6, default 0.
* Inserting a value with more digits than the column: rounding by default ("`.777` was rounded to `.78`, no warning or error"); with `SET @@sql_mode = sys.list_add(@@sql_mode, 'TIME_TRUNCATE_FRACTIONAL')` the value is truncated instead.

# What it was used to decide
[CO dataset record](/datasets/oracle-co.md): `orders.order_tms` has 9 fractional digits in every row; the converter must truncate (or round) to 6 deterministically. [OE](/datasets/oracle-oe-pm-ix.md) `orders.order_date` (6 digits) fits `DATETIME(6)` exactly.
