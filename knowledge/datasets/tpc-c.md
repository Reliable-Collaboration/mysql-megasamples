---
type: Dataset
title: TPC-C (derived) — tpcc
description: The nine-table order-entry OLTP schema of TPC Benchmark C populated for W warehouses by an open-source "TPC-C-like" loader (sysbench-tpcc, with HammerDB TPROC-C as the reference/fallback); no TPC software exists for TPC-C and no data is shipped.
resource: https://www.tpc.org/tpcc/
tags:
- tier-generated
- generated
- tpc
- oltp
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
- resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/tpc-c_v5.11.0.pdf
  title: TPC-C spec 5.11 (cardinalities, population rules, trademark notice)
  accessed: "2026-09-02"
- resource: https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp
  title: TPC current specifications (TPC-C v5.11.0; Source Code n/a)
  accessed: "2026-09-02"
- resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/Fair_Use_Quick_Reference_v1.0.0.pdf
  title: TPC Fair Use quick reference
  accessed: "2026-09-02"
- resource: https://github.com/Percona-Lab/sysbench-tpcc
  title: sysbench-tpcc @ f110afa (Apache-2.0)
  accessed: "2026-09-02"
- resource: https://github.com/akopytov/sysbench
  title: sysbench (GPL-2.0, --rand-seed)
  accessed: "2026-09-02"
- resource: https://github.com/TPC-Council/HammerDB
  title: HammerDB v6.0 (GPL-3.0, TPROC-C)
  accessed: "2026-09-02"
- resource: https://www.hammerdb.com/docs/ch03s02.html
  title: HammerDB TPROC-C naming and disclaimer
  accessed: "2026-09-02"
- resource: https://github.com/Percona-Lab/tpcc-mysql
  title: tpcc-mysql (archived, unlicensed)
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/keywords.html
  title: MySQL reserved words (ORDER)
  accessed: "2026-09-02"
---

# Identity
* Proposed MySQL database: **`tpcc`**; tables `warehouse, district, customer, history, new_orders, orders, order_line, item, stock` (spec names WAREHOUSE, DISTRICT, CUSTOMER, HISTORY, NEW-ORDER, ORDER, ORDER-LINE, ITEM, STOCK; `ORDER` is reserved in MySQL ([keywords](/sources/mysql-refman-9-7-keywords.md)) and every MySQL implementation uses `orders`; `new_orders` follows tpcc-mysql/sysbench-tpcc; HammerDB uses `new_order`).
* Derived from TPC Benchmark C, Standard Specification Revision 5.11 (February 2010; current on tpc.org as v5.11.0). The TPC ships **no TPC-C software** ("Source Code: n/a"), so the population comes from an OSS loader that implements Clause 4.3.3 ([spec record](/sources/tpc-c-specification-v5-11.md)).
* Naming: "derived from TPC-C" / "TPC-C-like"; never "tpmC". HammerDB's wording: "derived from the TPC-C Benchmark Standard and as such is not comparable to published TPC-C results, as the results comply with a subset rather than the full TPC-C Benchmark Standard" ([HammerDB docs](/sources/hammerdb-docs-ch03s02-tproc-c.md)).

# Source artifact
| Item | Value |
|---|---|
| Spec | https://www.tpc.org/TPC_Documents_Current_Versions/pdf/tpc-c_v5.11.0.pdf, 1.1 MB, free; copying permitted with the TPC copyright notice, title and date. |
| Loader (chosen) | https://github.com/Percona-Lab/sysbench-tpcc @ `f110afa8023c7924b1ba00177232a9090624acb5` (2025-07-03; 5 Lua files, ~70 KB; Apache-2.0) + Debian package `sysbench` 1.0.20+ds-7 (GPL-2.0; LuaJIT + libmariadb3) — [tool](/tools/tpcc-implementations.md). |
| Reference / fallback | HammerDB v6.0 (2026-06-26), official image `tpcorg/hammerdb:mysql` (Ubuntu 24.04, amd64+arm64), GPL-3.0. |
| Rejected | Percona-Lab/tpcc-mysql — archived, no license file, non-deterministic seed, ubuntu:16.04 build. |
| Checksums | none applicable; loaders insert directly, so the baseline is computed after load. |

