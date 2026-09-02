---
type: Source
title: "MySQL 9.7 Reference Manual: Identifier Length Limits"
description: "64-character limit for database, table, column, index, constraint and routine names; aliases 256; generated constraint names can overflow."
resource: https://dev.mysql.com/doc/refman/9.7/en/identifier-length.html
tags: [mysql, docs, identifiers]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/identifier-length.html
    title: "MySQL 9.7 Reference Manual: Identifier Length Limits"
    accessed: "2026-09-02"
    version: "MySQL 9.7 manual, section 11.2.1"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/identifier-length.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 11.2.1.

# Relevant excerpt
* Maximum lengths (characters): Database 64, Table 64, Column 64, Index 64, Constraint 64, Stored Program 64, View 64, Tablespace 64, Server 64, Log File Group 64, Alias 256, Compound Statement Label 16, User-Defined Variable 64, Resource Group 64.
* Identifiers are stored as UTF-8 and the limit is measured in characters.
* "Internally generated foreign key and CHECK constraint names consist of the table name plus _ibfk_ or _chk_ and a number. If the table name is close to the length limit for constraint names, the additional characters required for the constraint name may cause that name to exceed the limit, resulting in an error."

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): converters truncate and de-duplicate identifiers longer than 64 characters (SQL Server allows 128) and always name constraints explicitly.
