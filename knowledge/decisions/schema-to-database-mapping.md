---
type: Decision
title: Mapping SQL Server multi-schema databases (AdventureWorks, WideWorldImporters) into MySQL
description: "MySQL has no schema level below the database; AdventureWorks (5 schemas) and WideWorldImporters (4 data schemas) map to one database per dataset with lower-cased schema-prefixed table names (option A, accepted)."
resource: /decisions/schema-to-database-mapping.md
tags: [decision, naming, adventureworks, wideworldimporters]
status: stable
trust: inferred
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/oltp-install-script/instawdb.sql
    title: instawdb.sql (schemas HumanResources, Person, Production, Purchasing, Sales; 68 tables)
    accessed: "2026-09-02"
  - resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-oltp-database-catalog
    title: WWI OLTP catalog (Application, Purchasing, Sales, Warehouse, Website, Reports, PowerBI, Integration, Sequences)
    accessed: "2026-09-02"
  - resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-dw-database-catalog
    title: WWI DW catalog (Dimension, Fact, Integration)
    accessed: "2026-09-02"
---

# Question
In MySQL, `CREATE SCHEMA` is a synonym for `CREATE DATABASE`; there is no `schema.table` level inside a database. How should `Sales.SalesOrderHeader` (AdventureWorks), `Warehouse.StockItemTransactions` (WWI) and `Fact.Sale` / `Dimension.[Stock Item]` (WWI DW) be named so that the ~30-dataset image stays navigable and published SQL Server tutorials remain easy to adapt?

# Options considered
**A. One MySQL database per dataset, tables named `<Schema>_<Table>`** (`adventureworks.Sales_SalesOrderHeader`, `wideworldimporters.Warehouse_StockItemTransactions`, `wideworldimporters_dw.Fact_Sale`).
* Pro: one database per dataset (flat `SHOW DATABASES`, one `GRANT`, one `mysqldump`); provenance preserved; porting views/procedures is a mechanical `Schema.Table` -> `Schema_Table` rewrite; no cross-database joins needed.
* Con: users must rewrite `Sales.SalesOrderHeader` to `Sales_SalesOrderHeader` in every tutorial query; long names.

**B. One MySQL database per SQL Server schema** (`adventureworks_sales.SalesOrderHeader`, or shorter `aw_sales.SalesOrderHeader`; WWI: `wwi_application`, `wwi_sales`, ...; DW: `wwidw_dimension`, `wwidw_fact`).
* Pro: closest semantic match (MySQL database == schema); queries written as `Sales.SalesOrderHeader` work verbatim after `USE adventureworks_sales`? - no: only if the database is literally named `Sales`, which would collide across datasets (AdventureWorks and WWI both have `Sales`). With prefixed database names users still edit queries. Cross-database FKs, views and triggers work in MySQL.
* Con: AdventureWorks becomes 6 databases, WWI 4-10, WWI DW 3; dumps/grants/`information_schema` browsing fragment; dataset-level operations (drop/reload) need a list.

**C. Drop the schema prefix** (`adventureworks.SalesOrderHeader`).
* Pro: shortest names, matches many community MySQL ports of AdventureWorks. Table names are unique across schemas in AdventureWorks (verified: the 68 names in instawdb.sql do not repeat), WWI (catalog list has no duplicates) and WWI DW.
* Con: loses provenance, `Person.Address` vs nothing is fine but `Sales.Customer` vs `Person.Person` context is lost; procedure/view ports need a mapping table; collides if a future schema reuses a name.

**D. Snake-case everything** (`sales_order_header`) - orthogonal style choice; applies to any of A-C. Note MySQL on Linux is case-sensitive for table names (`lower_case_table_names=0` default); mixed-case names are legal but must be typed exactly, and Windows/macOS clients with `lower_case_table_names=1/2` semantics behave differently. WWI DW additionally has names with spaces (`Dimension.[Stock Item]`, `[Customer Key]`) that MySQL supports only with backticks.

