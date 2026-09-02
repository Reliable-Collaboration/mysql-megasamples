---
type: Source
title: instawdbdw.sql (AdventureWorksDW install script) - file analysis
description: "Analysis of the current AdventureWorksDW install script (updated 2025-11-14): 31 tables in dbo, 29 pipe-delimited UTF-8 BULK INSERTs, views and functions."
resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/data-warehouse-install-script/instawdbdw.sql
tags: [adventureworks-dw, script-analysis, tsql, bulk-insert]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/data-warehouse-install-script/instawdbdw.sql
    title: instawdbdw.sql at master
    accessed: "2026-09-02"
    version: 'master, 54,095 bytes; header "Date: October 26, 2017 / Updated: November 14, 2025"; commit b47eadc852'
---

# What was read
The full script (54,095 bytes, ASCII, no BOM) plus the GitHub contents listing of `data-warehouse-install-script/` (31 files: 30 CSVs + the script).

# Relevant excerpt
* SQLCMD mode, `:setvar DatabaseName "AdventureWorksDW"`, "Enable full-text search" instruction in the header (no full-text index is actually created in the DW script).
* **All tables are in `dbo`** (31 `CREATE TABLE`): DatabaseLog, AdventureWorksDWBuildVersion, DimAccount, DimCurrency, DimCustomer, DimDate, DimDepartmentGroup, DimEmployee, DimGeography, DimOrganization, DimProduct, DimProductCategory, DimProductSubcategory, DimPromotion, DimReseller, DimSalesReason, DimSalesTerritory, DimScenario, FactAdditionalInternationalProductDescription, FactCallCenter, FactCurrencyRate, FactFinance, FactInternetSales, FactInternetSalesReason, FactProductInventory, FactResellerSales, FactSalesQuota, FactSurveyResponse, NewFactCurrencyRate, ProspectiveBuyer, sysdiagrams.
* **29 BULK INSERT** statements, all `CODEPAGE = '65001'`, `DATAFILETYPE = 'char'`, `FIELDTERMINATOR = '|'`, `ROWTERMINATOR = '\n'` (DatabaseLog.csv and AdventureWorksDWBuildVersion are not bulk loaded by a matching statement in the same pattern; `DatabaseLog.csv` exists in the directory).
* Types: int (98), date (30), money (25), datetime (25), tinyint, smallint, float (10), bit (6), xml (2: DatabaseLog.XmlEvent and a DimProduct/DimEmployee xml column), nvarchar/nchar; **51 IDENTITY** columns; 46 FOREIGN KEY clauses; 0 CHECK constraints; 0 computed columns; 0 procedures.
* Views (5): dbo.vDMPrep, vTimeSeries, vTargetMail, vAssocSeqOrders, vAssocSeqLineItems. Functions (2-3): dbo.udfMinimumDate, dbo.udfTwoDigitZeroFill. One trigger (ddl logging).
* CSV sizes (GitHub API bytes): FactProductInventory 30,300,532; FactResellerSales 13,953,049; FactInternetSales 11,726,880; DimProduct 9,303,851; DimEmployee 9,282,825; DimCustomer 4,462,011; FactFinance 2,265,735; FactCurrencyRate 1,035,663; DimSalesTerritory 878,402; FactInternetSalesReason 777,833; ProspectiveBuyer 374,618; sysdiagrams 358,660; DimDate 353,497; DatabaseLog 330,288; FactAdditionalInternationalProductDescription 275,995; FactSurveyResponse 185,702; DimReseller 119,137; DimGeography 56,424; FactCallCenter 10,853; FactSalesQuota 9,681; DimAccount 5,540; DimPromotion 3,997; DimCurrency 2,104; NewFactCurrencyRate 1,775; DimProductSubcategory 1,546; DimOrganization 388; DimSalesReason 247; DimDepartmentGroup 172; DimProductCategory 130; DimScenario 29. Sum ~86 MB uncompressed; the release zip is 16,765,004 bytes.

# What it was used to decide
[AdventureWorks DW](/datasets/adventureworks-dw.md); [conversion-path decision](/decisions/mssql-adventureworks-conversion-path.md).
