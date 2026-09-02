---
type: Source
title: "MySQL Shell 9.7: Copy Instance, Schemas, and Tables"
description: "util.copyInstance/copySchemas/copyTables stream DDL and data between servers without intermediate files; local_infile=ON on the target; no resume."
resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utils-copy.html
tags: [mysql-shell, copy]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utils-copy.html
    title: "MySQL Shell 9.7: Copy Instance, Schemas, and Tables"
    accessed: 2026-09-02
    version: "MySQL Shell 9.7 manual, section 12.8"
---

# What was read
https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utils-copy.html, accessed 2026-09-02; version: MySQL Shell 9.7 manual, section 12.8.

# Relevant excerpt
> "The copy utilities enable you to copy DDL and data between MySQL instances, without the need for intermediate storage. The data is streamed from source to destination."
> "The copy utilities use LOAD DATA LOCAL INFILE statements to upload data, so the local_infile system variable must be set to ON on the target server."
* Signatures: `util.copyInstance(connectionData[, options])`, `util.copySchemas(schemaList, connectionData[, options])`, `util.copyTables(schemaName, tablesList, connectionData[, options])`; GA releases only; destination MySQL 5.7+; options include `threads` (4), `compatibility`, `deferTableIndexes` (default fulltext), `dryRun`, `ignoreVersion`.
* Limitations: consistency guaranteed only for InnoDB tables; object names must be latin1 or utf8; "Progress resumption is not supported by the copy utilities."

# What it was used to decide
[MySQL Shell utilities](/tools/mysql-shell-utilities.md): useful only when a source MySQL server exists (third-party MySQL ports); not used for the file-based conversion pipeline.