# Evidence
Schema inventories in [instawdb.sql](/sources/github-microsoft-sql-server-samples-instawdb-sql.md), [WWI OLTP catalog](/sources/learn-microsoft-wide-world-importers-oltp-database-catalog.md), [WWI DW catalog](/sources/learn-microsoft-wide-world-importers-dw-database-catalog.md); dataset records [adventureworks-oltp](/datasets/adventureworks-oltp.md), [adventureworks-dw](/datasets/adventureworks-dw.md) (single `dbo` schema - unaffected), [adventureworks-lt](/datasets/adventureworks-lt.md) (single `SalesLT` schema - prefix optional), [wideworldimporters](/datasets/wideworldimporters.md), [wideworldimporters-dw](/datasets/wideworldimporters-dw.md). MySQL 9.7 behaviour of `lower_case_table_names` and backticked identifiers is documented in the target-version records maintained by the coordinator ([tools/mysql-server-9-7](/tools/mysql-server-9-7.md)).

# Coordinator input already on file
The coordinator's [database naming convention](/decisions/database-naming-convention.md) (generated 2026-09-02T20:17:31Z) adopts option A in lower case (`<schema>_<table>`, e.g. `sales_salesorderheader`; database names `adventureworks`, `adventureworks_dw`, `adventureworks_lt`, `wideworldimporters`, `wideworldimporters_dw`) and rejects option B. What remains for the coordinator here is (1) confirming the treatment of WWI DW names with spaces (`Dimension.[Stock Item]` -> `dimension_stock_item` vs `dimension_stockitem`), (2) the `_Archive` history-table suffix (`sales_customers_archive`), and (3) whether single-schema datasets (`adventureworks_lt` = `SalesLT`, `adventureworks_dw` = `dbo`) drop the prefix (recommended: drop `dbo_`, drop `saleslt_`).

# Recommendation (research agent)
**Option A** with original casing preserved (`Sales_SalesOrderHeader`, `Warehouse_StockItemTransactions`, `Fact_Sale`, `Dimension_Stock Item` -> prefer `Dimension_StockItem` by removing spaces only in WWI DW, documented in a name-map file), single-schema datasets unprefixed (`adventureworks_lt.Customer`, `adventureworks_dw.FactInternetSales`). Reasons: keeps one database per dataset (the project's organising unit), preserves provenance for the many multi-schema tutorials, and makes the programmable-object port a deterministic identifier rewrite. Option B is the runner-up if the coordinator values verbatim `Schema.Table` query text more than a flat catalog; if chosen, use dataset-prefixed database names (`aw_sales`) and accept that the two `Sales` schemas still cannot both be named `Sales`.

# Outcome (coordinator, 2026-09-02)
Option A, lower-cased per [naming convention](/decisions/database-naming-convention.md): `<schema>_<table>` with schema and table names lower-cased and spaces removed (`sales_salesorderheader`, `warehouse_stockitemtransactions`, `fact_sale`, `dimension_stockitem`). Temporal history tables keep the `_archive` suffix (`sales_customers_archive`). Single-schema datasets are unprefixed (`adventureworks_lt.customer`, `adventureworks_dw.factinternetsales`); `dbo` tables in multi-schema databases are unprefixed too (`adventureworks.awbuildversion`) and SQL Server logging tables (`DatabaseLog`, `ErrorLog`) are dropped. Column names are lower-cased with spaces replaced by underscores (`Total Including Tax` → `total_including_tax`), otherwise unchanged. Every rename is recorded in `datasets/<name>/name_map.yaml` (source schema.table.column → target), generated by the converter and checked by CI, so upstream documentation remains navigable. Casing was not preserved because Linux MySQL is case-sensitive for table names by default and mixed-case names make queries fail when copied between platforms ([9.x notes](/tools/mysql-9x-behaviour-notes.md)).

# Status
accepted
