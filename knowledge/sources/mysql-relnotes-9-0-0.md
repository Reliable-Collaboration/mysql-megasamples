---
type: Source
title: "MySQL 9.0.0 Release Notes (2024-07-01)"
description: "Server-side removal of mysql_native_password, the VECTOR type, and JavaScript stored programs (Enterprise) introduced in 9.0."
resource: https://dev.mysql.com/doc/relnotes/mysql/9.0/en/news-9-0-0.html
tags: [mysql, release-notes, authentication]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/relnotes/mysql/9.0/en/news-9-0-0.html
    title: "MySQL 9.0.0 Release Notes (2024-07-01)"
    accessed: "2026-09-02"
    version: "9.0.0, 2024-07-01"
---

# What was read
https://dev.mysql.com/doc/relnotes/mysql/9.0/en/news-9-0-0.html, accessed 2026-09-02; version: 9.0.0, 2024-07-01.

# Relevant excerpt
> "The mysql_native_password authentication plugin, deprecated in MySQL 8.0, has been removed, and the server now rejects mysql_native authentication requests from older client programs which do not have CLIENT_PLUGIN_AUTH capability. For backward compatibility, mysql_native_password remains available on the client; the client-side built-in authentication plugin has been converted into a dynamically loadable plugin."
> "Support is added in this release for a VECTOR column type. ... A VECTOR column is declared with a maximum length or number of entries (in parentheses); the default is 2048, and the maximum is 16383."
* JavaScript stored programs are an Enterprise Edition feature (`LANGUAGE JAVASCRIPT`), not available in the Community image.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): upstream sample scripts containing `IDENTIFIED WITH mysql_native_password` (common in older tutorials) must be rewritten; VECTOR is available for any embedding demo but is not used by the inventory.
