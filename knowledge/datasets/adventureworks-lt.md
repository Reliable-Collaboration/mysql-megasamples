---
type: Dataset
title: AdventureWorksLT
description: The lightweight 12-table AdventureWorks (SalesLT schema); shipped as small version-specific .bak files (1.7-14 MB) and, only for the 2012/2008R2 releases, as a script + CSV zip (937 KB) that needs no SQL Server; MIT licensed.
resource: https://github.com/microsoft/sql-server-samples/releases/tag/adventureworks
tags:
- tier-core
- mssql-origin
- csv-load
- mit
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
sources:
- resource: https://api.github.com/repos/microsoft/sql-server-samples/releases/tags/adventureworks
  title: release assets AdventureWorksLT2012..2025.bak
  accessed: "2026-09-02"
- resource: https://github.com/microsoft/sql-server-samples/releases/download/adventureworks2012/adventure-works-2012-oltp-lt-script.zip
  title: adventure-works-2012-oltp-lt-script.zip (937,314 bytes) - listed and inspected
  accessed: "2026-09-02"
- resource: https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure
  title: AdventureWorks sample databases (Learn) - "Lightweight (LT) data is a lightweight and pared down version of the OLTP sample"
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/README.md
  title: adventure-works README.md
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/license.txt
  title: license.txt (MIT)
  accessed: "2026-09-02"
stale_after: "2027-03-01"
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
**Measured on load**: every count above reproduced exactly, and the loaded database is **4.1 MB** in InnoDB (the record inferred < 10 MB). Customer.csv's 152 non-ASCII bytes confirmed by byte count. 122 of the 762 descriptions contain non-ASCII text.
**Upstream data quirk (verified, not a conversion bug)**: Customer 205's last name is the byte `0xA1`, which under the script's own `CODEPAGE='ACP'` is `¡`, giving `Mart¡nez`; the intended `í` would be `0xA1` in CP850, not in Windows-1252. SQL Server loading this script produces the same string, so the conversion reproduces it rather than correcting it.
`ROWTERMINATOR='\n'` in the BULK INSERT clauses matches CRLF in the actual files, which is BULK INSERT's own documented behaviour; splitting on a bare newline leaves a CR on the last column of every row.

# Conversion path
CSV (after iconv) + DDL translated from `instawltdb.sql`, no SQL Server ([decision](/decisions/mssql-adventureworks-conversion-path.md)). Parity with the LT2022/LT2025 .bak content is an [open question](/questions/mssql-adventureworks-lt-script-vs-bak-parity.md); README says 2012-2022 differ only in name/compatibility level, and 2025 shifted dates.

