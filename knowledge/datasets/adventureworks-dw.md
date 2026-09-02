---
type: Dataset
title: AdventureWorksDW
description: The AdventureWorks star-schema data warehouse (31 dbo tables, dimension/fact naming), available as .bak files or as a SQLCMD install script with 30 pipe-delimited UTF-8 CSVs (~86 MB); MIT licensed.
resource: https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/adventure-works/data-warehouse-install-script
tags: [tier-extended, mssql-origin, csv-load, mit, star-schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/data-warehouse-install-script/instawdbdw.sql
    title: instawdbdw.sql (Updated November 14, 2025)
    accessed: "2026-09-02"
    version: master, commit b47eadc852
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/contents/samples/databases/adventure-works/data-warehouse-install-script
    title: directory listing (30 CSVs with sizes)
    accessed: "2026-09-02"
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/releases/tags/adventureworks
    title: release assets (AdventureWorksDW*.bak, AdventureWorksDW-data-warehouse-install-script.zip 16,765,004 bytes)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/license.txt
    title: license.txt (MIT)
    accessed: "2026-09-02"
stale_after: "2027-03-01"
---

# Identity
AdventureWorksDW. Proposed MySQL database name: **`adventureworks_dw`**. All tables are in `dbo`, so no schema prefix is needed (tables keep their `Dim*`/`Fact*` names).

# Source artifact
* Chosen: `samples/databases/adventure-works/data-warehouse-install-script/` at commit `b47eadc852` (2025-11-14): `instawdbdw.sql` (54,095 bytes, ASCII) + 30 CSVs, ~86 MB uncompressed; zip form `AdventureWorksDW-data-warehouse-install-script.zip` 16,765,004 bytes. No auth, no checksum published.
* Alternative .bak (release `adventureworks`): DW2025 25,305,088 B; DW2022 101,834,752; DW2019 101,834,752; DW2017 23,436,800; DW2016 22,484,480 (+DW2016_EXT 926,232,064); DW2014 22,450,176; DW2012 22,822,912; 2008R2 77,709,312.

# Native format and friendlier forms
Friendly form exists: every CSV is loaded with `CODEPAGE='65001', DATAFILETYPE='char', FIELDTERMINATOR='|', ROWTERMINATOR='\n'` (verified for all 29 BULK INSERTs). **Inferred:** files are LF-terminated UTF-8 like the OLTP set (not sampled individually; DimProduct/DimEmployee carry `varbinary` photos and an xml column as hex/inline text). `LOAD DATA ... FIELDS TERMINATED BY '|' ESCAPED BY '' LINES TERMINATED BY '\n'`.

# Shape
31 tables: DatabaseLog, AdventureWorksDWBuildVersion, DimAccount, DimCurrency, DimCustomer, DimDate, DimDepartmentGroup, DimEmployee, DimGeography, DimOrganization, DimProduct, DimProductCategory, DimProductSubcategory, DimPromotion, DimReseller, DimSalesReason, DimSalesTerritory, DimScenario, FactAdditionalInternationalProductDescription, FactCallCenter, FactCurrencyRate, FactFinance, FactInternetSales, FactInternetSalesReason, FactProductInventory, FactResellerSales, FactSalesQuota, FactSurveyResponse, NewFactCurrencyRate, ProspectiveBuyer, sysdiagrams (drop sysdiagrams - SSMS artefact).
Row counts - **Inferred from memory of AdventureWorksDW2014+; the 2025 edition shifted dates only**: FactInternetSales 60,398; FactResellerSales 60,855; FactProductInventory 776,286; FactInternetSalesReason 64,515; FactFinance 39,409; FactCurrencyRate 14,264; FactSalesQuota 3,455; FactSurveyResponse 2,727; FactCallCenter 120; FactAdditionalInternationalProductDescription 15,168; DimCustomer 18,484; DimProduct 606; DimDate 3,652; DimEmployee 296; DimReseller 701; DimGeography 655; DimCurrency 105; DimAccount 99; DimPromotion 16; DimSalesTerritory 11; DimProductSubcategory 37; DimProductCategory 4; DimSalesReason 10; DimScenario 3; DimDepartmentGroup 7; DimOrganization 14; ProspectiveBuyer 2,059; NewFactCurrencyRate ~50. Baseline: `wc -l` per CSV (single-line rows; no multi-line terminators are used in the DW script). Size: CSV 86 MB (FactProductInventory.csv alone 30.3 MB); **Inferred** ~150 MB loaded.
Encoding: **Inferred** UTF-8 (script says 65001); DimProduct has multilingual product names (French/Spanish/Arabic/Chinese/Hebrew/Thai columns `FrenchProductName`, `SpanishProductName` and FactAdditionalInternationalProductDescription rows) - good utf8mb4 probes.

# Conversion path
Same as OLTP: CSV + translated DDL, no SQL Server ([decision](/decisions/mssql-adventureworks-conversion-path.md)).

# Type-mapping hazards
* 25 `money` columns -> `DECIMAL(19,4)`; `float` (10) -> `DOUBLE`; `datetime` (25) -> `DATETIME`; `date` (30) -> `DATE`; `bit` -> `TINYINT(1)`; `nchar/nvarchar` -> utf8mb4; `xml` (2: DatabaseLog.XmlEvent, and one in DimProduct/DimEmployee - verify) -> `TEXT`; `varbinary(max)` photos -> `LONGBLOB` via `UNHEX`.
* 51 `IDENTITY` columns -> `AUTO_INCREMENT` with explicit values loaded (no IDENTITY_INSERT needed in MySQL).
* No CHECK constraints, no computed columns; 46 FKs port verbatim (load dimensions before facts or disable FK checks).
* DimDate has many date-part columns; `FactInternetSales` has a composite PK (SalesOrderNumber, SalesOrderLineNumber).

# Programmable objects
* Views (5): vDMPrep, vTimeSeries, vTargetMail, vAssocSeqOrders, vAssocSeqLineItems - data-mining prep views using `CASE`/`DATEPART`/`CONVERT`; port with `DATE_FORMAT`/`YEAR()` rewrites.
* Functions: `udfMinimumDate`, `udfTwoDigitZeroFill` -> port (trivial scalar).
* One DDL trigger (`ddlDatabaseTriggerLog`) -> drop.

# Indexing
PKs and 46 FKs from the script; add the script's nonclustered indexes if any (few). Consider `FactProductInventory` (776k rows) PK (ProductKey, DateKey).

# Tests and expected values
Row counts per CSV (measure); `SUM(SalesAmount)` over FactInternetSales (**Inferred** classic 29,358,677.2207) and FactResellerSales (**Inferred** 80,450,596.9823) pinned after first load; encoding probe on DimProduct `FrenchProductName`/`ArabicDescription` columns.

# Tier assignment
**extended**: 86 MB CSV / **Inferred** ~150 MB loaded.

# License and attribution
MIT via repository `license.txt` ([license record](/licenses/mit.md)); script header "Copyright (C) Microsoft Corporation ... All data in this database is ficticious [sic]." Attribution as for the OLTP database.

# Open questions
* Row counts and per-file encoding sampling for the DW CSVs (same experiment as [the OLTP question](/questions/mssql-adventureworks-row-counts.md)).
