---
type: Source
title: "MySQL 9.7 Reference Manual: CHECKSUM TABLE Statement"
description: What CHECKSUM TABLE computes and why it is not portable across versions or engines.
resource: https://dev.mysql.com/doc/refman/9.7/en/checksum-table.html
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
- resource: https://dev.mysql.com/doc/refman/9.7/en/checksum-table.html
  title: "MySQL 9.7 Reference Manual: CHECKSUM TABLE Statement"
  accessed: "2026-09-02"
---
# What was read
* https://dev.mysql.com/doc/refman/9.7/en/checksum-table.html, “MySQL 9.7 Reference Manual: CHECKSUM TABLE Statement”, accessed 2026-09-02

# Relevant excerpt
> "The checksum value depends on the table row format. If the row format changes, the checksum also changes."
> "because the hashing function used by CHECKSUM TABLE is not guaranteed to be collision-free, there is a slight chance that two tables which are not identical can produce the same checksum."
InnoDB: QUICK returns NULL; EXTENDED reads the whole table under a read lock.

# What it was used to decide
[Per-table checksum method](/decisions/test-checksum-method.md): CHECKSUM TABLE is used only as a same-image regression fingerprint (recorded in `baseline.json`, compared between two builds of the same MySQL version), never as the cross-system source-versus-MySQL comparison.
