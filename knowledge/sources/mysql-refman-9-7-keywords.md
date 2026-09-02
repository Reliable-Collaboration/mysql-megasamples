---
type: Source
title: MySQL 9.7 Reference Manual — Keywords and Reserved Words (DATE, ORDER)
description: DATE, TIME, YEAR are keywords but not reserved; ORDER is reserved — relevant to SSB's date table and TPC-C's ORDER table.
resource: https://dev.mysql.com/doc/refman/9.7/en/keywords.html
tags:
- mysql
- sql-syntax
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/keywords.html
  title: Keywords and Reserved Words
  accessed: "2026-09-02"
---
# What was read
* https://dev.mysql.com/doc/refman/9.7/en/keywords.html, “Keywords and Reserved Words”, accessed 2026-09-02

# Relevant excerpt
* "Reserved keywords are marked with (R)." Entries: `DATE`, `TIME`, `YEAR` (not reserved); `ORDER (R)` (reserved). PART, SUPPLIER, CUSTOMER, ORDERS, LINEITEM, NATION, REGION, ITEM, STOCK, HISTORY, DISTRICT, WAREHOUSE, INVENTORY, REASON, STORE, PROMOTION are not keywords.

# What it was used to decide
SSB keeps the table name `date` (unquoted works, but the DDL will quote it for safety); TPC-C uses `orders` — [SSB](/datasets/ssb.md), [TPC-C](/datasets/tpc-c.md).
