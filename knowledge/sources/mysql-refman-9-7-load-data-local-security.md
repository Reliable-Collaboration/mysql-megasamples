---
type: Source
title: "MySQL 9.7 Reference Manual: Security Considerations for LOAD DATA LOCAL"
description: "local_infile is disabled by default on the server; the client library default is also disabled; both sides must enable LOCAL loading."
resource: https://dev.mysql.com/doc/refman/9.7/en/load-data-local-security.html
tags: [mysql, docs, load-data, security]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/load-data-local-security.html
    title: "MySQL 9.7 Reference Manual: Security Considerations for LOAD DATA LOCAL"
    accessed: 2026-09-02
    version: "MySQL 9.7 manual, section 8.1.6"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/load-data-local-security.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 8.1.6.

# Relevant excerpt
* "By default, local_infile is disabled. (This is a change from previous versions of MySQL.)" Enable with `mysqld --local_infile=1` or `SET GLOBAL local_infile=1;`.
* Client: `mysql --local-infile[=1]` enables, `--local-infile=0` disables; C API `MYSQL_OPT_LOCAL_INFILE`; "By default, the client library in MySQL binary distributions is compiled with ENABLED_LOCAL_INFILE disabled."
* Error when either side is off: "ERROR 3950 (42000): Loading local data is disabled; this must be enabled on both the client and server side".
* `--load-data-local-dir` / `MYSQL_OPT_LOAD_DATA_LOCAL_DIR` restrict LOCAL loading to one directory.

# What it was used to decide
[LOAD DATA tool record](/tools/load-data-infile.md) and [MySQL Shell utilities](/tools/mysql-shell-utilities.md): every build step that uses LOCAL (all Shell utilities) must first run `SET GLOBAL local_infile=1` or start the temporary mysqld with `--local-infile=1`.
