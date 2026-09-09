---
type: Dataset
title: AdventureWorks (OLTP)
description: Microsoft's flagship 68-table, 5-schema OLTP sample (bicycle manufacturer); available as version-specific .bak files and as a SQLCMD install script plus 69 UTF-8 CSV files (~95 MB) that need no SQL Server to read; MIT licensed.
resource: https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/adventure-works/oltp-install-script
tags:
- tier-core-medium
- mssql-origin
- csv-load
- mit
- multi-schema
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/oltp-install-script/instawdb.sql
  title: instawdb.sql (Updated November 14, 2025)
  accessed: "2026-09-02"
  version: master, commit b47eadc852 (2025-11-14)
- resource: https://api.github.com/repos/microsoft/sql-server-samples/contents/samples/databases/adventure-works/oltp-install-script
  title: directory listing with CSV sizes; 46 small CSVs read in full, 5 large ones sampled by HTTP range
  accessed: "2026-09-02"
- resource: https://api.github.com/repos/microsoft/sql-server-samples/releases/tags/adventureworks
  title: release assets (.bak sizes, AdventureWorks-oltp-install-script.zip 17,486,641 bytes)
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/README.md
  title: adventure-works README.md
  accessed: "2026-09-02"
- resource: https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure
  title: AdventureWorks sample databases (Learn)
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/license.txt
  title: license.txt (MIT)
  accessed: "2026-09-02"
stale_after: "2027-03-01"
---

# Identity
AdventureWorks OLTP (Adventure Works Cycles). Proposed MySQL database name: **`adventureworks`**; schema mapping per [decision](/decisions/schema-to-database-mapping.md) (accepted: lower-cased schema-prefixed names such as `sales_salesorderheader` inside one database).

# Source artifact
Two upstream forms, both MIT, no auth, no click-through, no published checksums:
1. **Install script + CSV (chosen)**: `samples/databases/adventure-works/oltp-install-script/` at commit `b47eadc852` (2025-11-14, "AdventureWorks 2025 updates"): `instawdb.sql` (329,368 bytes, UTF-8 BOM) + 69 CSVs, ~95 MB uncompressed (largest: SalesOrderDetail.csv 13,727,911; Person.csv 13,565,030; WorkOrderRouting.csv 10,598,429; TransactionHistory.csv 8,937,794; WorkOrder.csv 8,239,894; SalesOrderHeader.csv 7,899,987; TransactionHistoryArchive.csv 6,928,414; ProductPhoto.csv 4,022,001; Address.csv 2,942,518). Same content zipped as release asset `AdventureWorks-oltp-install-script.zip` (17,486,641 bytes). Pin by commit SHA. This form produces the **2025 edition**: `AWBuildVersion` = `17.0.1000.3`, dates shifted (e.g. first SalesOrderHeader OrderDate 2022-05-30, Product SellStartDate 2019-04-30) per the README's "Dates have been adjusted".
2. **.bak backups** (release tag `adventureworks`): AdventureWorks2025.bak 50,229,248 B; 2022 209,838,080; 2019 208,789,504; 2017 50,286,592; 2016 48,749,568 (+2016_EXT 131,107,840); 2014 46,759,936; 2012 47,078,400; 2008R2 189,906,944 (tag `adventureworks2008r2`). Require SQL Server to restore. README: "The only differences between the various versions of AdventureWorks [2012-2022] are the name of the database and the database compatibility level."

