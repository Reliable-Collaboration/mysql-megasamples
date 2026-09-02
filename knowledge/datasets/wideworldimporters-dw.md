---
type: Dataset
title: WideWorldImportersDW
description: The star-schema warehouse companion of WideWorldImporters (Dimension/Fact/Integration schemas, 8 dimensions, 6 facts, table names with spaces), shipped only as .bak/.bacpac (Full with columnstore/partitioning, Standard without); MIT licensed.
resource: https://github.com/microsoft/sql-server-samples/releases/tag/wide-world-importers-v1.0
tags: [tier-extended, mssql-origin, bak-restore, mit, star-schema, multi-schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/releases/tags/wide-world-importers-v1.0
    title: release assets
    accessed: 2026-09-02
  - resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-dw-database-catalog
    title: WideWorldImporters OLAP database catalog (Learn)
    accessed: 2026-09-02
  - resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-dw-install-configure
    title: Install & configure WideWorldImportersDW (Learn)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/wide-world-importers/wwi-dw-ssdt/README.md
    title: wwi-dw-ssdt README and project tree
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/license.txt
    title: license.txt (MIT)
    accessed: 2026-09-02
stale_after: 2027-03-01
---

# Identity
WideWorldImportersDW. Proposed MySQL database name: **`wideworldimporters_dw`**. Schemas Dimension, Fact, Integration (staging), plus Application/Sequences/PowerBI/Reports procedure schemas - see [mapping decision](/decisions/schema-to-database-mapping.md).

# Source artifact
Release `wide-world-importers-v1.0`: `WideWorldImportersDW-Standard.bak` **53,865,472 B** (chosen), `-Full.bak` 50,044,416, `-Standard.bacpac` 22,448,674, `-Full.bacpac` 20,566,783. Learn: "SQL Server 2016 with Service Pack 1 (and later versions) ... To use the full version of the sample, use SQL Server Developer or Enterprise editions." No checksums; pin by asset name + measured sha256.

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
Per-table counts pinned at export; `SUM([Total Including Tax]) FROM Fact.Sale`, `SUM(Quantity) FROM Fact.Movement`, `MAX([Invoice Date Key])` pinned at export; City geography probe as in OLTP.

# Tier assignment
**extended** (needs SQL Server once; ~150 MB loaded, inferred).

# License and attribution
MIT via repository `license.txt` ([license record](/licenses/mit.md)); derived from WWI OLTP so the Natural Earth/data.gov public-data note applies ([Natural Earth](/licenses/natural-earth-public-domain.md)).

# Open questions
* [Row counts / sizes after restore](/questions/mssql-wideworldimporters-row-counts.md).
* [bacpac readability](/questions/mssql-bacpac-readable-without-sql-server.md).
