---
type: Source
title: Contoso V2 scripts/sql (CreateTablesCommon.sql, CreateTablesSales.sql, CreateTablesOrders.sql)
description: SQL Server DDL for the eight generated tables with exact column types, keys and dbo views - the reference for the MySQL schema.
resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/sql/CreateTablesCommon.sql
tags: [contoso, ddl, sql-server]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/sql/CreateTablesCommon.sql
    title: CreateTablesCommon.sql
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/sql/CreateTablesSales.sql
    title: CreateTablesSales.sql
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/sql/CreateTablesOrders.sql
    title: CreateTablesOrders.sql
    accessed: 2026-09-02
---

# What was read
The three scripts in full, accessed 2026-09-02.

# Relevant excerpt
Schema `Data`:
* CurrencyExchange(Date date, FromCurrency nchar(3), ToCurrency nchar(3), Exchange float) PK(Date, FromCurrency, ToCurrency).
* Customer(CustomerKey int PK, GeoAreaKey int, StartDT date, EndDT date, Continent nvarchar(50), Gender nvarchar(10), Title nvarchar(50), GivenName nvarchar(150), MiddleInitial nvarchar(150), Surname nvarchar(150), StreetAddress nvarchar(150), City nvarchar(50), State, StateFull, ZipCode, Country, CountryFull nvarchar(50), Birthday date NOT NULL, Age int, Occupation nvarchar(100), Company nvarchar(50), Vehicle nvarchar(50), Latitude float, Longitude float).
* Date(Date date, DateKey nvarchar(50) PK, Year int, YearQuarter nvarchar(30), YearQuarterNumber int, Quarter nvarchar(2), YearMonth, YearMonthShort nvarchar(30), YearMonthNumber int, Month, MonthShort nvarchar(30), MonthNumber int, DayofWeek, DayofWeekShort nvarchar(30), DayofWeekNumber int, WorkingDay bit, WorkingDayNumber int).
* Product(ProductKey int PK, ProductCode nvarchar(255), ProductName nvarchar(500), Manufacturer, Brand nvarchar(50), Color nvarchar(20), WeightUnit nvarchar(20), Weight float, Cost money, Price money, CategoryKey int, CategoryName nvarchar(30), SubCategoryKey int, SubCategoryName nvarchar(50)).
* Store(StoreKey int PK, StoreCode int, GeoAreaKey int, CountryCode, CountryName nvarchar(50), State nvarchar(100), OpenDate date, CloseDate date, Description nvarchar(100), SquareMeters int, Status nvarchar(50)).
* Sales(OrderKey bigint, LineNumber int, OrderDate date, DeliveryDate date, CustomerKey int, StoreKey int, ProductKey int, Quantity int, UnitPrice money, NetPrice money, UnitCost money, CurrencyCode nvarchar(5), ExchangeRate float) PK(OrderKey, LineNumber); FKs to Customer, Product, Store; indexes on CustomerKey, ProductKey, StoreKey.
* Orders(OrderKey bigint PK, CustomerKey, StoreKey, OrderDate, DeliveryDate, CurrencyCode nvarchar(5)); OrderRows(OrderKey, LineNumber, ProductKey, Quantity, UnitPrice, NetPrice, UnitCost money) PK(OrderKey, LineNumber); FKs and indexes as for Sales.
* dbo views rename columns with spaces ("Unit Price", "Order Number", ...).

# What it was used to decide
MySQL DDL mapping in [Contoso](/datasets/contoso.md).
