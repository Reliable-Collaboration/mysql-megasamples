---
type: Source
title: "MySQL 9.7 Reference Manual: Server Character Set and Collation"
description: "Default server character set utf8mb4 and collation utf8mb4_0900_ai_ci."
resource: https://dev.mysql.com/doc/refman/9.7/en/charset-server.html
tags: [mysql, docs, charset]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/charset-server.html
    title: "MySQL 9.7 Reference Manual: Server Character Set and Collation"
    accessed: "2026-09-02"
    version: "MySQL 9.7 manual, section 12.3.2"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/charset-server.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 12.3.2.

# Relevant excerpt
> "MySQL Server has a server character set and a server collation. By default, these are utf8mb4 and utf8mb4_0900_ai_ci, but they can be set explicitly at server startup on the command line or in an option file and changed at runtime."
> "If you don't specify a character set, that is the same as saying --character-set-server=utf8mb4. If you specify only a character set (for example, utf8mb4) but not a collation, that is the same as saying --character-set-server=utf8mb4 --collation-server=utf8mb4_0900_ai_ci because utf8mb4_0900_ai_ci is the default collation for utf8mb4."

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): converted schemas declare `CHARACTER SET utf8mb4` explicitly anyway; the default collation is accent- and case-insensitive, which changes the semantics of `=` and `DISTINCT` compared with SQL Server binary or Oracle case-sensitive collations.
