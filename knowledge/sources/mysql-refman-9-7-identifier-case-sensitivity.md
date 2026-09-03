---
type: Source
title: "MySQL 9.7 Reference Manual: Identifier Case Sensitivity"
description: lower_case_table_names defaults (Unix 0), can only be set at initialization, and which identifiers are case-insensitive everywhere.
resource: https://dev.mysql.com/doc/refman/9.7/en/identifier-case-sensitivity.html
tags:
- mysql
- docs
- identifiers
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/identifier-case-sensitivity.html
  title: "MySQL 9.7 Reference Manual: Identifier Case Sensitivity"
  accessed: "2026-09-02"
  version: MySQL 9.7 manual, section 11.2.3
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/identifier-case-sensitivity.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 11.2.3.

# Relevant excerpt
* Defaults: Unix 0, Windows 1, macOS 2. Value 0: names stored as given and "Name comparisons are case-sensitive"; value 1: "Table names are stored in lowercase on disk and name comparisons are not case-sensitive" (also database names and aliases).
> "lower_case_table_names can only be configured when initializing the server. Changing the lower_case_table_names setting after the server is initialized is prohibited."
> "If you are using InnoDB tables and you are trying to avoid these data transfer problems, you should use lower_case_table_names=1 on all platforms to force names to be converted to lowercase."
* "Partition, subpartition, column, index, stored routine, event, and resource group names are not case-sensitive on any platform, nor are column aliases." Trigger names are case-sensitive.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): the image keeps the Linux default `lower_case_table_names=0` unless the executor sets it at `--initialize` time in the build stage; either way every converter emits lowercase table and database names ([naming convention](/decisions/database-naming-convention.md)) so mixed-case SQL Server/Oracle names never collide.
