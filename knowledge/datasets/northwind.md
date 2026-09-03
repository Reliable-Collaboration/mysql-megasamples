---
type: Dataset
title: Northwind
description: Microsoft's classic 13-table trading-company sample (SQL Server 2000 era) shipped as a single 1 MB T-SQL script with all data inline; MIT licensed.
resource: https://github.com/microsoft/sql-server-samples/blob/master/samples/databases/northwind-pubs/instnwnd.sql
tags:
- tier-core
- mssql-origin
- script-translation
- mit
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/instnwnd.sql
  title: instnwnd.sql (blob ae61e5631d7f03029ec15213ce672b45ceb7e629)
  accessed: "2026-09-02"
  version: master, 1,049,720 bytes
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/readme.md
  title: northwind-pubs readme.md
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/license.txt
  title: sql-server-samples license.txt (MIT)
  accessed: "2026-09-02"
stale_after: "2027-03-01"
---

# Identity
Northwind Traders, the sample that shipped with SQL Server 2000 / Access. Upstream copy: `samples/databases/northwind-pubs/instnwnd.sql` in `microsoft/sql-server-samples`. Proposed MySQL database name: **`northwind`**. Single `dbo` schema, so no schema-prefix question arises (see [mapping decision](/decisions/schema-to-database-mapping.md)).

# Source artifact
* URL: `https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/instnwnd.sql`; pin by blob SHA `ae61e5631d7f03029ec15213ce672b45ceb7e629` (GitHub contents API) or by the directory's last commit `c6f4e6fb7a` (2024-06-27). A byte-identical-except-whitespace variant `instnwnd (Azure SQL Database).sql` (1,049,643 bytes) also exists.
* Format: T-SQL script, 1,049,720 bytes, UTF-8 without BOM, LF line endings; no auth or click-through.
* Checksum: none published upstream. **Verified 2026-09-02** at first fetch: sha256 `3cc62b3fca6d244a47dbde698b809331e4f85988a0685b2b370717d431e94871`, 1,049,720 bytes, pinned in `manifest.yaml` ([source record](/sources/github-microsoft-sql-server-samples-instnwnd-sql.md)).

# Native format and friendlier forms
The script *is* the friendly form: `CREATE TABLE` + 3,308 single-row `INSERT` statements, no `BULK INSERT`, no external files, no database creation ("This script does not create a database"). It needs no SQL Server at all; the only work is T-SQL to MySQL translation.

# Shape
13 tables. Row counts derived from counting INSERT statements in the script, **re-verified against the downloaded file on 2026-09-02** (all 13 exact, 3,308 INSERTs total; a naive `INSERT\s+<table>` regex over-counts the six identity tables by two each because the script writes `set identity_insert "Categories" on|off` in lower case — anchor the pattern with `(?<![_\w])`): Categories 8, Customers 91, Employees 9, Orders 830, `Order Details` 2,155, Products 77, Shippers 3, Suppliers 29, Region 4, Territories 53, EmployeeTerritories 49, CustomerDemographics 0, CustomerCustomerDemo 0 (total 3,308 rows). Binary payload: 8 Categories.Picture x 10,746 bytes and 9 Employees.Photo x 21.6 KB, as hex literals (~270 KB of the file). **Inferred:** loaded InnoDB size well under 5 MB.

Encoding hazards (verified in the file): Latin-1-range accented text in Customers/Orders/Products, e.g. `Avda. de la Constitución 2222`, `México D.F.`, `Berglunds snabbköp`/`Luleå`, `Frédérique Citeaux`, `Comércio Mineiro`, `Folk och fä HB`/`Åkergatan 24`, `München`, `Königlich Essen`, `Mère Paillarde`/`Montréal`/`Québec`, `Océano Atlántico Ltda.`, `Ottilies Käseladen`/`Köln`, `Paris spécialités`, `Estrada da saúde n. 58`; 433 lines carry non-ASCII, all valid UTF-8. `SET DATEFORMAT mdy` with `'mm/dd/yyyy'` date literals inside the `Orders` inserts must be rewritten to ISO. A good test string is `Königlich Essen` (customer `KOENE`).

# Conversion path
Pure script translation, no SQL Server: see [decision](/decisions/mssql-northwind-pubs-conversion-path.md). Steps: strip `GO`, `SET ... ON`, `if exists (... sysobjects ...) drop ...` blocks and `SET IDENTITY_INSERT`; map identifiers `"Order Details"` -> backticks; convert types; convert `0x...` literals (MySQL accepts `0x` hex literals for BLOB directly); reorder or `SET FOREIGN_KEY_CHECKS=0` around the inserts (the script inserts Employees with self-referential ReportsTo and Orders before Products).

