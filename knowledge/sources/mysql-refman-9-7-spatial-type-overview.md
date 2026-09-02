---
type: Source
title: MySQL 9.7 Reference Manual — Spatial Data Types (overview)
description: Spatial columns may carry an SRID attribute (e.g. POINT SRID 4326) which restricts stored values to that SRID and enables SPATIAL indexes in InnoDB.
resource: https://dev.mysql.com/doc/refman/9.7/en/spatial-type-overview.html
tags:
- mysql
- spatial
- type-mapping
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/spatial-type-overview.html
  title: Spatial Data Types
  accessed: "2026-09-02"
---

# What was read
The manual page, 2026-09-02.

# Relevant excerpt
> CREATE TABLE geom (p POINT SRID 0, g GEOMETRY NOT NULL SRID 4326);
> The `SRID` attribute makes a spatial column SRID-restricted, which has these implications: The column can contain only values with the given SRID. Attempts to insert values with a different SRID produce an error. The optimizer can use `SPATIAL` indexes on the column.
> `InnoDB` tables permit `SRID` values for Cartesian and geographic SRSs.
The page does not state the axis order for SRID 4326; that lives in the spatial reference system section (not read — see the open question).

# What it was used to decide
[OE dataset record](/datasets/oracle-oe-pm-ix.md): Oracle `SDO_GEOMETRY` points (SRID 8307, lon/lat) can become `POINT SRID 4326`, but because MySQL's 4326 axis order was not verified here the recommended mapping is two `DECIMAL(9,6)` columns (`geo_longitude`, `geo_latitude`) with an optional generated `POINT`; see [question](/questions/oracle-oe-xml-purchase-orders-scope.md) for the spatial follow-up experiment.