# Type-mapping hazards (as built)
Same family as OLTP but simpler: `money` (4 cols) -> `DECIMAL(19,4)`; `uniqueidentifier` rowguid (8) -> `CHAR(36)`; `xml` `ProductModel.CatalogDescription` (typed by `SalesLT.ProductDescriptionSchemaCollection`) -> `LONGTEXT`; `varbinary(max)` ThumbNailPhoto -> `LONGBLOB` (SQL Server's `MAX` is 2 GB, so the LONG forms are the faithful mapping; both are stored off-page by InnoDB either way); UDTs Name/Phone/AccountNumber/OrderNumber/Flag/NameStyle -> base types; 3 computed columns: `SalesOrderDetail.LineTotal` `DECIMAL(38,6)` and `SalesOrderHeader.TotalDue` `DECIMAL(19,4)` are `GENERATED ... STORED`, and **all 574 generated values were compared against the values the data files ship and match exactly**. `SalesOrderHeader.SalesOrderNumber` cannot be generated — MySQL rejects a generated column that reads an `AUTO_INCREMENT` column — so it is an ordinary `VARCHAR(25)` loaded from the data file, which carries the same `'SO' + SalesOrderID` value. Note that BULK INSERT ignores the data-file fields for computed columns, so the files carry a value for all three; `Customer.PasswordHash/PasswordSalt varchar` base64 text (fine). No hierarchyid/geography. `CHECK` constraints on OrderQty/UnitPrice/Status port verbatim.

# Programmable objects (as built)
All ten are accounted for; `datasets/adventureworks_lt/convert.py` fails the build if the upstream script's object list stops matching, so none can go missing quietly.

* **Views (3), all ported.** `vProductAndDescription` (1,764 rows) and `vGetAllCategories` (37 rows, needs `WITH RECURSIVE` — T-SQL just writes `WITH`) port directly. `vProductModelCatalogDescription` was expected to be stubbed, but **ports after all**: its XQuery `CatalogDescription.value(...)` calls become `ExtractValue(...)`. MySQL's XPath subset has no namespace support and rejects `local-name()`, but it matches a prefixed element name literally, and the catalog documents use exactly the prefixes the queries declare (`p1`, `wm`, `wf`, `html`), so the paths work as written once the `declare namespace` preamble is dropped. A sized result type becomes a `CAST`, matching SQL Server's truncation.
* **Functions (3), one ported.** `ufnGetSalesOrderStatusText` is hand-written in `datasets/adventureworks_lt/objects.sql`. `ufnGetCustomerInformation` and `ufnGetAllCategories` are table-valued, which MySQL does not have; the second returns exactly what `vGetAllCategories` returns, so nothing is lost.
* **Procedures (2), dropped.** `uspLogError` and `uspPrintError` exist to report T-SQL errors — `ERROR_NUMBER()`, `XACT_STATE()`, `PRINT`, `RAISERROR` — and have no MySQL equivalent. Emitting a stub under the same name would be worse than not having them.
* **Triggers (2), ported with two known divergences.** `iduSalesOrderDetail` becomes three row triggers (MySQL takes one event per trigger) that recompute `SalesOrderHeader.SubTotal`. `uSalesOrderHeader` becomes a **BEFORE** UPDATE trigger writing `NEW.RevisionNumber`, because MySQL forbids an AFTER trigger from updating its own table; the effect is the same. T-SQL's `UPDATE(column)` means "the column was in the SET list" whether or not the value changed, which MySQL cannot see, so the port compares values instead. As upstream, the triggers are created after the data is loaded — BULK INSERT does not fire triggers unless asked to.

# Indexing
PKs, FKs, unique `AK_*` indexes and rowguid unique indexes from the script. One index name exceeds MySQL's 64-character limit (`IX_Address_AddressLine1_AddressLine2_City_StateProvince_PostalCode_CountryRegion`, 82) and is truncated with a hash of the full name so the result stays deterministic. SQL Server's index on `vProductAndDescription` is dropped: MySQL has no indexed views.

# Tests and expected values
Row counts above, all **measured**. `SELECT SUM(totaldue) FROM salesorderheader` is **956,303.5949** — the inferred 1,124,180.4489 was the full OLTP figure and is wrong for LT. `SELECT companyname FROM customer WHERE customerid=1` is `A Bike Store`; `LENGTH(thumbnailphoto)` for productid 680 is **2,154**; productdescriptionid 1484 is `Acier chromé.` (the accent probe — note the server collation is accent-insensitive, so a `LIKE '%é%'` probe matches unaccented text and proves nothing; the tests use `REGEXP '[^ -~]'`). 13 smoke queries, 4 plan tests and per-table digests are pinned under `datasets/adventureworks_lt/tests/`.

# Tier assignment
**core**, confirmed: 937 KB download, 4.1 MB loaded.

# License and attribution
MIT via repository `license.txt` ([license record](/licenses/mit.md)); script header carries the Microsoft sample-code copyright and "All data in this database is fictitious".

# Open questions
* [Parity of the 2012 LT script data with LT2022/LT2025 .bak](/questions/mssql-adventureworks-lt-script-vs-bak-parity.md).