# Type-mapping hazards
* `money` -> `DECIMAL(19,4)`; `real` (Discount) -> `FLOAT`; `bit` -> `TINYINT(1)`/`BOOLEAN`; `datetime` -> `DATETIME(3)` (values are dates only); `nchar(5)` -> `CHAR(5)`; `nvarchar(n)` -> `VARCHAR(n)` utf8mb4; `ntext` -> `TEXT`/`MEDIUMTEXT`; `image` -> `MEDIUMBLOB`.
* `int IDENTITY(1,1)` -> `AUTO_INCREMENT`; `SET IDENTITY_INSERT` is a no-op in MySQL (explicit values are always allowed).
* Identifiers with spaces: `Order Details`, `Employee Sales by Country`, view names like `Alphabetical list of products` - legal in MySQL with backticks; decide whether to keep them (fidelity) or snake_case them (usability) - keep, since every Northwind tutorial uses them.
* `CK_Birthdate CHECK (BirthDate < getdate())` is non-deterministic and illegal in a MySQL CHECK - drop it. The other 7 CHECKs (>= 0, Discount range, Quantity > 0) port verbatim (MySQL 8.0.16+ enforces CHECK).
* Pictures/photos carry an OLE wrapper prefix `151C2F00...` (verified prefix; wrapper interpretation inferred) - keep bytes as-is and document, or strip 78 bytes to expose BMP (open question).
* Order date literals are `'mm/dd/yyyy'` style and rely on `SET DATEFORMAT mdy`.

# Programmable objects
* 16 views: port all; they use only joins, aggregates, `CONVERT`/`DATEPART`-style expressions and `TOP`-less selects - **Inferred:** `"Sales by Year"`-type procedures use `CONVERT(varchar, ..., 101)` and `"Ten Most Expensive Products"` uses `TOP 10`; rewrite to `DATE_FORMAT` and `LIMIT`.
* 7 procedures: port (`CustOrdersDetail`, `CustOrdersOrders`, `CustOrderHist`, `SalesByCategory`, `"Ten Most Expensive Products"`, `"Employee Sales by Country"`, `"Sales by Year"`); parameters like `@Beginning_Date datetime`.
* No triggers, functions or computed columns.

# Indexing
Primary keys on every table, `Order Details` composite PK (OrderID, ProductID), foreign keys as in the script, plus the script's secondary indexes on Customers (City, CompanyName, PostalCode, Region), Employees (LastName, PostalCode), Orders (CustomerID, EmployeeID, OrderDate, ShippedDate, ShipPostalCode), Products (CategoryID, ProductName, SupplierID), Suppliers (CompanyName, PostalCode). **Inferred** list from memory of the script's `CREATE INDEX` statements - the executor should copy them from the script (the grep pattern used in research only matched the `CREATE UNIQUE|CLUSTERED` forms and reported 0; the script uses `CREATE INDEX "City" ON dbo.Customers...` style).

# Tests and expected values
**S-03 result (2026-09-02): green.** All 13 documented row counts matched the load exactly and the translator emitted exactly 3,308 INSERT statements, the number this record derived from the script. 13 foreign keys with 0 orphans; 28 indexes; all 16 views created. Every probe in this record was confirmed against the loaded database: `KOENE` = `Königlich Essen`, `BERGS` city = `Luleå`, `LENGTH(picture)` for category 1 = 10746, and the order-details grand total = **1,265,793.04**, exactly the value this record predicted as inferred. `12/08/1948` lands as `1948-12-08`.
Two of seven procedures are **not ported** and are emitted as commented text naming the reason: `custordersdetail` and `salesbycategory` use T-SQL select-list aliasing (`alias = expr`) and variable assignment (`SELECT @v = ...`), which are semantic rewrites rather than translations. The other five port, including their parameters (renamed `p_*` so a parameter cannot be shadowed by a column of the same name).

* Row counts above (13 tables). `SELECT COUNT(*) FROM order_details` = 2155; `SUM(unitprice*quantity*(1-discount))` over `order_details` ~ 1,265,793.04 (**inferred** classic value; verify after load).
* Encoding probe: `SELECT companyname FROM customers WHERE customerid='KOENE'` must return `Königlich Essen`; `SELECT city FROM customers WHERE customerid='BERGS'` = `Luleå`.
* Binary probe: `SELECT LENGTH(picture) FROM categories WHERE categoryid=1` = 10746.

# Tier assignment
**core** - source 1 MB, loaded size single-digit MB ([release/API sizes](/sources/github-microsoft-sql-server-samples-northwind-pubs-readme.md)).

# License and attribution
MIT via the repository `license.txt` ([license record](/licenses/mit.md)); copyright line `Copyright (c) Microsoft Corporation`. The script itself carries `Copyright Microsoft, Inc. 1994 - 2000 All Rights Reserved.` - reproduce both notices in the image's NOTICE. No share-alike, no personal data (fictional names).

# Open questions
* [OLE header on Categories.Picture / Employees.Photo](/questions/mssql-northwind-picture-ole-header.md).
* Whether to keep space-containing identifiers verbatim (recommend yes) - coordinator style decision, see [mapping decision](/decisions/schema-to-database-mapping.md).
