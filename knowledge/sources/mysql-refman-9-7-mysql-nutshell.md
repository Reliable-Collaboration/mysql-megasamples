---
type: Source
title: "MySQL 9.7 Reference Manual: What Is New in MySQL 9.7"
description: "The 9.7 change list is small: innodb_log_writer_threads default logic, binlog_transaction_dependency_history_size default, SCRAM-SHA-1 deprecation, two variables removed."
resource: https://dev.mysql.com/doc/refman/9.7/en/mysql-nutshell.html
tags:
- mysql
- docs
- release
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/mysql-nutshell.html
  title: "MySQL 9.7 Reference Manual: What Is New in MySQL 9.7"
  accessed: "2026-09-02"
  version: MySQL 9.7 manual, section 1.4
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/mysql-nutshell.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 1.4.

# Relevant excerpt
* Added/changed: the default of `innodb_log_writer_threads` now depends on binary logging and CPU count (ON when log_bin=OFF and more than 4 logical CPUs; otherwise the 9.4-and-earlier rule of ON at 32+ CPUs); `binlog_transaction_dependency_history_size` default raised from 25000 to 1000000 (max 10000000).
* Deprecated: `SCRAM-SHA-1` for SASL LDAP (since 9.5.0), `SCRAM-SHA-256` is the default.
* Removed: `group_replication_allow_local_lower_version_join`, `replica_parallel_type`.
* Nothing about authentication plugins, character sets, JSON, spatial, LOAD DATA or mysqldump changed in 9.7 itself; the mysql_native_password removal is a 9.0 change ([9.0.0 release notes](/sources/mysql-relnotes-9-0-0.md)).

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): confirms that the 8.4-to-9.7 differences relevant to conversions are inherited from 9.0 (native password removal, VECTOR type) rather than introduced in 9.7.
