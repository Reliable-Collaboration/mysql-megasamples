---
type: Source
title: AdventureWorks oltp-install-script CSV files - sampling and row counts
description: Direct inspection of 46 small CSV data files (about 1 MB total) and ranged reads of the large ones to establish encoding, terminators, binary/XML/hierarchyid/geography serialisation and exact row counts for the small tables.
resource: https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/adventure-works/oltp-install-script
tags:
- adventureworks
- csv
- encoding
- row-counts
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://api.github.com/repos/microsoft/sql-server-samples/contents/samples/databases/adventure-works/oltp-install-script
  title: GitHub contents listing (70 files with sizes)
  accessed: "2026-09-02"
  version: master, commit b47eadc852 (2025-11-14)
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/oltp-install-script/AWBuildVersion.csv
  title: AWBuildVersion.csv and 45 other small CSVs (full reads); Address.csv, Person.csv, ProductPhoto.csv, Document.csv, SalesOrderHeader.csv (HTTP range 0-1500 bytes only)
  accessed: "2026-09-02"
---

# What was read
Full downloads of the CSVs under ~100 KB (46 files, 1,046,089 bytes total) and HTTP range requests (first 0.4-1.5 KB) of Address.csv, Person.csv, ProductPhoto.csv, Document.csv, SalesOrderHeader.csv. HEAD requests confirmed Content-Length of the big files: Person.csv 13,565,030; SalesOrderDetail.csv 13,727,911; SalesOrderHeader.csv 7,899,987; TransactionHistory.csv 8,937,794; WorkOrderRouting.csv 10,598,429. Sum of all 69 CSV sizes from the API listing is about 95 MB.

# Relevant excerpt
* **Encoding**: every sampled file is valid UTF-8 without BOM, LF-only line endings (0 CRLF). `file` reports ASCII for files without accents. Non-ASCII present in CountryRegion.csv (4 lines), StateProvince.csv (21), Employee.csv (2), JobCandidate.csv (24), ProductDescription.csv (114 lines, e.g. `Acier chromé.`, `Cuvettes en alliage d'aluminium ; axe de grand diamètre.`, `Vif et facile à manœuvrer` - French, and other cultures), Person.csv (`Sánchez` in row 1). This contradicts older knowledge that the files are UTF-16LE: the 2023 commits were "Update line endings for UTF-16 LE encoded files", and the 2025-11-14 commit re-encoded them to UTF-8 (`CODEPAGE = '65001'` in the script).
* **AWBuildVersion.csv** (one row): `1\t17.0.1000.3\t2025-10-06 21:25:57.990\t2025-11-14 12:13:16.797\n` - i.e. the repository script produces the **SQL Server 2025 (17.0) edition of AdventureWorks** with shifted dates (SalesOrderHeader row 43659 has OrderDate `2022-05-30`; Product row 1 SellStartDate `2019-04-30`; Department ModifiedDate `2008-04-30` unchanged).
* **hierarchyid is serialised as its binary hex form without `0x`**: Employee.csv rows 1-6 show OrganizationNode empty (root `/`), `58` (`/1/`), `5AC0`, `5AD6`, `5ADA`, `5ADE`, followed by a placeholder column for the computed OrganizationLevel (0..3). Document.csv likewise starts with ` ` (root) then `58`, `5AC0`. **Inferred:** decoding these to path strings needs the hierarchyid binary format (documented by Microsoft) or a SQL Server round-trip.
* **geography is serialised as SQL Server's internal binary hex** e.g. Address.csv row 1 `E6100000010CAE8BFC28BCE4474067A89189898A5EC0` (SRID 4326 = 0xE6100000, version 1, point flag 0x0C, then two IEEE doubles lat/long). Not WKT/WKB. **Inferred:** decodable with a 22-byte parser for points; a SQL Server round-trip (`.ToString()`) is the safe route.
* **XML columns are inline text** (Person.csv `<IndividualSurvey xmlns="...">...</IndividualSurvey>`; JobCandidate.csv `<ns:Resume ...>` spanning multiple physical lines - hence the `&|\n` row terminator).
* **varbinary is hex without `0x`** (ProductPhoto.csv `47494638396150003100...` = GIF89a; Document.csv `D0CF11E0A1B11AE1...` = OLE compound document, i.e. .doc files).
* Empty fields denote NULL; `KEEPIDENTITY` is used so identity values are in the files; computed columns have placeholder fields in the `+|` files (Document.csv has DocumentLevel values) and are absent in tab files where the table's computed column is last? (not verified for every table - see open question).
* **Row counts measured** (lines, or `&|` terminators for the 14 special files): AddressType 6, BillOfMaterials 2,679, BusinessEntityContact 909, ContactType 20, CountryRegion 238, CountryRegionCurrency 109, Culture 8, Currency 105, Department 16, Employee 290, EmployeeDepartmentHistory 296, EmployeePayHistory 316, JobCandidate 13, Location 14, PhoneNumberType 3, Product 504, ProductCategory 4, ProductCostHistory 395, ProductDescription 762, ProductDocument 32, ProductInventory 1,069, ProductListPriceHistory 395, ProductModel 128, ProductModelIllustration 7, ProductModelProductDescriptionCulture 762, ProductProductPhoto 504, ProductReview 4? (measured 34 lines because Comments contain embedded newlines - the table has 4 rows; the tab/0x0a load relies on... see open question), ProductSubcategory 37, ProductVendor 460, SalesPerson 17, SalesPersonQuotaHistory 163, SalesReason 10, SalesTaxRate 29, SalesTerritory 10, SalesTerritoryHistory 17, ScrapReason 16, Shift 3, ShipMethod 5, ShoppingCartItem 3, SpecialOffer 16, SpecialOfferProduct 538, StateProvince 181, UnitMeasure 38, Vendor 104, AWBuildVersion 1.

# What it was used to decide
[AdventureWorks OLTP](/datasets/adventureworks-oltp.md) shape/encoding/row-count sections; [row-count open question](/questions/mssql-adventureworks-row-counts.md); [conversion-path decision](/decisions/mssql-adventureworks-conversion-path.md).
