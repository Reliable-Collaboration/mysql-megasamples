---
type: Source
title: DuckDB documentation — TPC-DS extension
description: How DuckDB's built-in dsdgen generates TPC-DS tables, its parameters, stored answers, pre-generated datasets and the notice about TPC-DS v4 compatibility in DuckDB 2.0.
resource: https://duckdb.org/docs/current/core_extensions/tpcds.html
tags: [duckdb, tpc-ds, dsdgen]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://duckdb.org/docs/current/core_extensions/tpcds.html
    title: TPC-DS Extension (docs/stable/extensions/tpcds redirects here)
    accessed: 2026-09-02
---

# What was read
The extension page.

# Relevant excerpt
* "The tpcds extension will be transparently autoloaded on first use from the official extension repository." Manual: `INSTALL tpcds; LOAD tpcds;`.
* `CALL dsdgen(sf = 1);` — parameters: `sf` DOUBLE, `schema`, `catalog`, `suffix`, `keys` BOOLEAN ("Generate primary and foreign keys"), `overwrite` (not used). Schema only: `CALL dsdgen(sf = 0);`.
* `PRAGMA tpcds(8);`; `FROM tpcds_queries();`; `FROM tpcds_answers();` "for scale factors 1 and 10".
* Pre-generated DuckDB database files are offered for download from 2.9 GB (SF10) to 79.3 GB (SF300), "generated with DuckDB v1.x".
* "will change in DuckDB version 2.0 to make the generator compatible with TPC-DS version 4" (so the current generator predates v4; the bundled source says 2.10.0, see [extension source record](/sources/github-duckdb-tpch-tpcds-extension-source.md)).
* "It is not possible to change the query parameters using the tpcds extension." No licensing statement.

# What it was used to decide
[DuckDB extensions tool record](/tools/duckdb-tpch-tpcds-extensions.md); [TPC-DS generator decision](/decisions/tpcds-generator-path.md).
