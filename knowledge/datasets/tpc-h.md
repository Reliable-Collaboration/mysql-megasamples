---
type: Dataset
title: TPC-H (derived) — tpch
description: The eight-table decision-support schema of TPC Benchmark H, generated at a chosen scale factor by dbgen 2.17.3 (DuckDB port, cross-checked with tpch-kit), loaded from pipe-delimited files, with the 22 validation queries ported to MySQL; no pre-generated data is shipped.
resource: https://www.tpc.org/tpch/
tags:
- tier-generated
- generated
- tpc
- tpc-eula
- olap
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
- resource: https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp
  title: TPC current specifications (TPC-H v3.0.1)
  accessed: "2026-09-02"
- resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf
  title: TPC-H spec 3.0.1
  accessed: "2026-09-02"
- resource: https://www.tpc.org/TPC_Documents_Current_Versions/txt/EULA_v2.2.0.txt
  title: TPC EULA 2.2
  accessed: "2026-09-02"
- resource: https://github.com/gregrahn/tpch-kit
  title: tpch-kit @ 852ad0a
  accessed: "2026-09-02"
- resource: https://duckdb.org/docs/current/core_extensions/tpch.html
  title: DuckDB tpch extension
  accessed: "2026-09-02"
- resource: https://github.com/duckdb/duckdb/tree/main/extension/tpch
  title: DuckDB dbgen port source (2.17.3, TPC EULA)
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/load-data.html
  title: MySQL LOAD DATA
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/date-and-time-literals.html
  title: MySQL date literals
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/string-functions.html
  title: MySQL SUBSTRING forms
  accessed: "2026-09-02"
- resource: https://github.com/dhuny/tpch
  title: dhuny/tpch LOAD DATA script
  accessed: "2026-09-02"
- resource: https://github.com/catarinaribeir0/queries-tpch-dbgen-mysql
  title: Community MySQL port of the 22 queries
  accessed: "2026-09-02"
---

# Identity
* Proposed MySQL database: **`tpch`** (per [naming convention](/decisions/database-naming-convention.md)); tables `region, nation, supplier, part, partsupp, customer, orders, lineitem` (lower-case).
* What it is: the schema and population defined by TPC Benchmark H, Standard Specification Revision 3.0.1 ([spec record](/sources/tpc-h-specification-v3-0-1.md)); the population "must exactly match the output of DBGEN" (TPC README). We ship DDL, MySQL-ported queries and a generator runner — never generated rows.
* Naming rule (Fair Use): describe as "derived from TPC-H"; never publish QphH/timings as TPC results ([fair use](/sources/tpc-fair-use-quick-reference-v1-0-0.md)).

# Source artifact
| Item | Value |
|---|---|
| Official | `TPC-H_Tools_v3.0.1.zip` behind a registration form with EULA checkbox; link e-mailed ([form](/sources/tpc-tools-download-request-form.md)); size not shown; not automatable. Spec PDF 1.7 MB, freely downloadable. |
| Used instead (primary) | DuckDB `tpch` extension = port of dbgen **2.17.3** (`INSTALL tpch` at loader-image build, pinned DuckDB release; DuckDB v1.5.5 current on 2026-09-02) — [tool](/tools/duckdb-tpch-tpcds-extensions.md). |
| Used instead (cross-check, queries, answers) | https://github.com/gregrahn/tpch-kit @ `852ad0a5ee31ebefeed884cea4188781dd9613a3` (dbgen/qgen 2.17.3; GitHub API repo size 29,941 KB incl. docs and ref_data) — [tool](/tools/tpch-kit.md). |
| Checksums | None published by the TPC for the tools or output; the kit's `ref_data/<SF>/` holds sample reference files for dbgen validation; our pins are the commit SHA and the DuckDB version. |
| Version drift | Official tools 3.0.1 vs 2.17.3 mirrors: 3.0.x spec changes are metric-only, so data should be identical — [open question](/questions/tpch-dbgen-version-output-identity.md). |

# Native format and friendlier forms
dbgen writes eight ASCII files `<table>.tbl`, pipe-delimited with a **trailing `|` on every line**, dates `YYYY-MM-DD`, decimals with two places, no header, no quoting. DuckDB `COPY ... (FORMAT csv, DELIMITER '|', HEADER false)` writes the same layout **without** the trailing pipe. There is no friendlier upstream form (no SQL dump, no CSV); DuckDB's pre-generated `.duckdb` files exist only for TPC-DS.

