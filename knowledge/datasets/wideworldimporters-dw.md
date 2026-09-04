---
type: Dataset
title: WideWorldImportersDW
description: The star-schema warehouse companion of WideWorldImporters (Dimension/Fact/Integration schemas, 8 dimensions, 6 facts, table names with spaces), shipped only as .bak/.bacpac (Full with columnstore/partitioning, Standard without); MIT licensed.
resource: https://github.com/microsoft/sql-server-samples/releases/tag/wide-world-importers-v1.0
tags:
- tier-extended
- mssql-origin
- bak-restore
- mit
- star-schema
- multi-schema
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://api.github.com/repos/microsoft/sql-server-samples/releases/tags/wide-world-importers-v1.0
  title: release assets
  accessed: "2026-09-02"
- resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-dw-database-catalog
  title: WideWorldImporters OLAP database catalog (Learn)
  accessed: "2026-09-02"
- resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-dw-install-configure
  title: Install & configure WideWorldImportersDW (Learn)
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/wide-world-importers/wwi-dw-ssdt/README.md
  title: wwi-dw-ssdt README and project tree
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/license.txt
  title: license.txt (MIT)
  accessed: "2026-09-02"
stale_after: "2027-03-01"
---

# Identity
WideWorldImportersDW. Proposed MySQL database name: **`wideworldimporters_dw`**. Schemas Dimension, Fact, Integration (staging), plus Application/Sequences/PowerBI/Reports procedure schemas - see [mapping decision](/decisions/schema-to-database-mapping.md).

# Source artifact
Release `wide-world-importers-v1.0`: `WideWorldImportersDW-Standard.bak` **53,865,472 B** (chosen), `-Full.bak` 50,044,416, `-Standard.bacpac` 22,448,674, `-Full.bacpac` 20,566,783. Learn: "SQL Server 2016 with Service Pack 1 (and later versions) ... To use the full version of the sample, use SQL Server Developer or Enterprise editions." No checksums; pin by asset name + measured sha256.

# Built and measured (2026-09-03, task X-02)
Restored from `WideWorldImportersDW-Standard.bak` (sha256
`7604748509c07edec748c484aee26382947b1a78d50e85a7237380782ee22138`, 53,865,472 B — the size this
record predicted, to the byte) in the same SQL Server session as the [OLTP database](/datasets/wideworldimporters.md).
In MySQL: **16 tables, 923,643 rows, 249.9 MB in InnoDB**, loading in 7.0 s, with **29 foreign keys
and 0 orphans**, 13 secondary indexes, 14 AUTO_INCREMENT columns, 7 smoke queries and 3 plan tests
pinned. 235,317 `datetime2(7)` values were truncated to `DATETIME(6)`.

**Ten of the fourteen row counts this record inferred were right; four were not**, and all four are
wrong in the same direction and for the same reason — the dimensions are slowly-changing, so they hold
versioned rows and an "Unknown" member that the OLTP source does not:

| table | this record inferred | measured |
|---|---|---|
| Fact.Transaction | 91,109 | **99,585** |
| Dimension.Supplier | 13 | **28** |
| Dimension.Payment Method | 4 | **6** |
| Dimension.Transaction Type | 8 | **15** |

`SUM([Total Including Tax])` over `fact_sale` is **198,043,439.45**, which is the same number as
`SUM(extendedprice)` over the OLTP's `sales_invoicelines` — the cleanest available evidence that both
databases came out of one restore of one generation run.

## The dimension-key defect, and why the counts now come from SQL Server
Every dimension uses **key 0 for the "Unknown" member**. MySQL treats a 0 loaded into an
AUTO_INCREMENT column as "generate a value" unless `NO_AUTO_VALUE_ON_ZERO` is set — so the Unknown row
was renumbered onto key 1, collided with the real key-1 row, and `LOAD DATA LOCAL` (which implies
`IGNORE`, because the server cannot stop a client mid-file) dropped that row **without a word**.
`dimension_customer` came out with 402 of its 403 rows and no error anywhere.

What made it visible was refusing to pin the expectation from the load. `expected_counts.yaml` for both
WWI databases is generated from `sys.partitions` inside the restored backup and carries an
`# authority:` header that `scripts/verify.py --pin` now declines to overwrite; pinning it from MySQL
would have recorded 402 as correct. The load sets `NO_AUTO_VALUE_ON_ZERO`, and a smoke query asserts
that customer key 0 is still `Unknown`.

## Other conversion decisions
* Column names contain spaces — 314 of them, plus five table names. Table names lose the spaces
  (`dimension_stockitem`); column names replace them with underscores (`total_including_tax`), per the
  [mapping decision](/decisions/schema-to-database-mapping.md). Two upstream constraint names ran past
  MySQL's 64-character identifier limit and are truncated with a hash of the original.
