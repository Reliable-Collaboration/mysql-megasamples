---
type: Source
title: TPC-Council/HammerDB repository (license, Docker images, MySQL TPROC-C builder source, RNG)
description: Read README, LICENSE header, hammerdbcli header, Docker/Dockerfile and Docker/Readme.md, src/mysql/mysqloltp.tcl (DDL, constants), modules/tpcccommon-1.0.tm (RandomNumber), and release metadata.
resource: https://github.com/TPC-Council/HammerDB
tags:
- tpc-c
- hammerdb
- tproc-c
- github
- gpl-3-0
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://raw.githubusercontent.com/TPC-Council/HammerDB/master/README.md
  title: README.md
  accessed: "2026-09-02"
  version: master; latest release v6.0 "Version 6.0" published 2026-06-26; GitHub license GPL-3.0; pushed_at 2026-08-25; 780 stars
- resource: https://raw.githubusercontent.com/TPC-Council/HammerDB/master/LICENSE
  title: LICENSE (GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007)
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/TPC-Council/HammerDB/master/hammerdbcli
  title: hammerdbcli launcher
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/TPC-Council/HammerDB/master/Docker/Readme.md
  title: Docker/Readme.md (+ Docker/Dockerfile)
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/TPC-Council/HammerDB/master/src/mysql/mysqloltp.tcl
  title: src/mysql/mysqloltp.tcl
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/TPC-Council/HammerDB/master/modules/tpcccommon-1.0.tm
  title: modules/tpcccommon-1.0.tm
  accessed: "2026-09-02"
---

# What was read
The files above plus directory listings of the root, Docker/, src/, src/mysql/, src/generic/, modules/.

# Relevant excerpt
* README: "HammerDB is the industry standard open-source database benchmark for the worlds most popular databases supporting Oracle Database, Microsoft SQL Server, IBM Db2, PostgreSQL, MySQL and MariaDB." License: "GNU General Public License v3.0."
* hammerdbcli: a Tcl script ("exec ./bin/tclsh9.0"), header "Copyright (C) HammerDB Ltd / Hosted by the TPC-Council", GPL-3-or-later notice.
* Docker/Readme.md: "These Dockerfiles package the published HammerDB 6.0 Ubuntu 24.04 release tarballs"; images built "base → MySQL → MariaDB → PostgreSQL → Oracle → SQL Server → combined" for linux/amd64 and linux/arm64; "MySQL uses the architecture-specific libmysqlclient.so.24 supplied by HammerDB"; production tags `v6.0-*` with component aliases; Docker/Dockerfile references `docker.io/tpcorg/hammerdb:v6.0-mysql` etc.
* src/mysql/mysqloltp.tcl: GUI prompt "Ready to create a $mysql_count_ware Warehouse MySQL TPROC-C schema"; `proc CreateTables { mysql_handler mysql_storage_engine num_part history_pk }` creates `customer` (`c_id INT(5)`, `c_first VARCHAR(16) BINARY`, `c_since DATETIME`, `c_credit_lim DECIMAL(12, 2)`, `c_discount DECIMAL(4, 4)`, `c_data VARCHAR(500) BINARY`, PK (c_w_id,c_d_id,c_id), KEY (c_w_id,c_d_id,c_last(16),c_first(16))), `district`, `history` (optionally with `id INT NOT NULL AUTO_INCREMENT INVISIBLE` PK), `item`, `new_order` (singular), `orders`, `order_line` (optionally `PARTITION BY HASH (ol_w_id) PARTITIONS $num_part`), `stock`, `warehouse`, all `ENGINE = $mysql_storage_engine`; `proc do_tpcc` sets `MAXITEMS 100000`, `CUST_PER_DIST 3000`, `DIST_PER_WARE 10`, `ORD_PER_DIST 3000` and loads with num_vu virtual users (threads) each taking a warehouse range.
* modules/tpcccommon-1.0.tm: `proc RandomNumber {m M} {return [expr {int($m+rand()*($M+1-$m))}]}` and `NURand`; there is no `srand` call in the module or in mysqloltp.tcl.

# What it was used to decide
[TPC-C implementations tool record](/tools/tpcc-implementations.md); [TPC-C implementation choice](/decisions/tpcc-implementation-choice.md); [GPL-3.0](/licenses/gpl-3-0.md).