# Shape (SF = 1; spec Table 3 / Table 4)
| Table | Rows at SF=1 | Scales | Typical row | Raw size |
|---|---|---|---|---|
| region | 5 | fixed | 124 B | <1 MB |
| nation | 25 | fixed | 128 B | <1 MB |
| supplier | 10,000 | ×SF | 159 B | 2 MB |
| part | 200,000 | ×SF | 155 B | 30 MB |
| partsupp | 800,000 | ×SF | 144 B | 110 MB |
| customer | 150,000 | ×SF | 179 B | 26 MB |
| orders | 1,500,000 | ×SF | 104 B | 149 MB |
| lineitem | **6,001,215** | ≈×SF (SF10 59,986,052; SF100 600,037,902) | 112 B | 641 MB |
| total | 8,661,245 | | | 956 MB (1 MB = 2^20 B) |

Fractional SFs (0.01, 0.1) are supported by both generators but are non-compliant sizes; counts scale linearly except lineitem (avg 4 lines/order) — obtain from `SELECT COUNT(*)` after generation. Encoding: TPC-H text is generated from an English word grammar; **Inferred:** pure ASCII (verify with `LC_ALL=C grep -P '[\x80-\xff]' *.tbl`). Text columns hold lorem-style comments, `Customer#000000001`, `Supplier#000000001`, phone strings like `25-989-741-2988`, upper-case nation/region names.

MySQL DDL (from `dss.ddl`, MySQL-ised; keys per `dss.ri`):
```sql
CREATE TABLE region   (r_regionkey INT NOT NULL, r_name CHAR(25) NOT NULL, r_comment VARCHAR(152), PRIMARY KEY (r_regionkey));
CREATE TABLE nation   (n_nationkey INT NOT NULL, n_name CHAR(25) NOT NULL, n_regionkey INT NOT NULL, n_comment VARCHAR(152), PRIMARY KEY (n_nationkey));
CREATE TABLE supplier (s_suppkey INT NOT NULL, s_name CHAR(25) NOT NULL, s_address VARCHAR(40) NOT NULL, s_nationkey INT NOT NULL, s_phone CHAR(15) NOT NULL, s_acctbal DECIMAL(15,2) NOT NULL, s_comment VARCHAR(101) NOT NULL, PRIMARY KEY (s_suppkey));
CREATE TABLE part     (p_partkey INT NOT NULL, p_name VARCHAR(55) NOT NULL, p_mfgr CHAR(25) NOT NULL, p_brand CHAR(10) NOT NULL, p_type VARCHAR(25) NOT NULL, p_size INT NOT NULL, p_container CHAR(10) NOT NULL, p_retailprice DECIMAL(15,2) NOT NULL, p_comment VARCHAR(23) NOT NULL, PRIMARY KEY (p_partkey));
CREATE TABLE partsupp (ps_partkey INT NOT NULL, ps_suppkey INT NOT NULL, ps_availqty INT NOT NULL, ps_supplycost DECIMAL(15,2) NOT NULL, ps_comment VARCHAR(199) NOT NULL, PRIMARY KEY (ps_partkey, ps_suppkey));
CREATE TABLE customer (c_custkey INT NOT NULL, c_name VARCHAR(25) NOT NULL, c_address VARCHAR(40) NOT NULL, c_nationkey INT NOT NULL, c_phone CHAR(15) NOT NULL, c_acctbal DECIMAL(15,2) NOT NULL, c_mktsegment CHAR(10) NOT NULL, c_comment VARCHAR(117) NOT NULL, PRIMARY KEY (c_custkey));
CREATE TABLE orders   (o_orderkey BIGINT NOT NULL, o_custkey INT NOT NULL, o_orderstatus CHAR(1) NOT NULL, o_totalprice DECIMAL(15,2) NOT NULL, o_orderdate DATE NOT NULL, o_orderpriority CHAR(15) NOT NULL, o_clerk CHAR(15) NOT NULL, o_shippriority INT NOT NULL, o_comment VARCHAR(79) NOT NULL, PRIMARY KEY (o_orderkey));
CREATE TABLE lineitem (l_orderkey BIGINT NOT NULL, l_partkey INT NOT NULL, l_suppkey INT NOT NULL, l_linenumber INT NOT NULL, l_quantity DECIMAL(15,2) NOT NULL, l_extendedprice DECIMAL(15,2) NOT NULL, l_discount DECIMAL(15,2) NOT NULL, l_tax DECIMAL(15,2) NOT NULL, l_returnflag CHAR(1) NOT NULL, l_linestatus CHAR(1) NOT NULL, l_shipdate DATE NOT NULL, l_commitdate DATE NOT NULL, l_receiptdate DATE NOT NULL, l_shipinstruct CHAR(25) NOT NULL, l_shipmode CHAR(10) NOT NULL, l_comment VARCHAR(44) NOT NULL, PRIMARY KEY (l_orderkey, l_linenumber));
```
(`BIGINT` for orderkey because the spec sizes it as "int up to SF 300"; everything else is INT/DECIMAL(15,2)/CHAR/VARCHAR/DATE exactly as `dss.ddl`.) Character set `utf8mb4`; **Inferred:** collation `utf8mb4_bin` so ORDER BY/LIKE on text match the reference answers produced with ASCII ordering — confirm by the Q1–Q22 comparison test.

