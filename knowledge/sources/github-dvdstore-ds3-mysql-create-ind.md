---
type: Source
title: ds3/mysqlds3/build/mysqlds3_create_ind.sql (indexes and foreign keys)
description: Index/FK script for the MySQL DS3 build, including two FULLTEXT indexes on PRODUCTS.
resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/build/mysqlds3_create_ind.sql
tags:
- dvdstore
- ds3
- mysql
- indexes
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/build/mysqlds3_create_ind.sql
  title: mysqlds3_create_ind.sql (5/27/15)
  accessed: "2026-09-02"
---

# What was read
The whole script (2,437 bytes), accessed 2026-09-02.

# Relevant excerpt
Unique `IX_CUST_USERNAME(USERNAME)`; `IX_CUST_HIST_CUSTOMERID`; FK CUST_HIST->CUSTOMERS ON DELETE CASCADE; `IX_ORDER_CUSTID`; FK ORDERS->CUSTOMERS ON DELETE SET NULL; unique `IX_ORDERLINES_ORDERID(ORDERID, ORDERLINEID)`; FK ORDERLINES->ORDERS ON DELETE CASCADE; `CREATE FULLTEXT INDEX IX_PROD_ACTOR ON PRODUCTS (ACTOR)`; `IX_PROD_CATEGORY`; `CREATE FULLTEXT INDEX IX_PROD_TITLE ON PRODUCTS (TITLE)`; `IX_PROD_SPECIAL`; FK MEMBERSHIP->CUSTOMERS CASCADE; FK REVIEWS->CUSTOMERS CASCADE; `IX_REVIEWS_PROD_ID`, `IX_REVIEWS_STARS`, `IX_REVIEWS_PRODSTARS`; FK REVIEWS_HELPFULNESS->REVIEWS CASCADE; `IX_REVIEWS_HELP_REVID`, `IX_REVIEWS_HELP_CUSTID`, `IX_REORDER_PRODID`, `IX_PROD_PRODID_COMMON`, `IX_REVIEW_HELP_ID_HELPID`, `IX_REVIEWS_PRODID_REVID_DATE`, `IX_CUST_HIST_CUSTOMERID_PRODID`. No FK from ORDERLINES/CUST_HIST/INVENTORY to PRODUCTS.

# What it was used to decide
Indexing section of [Dell DVD Store](/datasets/dell-dvd-store.md).
