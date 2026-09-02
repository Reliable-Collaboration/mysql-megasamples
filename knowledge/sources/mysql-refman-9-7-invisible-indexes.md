---
type: Source
title: "MySQL 9.7 Reference Manual: Invisible Indexes"
description: "Invisible indexes are maintained but ignored by the optimizer; primary keys cannot be invisible; use_invisible_indexes switch."
resource: https://dev.mysql.com/doc/refman/9.7/en/invisible-indexes.html
tags: [mysql, docs, index]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/invisible-indexes.html
    title: "MySQL 9.7 Reference Manual: Invisible Indexes"
    accessed: 2026-09-02
    version: "MySQL 9.7 manual, section 10.3.12"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/invisible-indexes.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 10.3.12.

# Relevant excerpt
* `INDEX i_idx (i) INVISIBLE`, `ALTER TABLE t1 ALTER INDEX i_idx INVISIBLE|VISIBLE`; primary keys (explicit or implicit UNIQUE NOT NULL) cannot be invisible ("ERROR 3522 (HY000): A primary key index cannot be invisible").
* Index maintenance is unaffected; visibility changes are fast in-place operations; `optimizer_switch='use_invisible_indexes=on'` (default off) makes the optimizer consider them, also via `SET_VAR` hint.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): the optional `indexes-extra.sql` ships tutorial indexes as INVISIBLE so users can demonstrate the optimizer effect by toggling visibility.
