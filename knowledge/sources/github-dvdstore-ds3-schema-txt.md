---
type: Source
title: ds3/ds3_schema.txt (logical schema and stored-procedure narrative)
description: Column lists of the 11 DS3 tables with Large-size row counts, plus the description of the 17 stored procedures used by the drivers.
resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/ds3_schema.txt
tags: [dvdstore, ds3, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/ds3_schema.txt
    title: ds3_schema.txt
    accessed: "2026-09-02"
---

# What was read
The file in full (7,206 bytes), accessed 2026-09-02.

# Relevant excerpt
Tables and Large-size rows: Customers (CUSTOMERID ... GENDER) 200 million; Orders 120 million; Orderlines 600 million; Cust_Hist 600 million; Products 1 million; Inventory 1 million; Reorder "variable"; Categories 16; Membership (CUSTOMERID, MEMBERSHIPTYPE, EXPIREDATE); Reviews (REVIEW_ID, PROD_ID, REVIEW_DATE, STARS, CUSTOMERID, REVIEW_SUMMARY, REVIEW_TEXT); Reviews_Helpfulness (REVIEW_HELPFULNESS_ID, REVIEW_ID, CUSTOMER_ID, HELPFULNESS).
> The DVD Store database is managed through 17 stored procedures. ... Login ... New_customer ... new_member ... Browse_by_category, Browse_by_actor and Browse_by_title ... get_prod_reviews ... get_prod_reviews_by_stars ... get_prod_reviews_by_date ... get_prod_reviews_by_actor and by_title ... Purchase

Driver parameters table (n_threads, ramp_rate, run_time, db_size, think_time, pct_newcustomers, ...).

# What it was used to decide
Table inventory and the finding that the MySQL kit implements only 4 of the 17 procedures ([dataset](/datasets/dell-dvd-store.md)).
