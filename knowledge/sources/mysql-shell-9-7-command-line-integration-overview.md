---
type: Source
title: "MySQL Shell 9.7: Command Line Integration Overview"
description: "mysqlsh [options] -- object method [arguments]; camelCase methods become hyphenated; exit status 10 on unknown object/method; --no-defaults."
resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/command-line-integration-overview.html
tags: [mysql-shell, cli]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/command-line-integration-overview.html
    title: "MySQL Shell 9.7: Command Line Integration Overview"
    accessed: "2026-09-02"
    version: "MySQL Shell 9.7 manual, section 5.8.1"
---

# What was read
https://dev.mysql.com/doc/mysql-shell/9.7/en/command-line-integration-overview.html, accessed 2026-09-02; version: MySQL Shell 9.7 manual, section 5.8.1.

# Relevant excerpt
* Syntax `mysqlsh [options] -- [shell_object]+ object_method [arguments]`; method names convert from camelCase to hyphenated lowercase (`checkForServerUpgrade` → `check-for-server-upgrade`).
* Examples on the page: `mysqlsh -- util check-for-server-upgrade --user=root --host=localhost --port=3301 --password='password' --outputFormat=JSON --config-path=/etc/mysql/my.cnf`; `mysqlsh root@localhost:1234 -- dba create-cluster mycluster`; `mysqlsh -- --help`; `mysqlsh -- object --help`.
* "If shell objects or methods don't correspond to valid objects and their methods, MySQL Shell exits with status 10." MySQL Shell reads option files and login paths unless `--no-defaults`.

# What it was used to decide
[MySQL Shell utilities](/tools/mysql-shell-utilities.md): build scripts call `mysqlsh --no-defaults root@localhost --socket=... -- util import-table ...` non-interactively; the exact hyphenated option names are checked with `mysqlsh -- util import-table --help` at build time.
