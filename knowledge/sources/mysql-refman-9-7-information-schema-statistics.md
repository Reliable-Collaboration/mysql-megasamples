---
type: Source
title: "MySQL 9.7 Reference Manual: INFORMATION_SCHEMA STATISTICS Table"
description: Columns describing every index; basis for the index-existence test.
resource: https://dev.mysql.com/doc/refman/9.7/en/information-schema-statistics-table.html
tags:
- mysql
- docs
- testing
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:21:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:21:00Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/information-schema-statistics-table.html
  title: "MySQL 9.7 Reference Manual: INFORMATION_SCHEMA STATISTICS Table"
  accessed: "2026-09-02"
---
# What was read
* https://dev.mysql.com/doc/refman/9.7/en/information-schema-statistics-table.html, “MySQL 9.7 Reference Manual: INFORMATION_SCHEMA STATISTICS Table”, accessed 2026-09-02

# Relevant excerpt
Columns: TABLE_SCHEMA, TABLE_NAME, NON_UNIQUE (0/1), INDEX_NAME (`PRIMARY` for primary keys), SEQ_IN_INDEX (from 1), COLUMN_NAME (NULL for functional key parts), COLLATION (A/D/NULL), CARDINALITY, SUB_PART (prefix length or NULL), NULLABLE, INDEX_TYPE ("BTREE, FULLTEXT, HASH, RTREE"), COMMENT, INDEX_COMMENT, IS_VISIBLE, EXPRESSION.
> "CARDINALITY ... An estimate of the number of unique values in the index. To update this number, run ANALYZE TABLE"

# What it was used to decide
[Indexing strategy](/decisions/indexing-strategy.md): `tests/indexes.yaml` is compared against a query over STATISTICS grouped by INDEX_NAME (ordered SEQ_IN_INDEX) with NON_UNIQUE and INDEX_TYPE; spatial indexes appear as `SPATIAL` in SHOW INDEX and `RTREE`/`SPATIAL` here — the executor records the exact string seen on 9.7.
