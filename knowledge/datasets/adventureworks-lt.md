---
type: Dataset
title: AdventureWorksLT
description: The lightweight 12-table AdventureWorks (SalesLT schema); shipped as small version-specific .bak files (1.7-14 MB) and, only for the 2012/2008R2 releases, as a script + CSV zip (937 KB) that needs no SQL Server; MIT licensed.
resource: https://github.com/microsoft/sql-server-samples/releases/tag/adventureworks
tags: [tier-core, mssql-origin, csv-load, mit]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/releases/tags/adventureworks
    title: release assets AdventureWorksLT2012..2025.bak
    accessed: 2026-09-02
  - resource: https://github.com/microsoft/sql-server-samples/releases/download/adventureworks2012/adventure-works-2012-oltp-lt-script.zip
    title: adventure-works-2012-oltp-lt-script.zip (937,314 bytes) - listed and inspected
    accessed: 2026-09-02
  - resource: https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure
    title: AdventureWorks sample databases (Learn) - "Lightweight (LT) data is a lightweight and pared down version of the OLTP sample"
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/README.md
    title: adventure-works README.md
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/license.txt
    title: license.txt (MIT)
    accessed: 2026-09-02
stale_after: 2027-03-01
---

# Identity
AdventureWorksLT (schema `SalesLT` + `dbo`). Proposed MySQL database name: **`adventureworks_lt`**; with a single data schema the prefix question is moot (recommend dropping the `SalesLT_` prefix, see [mapping decision](/decisions/schema-to-database-mapping.md)).

# Source artifact
* `.bak` on release `adventureworks` (no auth, no checksums): LT2025 1,765,376 B; LT2022 8,511,488; LT2019 8,511,488; LT2017 7,458,816; LT2016 7,458,816; LT2014 13,983,744; LT2012 14,077,952; plus `adventure-works-2008r2-lt.bak` 6,406,144 on tag `adventureworks2008r2`.
* Script form (chosen): `https://github.com/microsoft/sql-server-samples/releases/download/adventureworks2012/adventure-works-2012-oltp-lt-script.zip` (937,314 bytes; 2,693,365 uncompressed) containing `instawltdb.sql` (UTF-16LE BOM, CRLF, "Creates the AdventureWorksLT 2012 OLTP sample database ... June 05, 2012") and 11 CSVs. A near-identical `adventure-works-2008r2-lt-script.zip` (937,692 bytes) exists on the 2008R2 tag. The current `adventureworks` tag has **no LT script**.

# Native format and friendlier forms
The 2012 zip is the SQL-Server-free form. Its CSVs are **not UTF-8**: 10 files are loaded with `CODEPAGE='ACP'` (Windows-1252; Customer.csv has 152 non-ASCII characters, ProductDescription.csv 391, Address.csv 1) and `ProductModel.csv` is UTF-16LE with BOM loaded as `widechar` with terminators `~~\t` / `~~\n` (XML with embedded newlines). All rows are CRLF-terminated. Convert with `iconv -f WINDOWS-1252 -t UTF-8` and `iconv -f UTF-16LE -t UTF-8` (strip BOM) before `LOAD DATA`.

# Shape
12 tables: dbo.BuildVersion, dbo.ErrorLog, SalesLT.Address, Customer, CustomerAddress, Product, ProductCategory, ProductDescription, ProductModel, ProductModelProductDescription, SalesOrderDetail, SalesOrderHeader. Row counts **verified from the 2012 zip CSVs**: Address 450, BuildVersion 1, Customer 847, CustomerAddress 417, Product 295, ProductCategory 41, ProductDescription 762, ProductModel 128, ProductModelProductDescription 762, SalesOrderDetail 542, SalesOrderHeader 32 (ErrorLog 0). Product.csv is 1.35 MB because `ThumbNailPhoto varbinary(max)` is inline hex. Loaded size **Inferred** < 10 MB.
Encoding probes: Customer names/companies with Windows-1252 accents; ProductDescription in fr/ar/he/th/zh (same text as the OLTP ProductDescription table, 762 rows).

# Conversion path
CSV (after iconv) + DDL translated from `instawltdb.sql`, no SQL Server ([decision](/decisions/mssql-adventureworks-conversion-path.md)). Parity with the LT2022/LT2025 .bak content is an [open question](/questions/mssql-adventureworks-lt-script-vs-bak-parity.md); README says 2012-2022 differ only in name/compatibility level, and 2025 shifted dates.

# Type-mapping hazards
Same family as OLTP but simpler: `money` (4 cols) -> `DECIMAL(19,4)`; `uniqueidentifier` rowguid (8) -> `CHAR(36)`; `xml` `ProductModel.CatalogDescription` (typed by `SalesLT.ProductDescriptionSchemaCollection`) -> `MEDIUMTEXT`; `varbinary(max)` ThumbNailPhoto -> `MEDIUMBLOB`; UDTs Name/Phone/AccountNumber/OrderNumber/Flag/NameStyle -> base types; 3 computed columns (`SalesOrderDetail.LineTotal`, `SalesOrderHeader.SalesOrderNumber`, `TotalDue`) -> `GENERATED ... STORED`; `Customer.PasswordHash/PasswordSalt varchar` base64 text (fine). No hierarchyid/geography. `CHECK` constraints on OrderQty/UnitPrice/Status port verbatim.

# Programmable objects
Views (3): `vProductAndDescription` (port), `vGetAllCategories` (recursive CTE - port), `vProductModelCatalogDescription` (XQuery over CatalogDescription - stub/drop). Functions (3): `ufnGetSalesOrderStatusText` (port), `ufnGetAllCategories` (table-valued, recursive - replace by the view), `ufnGetCustomerInformation` (TVF - drop). Procedures: `uspLogError`, `uspPrintError` -> stub. Triggers (2): `iduSalesOrderDetail` (maintains SalesOrderHeader.SubTotal) and `uSalesOrderHeader` (sets RevisionNumber/ModifiedDate) -> port as row triggers.

# Indexing
PKs, FKs, unique `AK_*` indexes and rowguid unique indexes from the script.

# Tests and expected values
Row counts above; `SELECT SUM(TotalDue) FROM SalesOrderHeader` pinned after load (**Inferred** classic 1,124,180.4489 (approx.) - measure); probe `SELECT CompanyName FROM Customer WHERE CustomerID=1` and a `fr` ProductDescription row for accents; `LENGTH(ThumbNailPhoto)` for ProductID 680.

# Tier assignment
**core**: <1 MB download, <10 MB loaded.

# License and attribution
MIT via repository `license.txt` ([license record](/licenses/mit.md)); script header carries the Microsoft sample-code copyright and "All data in this database is fictitious".

# Open questions
* [Parity of the 2012 LT script data with LT2022/LT2025 .bak](/questions/mssql-adventureworks-lt-script-vs-bak-parity.md).
