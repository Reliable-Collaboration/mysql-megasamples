---
type: Open Question
title: AdventureWorks OLTP/DW - exact row counts of the large CSVs, the ProductReview line anomaly, and decoders for hierarchyid/geography
description: Small-table counts were measured; the 25 largest OLTP tables and all DW tables are only inferred from memory, ProductReview.csv shows 34 physical lines for a 4-row table, and hierarchyid/geography values are binary hex that must be decoded without SQL Server.
resource: /questions/mssql-adventureworks-row-counts.md
tags: [open-question, adventureworks, row-counts, encoding]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/contents/samples/databases/adventure-works/oltp-install-script
    title: CSV sampling results
    accessed: "2026-09-02"
---

# Question
1. What are the exact row counts of SalesOrderDetail, SalesOrderHeader, Person, EmailAddress, PersonPhone, Password, BusinessEntity, BusinessEntityAddress, Address, Customer, CreditCard, PersonCreditCard, CurrencyRate, TransactionHistory, TransactionHistoryArchive, WorkOrder, WorkOrderRouting, PurchaseOrderDetail, PurchaseOrderHeader, SalesOrderHeaderSalesReason, Store, ProductPhoto, Document, Illustration in the 2025 CSVs, and of all 30 DW CSVs? (Inferred values are listed in the dataset records.)
2. `ProductReview.csv` is loaded with `FIELDTERMINATOR='\t', ROWTERMINATOR='0x0a'` yet contains 34 LF-terminated lines for a table documented as 4 rows - do the Comments contain literal newlines (which would break `LOAD DATA` with `LINES TERMINATED BY '\n'`) or are there 34 rows in the 2025 edition?
3. Is the pure-Python decoding of hierarchyid (`58` -> `/1/`, `5AC0` -> `/1/1/`) and of the 22-byte geography point (`E6100000010C` + lat + long doubles) correct for every row?

# Cheapest experiment
* Download the two script zips (17.5 MB + 16.8 MB) once; for each table run `grep -c '&|$' file` (14 `+|` tables) or `wc -l file` (others); for ProductReview open the file and count `\t` fields per line - if lines have fewer than 9 tabs the comments wrap. Total cost: one download, one shell loop.
* For decoders: decode all 290 Employee.OrganizationNode values and check that decoded depth equals the placeholder `OrganizationLevel` column shipped in the same CSV (built-in oracle); decode 20 Address points and compare against city/postal code plausibility (Bothell WA ~ 47.7, -122.2). If any mismatch, do the one-off SQL Server round-trip (`SELECT OrganizationNode.ToString(), SpatialLocation.STAsText()`) in the [container](/tools/mssql-server-container.md).

# Resolves
[AdventureWorks OLTP](/datasets/adventureworks-oltp.md) and [DW](/datasets/adventureworks-dw.md) `# Tests and expected values`.
