---
type: Source
title: Percona-Lab/tpcc-mysql (archived C implementation of a TPC-C-like load and driver for MySQL)
description: Read README, create_table.sql, add_fkey_idx.sql, Dockerfile, load.sh, src/tpc.h, src/load.c, src/support.c; no license file exists and the repository is archived.
resource: https://github.com/Percona-Lab/tpcc-mysql
tags:
- tpc-c
- mysql
- github
- archived
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://raw.githubusercontent.com/Percona-Lab/tpcc-mysql/master/README.md
  title: README.md
  accessed: "2026-09-02"
  version: master @ 1ec1c5eb5b11b55ecf26f81a74db86b659c4e7b9 (2017-01-20, latest commit); GitHub API archived=true, license=null, pushed_at 2018-06-13, 487 stars
- resource: https://raw.githubusercontent.com/Percona-Lab/tpcc-mysql/master/create_table.sql
  title: create_table.sql
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/Percona-Lab/tpcc-mysql/master/add_fkey_idx.sql
  title: add_fkey_idx.sql
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/Percona-Lab/tpcc-mysql/master/src/load.c
  title: src/load.c (+ src/tpc.h, src/support.c, Dockerfile, load.sh)
  accessed: "2026-09-02"
---

# What was read
Root listing (Dockerfile, README.md, add_fkey_idx.sql, count.sql, create_table.sql, drop_cons.sql, load.sh, load_multi_schema.sh, schema2/, scripts/, src/ — **no LICENSE/COPYING file**), and the files above. Source headers carry no copyright or license lines.

# Relevant excerpt
* README: "cd src ; make ( you should have mysql_config available in $PATH)"; `mysqladmin create tpcc1000`; `mysql tpcc1000 < create_table.sql`; `mysql tpcc1000 < add_fkey_idx.sql` ("this step can be done after loading data"); `tpcc_load -h127.0.0.1 -d tpcc1000 -u root -p "" -w 1000`; parallel loading via load.sh (`-l 1..4` = part ITEMS/WAREHOUSE/CUSTOMER/ORDERS, `-m`/`-n` warehouse range); `tpcc_start ... -w1000 -c32 -r10 -l10800`.
* create_table.sql: nine InnoDB tables `warehouse, district, customer, history, new_orders, orders, order_line, item, stock` with tinyint/smallint/int keys, `decimal(4,2)` tax, `decimal(12,2)` balances, `datetime`, `c_data text`, `s_dist_01..10 char(24)`; `history` has no primary key. add_fkey_idx.sql adds `idx_customer (c_w_id,c_d_id,c_last,c_first)`, `idx_orders (o_w_id,o_d_id,o_c_id,o_id)`, `fkey_stock_2 (s_i_id)`, `fkey_order_line_2 (ol_supply_w_id,ol_i_id)` and ten foreign keys.
* src/tpc.h: `#define MAXITEMS 100000 / CUST_PER_DIST 3000 / DIST_PER_WARE 10 / ORD_PER_DIST 3000` (the spec's A.6 constants).
* src/load.c: seed comes from `/dev/urandom` (fallback /dev/random, then time-of-day), then `SetSeed(seed)` → `srand(seed)`; `RandomNumber` is `min + (rand() % ...)`. Orders: `for (o_id = 1; o_id <= ORD_PER_DIST; ...)`, `o_ol_cnt = RandomNumber(5L, 15L)`, `if (o_id > 2100) { /* the last 900 orders have not been delivered */` → new_orders insert. No command-line seed option.
* Dockerfile: `FROM ubuntu:16.04` + `libmysqlclient-dev`, `cd src && make`.

# What it was used to decide
Rejected in [TPC-C implementation choice](/decisions/tpcc-implementation-choice.md): unlicensed, archived, non-deterministic, EOL base image.
