---
type: Source
title: "MySQL 9.7 Reference Manual: Restrictions and Limitations on Partitioning"
description: "InnoDB partitioned tables do not support foreign keys; unique keys must include all partitioning columns; no FULLTEXT, no spatial columns; 8192 partitions."
resource: https://dev.mysql.com/doc/refman/9.7/en/partitioning-limitations.html
tags: [mysql, docs, partitioning]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/partitioning-limitations.html
    title: "MySQL 9.7 Reference Manual: Restrictions and Limitations on Partitioning"
    accessed: 2026-09-02
    version: "MySQL 9.7 manual, section 26.6"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/partitioning-limitations.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 26.6.

# Relevant excerpt
> "Partitioned tables using the InnoDB storage engine do not support foreign keys." Specifically: "No definition of an InnoDB table employing user-defined partitioning may contain foreign key references; no InnoDB table whose definition contains foreign key references may be partitioned" and "No InnoDB table definition may contain a foreign key reference to a user-partitioned table; no InnoDB table with user-defined partitioning may contain columns referenced by foreign keys."
* Every unique key (including the primary key) must include all columns in the partitioning expression; maximum 8192 partitions including subpartitions; "Partitioned tables do not support FULLTEXT indexes or searches"; spatial columns cannot be used in partitioned tables; temporary tables cannot be partitioned.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md); [indexing strategy](/decisions/indexing-strategy.md) rule 6 (partitioning only as an opt-in script for FK-less fact tables).