# Conversion path
**Chosen:** `make gen-tpch SF=1` in the loader image runs DuckDB: `INSTALL tpch; LOAD tpch; CALL dbgen(sf=$SF)` (with `children/step` partitions when SF ≥ 10), `COPY <table> TO '/build/tpch/<table>.tbl' (FORMAT csv, DELIMITER '|', HEADER false)`, computes `baseline.json` (counts, canonical digests) from the DuckDB tables, then loads MySQL with `LOAD DATA LOCAL INFILE ... FIELDS TERMINATED BY '|'` in the order region→nation→supplier→part→partsupp→customer→orders→lineitem, PKs pre-created, then `indexes.sql`, `constraints.sql`, `ANALYZE TABLE`. Decision and alternatives (tpch-kit C build; direct `ATTACH ... TYPE mysql`): [tpch-generator-path](/decisions/tpch-generator-path.md). If the fidelity experiment fails, the fallback is tpch-kit's dbgen in a builder stage with `LINES TERMINATED BY '|\n'` to absorb the trailing pipe.

# Type-mapping hazards
1. Trailing `|` in dbgen output: use `LINES TERMINATED BY '|\n'` ([dhuny](/sources/github-dhuny-tpch.md)) or accept "extra fields are ignored" warnings ([LOAD DATA](/sources/mysql-refman-9-7-load-data.md)); DuckDB export has no trailing pipe.
2. `CHAR(n)` columns: dbgen emits unpadded values; MySQL CHAR pads on store and strips on read — digests must `RTRIM` on both sides ([checksum method](/decisions/test-checksum-method.md) already allows this for padded sources).
3. DECIMAL(15,2) round-trips exactly; `l_discount`/`l_tax` are 0.00–0.10 / 0.00–0.08.
4. Query text: the 22 qgen/DuckDB queries need these MySQL edits (community-verified on [catarinaribeir0](/sources/github-catarinaribeir0-queries-tpch-dbgen-mysql.md); MySQL syntax verified in the manual): keep `date '1998-12-01'` (standard literal accepted, [date literals](/sources/mysql-refman-9-7-date-and-time-literals.md)); keep `interval '90' day` but **delete the SQL-92 precision suffix `(3)`** from Q1's template; `extract(year from o_orderdate)` and `substring(c_phone from 1 for 2)` are supported ([string functions](/sources/mysql-refman-9-7-string-functions.md)); row limits use `limit N` (qgen `DATABASE=POSTGRESQL` emits this; Q2 100, Q3 10, Q10 20, Q18 100, Q21 100); Q15 `create view revenue0 … drop view` works as-is; Q13 `not like '%special%requests%'` fine; **Inferred until run:** no other rewrites are needed — see [query syntax question](/questions/mysql-tpch-query-port-syntax.md).
5. Reference answers print `avg_disc` as `0.05`/`.05` and the spec truncates to two decimals; compare numerically with tolerance (`check_answers/colprecision.txt` semantics), not textually.

# Programmable objects
None in the schema. Q15's temporary view is part of the query script, created with `SQL SECURITY INVOKER`-irrelevant plain `CREATE VIEW` by the `demo` user? No — `demo` has SELECT only; ship Q15 in its CTE form (`with revenue0 as (...)`) which is also a listed variant (`variants/15a.sql`). Nothing ported/stubbed/dropped.

# Indexing
Per [indexing strategy](/decisions/indexing-strategy.md) rule 1 (declared keys carried over) and rule 2 for benchmark-motivated secondaries:
* PKs as in `dss.ri` (above); lineitem loaded pre-sorted by (l_orderkey, l_linenumber) — dbgen already emits that order.
* `indexes.sql`: `lineitem (l_partkey, l_suppkey)`, `lineitem (l_suppkey)`, `lineitem (l_shipdate)`, `lineitem (l_orderkey, l_suppkey)`; `orders (o_custkey)`, `orders (o_orderdate)`; `partsupp (ps_suppkey)`; `customer (c_nationkey)`; `supplier (s_nationkey)`; `nation (n_regionkey)`.
* `constraints.sql`: the eight FKs of `dss.ri` (nation→region, supplier→nation, customer→nation, partsupp→part, partsupp→supplier, orders→customer, lineitem→orders, lineitem(l_partkey,l_suppkey)→partsupp). Orphans expected: 0.
* Optional `indexes-partitioned.sql`: none for TPC-H (FKs would have to be dropped).

