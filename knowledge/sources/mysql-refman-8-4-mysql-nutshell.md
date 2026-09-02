---
type: Source
title: "MySQL 8.4 Reference Manual: What Is New in MySQL 8.4"
description: "mysqlpump and mysql_upgrade were removed in 8.4; mysql_native_password disabled by default; innodb_change_buffering default none."
resource: https://dev.mysql.com/doc/refman/8.4/en/mysql-nutshell.html
tags: [mysql, docs, release]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/8.4/en/mysql-nutshell.html
    title: "MySQL 8.4 Reference Manual: What Is New in MySQL 8.4"
    accessed: "2026-09-02"
    version: "MySQL 8.4 manual, section 1.4"
---

# What was read
https://dev.mysql.com/doc/refman/8.4/en/mysql-nutshell.html, accessed 2026-09-02; version: MySQL 8.4 manual, section 1.4.

# Relevant excerpt
> "The mysqlpump utility along with its helper utilities lz4_decompress and zlib_decompress, deprecated in MySQL 8.0.34, were removed."
> "Beginning with MySQL 8.4.0, the deprecated mysql_native_password authentication plugin is no longer enabled by default."
> "The mysql_upgrade utility, deprecated in MySQL 8.0.16, has been removed."
* Default of `innodb_change_buffering` changed from `all` (8.0) to `none` (8.4).

# What it was used to decide
[LOAD DATA tool record](/tools/load-data-infile.md): mysqlpump is not an option on 8.4/9.x; [MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): the change-buffer default `none` means the `unique_checks=0` change-buffer benefit described in the bulk-load page is smaller on 8.4+ (**Inferred**).
