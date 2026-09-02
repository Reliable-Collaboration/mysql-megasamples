---
type: Source
title: wwi-ssdt README and SSDT project sources (WideWorldImporters OLTP)
description: How the WideWorldImporters OLTP database is generated (SSDT publish + T-SQL post-deployment reference data + DataLoadSimulation procedures), with table definitions read for temporal, JSON, geography, sequence, columnstore and memory-optimized features.
resource: https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/wide-world-importers/wwi-ssdt
tags: [wideworldimporters, ssdt, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/wide-world-importers/wwi-ssdt/README.md
    title: wwi-ssdt/README.md (6,179 bytes)
    accessed: 2026-09-02
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/contents/samples/databases/wide-world-importers/wwi-ssdt/wwi-ssdt
    title: SSDT project tree listings (Application/Tables, Sales/Tables, Purchasing/Tables, Warehouse/Tables, Sequences/Sequences, Security, DataLoadSimulation/Stored Procedures, PostDeploymentScripts)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/wide-world-importers/wwi-ssdt/wwi-ssdt/Sales/Tables/Orders.sql
    title: Table definitions read in full or grep'd - Sales/Orders.sql, Sales/Customers.sql, Sales/Invoices.sql, Sales/OrderLines.sql, Sales/InvoiceLines.sql, Application/Cities.sql, Application/People.sql, Application/Countries.sql, Warehouse/StockItems.sql, Warehouse/ColdRoomTemperatures.sql, Warehouse/StockItemTransactions.sql; PostDeploymentScripts/Script.PostDeployment1.sql and the first ~1 KB of pds100-ins-app-people.sql, pds110-ins-app-countries.sql, pds150-ins-app-cities.sql
    accessed: 2026-09-02
---

# What was read
See sources list. All at master (2026-09-02).

# Relevant excerpt (README)
> The Visual Studio SQL Server Data Tools project in this folder is used to construct the WideWorldImporters database from scratch on SQL Server or Azure SQL Database. It is possible to vary the data size.
> Note that each time the database is created from scratch, the data in many tables will be different as a degree of randomization is used throughout the code.
> (Optional) Data population: After step 3, the database contains data for January 2013. This step populates data from February 2013 up to the current data. ... populating data from Feb 2013 to Jun 2016 took about 40 minutes ...
> The default is 60 orders per day and produces a reasonable OLTP database size of around 160MB compressed for a period of 3.5 years

# Findings from the project tree
* Data schemas and tables exactly as the Learn catalog lists; every reference table has a `_Archive` history table (Application: Cities, Countries, DeliveryMethods, PaymentMethods, People, StateProvinces, TransactionTypes; Purchasing: SupplierCategories, Suppliers; Sales: BuyingGroups, CustomerCategories, Customers; Warehouse: ColdRoomTemperatures, Colors, PackageTypes, StockGroups, StockItems). Transaction tables (Orders, OrderLines, Invoices, InvoiceLines, CustomerTransactions, PurchaseOrders, PurchaseOrderLines, SupplierTransactions, StockItemTransactions, StockItemHoldings, VehicleTemperatures, SpecialDeals, StockItemStockGroups, SystemParameters, Logs) are not temporal.
* **Temporal**: `[ValidFrom] DATETIME2(7) GENERATED ALWAYS AS ROW START NOT NULL, [ValidTo] ... ROW END`, `PERIOD FOR SYSTEM_TIME`, `WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE=[Application].[Cities_Archive], DATA_CONSISTENCY_CHECK=ON))`.
* **Memory-optimized**: `Warehouse.ColdRoomTemperatures` is `MEMORY_OPTIMIZED = ON` and system-versioned with `BIGINT IDENTITY(1,1)`; VehicleTemperatures is also memory-optimized (per catalog) - both use IDENTITY, everything else uses sequences.
* **Sequences** (26 in `Sequences` schema): BuyingGroupID, CityID, ColorID, CountryID, CustomerCategoryID, CustomerID, DeliveryMethodID, InvoiceID, InvoiceLineID, OrderID, OrderLineID, PackageTypeID, PaymentMethodID, PersonID, PurchaseOrderID, PurchaseOrderLineID, SpecialDealID, StateProvinceID, StockGroupID, StockItemID, StockItemStockGroupID, SupplierCategoryID, SupplierID, SystemParameterID, TransactionID (shared by CustomerTransactions/SupplierTransactions/StockItemTransactions), TransactionTypeID. Keys are `DEFAULT (NEXT VALUE FOR [Sequences].[OrderID])`.
* **JSON**: `Application.People.UserPreferences NVARCHAR(MAX)`, `CustomFields NVARCHAR(MAX)` with computed `OtherLanguages AS json_query([CustomFields],N'$.OtherLanguages')`; `Warehouse.StockItems.CustomFields` with computed `Tags AS json_query(CustomFields,'$.Tags')` and `SearchDetails AS concat(StockItemName,' ',MarketingComments)`; `Sales.Invoices.ReturnedDeliveryData` with computed `ConfirmedDeliveryTime AS TRY_CONVERT(datetime2(7), json_value(ReturnedDeliveryData,'$.DeliveredWhen'),126)` and `ConfirmedReceivedBy AS json_value(...,'$.ReceivedBy')`, `CHECK (ReturnedDeliveryData IS NULL OR isjson(ReturnedDeliveryData)<>0)`; `Application.People.SearchName AS concat(PreferredName,' ',FullName) PERSISTED`.
* **Geography**: `Application.Cities.Location [sys].[geography]`, `Application.Countries.Border [sys].[geography]` ("Geographic border of the country as described by the United Nations"), StateProvinces.Border likewise.
* **Binary**: `Application.People.HashedPassword VARBINARY(MAX)`, `Photo VARBINARY(MAX)`, `Warehouse.StockItems.Photo VARBINARY(MAX)`.
* **Columnstore**: `CREATE CLUSTERED COLUMNSTORE INDEX [CCX_Warehouse_StockItemTransactions]`; nonclustered `NCCX_Sales_OrderLines`, `NCCX_Sales_InvoiceLines`.
* **RLS**: `Security/FilterCustomersBySalesTerritoryRole.sql` plus roles `External Sales`, `Far West Sales`, `Great Lakes Sales`, `Mideast Sales`, `New England Sales`, `Plains Sales`, `Rocky Mountain Sales`, `Southeast Sales`, `Southwest Sales`; schemas Website, WebApi, PowerBI, Reports, Integration, DataLoadSimulation exist as security/procedure schemas.
* **Reference data exists as T-SQL INSERT scripts** in `PostDeploymentScripts/` (about 7.5 MB): people (15 KB, contains JSON `UserPreferences` and `0x...` password hashes), countries (2.97 MB, contains geography borders as `0xE6100000...` hex and `CAST(... AS Numeric(16,6))`), stateprovinces + borders (253 KB), cities (394 KB required subset + 26 optional a-z files totalling ~5.6 MB; each row `0xe6100000010c...` point hex), deliverymethods, paymentmethods, transactiontypes, suppliercategories, customer groups/categories. Values are dated `@CurrentDateTime = '20200101'`, `@EndOfTime = '99991231 23:59:59.9999999'`.
* **Transactional data is generated, not stored**: `Script.PostDeployment1.sql` runs `Application.Configuration_ApplyFullTextIndexing`, `DataLoadSimulation.DeactivateTemporalTablesBeforeDataLoad`, then the `DataLoadSimulation` procedures (AddCustomers, AddStockItems, CreateCustomerOrders, DailyProcessToCreateHistory, InvoicePickedOrders, PaySuppliers, PerformStocktake, PickStockForCustomerOrders, RecordColdRoomTemperatures, MakeTemporalChanges, ...) produce the orders/invoices/transactions with randomisation. So the only deterministic copies of the shipped data are the release .bak/.bacpac files.

# What it was used to decide
[WideWorldImporters](/datasets/wideworldimporters.md) shape and programmable-object sections; [conversion-path decision](/decisions/mssql-wideworldimporters-conversion-path.md).
