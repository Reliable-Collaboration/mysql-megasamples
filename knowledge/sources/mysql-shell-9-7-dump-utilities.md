---
type: Source
title: "MySQL Shell 9.7: Instance, Schema and Table Dump Utilities"
description: "util.dumpInstance/dumpSchemas/dumpTables output layout (@.json, @.sql, schema.sql, schema@table.json/.sql, schema@table@@N.tsv.zst + .idx), compression, chunking 64 MB, threads 4, compatibility modifiers."
resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-dump-instance-schema.html
tags: [mysql-shell, dump]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-dump-instance-schema.html
    title: "MySQL Shell 9.7: Instance, Schema and Table Dump Utilities"
    accessed: "2026-09-02"
    version: "MySQL Shell 9.7 manual, section 12.5"
---

# What was read
https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-dump-instance-schema.html, accessed 2026-09-02; version: MySQL Shell 9.7 manual, section 12.5.

# Relevant excerpt
* Output: DDL `.sql` files, tab-separated `.tsv` data files (default `.tsv.zst` with `.idx` index files), `.json` metadata (`@.json`, `@.done.json`, `schema.json`, `schema@table.json`), plus `@.sql`/`@.post.sql`. Example listing: `worlddump/@.done.json @.json @.post.sql @.sql world.json world.sql world@city.json world@city.sql world@city@@0.tsv.zst world@city@@0.tsv.zst.idx`.
* `compression`: `none`, `gzip` (level 0-9, default 1), `zstd` (default; level 1-22, default 1). `chunking` default true, `bytesPerChunk` default 64 MB, `threads` default 4, `consistent` default true, `ddlOnly`, `dataOnly`, `dryRun`, `ocimds`.
* `compatibility` modifiers: force_innodb, lock_invalid_accounts, skip_invalid_accounts, strip_definers (removes DEFINER and sets SQL SECURITY INVOKER on views/routines/events/triggers), strip_restricted_grants, strip_tablespaces, target_has_mysql_native_password, ignore_missing_pks, ignore_wildcard_grants, strip_invalid_grants, unescape_wildcard_grants, create_invisible_pks.
* Source and destination MySQL 5.7 or later. Local output directory: `util.dumpInstance("C:/Users/hanna/worlddump", {...})` or a `file://` URL.

# What it was used to decide
[MySQL Shell utilities](/tools/mysql-shell-utilities.md): the dump format is the interchange format for MySQL-native sources (Sakila, Employees, World) and for publishing extended-tier bundles; `strip_definers` removes hard-coded DEFINER accounts from upstream views.