* `Integration.*_Staging` (13 tables) are dropped: they exist for the SSIS package, are empty in the
  shipped backup, and nothing in the star schema references them. `Integration.ETL Cutoff` (14 rows)
  and `Integration.Lineage` (13 rows) are kept.
* `Dimension.City.Location` becomes `POINT SRID 4326` with the same long-lat axis-order handling as the
  OLTP database. Every `Photo` column is NULL in the shipped backup, in both databases.
* Loaded size is **249.9 MB**, above the 120–200 MB this record inferred.

**Not yet ported (task V-02)**: 24 stored procedures (the `Integration.MigrateStaged*` ETL set, the
`Application.Configuration_*` feature switches, `Sequences.Reseed*`) and
`Integration.GenerateDateDimensionColumns`.

# Native format and friendlier forms
.bak only (plus .bacpac). The SSDT project builds an **empty** schema; population requires running the SSIS `Daily.ETL.ispac` package against a WideWorldImporters OLTP database. No CSV or script data anywhere. `Application.Configuration_PopulateLargeSaleTable` can inflate Fact.Sale by ~12 M rows for 2012 (not part of the shipped data).

# Shape
Dimension tables (8): City, Customer, Date, Employee, `Payment Method`, `Stock Item`, Supplier, `Transaction Type` (four names contain spaces). Fact tables (6): Movement, Order, Purchase, Sale, `Stock Holding`, Transaction. Integration.*: staging tables (`*_Staging`) and `ETL Cutoff`/`Lineage` tables - **Inferred** names; drop staging in MySQL. Row counts **not published; Inferred from memory:** Fact.Sale 228,265; Fact.Order 231,412; Fact.Movement 236,667; Fact.Transaction 91,109; Fact.Purchase 8,367; Fact.`Stock Holding` 227; Dimension.City 116,295; Customer 403; Employee 213; `Stock Item` 672; Supplier 13; Date 1,461; `Payment Method` 4; `Transaction Type` 8. Baseline via `COUNT(*)` after restore ([open question](/questions/mssql-wideworldimporters-row-counts.md)). Size: .bak 54 MB; **Inferred** MySQL ~120-200 MB loaded (City dimension has geography `Location`, Full edition stores facts in columnstore so the .bak understates row-store size).
Encoding: city/country names as in OLTP (accents present); `nvarchar` everywhere.

# Conversion path
Restore in the SQL Server container, export, cache - same pipeline as OLTP ([decision](/decisions/mssql-wideworldimporters-conversion-path.md)). Both DBs should be exported from the same container session.

# Type-mapping hazards
* Slowly-changing dimensions with `Valid From`/`Valid To` `DATETIME2(7)` columns and `Lineage Key`s (column names contain spaces: `[Customer Key]`, `[WWI Customer ID]`, `[Valid From]`) - MySQL accepts backticked names with spaces; decide keep-verbatim vs snake_case (coordinator; recommend verbatim for fidelity to the many published WWI DW queries).
* `Dimension.City.Location geography` -> `POINT SRID 4326` via WKT export; `[Latest Recorded Population] BIGINT`.
* Columnstore (clustered on facts in Full; none in Standard) and partitioning by `PS_Date` -> drop; optional MySQL partitioning by `[Invoice Date Key]` is cosmetic.
* `DECIMAL(18,2)` money-like columns fine; `DATE` keys; `INT IDENTITY` keys on facts -> AUTO_INCREMENT; Integration staging memory-optimized tables (Full) -> drop.
* Sequences in `Sequences` schema (e.g. CityKey, CustomerKey, ...) -> AUTO_INCREMENT.

# Programmable objects
Drop all: `Application.Configuration_*` (columnstore/in-memory/PolyBase/partitioning/PopulateLargeSaleTable/ReseedETL), `Integration.Get*/Migrate*` ETL procedures, `Integration.PopulateDateDimensionForYear` (could be ported as a MySQL procedure - nice to have), `Sequences.Reseed*`. Views: **Inferred** few/none beyond PowerBI helpers - port if trivial.

# Indexing
PKs on keys, FKs from facts to dimensions (present in the .bak), nonclustered indexes on fact foreign keys; drop columnstore.

# Tests and expected values
Per-table counts pinned at export; `SUM(total_including_tax) FROM fact_sale`, `SUM(quantity) FROM fact_movement`, `MAX(invoice_date_key) FROM fact_sale` pinned at export; City geography probe as in OLTP.

# Tier assignment
**extended** (needs SQL Server once; ~150 MB loaded, inferred).

# License and attribution
MIT via repository `license.txt` ([license record](/licenses/mit.md)); derived from WWI OLTP so the Natural Earth/data.gov public-data note applies ([Natural Earth](/licenses/natural-earth-public-domain.md)).

# Open questions
* [Row counts / sizes after restore](/questions/mssql-wideworldimporters-row-counts.md).
* [bacpac readability](/questions/mssql-bacpac-readable-without-sql-server.md).
