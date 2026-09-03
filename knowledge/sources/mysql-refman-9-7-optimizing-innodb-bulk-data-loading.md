---
type: Source
title: "MySQL 9.7 Reference Manual: Bulk Data Loading for InnoDB Tables"
description: "The official bulk-load recommendations: autocommit off, unique_checks=0, foreign_key_checks=0, innodb_autoinc_lock_mode=2, PK order, multi-row INSERT, FULLTEXT after load, optional redo-log disable."
resource: https://dev.mysql.com/doc/refman/9.7/en/optimizing-innodb-bulk-data-loading.html
tags:
- mysql
- docs
- innodb
- bulk-load
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/optimizing-innodb-bulk-data-loading.html
  title: "MySQL 9.7 Reference Manual: Bulk Data Loading for InnoDB Tables"
  accessed: "2026-09-02"
  version: MySQL 9.7 manual, section 10.5.5
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/optimizing-innodb-bulk-data-loading.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 10.5.5.

# Relevant excerpt
* "When importing data into InnoDB, turn off autocommit mode, because it performs a log flush to disk for every insert." (`SET autocommit=0; ...; COMMIT;`)
* "If you have UNIQUE constraints on secondary keys, you can speed up table imports by temporarily turning off the uniqueness checks during the import session ... For big tables, this saves a lot of disk I/O because InnoDB can use its change buffer to write secondary index records in a batch." (`SET unique_checks=0;`)
* "If you have FOREIGN KEY constraints in your tables, you can speed up table imports by turning off the foreign key checks for the duration of the import session ... For big tables, this can save a lot of disk I/O." (`SET foreign_key_checks=0;`)
* "Use the multiple-row INSERT syntax to reduce communication overhead between the client and the server if you need to insert many rows."
* "When doing bulk inserts into tables with auto-increment columns, set innodb_autoinc_lock_mode to 2 (interleaved) instead of 1 (consecutive)."
* "When performing bulk inserts, it is faster to insert rows in PRIMARY KEY order. ... Performing bulk inserts in PRIMARY KEY order is particularly important for tables that do not fit entirely within the buffer pool."
* "For optimal performance when loading data into an InnoDB FULLTEXT index ... Create the FULLTEXT index after the data is loaded."
* "If loading data into a new MySQL instance, consider disabling redo logging using ALTER INSTANCE {ENABLE|DISABLE} INNODB REDO_LOG syntax."
* The page does not mention `sql_log_bin`, `bulk_insert_buffer_size`, `innodb_ddl_threads` or `LOAD DATA` itself.

# What it was used to decide
[LOAD DATA tool record](/tools/load-data-infile.md) performance section; [indexing strategy](/decisions/indexing-strategy.md) order of operations.