# Native format and friendlier forms
The friendlier form exists and is current: plain UTF-8 CSVs loaded by `BULK INSERT ... CODEPAGE='65001', DATAFILETYPE='char'`. Terminators (verified per table): 51 tables tab-delimited with LF rows (`ROWTERMINATOR '0x0a'` or `'\n'`); 14 tables use field terminator `+|` and row terminator `&|\n` because their fields contain newlines/XML/binary: JobCandidate, BusinessEntity, BusinessEntityAddress, BusinessEntityContact, EmailAddress, Password, Person, PersonPhone, PhoneNumberType, Document, Illustration, ProductModel, ProductPhoto, Store. MySQL `LOAD DATA LOCAL INFILE ... FIELDS TERMINATED BY '+|' LINES TERMINATED BY '&|\n'` handles both directly (multi-character terminators are allowed). Empty field = NULL (`KEEPNULLS` semantics: use `NULLIF` in `SET` clauses or `FIELDS ... ESCAPED BY ''` + post-fix). No quoting anywhere; no `\` escapes (must set `ESCAPED BY ''`).

# Shape
5 schemas (HumanResources, Person, Production, Purchasing, Sales) + dbo (AWBuildVersion, DatabaseLog, ErrorLog): 71 tables. Row counts:
**Built and measured 2026-09-03**: 69 tables (71 upstream, less `DatabaseLog` and `ErrorLog`, which the naming decision drops), **759,240 rows**, **162 MB** in InnoDB, loading in 14 s; 91 foreign keys with 0 orphans; 14 smoke queries and 5 plan tests pinned. Every one of the 45 counts verified during research reproduced exactly on the first load, and the previously unknown ones are now in `datasets/adventureworks/tests/expected_counts.yaml` — SalesOrderDetail 121,317; SalesOrderHeader 31,465; TransactionHistory 113,443; TransactionHistoryArchive 89,253; WorkOrder 72,591; WorkOrderRouting 67,131; SalesOrderHeaderSalesReason 27,647; Person/EmailAddress/PersonPhone/Password 19,972 each; BusinessEntity 20,777; Address and BusinessEntityAddress 19,614; Customer 19,820; CreditCard and PersonCreditCard 19,118; CurrencyRate 13,532; PurchaseOrderDetail 8,845; PurchaseOrderHeader 4,012; Store 701; ProductPhoto 101; Document 12; Illustration 5 ([row-count question](/questions/mssql-adventureworks-row-counts.md), now answered).

**How the data files are actually read.** BULK INSERT does not split a file into lines and then into fields: it reads field by field, and only the *last* field of a row ends at the row terminator. That is why `ProductReview.csv` is 4 rows despite 34 physical lines — the comments contain newlines and sit in the 7th of 8 columns — and it is the same mechanism that makes the 14 `+|` / `&|\n` tables work. Two further details of the format matter: a `ROWTERMINATOR` of `\n` means `\r\n` in the files that are CRLF, and a field holding a single NUL byte is the empty string rather than NULL (5 fields in `Document.csv` depend on it, including the root hierarchyid).

* Verified from the CSVs (small tables): AddressType 6, BillOfMaterials 2,679, BusinessEntityContact 909, ContactType 20, CountryRegion 238, CountryRegionCurrency 109, Culture 8, Currency 105, Department 16, Employee 290, EmployeeDepartmentHistory 296, EmployeePayHistory 316, JobCandidate 13, Location 14, PhoneNumberType 3, Product 504, ProductCategory 4, ProductCostHistory 395, ProductDescription 762, ProductDocument 32, ProductInventory 1,069, ProductListPriceHistory 395, ProductModel 128, ProductModelIllustration 7, ProductModelProductDescriptionCulture 762, ProductProductPhoto 504, ProductSubcategory 37, ProductVendor 460, SalesPerson 17, SalesPersonQuotaHistory 163, SalesReason 10, SalesTaxRate 29, SalesTerritory 10, SalesTerritoryHistory 17, ScrapReason 16, Shift 3, ShipMethod 5, ShoppingCartItem 3, SpecialOffer 16, SpecialOfferProduct 538, StateProvince 181, UnitMeasure 38, Vendor 104, AWBuildVersion 1. ProductReview.csv has 34 physical lines for what is documented as 4 rows (comments contain newlines but the file is tab/`0x0a` - see open question).
* **Inferred (from memory of the canonical 2014+ database, unchanged in row count by the 2025 date shift):** SalesOrderDetail 121,317; SalesOrderHeader 31,465; SalesOrderHeaderSalesReason 27,647; Person 19,972; EmailAddress 19,972; PersonPhone 19,972; Password 19,972; BusinessEntity 20,777; BusinessEntityAddress 19,614; Address 19,614; Customer 19,820; CreditCard 19,118; PersonCreditCard 19,118; CurrencyRate 13,532; TransactionHistory 113,443; TransactionHistoryArchive 89,253; WorkOrder 72,591; WorkOrderRouting 67,131; PurchaseOrderDetail 8,845; PurchaseOrderHeader 4,012; Store 701; ProductPhoto 101; Document 13; Illustration 5; DatabaseLog and ErrorLog 0 at load. Total ~750k rows. Baseline: count rows in the CSVs (`grep -c '&|$'` for the 14 special files, `wc -l` otherwise) - [open question](/questions/mssql-adventureworks-row-counts.md).
* Size: CSV 95 MB; **Inferred** InnoDB ~180-250 MB with indexes (ProductPhoto/Document binary ~5 MB, XML text ~30 MB).
* Encoding: UTF-8, no BOM, LF. Non-ASCII in Person (`Sánchez`), CountryRegion (4 rows), StateProvince (21), Employee (2), JobCandidate (24), ProductDescription (114 rows: French `Acier chromé.`, `axe de grand diamètre`, `manœuvrer`, plus Arabic/Chinese/Hebrew/Thai descriptions - the file has cultures ar, fr, he, th, zh-cht in Culture.csv (8 rows)).

# Conversion path
CSV + DDL translated from `instawdb.sql`, loaded with `LOAD DATA LOCAL INFILE`; no SQL Server. See [decision](/decisions/mssql-adventureworks-conversion-path.md). Fallback for the three exotic column types is a one-off SQL Server round-trip (or the documented binary decoders).

# Routines ported (2026-09-04, task V-02)
`megasamples/sources/tsqlbody.py` translates the routine bodies. Of this database's 31 routines, **16 are
created and accepted by MySQL** -- 10 functions and 6 procedures -- and 15 are refused, each with a
reason the converter prints. Nothing is emitted on a guess.

Verified by calling them, not by their creating: `ufnLeadingZeros(42)` is `00000042`,
`ufnGetStock(1)` is 324 against the loaded inventory, and for product 707 on 2023-06-01 the standard
cost is 13.8782, the list price 33.6442 and the dealer price 20.1865 -- exactly 60% of list, which is
what the function's own constant says.

**Refused, with reasons**: all 11 triggers (2 are `INSTEAD OF`; 3 aggregate over the
`inserted`/`deleted` pseudo-tables, which a MySQL row trigger cannot express; 3 control a
transaction, which MySQL forbids inside a trigger with error 1422; 2 call XML methods; 1 is a DDL
trigger on the database), `uspLogError` (calls `ERROR_*()`), `ufnGetContactInformation` (returns a
table), and `uspGetEmployeeManagers`/`uspGetManagerEmployees` (call hierarchyid methods -- the decoded
`*_path` columns are the MySQL equivalent, and porting them to recursive CTEs is separate work).

**A note on precision.** T-SQL `datetime` keeps milliseconds and these routines rely on it:
`ufnGetAccountingEndDate` is `DATEADD(ms, -2, ...)`, which a MySQL `DATETIME` with no fractional
digits rounds straight back up to the next day. Routine types widen to `DATETIME(3)`; columns are
unchanged. The function now returns `2004-06-30 23:59:59.998`.

# Type-mapping hazards
* **hierarchyid** (three columns: Employee.OrganizationNode, Document.DocumentNode, ProductDocument.DocumentNode). **As built**: the raw bytes stay in a `VARBINARY(892)` column and a decoded `<column>_path VARCHAR(300)` sits beside it, written by `megasamples/sources/hierarchyid.py`. No SQL Server round-trip was needed — the decoder is checked against every row instead: all 290 employee paths have the depth the shipped `OrganizationLevel` states, all 290 re-encode to their original bytes, and every parent path exists. `GetLevel()` becomes the materialised level column from the data file.
* **geography** (Person.Address.SpatialLocation). **As built**: `POINT SRID 4326`, decoded from the 22-byte serialization (SRID, version, flags, then latitude and longitude as little-endian doubles) and loaded with `ST_GeomFromText(..., 4326)`. Address 1 is 47.7869921906598, -122.164644615406 — Bothell, WA, as the row says — and all 19,614 points carry a latitude inside [-90, 90]. MySQL's axis order for 4326 was [measured](/sources/mysql-9-7-srid-4326-axis-order-probe.md), not assumed.
* **xml** (Person.Person.AdditionalContactInfo/Demographics, JobCandidate.Resume, ProductModel.CatalogDescription/Instructions, Store.Demographics, Illustration.Diagram, DatabaseLog.XmlEvent): -> `LONGTEXT`/`MEDIUMTEXT`; XML schema collections and primary XML indexes dropped; XQuery-based views (vAdditionalContactInfo, vJobCandidate*, vProductModelCatalogDescription, vProductModelInstructions, vStoreWithDemographics, vPersonDemographics, vIndividualCustomer) cannot be ported as-is (MySQL has only `ExtractValue`).
* **money/smallmoney** (48 columns) -> `DECIMAL(19,4)` / `DECIMAL(10,4)`; `uniqueidentifier` (29 rowguid) -> `CHAR(36)` (or `BINARY(16)`); `varbinary(max)` -> `LONGBLOB` (hex in CSV -> `UNHEX()` in `SET`); `datetime` -> `DATETIME(3)`; `time(7)` (Shift) -> `TIME(6)`; `bit`/`Flag`/`NameStyle` -> `TINYINT(1)`; UDTs `Name`, `Phone`, `AccountNumber`, `OrderNumber` -> `VARCHAR(50/25/15/25)`.
* **Computed columns (10)** -> MySQL generated columns where deterministic: `SalesOrderDetail.LineTotal`, `SalesOrderHeader.TotalDue`, `SalesOrderNumber`, `PurchaseOrderDetail.LineTotal/StockedQty`, `PurchaseOrderHeader.TotalDue`, `WorkOrder.StockedQty` as `GENERATED ALWAYS AS (...) STORED`; `Customer.AccountNumber` uses a UDF (`ufnLeadingZeros`) -> inline `CONCAT('AW', LPAD(CustomerID, 8, '0'))` (**inferred** semantics of ufnLeadingZeros = 8 digits); `GetLevel()` ones -> stored plain columns. Note the CSVs include placeholder fields for computed columns in the `+|` files; `LOAD DATA` must map them to user variables and ignore them.
* 89 CHECK constraints port mostly verbatim (range/`IN` checks); those using `LIKE '[A-Z]...'` classes (e.g. `CountryRegionCode`, `AccountNumber` patterns) need `REGEXP`.
* Table/column names are mixed case upstream; the coordinator's [naming convention](/decisions/database-naming-convention.md) lower-cases them with a schema prefix (`sales_salesorderheader`), so every ported view/procedure/trigger body must be rewritten case-consistently (Linux MySQL is case-sensitive for table names by default).

# Programmable objects
* Views (20): port the join-only ones (vEmployee, vEmployeeDepartment, vEmployeeDepartmentHistory, vSalesPerson, vSalesPersonSalesByFiscalYears (uses `PIVOT` - rewrite with conditional aggregation), vStateProvinceCountryRegion, vStoreWithContacts, vStoreWithAddresses, vVendorWithContacts, vVendorWithAddresses, vProductAndDescription); **stub/drop** the XQuery ones listed above with a comment.
* Functions (11): port scalar ones (`ufnLeadingZeros`, `ufnGetAccountingStartDate/EndDate`, `ufnGetProductDealerPrice/ListPrice/StandardCost`, `ufnGetStock`, `ufnGet*StatusText`); `ufnGetContactInformation` is a table-valued function -> drop (MySQL has no TVFs) or replace with a view.
**Not yet ported (2026-09-03)**: the 10 procedures, 11 functions and 8 remaining triggers. Their T-SQL bodies (`@parameters`, `RETURNS ... AS BEGIN`, the `inserted`/`deleted` pseudo-tables, `RAISERROR`) need a routine translator that does not exist yet; the converter names each one it skips rather than emitting something broken. Six views are dropped for the same honesty reason — four use XML `.nodes()`, one `PIVOT` — leaving 13 of 20 ported, including the two that read the store and product XML through `ExtractValue`. The plan below is unchanged and stands as the specification for that work.

* Procedures (10): port `uspGetBillOfMaterials`, `uspGetWhereUsedProductID`, `uspGetEmployeeManagers`, `uspGetManagerEmployees` using recursive CTEs (they use hierarchyid `IsDescendantOf` - rewrite against the decoded path); `uspLogError`/`uspPrintError` (use `ERROR_*()` functions) -> stub; `uspSearchCandidateResumes` (full-text on XML) -> drop; `uspUpdateEmployee*` -> port with `SIGNAL`.
* Triggers (11): port `iuPerson`, `uSalesOrderHeader` (recalculates `SalesYTD`), `iduSalesOrderDetail`, `uPurchaseOrderHeader`, `iPurchaseOrderDetail`, `uPurchaseOrderDetail`, `iWorkOrder`, `uWorkOrder` as row-level triggers (T-SQL ones are statement-level with `inserted`/`deleted` - semantics change on multi-row DML); `dEmployee` and `dVendor` are INSTEAD OF DELETE triggers (MySQL has none) -> drop and document; `ddlDatabaseTriggerLog` (DDL trigger) -> drop.
* Full-text: `FULLTEXT` index on ProductReview(Comments) ports to InnoDB FULLTEXT; the XML/varbinary full-text indexes (JobCandidate.Resume, Document.Document) are dropped.
* 538 `MS_Description` extended properties -> `COMMENT` clauses on tables/columns (fits MySQL's 1024/2048-char limits).

# Indexing
Port PKs, 170 FKs, 59 unique indexes (rowguid, AK_ names), the nonclustered indexes from the script; drop XML/spatial/full-text-XML indexes. Add a `SPATIAL INDEX` on the converted POINT column only if it is NOT NULL (MySQL requirement) - it is nullable, so skip.

# Tests and expected values
* Row counts per table (verified list above; inferred list to be replaced by CSV counts).
* `SELECT SUM(totaldue) FROM sales_salesorderheader` and `SUM(linetotal) FROM sales_salesorderdetail` computed from the loaded data and pinned as checksums after first load (**Inferred** classic values: 123,216,786.1159 and 109,846,381.4 - the 2025 edition kept amounts, only dates moved, but do not trust without measuring).
* Encoding probe: `SELECT lastname FROM person_person WHERE businessentityid=1` = `Sánchez`; ProductDescription rows for culture `fr` contain `chromé`; culture `zh-cht`/`ar`/`th` rows must round-trip (4-byte-safe utf8mb4).
* hierarchyid probe: Employee 2's decoded path = `/1/`, level 1; Employee 3 = `/1/1/`.

# Tier assignment
**core (medium)** per [tier assignments](/decisions/tier-assignments.md): 95 MB of CSV, **Inferred** 180–250 MB loaded, inside the medium-core band because it is the one "big classic" that needs no SQL Server. It is the first dataset moved to extended if the measured core data directory exceeds 3 GB (task E-01).

# License and attribution
MIT, repository `license.txt` ([license record](/licenses/mit.md)); the script header adds "Copyright (C) Microsoft Corporation. All rights reserved. ... All data in this database is fictitious." Attribution string: "AdventureWorks sample database, Copyright (c) Microsoft Corporation, MIT License (https://github.com/microsoft/sql-server-samples/blob/master/license.txt)". No share-alike, no real personal data.

# Open questions
* [Big-table row counts and ProductReview line-count anomaly](/questions/mssql-adventureworks-row-counts.md).
* Decoding hierarchyid and geography binary without SQL Server (covered in the same question record; fallback is the [SQL Server container](/tools/mssql-server-container.md)).
* Whether to ship the 2025 (date-shifted) edition or an older 2014-style dataset (the .bak route) - the CSV form only exists for 2025; recommend 2025 and state it in the README.
