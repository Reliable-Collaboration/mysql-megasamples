---
type: Source
title: "MySQL 9.7 Reference Manual: Full-Text Search Functions"
description: FULLTEXT on InnoDB/MyISAM CHAR, VARCHAR, TEXT columns; three search modes; load data first then create the index.
resource: https://dev.mysql.com/doc/refman/9.7/en/fulltext-search.html
tags:
- mysql
- docs
- fulltext
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/fulltext-search.html
  title: "MySQL 9.7 Reference Manual: Full-Text Search Functions"
  accessed: "2026-09-02"
  version: MySQL 9.7 manual, section 14.9
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/fulltext-search.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 14.9.

# Relevant excerpt
* Full-text indexes only on InnoDB or MyISAM tables and only on CHAR, VARCHAR, TEXT columns; syntax `MATCH (col1, col2, ...) AGAINST (expr [search_modifier])` with natural language (default), boolean and query expansion modes.
* For large data sets it is "much faster" to load data into a table with no FULLTEXT index and create the index after loading.
* Built-in ngram parser for CJK and the MeCab plugin for Japanese.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md); [indexing strategy](/decisions/indexing-strategy.md) rule 4.
