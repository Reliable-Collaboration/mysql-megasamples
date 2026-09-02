---
type: Source
title: Microsoft Learn - WideWorldImporters OLAP (DW) database catalog
description: "Official schema catalog for WideWorldImportersDW: Dimension, Fact, Integration schemas; 8 dimension tables, 6 fact tables; configuration procedures for columnstore, in-memory, PolyBase and the large Fact.Sale generator."
resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-dw-database-catalog
tags: [wideworldimporters-dw, docs, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-dw-database-catalog
    title: WideWorldImporters OLAP database catalog - SQL Server | Microsoft Learn
    accessed: 2026-09-02
    version: ms.date 2018-08-04, updated_at 2026-07-20, git commit 2ceb7c07640735a9c49dbb6ff1de511aceead449
---

# What was read
The full page.

# Relevant excerpt
> The data in WideWorldImportersDW thus mirrors the data in WideWorldImporters, but the tables are organized differently. While WideWorldImporters has a traditional normalized schema, WideWorldImportersDW uses the star schema approach ... Besides the fact and dimension tables, the database includes a number of staging tables that are used in the ETL process.

Schemas: Dimension, Fact, Integration. Dimension tables: City, Customer, Date ("financial year (based on November 1st start)"), Employee, StockItem, Supplier, PaymentMethod, TransactionType. Fact tables: Order (Sales.Orders/OrderLines), Sale (Sales.Invoices/InvoiceLines), Purchase (Purchasing.PurchaseOrderLines), Transaction (Sales.CustomerTransactions and Purchasing.SupplierTransactions), Movement (Warehouse.StockTransactions), Stock Holding (Warehouse.StockItemHoldings).

Procedures: Application.{Configuration_ApplyPartitionedColumnstoreIndexing, Configuration_ConfigureForEnterpriseEdition ("Applies partitioning, columnstore indexing and in-memory"), Configuration_EnableInMemory (SCHEMA_ONLY memory-optimized staging), Configuration_ApplyPolyBase, Configuration_PopulateLargeSaleTable ("populates a larger amount of data for the 2012 calendar year"), Configuration_ReseedETL}; Integration.{Get*, Migrate*, PopulateDateDimensionForYear}; Sequences.{ReseedAllSequences, ReseedSequenceBeyondTableValue}.

No row counts are published.

# What it was used to decide
[WideWorldImportersDW](/datasets/wideworldimporters-dw.md).
