---
type: Source
title: DuckDB documentation — TPC-H extension
description: How DuckDB's built-in dbgen generates TPC-H tables, its parameters, and which scale factors have stored answers.
resource: https://duckdb.org/docs/current/core_extensions/tpch.html
tags: [duckdb, tpc-h, dbgen]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://duckdb.org/docs/current/core_extensions/tpch.html
    title: TPC-H Extension (docs/stable/extensions/tpch redirects here)
    accessed: "2026-09-02"
    version: DuckDB docs "current" (latest DuckDB release v1.5.5, 2026-07-22 per GitHub)
---

# What was read
The extension page (the stable URL from the brief is a redirect to this one).

# Relevant excerpt
* "The tpch extension is shipped by default in some DuckDB builds, otherwise it will be transparently autoloaded on first use." Manual: `INSTALL tpch; LOAD tpch;`.
* `CALL dbgen(sf = 1);` — parameters: `sf` DOUBLE (scale factor), `catalog` VARCHAR, `children` UINTEGER (number of partitions), `step` UINTEGER ("Partition to be generated, indexed from 0 to children - 1"), `suffix` VARCHAR ("Append the suffix to table names"), `overwrite` BOOLEAN ("Not used"). "Calling dbgen does not clean up existing TPC-H tables."
* Tables: customer, lineitem, nation, orders, part, partsupp, region, supplier.
* `PRAGMA tpch(4);` runs query 4; `FROM tpch_queries();` (query_nr, query); `FROM tpch_answers();` (query_nr, scale_factor, answer) with "Pre-computed answers available for: scale factors 0.01, 0.1, and 1".
* "It is not possible to change the query parameters using the tpch extension."
* Source: https://github.com/duckdb/duckdb/tree/main/extension/tpch. The page carries no licensing statement about the generator.

# What it was used to decide
[DuckDB TPC-H/TPC-DS extensions tool record](/tools/duckdb-tpch-tpcds-extensions.md); [TPC-H generator decision](/decisions/tpch-generator-path.md).