# Native format and friendlier forms
There is no data file format: every implementation generates rows in memory and INSERTs them (sysbench-tpcc: multi-row INSERT batches; tpcc-mysql: prepared statements; HammerDB: Tcl VUs). Alternative considered: a ~150-line seeded Python populator writing `.tbl` files from Clause 4.3.3 + Appendix A.6 (which the spec publishes) — deterministic and license-clean; recorded as the option to switch to if the determinism question resolves badly ([question](/questions/tpcc-loader-determinism.md)).

# Shape (per configured warehouse W; spec Clause 4.2 table and 4.3.3.1)
| Table | Rows | Typical row | Notes |
|---|---|---|---|
| warehouse | 1 × W | 89 B | W_YTD = 300,000.00, W_TAX ∈ [0,0.2] |
| district | 10 × W | 95 B | D_YTD = 30,000.00, D_NEXT_O_ID = 3,001 |
| customer | 30,000 × W | 655 B | 3,000 per district; C_LAST from the NURand(255,0,999) name syllables; C_CREDIT 'GC' 90% / 'BC' 10%; C_DATA 300–500 chars |
| history | 30,000 × W | 46 B | one per customer; no PK in the spec |
| orders | 30,000 × W | 24 B | O_C_ID = random permutation of 1..3,000; O_CARRIER_ID NULL iff O_ID > 2,100; O_OL_CNT ∈ [5,15] |
| new_orders | 9,000 × W | 8 B | O_ID 2,101..3,000 per district |
| order_line | ≈ 300,000 × W (±1%) | 54 B | O_OL_CNT lines per order (avg 10); OL_DELIVERY_D NULL and OL_AMOUNT random iff O_ID > 2,100 |
| stock | 100,000 × W | 306 B | S_QUANTITY ∈ [10,100]; ten 24-char S_DIST_xx |
| item | **100,000 fixed** | 82 B | I_IM_ID ∈ [1,10,000], I_PRICE ∈ [1.00,100.00], 10% contain "ORIGINAL" |