# Tests and expected values
* Counts at SF=1 exactly as the Shape table (lineitem 6,001,215; total 8,661,245); at other SFs from the generator's `baseline.json`.
* Q1 (DELTA=90) at SF=1 must return the four rows of the spec's validation output / `answers/q1.out`: `A|F|37734107.00|56586554400.73|53758257134.87|55909065222.83|25.52|38273.13|0.05|1478493`, `N|F|991417.00|1487504710.38|1413082168.05|1469649223.19|25.52|38284.47|0.05|38854`, `N|O|74476040.00|111701729697.74|106118230307.61|110367043872.50|25.50|38249.12|0.05|2920374`, `R|F|37719753.00|56568041380.90|53741292684.60|55889619119.83|25.51|38250.85|0.05|1478870`.
* Q1–Q22 at SF 0.01, 0.1 and 1 compared with DuckDB `tpch_answers()` (numeric tolerance per column precision); at SF=1 additionally with tpch-kit `answers/`.
* Row digests (BIT_XOR/SUM of canonical rows) computed by the generator step from DuckDB before export and re-computed in MySQL after load ([checksum method](/decisions/test-checksum-method.md)); `CHAR` columns RTRIM'd.
* EXPLAIN smoke set: Q1 (range on l_shipdate), Q3, Q6 must not full-scan `lineitem` without the shipdate index? — Q1 scans ~95% of lineitem by design; exempt Q1 from the no-`ALL` rule, keep Q6/Q14 (date range) and Q4/Q12 (orders join).

# Tier assignment
**Extended** (generated at `make gen-tpch SF=…`, never baked): SF=1 raw 956 MB, InnoDB with the indexes above **Inferred** 1.5–2.5 GB; SF=0.01 ≈ 10 MB raw (**Inferred**, linear) is the CI smoke size; documented default **SF=1**; SF=10 ≈ 10 GB raw needs the partitioned DuckDB generation and ≥ 30 GB free disk (**Inferred**). Evidence: spec Table 3 sizes ([spec](/sources/tpc-h-specification-v3-0-1.md)); InnoDB factor is an estimate to be measured ([size question](/questions/benchmark-innodb-size-per-sf.md)).

# License and attribution
* Tools and any query/DDL text derived from them: [TPC EULA v2.2](/licenses/tpc-eula.md) — the repo clones/installs at build time and vendors nothing; `datasets/tpch/LICENSE` carries the EULA copy plus the legend "THE TPC SOFTWARE IS AVAILABLE WITHOUT CHARGE FROM TPC." for any TPC-derived text we do ship (our DDL is written from the spec's Clause 1.4 table definitions, which the spec permits copying "for the primary purpose of disseminating TPC material" with the copyright notice, title and date).
* Generated rows: not addressed by the EULA → we ship none ([question](/questions/tpc-eula-generated-data-redistribution.md)); if a user publishes a dump, the README says the data was produced with TPC dbgen 2.17.3 and carries the disclaimer.
* Attribution string: "Derived from the TPC Benchmark™ H Standard Specification Revision 3.0.1 (© 1993–2022 Transaction Processing Performance Council); data generated with TPC dbgen 2.17.3. TPC Benchmark and TPC-H are trademarks of the Transaction Processing Performance Council. This database is derived from TPC-H and as such is not comparable to published TPC-H results, as it does not comply with the TPC-H Specification."

# Open questions
* [tpch-dbgen-version-output-identity](/questions/tpch-dbgen-version-output-identity.md) — 2.17.3 mirrors vs official 3.0.1.
* [duckdb-generator-fidelity](/questions/duckdb-generator-fidelity.md) — DuckDB port vs C dbgen byte identity; ATTACH-mysql throughput.
* [mysql-tpch-query-port-syntax](/questions/mysql-tpch-query-port-syntax.md) — exact MySQL edits for all 22 queries and the collation choice.
* [tpc-query-text-redistribution](/questions/tpc-query-text-redistribution.md) — ship ported query text in the repo vs generate + sed at build.
* [benchmark-innodb-size-per-sf](/questions/benchmark-innodb-size-per-sf.md).
