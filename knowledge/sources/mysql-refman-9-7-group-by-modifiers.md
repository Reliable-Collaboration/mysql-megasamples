---
type: Source
title: MySQL 9.7 Reference Manual — GROUP BY Modifiers (ROLLUP, GROUPING())
description: MySQL supports both WITH ROLLUP and GROUP BY ROLLUP(...), GROUPING() in select/HAVING/ORDER BY, and ORDER BY together with ROLLUP; no CUBE/GROUPING SETS.
resource: https://dev.mysql.com/doc/refman/9.7/en/group-by-modifiers.html
tags:
- mysql
- sql-syntax
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/group-by-modifiers.html
  title: GROUP BY Modifiers
  accessed: "2026-09-02"
---
# What was read
* https://dev.mysql.com/doc/refman/9.7/en/group-by-modifiers.html, “GROUP BY Modifiers”, accessed 2026-09-02

# Relevant excerpt
* `GROUP BY year WITH ROLLUP` and, "MySQL supports an additional, alternative syntax for this modifier ... GROUP BY ROLLUP (year)".
* GROUPING() usable in the select list, HAVING and ORDER BY; returns 1 for super-aggregate NULLs.
* "ORDER BY and ROLLUP can be used together, which enables the use of ORDER BY and GROUPING() to achieve a specific sort order of grouped results."
* CUBE and GROUPING SETS are not mentioned on the page.

# What it was used to decide
[TPC-DS dataset](/datasets/tpc-ds.md): the 11 ROLLUP queries and 4 GROUPING() queries need no rewrite (to be verified).
