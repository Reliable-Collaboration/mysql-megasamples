---
type: Source
title: "dhuny/tpch (TPC-H helper for MySQL and MariaDB: DDL + LOAD DATA script)"
description: A small community repo whose tpch_to_mariadb.sql shows the LOAD DATA LOCAL INFILE ... LINES TERMINATED BY '|\n' trick for dbgen's trailing pipe and a MySQL DDL with PK/FK.
resource: https://github.com/dhuny/tpch
tags:
- tpc-h
- mysql
- mariadb
- community
- github
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://raw.githubusercontent.com/dhuny/tpch/master/README.md
  title: README.md (+ tpch_to_mariadb.sql)
  accessed: "2026-09-02"
  version: master; pushed_at 2024-06-08; license null; 6 stars
---
# What was read
* https://raw.githubusercontent.com/dhuny/tpch/master/README.md, “README.md (+ tpch_to_mariadb.sql)”, accessed 2026-09-02, version master; pushed_at 2024-06-08; license null; 6 stars

# Relevant excerpt
* README: build with `DATABASE= ORACLE MACHINE = LINUX WORKLOAD = TPCH`, `./dbgen -s 1`; "based on Catarina Ribeiro's port to MySQL"; references "TPC-H version 3.0.0 (published 18 February 2021)".
* tpch_to_mariadb.sql: `CREATE TABLE NATION ( N_NATIONKEY INTEGER primary key, ...)` … `LINEITEM (... primary key(L_ORDERKEY,L_LINENUMBER))`; loads with `LOAD DATA LOCAL INFILE 'PATH/lineitem.tbl' INTO TABLE \`LINEITEM\` FIELDS TERMINATED BY '|' LINES TERMINATED BY '|\n';` for all eight tables; then `ALTER TABLE ... ADD FOREIGN KEY IF NOT EXISTS ...` (MariaDB syntax) for the dss.ri constraints.

# What it was used to decide
Trailing-delimiter handling in [TPC-H dataset](/datasets/tpc-h.md) (and reused for TPC-DS/SSB).
