---
type: Source
title: "MySQL 9.7 Reference Manual: Functions That Create Geometry Values from WKT Values"
description: "ST_GeomFromText(wkt, srid, options) with axis-order=lat-long|long-lat|srid-defined, and the latitude/longitude range errors for geographic SRSs."
resource: https://dev.mysql.com/doc/refman/9.7/en/gis-wkt-functions.html
tags: [mysql, docs, spatial]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/gis-wkt-functions.html
    title: "MySQL 9.7 Reference Manual: Functions That Create Geometry Values from WKT Values"
    accessed: "2026-09-02"
    version: "MySQL 9.7 manual, section 14.16.3"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/gis-wkt-functions.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 14.16.3.

# Relevant excerpt
* Syntax `ST_GeomFromText(wkt [, srid [, options]])`; options `axis-order=lat-long|long-lat|srid-defined`, default `srid-defined` ("uses the order specified by the spatial reference system").
* "For geographic SRS geometry arguments, geographic coordinates (latitude, longitude) are interpreted in the order specified by the spatial reference system of geometry arguments by default."
* Range errors for geographic SRSs: longitude not in (−180, 180] raises ER_LONGITUDE_OUT_OF_RANGE; latitude not in [−90, 90] raises ER_LATITUDE_OUT_OF_RANGE.
* Example on the page: `ST_GeomFromText('POINT(10 20)', 4326)`.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): every converter that emits WKT for SRID 4326 must call `ST_GeomFromText(@wkt, 4326, 'axis-order=long-lat')` because SQL Server geography and GeoJSON/WKT sources are longitude-first; a lat/long swap is not an error unless a coordinate exceeds 90, so the tests compare `ST_Latitude`/`ST_Longitude` of sampled rows.
