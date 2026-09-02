---
type: Source
title: Microsoft Learn - WideWorldImporters OLTP database catalog
description: Official schema and table catalog for WideWorldImporters (Application, Purchasing, Sales, Warehouse data schemas; Website, Reports, PowerBI, Integration, Sequences, DataLoadSimulation), design notes and the stored-procedure inventory.
resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-oltp-database-catalog
tags:
- wideworldimporters
- docs
- schema
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-oltp-database-catalog
  title: WideWorldImporters OLTP database catalog - SQL Server | Microsoft Learn
  accessed: "2026-09-02"
  version: ms.date 2018-04-04, updated_at 2026-01-23, git commit f6b13d333be03651dafb8f1c24ac816d53f1f877
---

# What was read
The full page.

# Relevant excerpt
Data schemas: Application ("Application-wide users, contacts, and parameters ... reference tables"), Purchasing, Sales, Warehouse. Secure-access schemas: Website, Reports, PowerBI. Development schemas: Integration, Sequences. Tables: Application.{SystemParameters, People, Cities, StateProvinces, Countries, DeliveryMethods, PaymentMethods, TransactionTypes}; Purchasing.{Suppliers, SupplierCategories, SupplierTransactions, PurchaseOrders, PurchaseOrderLines}; Sales.{Customers, CustomerCategories, BuyingGroups, CustomerTransactions, SpecialDeals, Orders, OrderLines, Invoices, InvoiceLines}; Warehouse.{StockItems, StockItemHoldings, StockGroups, StockItemStockGroups, Colors, PackageTypes, StockItemTransactions, VehicleTemperatures, ColdRoomTemperatures}.

> Auto-numbering in tables is based on sequences. ... Memory-optimized tables use IDENTITY columns since they don't support [sequences] in SQL Server 2016.
> A single sequence (TransactionID) is used for these tables: CustomerTransactions, SupplierTransactions, and StockItemTransactions.
> All schemas, tables, columns, indexes, and check constraints have a Description extended property

Procedures: Website.{ActivateWebsiteLogon, ChangePassword, InsertCustomerOrders, InvoiceCustomerOrders, RecordColdRoomTemperatures (TVP into the temporal table), RecordVehicleTemperature (JSON array), SearchForCustomers, SearchForPeople, SearchForStockItems, SearchForStockItemsByTags, SearchForSuppliers}; DataLoadSimulation.{Configuration_ApplyDataLoadSimulationProcedures, Configuration_RemoveDataLoadSimulationProcedures, DeactivateTemporalTablesBeforeDataLoad, PopulateDataToCurrentDate, ReactivateTemporalTablesAfterDataLoad}; Application.{AddRoleMemberIfNonexistent, Configuration_ApplyAuditing, Configuration_ApplyColumnstoreIndexing (Sales.OrderLines, Sales.InvoiceLines), Configuration_ApplyFullTextIndexing, Configuration_ApplyPartitioning (Sales.CustomerTransactions, Purchasing.SupplierTransactions), Configuration_ApplyRowLevelSecurity, Configuration_ConfigureForEnterpriseEdition, Configuration_EnableInMemory (replaces Warehouse.ColdRoomTemperatures, VehicleTemperatures with in-memory equivalents), Configuration_RemoveAuditing, Configuration_RemoveRowLevelSecurity, CreateRoleIfNonexistent}; Sequences.{ReseedAllSequences, ReseedSequenceBeyondTableValue}.

The page publishes **no row counts**. It links "wide-world-importers/wwi-database-scripts" to the `sample-scripts` directory (see repo readme source).

# What it was used to decide
[WideWorldImporters](/datasets/wideworldimporters.md); [schema-to-database mapping decision](/decisions/schema-to-database-mapping.md).