≈ 499,010 rows and ≈ 65–70 MB raw per warehouse (**Inferred** from the spec's typical row lengths: 19.65 + 1.38 + 0.72 + 0.07 + 16.2 + 30.6 MB ≈ 68.6 MB plus item 8.2 MB once). All text is random a-strings/n-strings (ASCII letters and digits) — no encoding hazards. sysbench-tpcc DDL (same column types as tpcc-mysql; HammerDB differs slightly): `w_id smallint`, `d_id tinyint`, `c_id int`, `c_since datetime`, `c_credit_lim bigint`, `c_discount decimal(4,2)`, balances `decimal(12,2)`, `c_data text`, `o_entry_d datetime`, `ol_amount decimal(6,2)`, `ol_dist_info char(24)`, `s_dist_01..10 char(24)`, `i_price decimal(5,2)`, `h_amount decimal(6,2)`. Note `smallint w_id` caps W at 32,767 and `tinyint` district/carrier ids are fine; keep them (spec 1.3.1 allows any representation holding the required id range).

# Conversion path
**Chosen** ([decision](/decisions/tpcc-implementation-choice.md)): `make gen-tpcc W=10` in the loader image runs `sysbench tpcc.lua --db-driver=mysql --mysql-host=… --mysql-db=tpcc --tables=1 --scale=$W --threads=$T --use_fk=0 --rand-seed=$SEED prepare`, then `RENAME TABLE warehouse1 TO warehouse, …` (9 renames), then our `indexes.sql` (the four secondary indexes) and `constraints.sql` (the ten FKs, as in tpcc-mysql `add_fkey_idx.sql`), `ANALYZE TABLE`, then `baseline.json` computed from MySQL. Fallback: `docker run --network host tpcorg/hammerdb:mysql ./hammerdbcli auto build.tcl` with `dbset db mysql; diset tpcc mysql_count_ware $W; diset tpcc mysql_num_vu $T; buildschema` ([CLI docs](/sources/hammerdb-docs-ch09s03-cli-commands.md)), then rename `new_order`→`new_orders`.

# Built and measured (2026-09-04, task B-03)
sysbench 1.0.20 with Percona's sysbench-tpcc at commit `f110afa8023c7924b1ba00177232a9090624acb5` —
the commit [the decision](/decisions/tpcc-implementation-choice.md) names — both inside
`engines/mysql/loader.Dockerfile`. At W=1, `--tables=1 --use_fk=0 --threads=1`: **9 tables, 54.2 MB**.

**The first execution task is answered: sysbench connects to MySQL 9.7 without trouble.** The
concern was `caching_sha2_password`, which 9.x is the only supported plugin for; Debian 12's
`default-mysql-client` is MariaDB 10.11 and it authenticates fine, as does sysbench's own driver.

**The determinism experiment (risk 10) is answered too, and the answer is no.** Two loads with
identical parameters — same `--rand-seed=42`, same `--threads=1`, same scale — produce **different
data in eight of the nine tables**. Only `new_orders` matches, and that one is derived structurally
rather than randomly. sysbench-tpcc does not thread its seed through the row generation.

Row *counts* are a different matter and are stable: seven of the nine are exactly the
specification's W=1 cardinalities — warehouse 1, district 10, customer 30,000, history 30,000,
orders 30,000, new_orders 9,000, item 100,000, stock 100,000 — and only `order_line` varies
(299,674 here), because TPC-C specifies 5 to 15 lines per order at random.

The consequence for this project: **TPC-C cannot carry pinned digests the way every other dataset
does.** Counts can be asserted, content cannot. That is a property of the generator, not of the
conversion, and it is why the dataset ships as a `make load-tpcc` target rather than as a verified
database with a checksum file.

# Type-mapping hazards
1. `history` has no primary key → InnoDB uses a hidden row id; the [indexing strategy](/decisions/indexing-strategy.md) prefers an explicit surrogate: add `h_id BIGINT AUTO_INCREMENT PRIMARY KEY` (sysbench `--force_pk=1` does exactly this; HammerDB offers an INVISIBLE auto-inc PK for the same reason).
2. Timestamps: loaders insert `NOW()` for `c_since`, `h_date`, `o_entry_d`, `ol_delivery_d` → non-reproducible; exclude from digests; document that "current date/time given by the operating system" is what the spec requires.
3. Determinism: sysbench `--rand-seed` seeds `sysbench.rand.*`, but the O_C_ID permutation uses Lua `math.random`, and multi-threaded loads interleave RNG streams → identical re-runs only with `--threads=1` and a verified seeding of `math.random` ([question](/questions/tpcc-loader-determinism.md)). HammerDB and tpcc-mysql are unseeded.
4. `c_discount decimal(4,2)` holds 0.00–0.50 correctly; `w_tax/d_tax decimal(4,2)` loses the spec's 4-decimal range [0.0000..0.2000] (sysbench inserts `uniform_double()*0.2` rounded to 2 places) — accept (HammerDB uses DECIMAL(4,4)); note in PROVENANCE.
5. Table names with numeric suffixes (`warehouse1`) if `--tables>1`; always use `--tables=1`.
6. Client auth: sysbench links libmariadb3 → must support `caching_sha2_password` (MySQL 9.x has no `mysql_native_password`): **Inferred** OK, verify at first run; HammerDB ships libmysqlclient 24.

# Programmable objects
None in the schema. sysbench-tpcc's transactions are Lua, HammerDB's MySQL TPROC-C uses stored procedures (`neword`, `payment`, `delivery`, `ostat`, `slev`) only when *running* the workload — not created by `buildschema`'s data load? (HammerDB creates them during build — **Inferred** from `mysqloltp.tcl` containing the procedure bodies.) Decision: **drop/skip** workload procedures; the image is a data sample, not a driver. If HammerDB is used, `DROP PROCEDURE` the five after load and record it.

# Indexing
* PKs: `warehouse(w_id)`, `district(d_w_id,d_id)`, `customer(c_w_id,c_d_id,c_id)`, `new_orders(no_w_id,no_d_id,no_o_id)`, `orders(o_w_id,o_d_id,o_id)`, `order_line(ol_w_id,ol_d_id,ol_o_id,ol_number)`, `item(i_id)`, `stock(s_w_id,s_i_id)`, `history(h_id)` surrogate.
* `indexes.sql` (tpcc-mysql/sysbench set): `customer (c_w_id,c_d_id,c_last,c_first)`, `orders (o_w_id,o_d_id,o_c_id,o_id)`, `stock (s_i_id)`, `order_line (ol_supply_w_id,ol_i_id)`, `history (h_c_w_id,h_c_d_id,h_c_id)`, `history (h_w_id,h_d_id)`.
* `constraints.sql`: `district→warehouse`, `customer→district`, `history→customer`, `history→district`, `new_orders→orders`, `orders→customer`, `order_line→orders`, `order_line→stock (ol_supply_w_id,ol_i_id)`, `stock→warehouse`, `stock→item`. Orphans expected 0 (all supply warehouses = home warehouse at population).
* No partitioning by default (HammerDB's `PARTITION BY HASH (ol_w_id)` needs FK removal).

# Tests and expected values
* Counts: `item` = 100,000; per W the table above (order_line within ±1% of 300,000·W); structural invariants: 10 districts per warehouse, 3,000 customers per district, `orders` o_id 1..3,000 per district, `new_orders` = orders with o_id > 2,100 (exactly 900/district), `o_carrier_id IS NULL` ⇔ `o_id > 2100`, `ol_delivery_d IS NULL` ⇔ `ol_o_id > 2100`, `SUM(ol_number)` per order = ol_cnt·(ol_cnt+1)/2, `d_next_o_id = 3001`, `w_ytd = 300000`, `d_ytd = 30000`.
* Digests computed after load (columns with NOW() excluded); a re-run with the same seed and `--threads=1` must reproduce them if the determinism question resolves positively.
* Smoke queries: the spec's Stock-Level read (`SELECT COUNT(DISTINCT s_i_id) … WHERE ol_o_id < d_next_o_id AND ol_o_id >= d_next_o_id - 20 AND s_quantity < 15`) and Order-Status lookup by `(c_w_id,c_d_id,c_last)`; EXPLAIN must use the customer name index.

# Tier assignment
**Extended**, generated: W=1 ≈ 0.5 M rows, **Inferred** ≈ 120–150 MB InnoDB with indexes (68.6 MB raw + item 8 MB + secondary indexes); the documented default **W=10** (≈ 5 M rows, ≈ 1–1.5 GB InnoDB, **Inferred**); smoke test **W=1**. Load time scales with W and `--threads`. See [size question](/questions/benchmark-innodb-size-per-sf.md).

# License and attribution
* Loader: sysbench-tpcc [Apache-2.0](/licenses/apache-2-0.md) (cloned at build, not vendored); sysbench [GPL-2.0](/licenses/gpl-2-0.md) (distro package, executed only); HammerDB [GPL-3.0](/licenses/gpl-3-0.md) (official image, executed only). No TPC EULA applies (no TPC software) — only the spec's copying notice and trademarks: "TPC Benchmark, TPC-C, and tpmC are trademarks of the Transaction Processing Performance Council."
* Our DDL is written from spec Clause 1.3 table layouts (copying permitted with notice), not copied from GPL HammerDB.
* Attribution string: "Schema and population rules derived from the TPC Benchmark™ C Standard Specification Revision 5.11 (© 2010 Transaction Processing Performance Council; copied by permission). Data populated with Percona-Lab/sysbench-tpcc (Apache-2.0) running on sysbench (GPL-2.0). TPC Benchmark, TPC-C and tpmC are trademarks of the Transaction Processing Performance Council. This database is derived from TPC-C and as such is not comparable to published TPC-C results, as it does not comply with the TPC-C Specification."

# Open questions
* [tpcc-loader-determinism](/questions/tpcc-loader-determinism.md) — seed coverage of sysbench-tpcc; whether to write a seeded file-based populator instead.
* [benchmark-innodb-size-per-sf](/questions/benchmark-innodb-size-per-sf.md).
* sysbench/libmariadb3 vs MySQL 9.7 `caching_sha2_password` — folded into the determinism question's first experiment (it must connect before anything else can be measured).
