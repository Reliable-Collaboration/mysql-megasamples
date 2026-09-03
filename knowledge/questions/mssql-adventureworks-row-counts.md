---
type: Open Question
title: AdventureWorks OLTP/DW - exact row counts of the large CSVs, the ProductReview line anomaly, and decoders for hierarchyid/geography
description: Answered for the OLTP half - all 69 tables counted on a real load, ProductReview confirmed at 4 rows, and both binary decoders verified over every row; the DW counts remain for task X-01.
resource: /questions/mssql-adventureworks-row-counts.md
tags:
- open-question
- adventureworks
- row-counts
- encoding
status: deprecated
trust: verified
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
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

# Answer
Answered 2026-09-03 by building the OLTP database. The DW half of question 1 is still open and moves
to task X-01.

**1. Row counts (OLTP, 2025 edition), measured.** Every one of the 45 counts the record had already
verified from the CSVs reproduced exactly on the first load, so these are the ones that were unknown:

| table | rows |
|---|---|
| sales_salesorderdetail | 121,317 |
| sales_salesorderheader | 31,465 |
| person_person | 19,972 |
| person_emailaddress | 19,972 |
| person_personphone | 19,972 |
| person_password | 19,972 |
| person_businessentity | 20,777 |
| person_businessentityaddress | 19,614 |
| person_address | 19,614 |
| sales_customer | 19,820 |
| sales_creditcard | 19,118 |
| sales_personcreditcard | 19,118 |
| sales_currencyrate | 13,532 |
| production_transactionhistory | 113,443 |
| production_transactionhistoryarchive | 89,253 |
| production_workorder | 72,591 |
| production_workorderrouting | 67,131 |
| purchasing_purchaseorderdetail | 8,845 |
| purchasing_purchaseorderheader | 4,012 |
| sales_salesorderheadersalesreason | 27,647 |
| sales_store | 701 |
| production_productphoto | 101 |
| production_document | 12 |
| production_illustration | 5 |

69 tables and **759,240 rows** in total (71 upstream, less the two SQL Server logging tables the
naming decision drops). All 69 counts are pinned in `datasets/adventureworks/tests/expected_counts.yaml`.

**2. ProductReview has 4 rows, and the comments do contain literal newlines.** The premise behind the
worry was wrong, not the file: BULK INSERT does not split a file into lines and then into fields. It
reads field by field, and only the *last* field of a row is delimited by the row terminator, so a
newline inside the Comments column -- which is the 7th of 8 -- is data. The converter now reads the
files the same way, which is also what makes the 14 `+|`/`&|\n` tables work. Comment lengths are 509,
337, 252 and 3,782 characters.

**3. Yes, both decoders are correct for every row.** hierarchyid: all 290 employees decode to a path
whose depth equals the shipped `OrganizationLevel`, all 290 re-encode to their original bytes, all
290 are distinct and every parent path exists; employee 2 is `/1/` and employee 3 `/1/1/`, matching
Microsoft's documented values. geography: address 1 decodes to 47.7869921906598, -122.164644615406 --
Bothell, WA, as the row says -- and all 19,614 addresses carry a latitude inside [-90, 90]. See
[the probe](/sources/mysql-9-7-srid-4326-axis-order-probe.md).

# Resolves
[AdventureWorks OLTP](/datasets/adventureworks-oltp.md) and [DW](/datasets/adventureworks-dw.md) `# Tests and expected values`.
