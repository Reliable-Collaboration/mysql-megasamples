---
type: Source
title: "MySQL 9.7 Reference Manual: Creating Spatial Indexes"
description: "SPATIAL indexes: InnoDB/MyISAM only, NOT NULL columns, SRID-restricted columns for optimizer use, R-tree."
resource: https://dev.mysql.com/doc/refman/9.7/en/creating-spatial-indexes.html
tags: [mysql, docs, spatial, index]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/creating-spatial-indexes.html
    title: "MySQL 9.7 Reference Manual: Creating Spatial Indexes"
    accessed: "2026-09-02"
    version: "MySQL 9.7 manual, section 13.4.10"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/creating-spatial-indexes.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 13.4.10.

# Relevant excerpt
* Only InnoDB and MyISAM support spatial indexes; "Indexed columns must be declared NOT NULL"; "The optimizer can use spatial indexes defined on columns that are SRID-restricted."
* `SPATIAL INDEX` creates an R-tree; engines that support non-spatial indexing of spatial columns create a B-tree, useful for exact lookups only.
* Examples: `CREATE TABLE geom (g GEOMETRY NOT NULL SRID 4326, SPATIAL INDEX(g));`, `ALTER TABLE geom ADD SPATIAL INDEX(g);`, `CREATE SPATIAL INDEX g ON geom (g);`

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md); [indexing strategy](/decisions/indexing-strategy.md).
