---
type: Source
title: Percona-Lab/sysbench-tpcc (Apache-2.0 Lua TPCC-like workload for sysbench)
description: Read README, LICENSE, tpcc_common.lua (DDL, population loops, RNG calls) and repository metadata.
resource: https://github.com/Percona-Lab/sysbench-tpcc
tags: [tpc-c, sysbench, lua, github]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/Percona-Lab/sysbench-tpcc/master/README.md
    title: README.md
    accessed: 2026-09-02
    version: master @ f110afa8023c7924b1ba00177232a9090624acb5 (2025-07-03); GitHub license Apache-2.0; 331 stars
  - resource: https://raw.githubusercontent.com/Percona-Lab/sysbench-tpcc/master/LICENSE
    title: LICENSE (Apache License Version 2.0, January 2004)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/Percona-Lab/sysbench-tpcc/master/tpcc_common.lua
    title: tpcc_common.lua
    accessed: 2026-09-02
---

# What was read
Root: LICENSE (11,342 B Apache-2.0), README.md, tpcc-scm-1.rockspec, tpcc.lua, tpcc_check.lua, tpcc_common.lua, tpcc_run.lua.

# Relevant excerpt
* README: "TPCC-like workload for sysbench 1.0.x. Make sure you are using sysbench 1.0.14 or better!"; "This is NOT an implementation of TPCC workload. It is "TPCC-like" and uses only queries and schemas from TPCC specification. ... Please do not use sysbench-tpcc to generate TPC-C results for comparing between vendors, or please attach a similar disclaimer as to the TPCC-like nature." Prepare: `./tpcc.lua --mysql-socket=... --mysql-user=root --mysql-db=sbt --time=300 --threads=64 --report-interval=1 --tables=10 --scale=100 --db-driver=mysql prepare`; RocksDB example adds `--use_fk=0 --mysql_storage_engine=rocksdb --trx_level=RC`.
* tpcc_common.lua: `MAXITEMS=100000`, `CUST_PER_DIST=3000`, `DIST_PER_WARE` (10); options `scale` "Scale factor (warehouses)" default 100, `tables` (number of table sets), `use_fk` default 1, `force_pk` ("Force using auto-inc PK on history table") default 0, `mysql_storage_engine` default innodb. Tables are created per set with a numeric suffix: `CREATE TABLE IF NOT EXISTS warehouse%d (w_id smallint not null, w_name varchar(10), ..., w_tax decimal(4,2), w_ytd decimal(12,2), primary key (w_id))`, likewise `district%d`, `customer%d`, `history%d` (no PK unless force_pk), `orders%d`, `new_orders%d`, `order_line%d`, `stock%d`, `item%d` — same column types as tpcc-mysql. Secondary indexes `idx_orders`, `fkey_stock_2`, `fkey_order_line_2`, `fkey_history_1/2` and (with use_fk=1) ten FKs. Population: items `for j = 1 , MAXITEMS`; per warehouse `for d_id = 1 , DIST_PER_WARE`, `for c_id = 1 , CUST_PER_DIST` (c_last from `Lastname(c_id - 1)` for c_id ≤ 1000 else `Lastname(NURand(255, 0, 999))`), history one row per customer, orders `for o_id = 1 , 3000` with `o_carrier_id` = `o_id < 2101 and sysbench.rand.uniform(1,10) or "NULL"`, o_ol_cnt `sysbench.rand.uniform(5,15)`, `INSERT INTO new_orders%d ... SELECT o_id, o_d_id, o_w_id FROM orders%d WHERE o_id>2100`, stock `for s_id = 1 , 100000`. The O_C_ID permutation uses Lua's `math.random(i, 3000)` (not sysbench.rand); all other values use `sysbench.rand.*`.
* Loads with `SET SESSION autocommit=1` and `bulk_insert_init/next/done` multi-row INSERTs; no LOAD DATA.

# What it was used to decide
[TPC-C implementation choice](/decisions/tpcc-implementation-choice.md); [TPC-C dataset](/datasets/tpc-c.md); determinism [open question](/questions/tpcc-loader-determinism.md).
