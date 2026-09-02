---
type: Source
title: "MySQL 9.7 Reference Manual: INFORMATION_SCHEMA TABLES Table"
description: TABLE_ROWS is an estimate for InnoDB; DATA_LENGTH/INDEX_LENGTH definitions; statistics caching.
resource: https://dev.mysql.com/doc/refman/9.7/en/information-schema-tables-table.html
tags:
- mysql
- docs
- testing
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:21:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:21:00Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/information-schema-tables-table.html
  title: "MySQL 9.7 Reference Manual: INFORMATION_SCHEMA TABLES Table"
  accessed: "2026-09-02"
---
# What was read
* https://dev.mysql.com/doc/refman/9.7/en/information-schema-tables-table.html, “MySQL 9.7 Reference Manual: INFORMATION_SCHEMA TABLES Table”, accessed 2026-09-02

# Relevant excerpt
> "For other storage engines, such as InnoDB, this value is an approximation, and may vary from the actual value by as much as 40% to 50%. In such cases, use SELECT COUNT(*) to obtain an accurate count."
> "For InnoDB, DATA_LENGTH is the approximate amount of space allocated for the clustered index, in bytes." "INDEX_LENGTH is the approximate amount of space allocated for non-clustered indexes, in bytes."
> "The information_schema_stats_expiry system variable defines the period of time before cached table statistics expire. The default is 86400 seconds (24 hours)... To always retrieve the latest statistics directly from storage engines, set information_schema_stats_expiry to 0."

# What it was used to decide
Size tests use `DATA_LENGTH + INDEX_LENGTH` after `SET SESSION information_schema_stats_expiry = 0` and `ANALYZE TABLE`; row-count tests always use `SELECT COUNT(*)`, never TABLE_ROWS ([checksum method](/decisions/test-checksum-method.md)).
