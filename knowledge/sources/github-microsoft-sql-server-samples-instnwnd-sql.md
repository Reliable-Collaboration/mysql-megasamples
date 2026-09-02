---
type: Source
title: instnwnd.sql (Northwind install script) - file analysis
description: Byte-level and structural analysis of the Northwind T-SQL install script performed in this session (encoding, tables, insert counts, objects, T-SQL constructs).
resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/instnwnd.sql
tags: [northwind, script-analysis, tsql]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/instnwnd.sql
    title: instnwnd.sql at master
    accessed: 2026-09-02
    version: blob ae61e5631d7f03029ec15213ce672b45ceb7e629, 1,049,720 bytes
---

# What was read
The whole file was downloaded with curl (1,049,720 bytes, matches the GitHub API size) and analysed with `file`, `xxd`, `grep`, `awk`, `iconv`.

# Findings (all measured on the file)
* **Encoding**: no BOM (first bytes `2f2a0a` = `/*\n`); `file` reports "ASCII text, with very long lines"; `iconv -f UTF-8` validates it as UTF-8; 433 lines contain non-ASCII bytes (UTF-8 encoded), LF line endings (0 CRLF lines), longest line 44,123 characters (an `Employees.Photo` hex literal).
* Header: `** Copyright Microsoft, Inc. 1994 - 2000  ** All Rights Reserved.` then `-- This script does not create a database. -- Run this script in the database you want the objects to be created. -- Default schema is dbo.` `SET DATEFORMAT mdy` is set explicitly.
* Batches: 122 `GO` separators. `set quoted_identifier on`; identifiers are double-quoted (e.g. `"Order Details"`, `"Employee Sales by Country"`), and the 2000-era tail uses `[dbo].[Region]` bracket style.
* **Tables (13)**: `Employees`, `Categories`, `Customers`, `Shippers`, `Suppliers`, `Orders`, `Products`, `Order Details` (created at lines 132-344), then `CustomerCustomerDemo`, `CustomerDemographics`, `Region`, `Territories`, `EmployeeTerritories` (lines 9121-9146).
* **INSERT statements per table** (counted with grep, one row per INSERT): Categories 8, Customers 91, Employees 9, Order Details 2155, Orders 830, Products 77, Shippers 3, Suppliers 29, Region 4, Territories 53, EmployeeTerritories 49. `CustomerDemographics` and `CustomerCustomerDemo` have no INSERTs (0 rows).
* **Identity columns**: EmployeeID, CategoryID, ShipperID, SupplierID, OrderID, ProductID are `int IDENTITY (1, 1)`; `SET IDENTITY_INSERT <table> ON/OFF` wraps the inserts for Categories, Employees, Orders, Products, Shippers, Suppliers.
* **Types used**: `nvarchar` (43 columns), `nchar` (2: CustomerID, Orders.CustomerID), `int`, `smallint`, `money` (Products.UnitPrice, Order Details.UnitPrice, Orders.Freight), `real` (Discount), `bit` (Discontinued), `datetime` (BirthDate, HireDate, OrderDate, RequiredDate, ShippedDate), `ntext` (Employees.Notes, Categories.Description, Suppliers.HomePage, CustomerDemographics.CustomerDesc), `image` (Employees.Photo, Categories.Picture).
* **Binary literals**: 8 `Categories.Picture` values of 10,746 bytes each and 9 `Employees.Photo` values of 21,626-21,722 bytes, written as `0x...` hex; every one starts with `151C2F00020000000D000E00` (not a BMP/GIF signature). **Inferred:** this is the 78-byte Access OLE-object wrapper that the classic Northwind pictures are known to carry; strip it to obtain a BMP (see open question).
* **CHECK constraints (8)**: `CK_Birthdate CHECK (BirthDate < getdate())`, `CK_Products_UnitPrice (UnitPrice >= 0)`, `CK_ReorderLevel`, `CK_UnitsInStock`, `CK_UnitsOnOrder`, `CK_Discount (Discount >= 0 and (Discount <= 1))`, `CK_Quantity (Quantity > 0)`, `CK_UnitPrice (UnitPrice >= 0)`. No computed columns, no triggers, no functions.
* **Views (16)**: "Customer and Suppliers by City", "Alphabetical list of products", "Current Product List", "Orders Qry", "Products Above Average Price", "Products by Category", "Quarterly Orders", Invoices, "Order Details Extended", "Order Subtotals", "Product Sales for 1997", "Category Sales for 1997", "Sales by Category", "Sales Totals by Amount", "Summary of Sales by Quarter", "Summary of Sales by Year".
* **Stored procedures (7)**: "Ten Most Expensive Products", "Employee Sales by Country", "Sales by Year", CustOrdersDetail, CustOrdersOrders, CustOrderHist, SalesByCategory.
* **Non-ASCII data present** (UTF-8 in file): e.g. `Ana Trujillo Emparedados y helados` / `Avda. de la Constitución 2222` / `México D.F.`, `Antonio Moreno Taquería`, `Berglunds snabbköp` / `Luleå`, `Blondesddsl père et fils` / `Frédérique Citeaux`, `Bólido Comidas preparadas`, `Comércio Mineiro`, `Folk och fä HB` / `Åkergatan 24` / `Bräcke`, `München`, `Galería del gastrónomo`, `Godos Cocina Típica`, `Königlich Essen`, `Mère Paillarde` / `Montréal` / `Québec`, `Océano Atlántico Ltda.`, `Ottilies Käseladen` / `Köln`, `Paris spécialités`, `Princesa Isabel Vinhos` / `Estrada da saúde n. 58`; Products include `Chartreuse verte`. Order rows repeat ship names/addresses with `N'...'` literals (2,494 `N'` literals in the file). Note: the string "Blauer See Delikatessen" contains no umlaut.

# What it was used to decide
[Northwind](/datasets/northwind.md); [conversion-path decision](/decisions/mssql-northwind-pubs-conversion-path.md); [open question on the OLE picture header](/questions/mssql-northwind-picture-ole-header.md).
