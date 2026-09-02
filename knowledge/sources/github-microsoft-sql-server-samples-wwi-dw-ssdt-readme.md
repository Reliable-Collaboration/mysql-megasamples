---
type: Source
title: wwi-dw-ssdt README and project tree (WideWorldImportersDW)
description: The DW SSDT project builds an empty star schema that is populated only by running the SSIS "Daily ETL" package against a WideWorldImporters OLTP database.
resource: https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/wide-world-importers/wwi-dw-ssdt
tags: [wideworldimporters-dw, ssdt, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/wide-world-importers/wwi-dw-ssdt/README.md
    title: wwi-dw-ssdt/README.md (3,792 bytes)
    accessed: 2026-09-02
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/contents/samples/databases/wide-world-importers/wwi-dw-ssdt/wwi-dw-ssdt
    title: project tree (Application, Dimension, Fact, Integration, PostDeploymentScripts, Security, Sequences, Storage, dbo) and Fact/Tables, Dimension/Tables listings
    accessed: 2026-09-02
---

# What was read
README and tree listings at master, 2026-09-02.

# Relevant excerpt
> The below steps reconstruct the WideWorldImportersDW database. To populate the database, you need to have the WideWorldImporters database as well.
> 4. Execute the SQL Server Integration Services package **Daily ETL** once, to seed the WideWorldImportersDW database based on the contents of the WideWorldImporters database.
> A. Update the partition scheme `Storage\PS_Date.sql` ... B. Delete the filegroups `Storage\USERDATA.sql` and `Storage\WWI_MemoryOptimized_Date.sql`.

# Findings
* Fact tables (files): `Fact/Tables/Movement.sql`, `Order.sql`, `Purchase.sql`, `Sale.sql`, `Stock Holding.sql`, `Transaction.sql` (note the space in `Stock Holding`).
* Dimension tables: `City.sql`, `Customer.sql`, `Date.sql`, `Employee.sql`, `Payment Method.sql`, `Stock Item.sql`, `Supplier.sql`, `Transaction Type.sql` (table names contain spaces: `Dimension.[Payment Method]`, `[Stock Item]`, `[Transaction Type]`, `Fact.[Stock Holding]`).
* Partitioned by date (`PS_Date`), memory-optimized staging filegroup, Integration schema for ETL staging, Sequences schema.
* No stored data in the repository for the DW; the release .bak/.bacpac is the only shipped data.

# What it was used to decide
[WideWorldImportersDW](/datasets/wideworldimporters-dw.md); [conversion-path decision](/decisions/mssql-wideworldimporters-conversion-path.md).
