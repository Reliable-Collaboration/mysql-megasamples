---
type: Source
title: ds3/mysqlds3 readme, mysqlds3_create_all.sh and the load/*.sql loaders
description: MySQL kit instructions (user web/web, create_all sequence) and the LOAD DATA LOCAL INFILE loader scripts with relative CSV paths.
resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/ds3_mysql_readme.txt
tags: [dvdstore, ds3, mysql, load-data]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/ds3_mysql_readme.txt
    title: ds3_mysql_readme.txt (6/2/15)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/mysqlds3_create_all.sh
    title: mysqlds3_create_all.sh
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/load/cust/mysqlds3_load_cust.sql
    title: mysqlds3_load_cust.sql
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/load/orders/mysqlds3_load_orders.sql
    title: mysqlds3_load_orders.sql
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/load/reviews/mysqlds3_load_reviews.sql
    title: mysqlds3_load_reviews.sql
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/build/mysqlds3_cleanup_small.sql
    title: mysqlds3_cleanup_small.sql
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/ds3_mysql_change_log.txt
    title: ds3_mysql_change_log.txt
    accessed: 2026-09-02
---

# What was read
The MySQL kit readme, create_all script, three representative loaders, the Small cleanup script and the MySQL change log, accessed 2026-09-02.

# Relevant excerpt
* create_all sequence: `mysql -u web --password=web < mysqlds3_create_db.sql`, `< mysqlds3_create_ind.sql`, `< mysqlds3_create_sp.sql`, then loaders for cust, orders, orderlines, cust_hist, prod, inv, member, reviews, review_helpfulness. Requires a MySQL user `web`/`web`. "untar ds3.tar.gz from linux.dell.com/dvdstore".
* Loader pattern: `use DS3; SET UNIQUE_CHECKS=0; SET FOREIGN_KEY_CHECKS=0; ALTER TABLE CUSTOMERS DISABLE KEYS; LOAD DATA LOCAL INFILE "../../../data_files/cust/us_cust.csv" INTO TABLE CUSTOMERS FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'; ...` (12 monthly files for ORDERS/ORDERLINES/CUST_HIST; one file each for PRODUCTS, INVENTORY, MEMBERSHIP, REVIEWS, REVIEWS_HELPFULNESS). No `LINES TERMINATED BY`, no `IGNORE 1 LINES` (files have no header).
* Cleanup (Small): `delete from CUSTOMERS where CUSTOMERID > 20000; delete from ORDERS where ORDERID > 12000; ...` then drops and reloads INVENTORY from inv.csv - documents the baseline counts 20,000 customers and 12,000 orders.
* Change log: MySQL support since 5/13/05 (DS2); "9/13/05: Made type of PRODUCTS table explicit with TYPE=MyISAM"; DS3 6/2/15 added REVIEWS, REVIEWS_HELPFULNESS, MEMBERSHIP tables, indexes and the NEW_* procedures.

# What it was used to decide
Loader design (server-side LOAD DATA or generated INSERTs instead of LOCAL INFILE) in [Dell DVD Store](/datasets/dell-dvd-store.md) and [csv load tool note](/tools/smallcsv-load-data-infile.md).
