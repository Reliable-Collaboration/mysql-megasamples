---
type: Tool
title: TPC-C-derived loaders for MySQL — tpcc-mysql, sysbench-tpcc, HammerDB TPROC-C
description: Evaluation of the three open-source ways to create and populate a TPC-C-derived schema in MySQL, with license, schema, row counts, determinism and container fit.
resource: /tools/tpcc-implementations.md
tags:
- tool
- tpc-c
- loader
- sysbench
- hammerdb
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
- resource: https://github.com/Percona-Lab/tpcc-mysql
  title: Percona-Lab/tpcc-mysql (README, create_table.sql, add_fkey_idx.sql, src/load.c, src/support.c, src/tpc.h, Dockerfile, load.sh)
  accessed: "2026-09-02"
- resource: https://github.com/Percona-Lab/sysbench-tpcc
  title: Percona-Lab/sysbench-tpcc (README, LICENSE, tpcc_common.lua)
  accessed: "2026-09-02"
- resource: https://github.com/akopytov/sysbench
  title: akopytov/sysbench README + Debian package page
  accessed: "2026-09-02"
- resource: https://github.com/TPC-Council/HammerDB
  title: TPC-Council/HammerDB (README, LICENSE, hammerdbcli, Docker/, src/mysql/mysqloltp.tcl, modules/tpcccommon-1.0.tm)
  accessed: "2026-09-02"
- resource: https://www.hammerdb.com/docs/ch03s02.html
  title: HammerDB docs ch03s02, ch04s03, ch01s12, ch09s03
  accessed: "2026-09-02"
- resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/tpc-c_v5.11.0.pdf
  title: TPC-C spec 5.11
  accessed: "2026-09-02"
---

# Facts
| | Percona-Lab/tpcc-mysql | Percona-Lab/sysbench-tpcc (+ sysbench) | HammerDB TPROC-C (MySQL) |
|---|---|---|---|
| Record | [source](/sources/github-percona-lab-tpcc-mysql.md) | [source](/sources/github-percona-lab-sysbench-tpcc.md), [sysbench](/sources/github-akopytov-sysbench.md) | [source](/sources/github-tpc-council-hammerdb.md), [docs](/sources/hammerdb-docs-ch03s02-tproc-c.md) |
| License | **none** (no LICENSE file, no headers; GitHub license=null) → cannot be redistributed; usable only as a reference | Lua scripts **Apache-2.0**; sysbench binary **GPL-2.0** (Debian package `sysbench` 1.0.20+ds-7 depends on libluajit-5.1-2 and libmariadb3) | **GPL-3.0** (hosted by the TPC Council; "Copyright (C) HammerDB Ltd") |
| Status | **archived**, last commit 2017-01-20, Dockerfile on ubuntu:16.04, needs libmysqlclient-dev + mysql_config | active (2025-07-03); needs sysbench ≥ 1.0.14 | active; v6.0 released 2026-06-26; official multi-arch images `tpcorg/hammerdb:mysql` (Ubuntu 24.04, ships libmysqlclient.so.24) |
| Schema creation | `create_table.sql` (9 tables: warehouse, district, customer, history, new_orders, orders, order_line, item, stock; InnoDB; smallint/tinyint keys) then `add_fkey_idx.sql` (4 indexes, 10 FKs) | `prepare` creates `warehouse1..N`, …, `item1..N` per `--tables` (numeric suffix always present), same column types as tpcc-mysql; `--use_fk=1` adds the 10 FKs; `--force_pk=1` adds an auto-inc PK to history | `buildschema` creates customer, district, history (optional invisible auto-inc PK), item, **new_order** (singular), orders, order_line (optional HASH partitioning by ol_w_id), stock, warehouse; MySQL-specific types (`INT(5)`, `VARCHAR(16) BINARY`, `DECIMAL(4,4)` discount, `c_data VARCHAR(500)`) |
| Loading | `tpcc_load -w W` (C, prepared statements), parallel via `load.sh` parts 1–4 | multi-row INSERT batches (`bulk_insert_*`), `--threads` parallel, no LOAD DATA | multi-threaded virtual users (`mysql_num_vu`), one warehouse range per VU |
| Row counts per warehouse | spec A.6 constants (`MAXITEMS 100000, CUST_PER_DIST 3000, DIST_PER_WARE 10, ORD_PER_DIST 3000`): item 100,000 fixed; per W: district 10, customer 30,000, history 30,000, orders 30,000, new_orders 9,000 (o_id > 2100), order_line ≈ 300,000 (5–15 per order), stock 100,000 | same constants (`MAXITEMS=100000`, `CUST_PER_DIST=3000`, orders 1..3000, `new_orders … WHERE o_id>2100`, stock 1..100000) | same constants (`MAXITEMS 100000 CUST_PER_DIST 3000 DIST_PER_WARE 10 ORD_PER_DIST 3000`) |
| Determinism | **No**: seed read from /dev/urandom (fallback time), no seed flag | **Partly**: `--rand-seed` ("When 0, the current time is used"); the O_C_ID permutation uses Lua `math.random` — seeding of that path is unverified; NOW() timestamps embedded → [open question](/questions/tpcc-loader-determinism.md) | **No**: `RandomNumber` uses Tcl `rand()`; no `srand` in the code (Tcl seeds from time/pid — **Inferred**) |
| Fair-use naming | README says "tpcc" only | README: "This is NOT an implementation of TPCC workload. It is "TPCC-like" ... please attach a similar disclaimer" | "TPROC-C ... derived from the TPC-C specification ... not comparable to published TPC-C results" |
| Container fit | needs a C build against the MySQL client library; EOL base | `apt-get install sysbench` + `git clone` of 5 Lua files in the existing loader image | separate ~large image (Tcl 9 + all DB clients; size not measured) or the `:mysql` variant; scriptable via `hammerdbcli` (`dbset db mysql`, `diset tpcc mysql_count_ware N`, `buildschema`) |
| MySQL 9.x | unverified (2017 code, libmysqlclient of the build host) | libmariadb3 client + caching_sha2_password: **Inferred** OK (MariaDB Connector/C ≥ 3.0.? supports caching_sha2) — verify | v6.0 ships MySQL 8.x client library 24 → **Inferred** OK with 9.7 |

# Recommendation
See [TPC-C implementation choice](/decisions/tpcc-implementation-choice.md): **sysbench-tpcc** is the loader (light, Apache-2.0 scripts, packaged GPL binary, seedable), with the schema normalised afterwards (`RENAME TABLE warehouse1 TO warehouse` …) and our own `indexes.sql`/`constraints.sql`; **HammerDB** is the reference for naming/disclaimer and the fallback loader; **tpcc-mysql** is rejected (unlicensed, archived).

# Limits
* None of the three writes flat files; all insert directly, so the row digests of the [checksum method](/decisions/test-checksum-method.md) must be computed *after* load from MySQL, and only counts (and structural invariants: 10 districts/warehouse, 3,000 customers/district, 900 new orders/district, orders 1..3000, o_carrier_id NULL iff o_id > 2100) are pre-known.
* Every loader embeds "now" in c_since/o_entry_d/h_date → those columns are excluded from digests.
