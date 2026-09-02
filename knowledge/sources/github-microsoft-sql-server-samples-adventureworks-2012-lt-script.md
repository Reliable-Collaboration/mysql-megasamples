---
type: Source
title: adventure-works-2012-oltp-lt-script.zip (AdventureWorksLT 2012 install script) - contents
description: Listing and analysis of the only script-plus-CSV form of AdventureWorksLT, taken from the adventureworks2012 release; UTF-16LE script, Windows-1252 (CODEPAGE ACP) CSVs plus one UTF-16 widechar CSV.
resource: https://github.com/microsoft/sql-server-samples/releases/download/adventureworks2012/adventure-works-2012-oltp-lt-script.zip
tags: [adventureworks-lt, script-analysis, encoding]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://github.com/microsoft/sql-server-samples/releases/download/adventureworks2012/adventure-works-2012-oltp-lt-script.zip
    title: adventure-works-2012-oltp-lt-script.zip (937,314 bytes, release adventureworks2012 published 2018-02-28)
    accessed: 2026-09-02
stale_after: 2027-03-01
---

# What was read
The 937,314-byte zip was downloaded into the scratchpad and listed/extracted with Python `zipfile`; `instawltdb.sql` and each CSV were inspected for BOM, encoding, line terminators and row counts.

# Findings
* Contents (uncompressed 2,693,365 bytes) under `AdventureWorks 2012 LT Script/`: `instawltdb.sql` 189,508 (UTF-16LE with BOM `FF FE`, CRLF), `Address.csv` 56,302, `BuildVersion.csv` 66, `Customer.csv` 194,565, `CustomerAddress.csv` 35,092, `Product.csv` 1,352,129, `ProductCategory.csv` 3,138, `ProductDescription.csv` 103,964, `ProductModel.csv` 51,926, `ProductModelProductDescription.csv` 58,690, `SalesOrderDetail.csv` 57,843, `SalesOrderHeader.csv` 8,162, plus `AdventureWorksLT.pdf/.png/.vsd` diagrams.
* Script header: "Creates the AdventureWorksLT 2012 OLTP sample database. Date: June 05, 2012 ... SQL Server Version: 10.0.2531"; `CREATE DATABASE [AdventureWorksLT2012]`; SQLCMD `$(SqlSamplesSourceDataPath)`.
* Schema `SalesLT` + `dbo`. **12 tables**: dbo.ErrorLog, dbo.BuildVersion, SalesLT.{Address, Customer, CustomerAddress, Product, ProductCategory, ProductDescription, ProductModel, ProductModelProductDescription, SalesOrderDetail, SalesOrderHeader}. 3 views (SalesLT.vProductAndDescription, vProductModelCatalogDescription, vGetAllCategories), 3 functions (dbo.ufnGetCustomerInformation, ufnGetSalesOrderStatusText, ufnGetAllCategories), 2 procedures (dbo.uspPrintError, uspLogError), 2 triggers (SalesLT.iduSalesOrderDetail, uSalesOrderHeader), 6 UDTs (AccountNumber, Flag, NameStyle, Name, OrderNumber, Phone), 1 XML schema collection (SalesLT.ProductDescriptionSchemaCollection for ProductModel.CatalogDescription), 3 computed columns (SalesOrderDetail.LineTotal, SalesOrderHeader.SalesOrderNumber, SalesOrderHeader.TotalDue), money and uniqueidentifier columns, no hierarchyid/geography, no full-text.
* **11 BULK INSERTs, all `CODEPAGE = 'ACP'`** (Windows-1252 on a Windows host): 10 with `DATAFILETYPE='char'`, `FIELDTERMINATOR='\t'`, `ROWTERMINATOR='\n'`; ProductModel.csv uses `DATAFILETYPE='widechar'` with `FIELDTERMINATOR='~~\t'` and `ROWTERMINATOR='~~\n'` (XML with embedded newlines).
* CSV encodings measured: `ProductModel.csv` is UTF-16LE with BOM; `Address.csv` (1 non-ASCII char), `Customer.csv` (152), `ProductDescription.csv` (391) are **not valid UTF-8** (consistent with Windows-1252); the rest are pure ASCII. All use CRLF.
* Row counts (CRLF count = rows): Address 450, BuildVersion 1, Customer 847, CustomerAddress 417, Product 295, ProductCategory 41, ProductDescription 762, ProductModel 128, ProductModelProductDescription 762, SalesOrderDetail 542, SalesOrderHeader 32.

# What it was used to decide
[AdventureWorks LT](/datasets/adventureworks-lt.md); [conversion-path decision](/decisions/mssql-adventureworks-conversion-path.md); [LT parity open question](/questions/mssql-adventureworks-lt-script-vs-bak-parity.md).
