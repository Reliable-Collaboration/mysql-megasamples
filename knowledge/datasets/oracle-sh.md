---
type: Dataset
title: Oracle SH (Sales History) sample schema
description: Oracle's star-schema data-warehouse sample (918,843 SALES facts, 55,500 customers, 9 tables) whose v23.3 data ships as six plain CSV files loaded by SQLcl; converted with LOAD DATA, partitions/bitmap indexes/MVs/dimensions replaced.
resource: https://github.com/oracle-samples/db-sample-schemas/tree/v23.3/sales_history
tags: [tier-core, medium, oracle, sh, star-schema, csv, mit]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: /sources/github-oracle-samples-db-sample-schemas-releases-and-tree.md
    title: Releases, tags, tree sizes
    accessed: 2026-09-02
  - resource: /sources/github-oracle-samples-db-sample-schemas-sh-scripts.md
    title: sh_install/sh_create/sh_populate scripts and CSV samples
    accessed: 2026-09-02
  - resource: /sources/oracle-docs-database-sample-schemas-guide-23-comsc.md
    title: Oracle Sample Schemas guide (SH pages, SQLcl requirement)
    accessed: 2026-09-02
  - resource: /sources/oracle-docs-sqlcl-26-2-load-and-sqlformat.md
    title: SQLcl LOAD defaults
    accessed: 2026-09-02
  - resource: /sources/github-oracle-samples-db-sample-schemas-oe-pm-ix-scripts.md
    title: v19.2 SQL*Loader control files (for comparison)
    accessed: 2026-09-02
  - resource: /sources/mysql-refman-9-7-char.md
    title: MySQL CHAR semantics
    accessed: 2026-09-02
---

# Identity
Oracle "SH" — sales fact table with costs, customers (+ supplementary demographics), products, promotions, channels, countries and a 5-year times dimension. Current in v23.3 / 26ai guide ("designed to allow for demos with large amounts of data"). Proposed MySQL database name: **`oracle_sh`**.

# Source artifact
* Same repo/tag/commit as HR (v23.3 = `e3325a8`; note the 2024-03-28 commit that moved the tag is exactly "Update supplementary demographics data (#24)", so SH data differs between the 2023 release zip and the current tag — pin the SHA).
* Files (bytes): `sales_history/sh_install.sql` 8,412; `sh_create.sql` 25,051; `sh_populate.sql` 41,072; `sh_uninstall.sql` 2,902; **`sales.csv` 74,426,366; `customers.csv` 12,615,719; `costs.csv` 2,658,415; `supplementary_demographics.csv` 701,892; `times.csv` 439,487; `promotions.csv` 56,158** (CSV total 90,898,037; directory 90,977,907). Raw URLs `https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/<sha>/sales_history/<file>` served with `content-type: text/plain; charset=utf-8` and `Content-Length` matching the API sizes; no auth or click-through. Schema version "21.1", release date 06-DEC-2022.
* Checksums: none upstream; executor records sha256 per file. Row counts are published inside `sh_install.sql` (below).

# Native format and friendlier forms
* Small dimensions (`channels` 5, `countries` 35, `products` 72) are literal `INSERT ... VALUES` in `sh_populate.sql` (products use `to_date('2019-01-01-00-00-00','YYYY-MM-DD-HH24-MI-SS')`).
* Everything else is **plain CSV** loaded by SQLcl `LOAD <table> <file>.csv` after `SET LOAD BATCH_ROWS 10000 BATCHES_PER_COMMIT 1 DATE_FORMAT YYYY-MM-DD` — which is why the README says "Requires SQLcl" and the docs say "You cannot use SQL*Plus to install the sh schema". The v19.2 layout used pipe-delimited `.dat` files with SQL*Loader `.ctl` files (`FIELDS TERMINATED BY "|"`, `DATE(19) "YYYY-MM-DD-HH24-MI-SS"`); v23 replaced them with header-bearing comma CSVs, so **no Oracle product and no SQLcl are needed**: any RFC-4180 reader / `LOAD DATA LOCAL INFILE` works.
* CSV dialect (observed): header row of double-quoted column names in DDL order; comma delimiter; strings double-quoted, numbers/dates unquoted; dates `YYYY-MM-DD` (no time in any date column); NULL number/date = empty field; NULL string = `""`; LF endings, no CR; UTF-8 declared, ASCII observed. **`sales.csv` rows are space-padded to exactly 80 characters** (trailing blanks after `AMOUNT_SOLD`); the other files are not padded. `times.csv` is unsorted.

# Shape
| table | rows | DDL notes |
|---|---|---|
| channels | 5 | 6 cols; `channel_id NUMBER` PK |
| countries | 35 | 9 cols; `country_id NUMBER` PK, `country_iso_code CHAR(2)` (the brief's "23" is wrong for v23.3) |
| customers | 55,500 | 23 cols; `cust_id NUMBER` PK; `cust_gender CHAR(1)`; `cust_year_of_birth NUMBER(4)`; `cust_marital_status` nullable; `cust_credit_limit NUMBER`; `cust_eff_from/to DATE`; FK countries |
| products | 72 | 22 cols; `prod_id NUMBER(6)` PK; `prod_desc VARCHAR2(4000)`; `prod_list_price/prod_min_price NUMBER(8,2)` |
| promotions | 503 | 11 cols; `promo_id NUMBER(6)` PK; `promo_cost NUMBER(10,2)`; begin/end DATE |
| times | 1,826 | 38 cols; `time_id DATE` PK, 2019-01-01 … 2023-12-31; `calendar_quarter_desc CHAR(7)` |
| sales | **918,843** | 7 cols; no PK; FKs to products, customers, times, channels, promotions; range-partitioned by `time_id` (15 partitions up to 2023-01-01) |
| costs | 82,112 | 6 cols; FKs; 20 `COMPRESS` range partitions up to 2024-01-01 |
| supplementary_demographics | 4,500 | 14 cols; `cust_id NUMBER` PK; `comments VARCHAR2(4000)` free text with an Oracle Text index |

Total ≈ 1.06 M rows. Loaded InnoDB size **inferred** ≈ 150–250 MB (sales ≈ 918 k × ~30 B data + 5 secondary indexes; customers ≈ 15 MB) — must be measured (task for the executor); dump compressed with zstd is expected to be ≈ 20–30 MB (**inferred** from 74 MB of highly repetitive padded CSV).
Encoding: no non-ASCII bytes seen in three 64 KB samples of `customers.csv`, the whole `promotions.csv`, the CSV heads/tails, or `sh_populate.sql`; treat as ASCII/UTF-8 (full-file verification is a one-line `grep -P` at build time).

# Conversion path
Path (a): Python converter emits MySQL DDL, inserts the three small dimensions from the parsed script, and loads the six CSVs with `LOAD DATA LOCAL INFILE ... FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES` after a streaming pre-pass that (1) strips trailing whitespace from every `sales.csv` line, (2) converts `""` to `\N` for nullable string columns (Oracle treats `''` as NULL; MySQL would store an empty string), and (3) leaves `,,` as NULL (`LOAD DATA` maps empty unquoted fields of numeric/date columns to `NULL` only with explicit `SET col = NULLIF(@v,'')` — the converter uses user variables for the nullable columns). See [decision](/decisions/oracle-conversion-path.md). No Oracle container required.

# Type-mapping hazards
* Unconstrained `NUMBER` keys (`cust_id`, `country_id`, `channel_id`, `*_id` hierarchy ids, `cust_credit_limit`, `yrs_residence`, `days_in_*`) → `INT` after the converter asserts every value is integral (all sampled values are); `NUMBER(6)`/`NUMBER(4)`/`NUMBER(3)`/`NUMBER(1)`/`NUMBER(2)` → `INT`/`SMALLINT`/`TINYINT`; `NUMBER(10,2)`/`NUMBER(8,2)` → `DECIMAL(10,2)`/`DECIMAL(8,2)`; `NUMBER(10)` flags → `INT` (values 0/1).
* `DATE` columns → `DATE` (no time component in any CSV value or script literal); `time_id` stays `DATE` so `times` remains a proper calendar dimension.
* `CHAR(1)`/`CHAR(2)`/`CHAR(7)` → `CHAR(n)`; values are always full length so MySQL's trailing-space stripping ([CHAR semantics](/sources/mysql-refman-9-7-char.md)) has no visible effect.
* `VARCHAR2(4000)` → `VARCHAR(4000)` (utf8mb4: 16,000 bytes, under the 65,535-byte row limit but `products` has two of them plus `VARCHAR2(2000)`×2 → row max ≈ 40 KB, still under the limit; alternatively `TEXT`). Keep `VARCHAR`.
* `sales` has **no primary key** upstream ("all rows are uniquely identified by the combination of all foreign keys" — the comment even admits duplicates are possible). InnoDB works without a PK (hidden row id) but `mysqlsh util.dumpTables`/`loadDump` chunking and replication prefer one; add an invisible `sales_id BIGINT AUTO_INCREMENT INVISIBLE PRIMARY KEY`? **Recommendation (inferred, invisible-column syntax from memory):** add `INVISIBLE` surrogate PK columns to `sales` and `costs` (does not change `SELECT *`), document it.
* **Partitioning:** **Inferred:** (from memory, verify on 9.7) InnoDB partitioned tables cannot carry foreign keys; keep the FKs and **drop partitioning** (document the original 15/20 range partitions in the table COMMENT). `COMPRESS` → nothing (or `ROW_FORMAT=COMPRESSED`, not recommended).
* **Bitmap indexes** (sales ×5, costs ×2, products, customers ×3) → ordinary B-tree indexes on the same columns (the FK columns get them anyway).
* **Oracle Text** `sup_text_idx` (`INDEXTYPE IS ctxsys.context`) → `FULLTEXT INDEX (comments)` (InnoDB FULLTEXT; behaviour differs from Oracle Text, documented).
* **Materialized views** `cal_month_sales_mv`, `fweek_pscat_sales_mv` (+ their bitmap indexes) → create as ordinary `VIEW`s with the same names (query rewrite is lost; documented).
* **Dimensions** (`CREATE DIMENSION customers_dim, products_dim, times_dim, channels_dim, promotions_dim`) → dropped; no MySQL equivalent; hierarchies are implicit in the `*_id` columns.
* `dbms_stats.gather_schema_stats` → `ANALYZE TABLE`.
* Constraint enable/disable NOVALIDATE choreography → `SET foreign_key_checks=0` during load, then `1`; the executor must verify the FK checks pass afterwards (the upstream `NOVALIDATE` hints that upstream never validated them; `promo_id` 999 appears in sales/costs and must exist in promotions — check).

# Programmable objects
| object | action |
|---|---|
| view `profits` | port verbatim (4-column equi-join) |
| MVs `cal_month_sales_mv`, `fweek_pscat_sales_mv` | recreate as plain views |
| dimensions ×5 | drop (documented) |
| Oracle Text index | replace with FULLTEXT |
| partitions, bitmap/LOCAL indexes, COMPRESS, NOLOGGING | drop/replace as above |
| `COMMENT ON` | port |

# Indexing
PK/FK indexes; B-tree replacements for the bitmap indexes; `products(prod_subcategory)`, `products(prod_category)`; FULLTEXT on `supplementary_demographics(comments)`. Load order: dimensions, then `costs`, `sales` with FK checks off, then `ALTER TABLE ... ADD INDEX` after bulk load for speed (**inferred** best practice).

# Tests and expected values
* Row counts from `sh_install.sql`: channels 5, costs 82,112, countries 35, customers 55,500, products 72, promotions 503, **sales 918,843**, times 1,826, supplementary_demographics 4,500. `wc -l` minus header on each CSV must reproduce the CSV-loaded counts (`promotions.csv` = 503 data rows verified).
* `SELECT MIN(time_id), MAX(time_id) FROM sales` within 2019-01-01 … 2022-12-31 (partition bounds) and `costs` within 2019-01-01 … 2023-12-31; `SELECT COUNT(*) FROM times` = 1826 = 2019-01-01..2023-12-31.
* `SELECT SUM(amount_sold) FROM sales` — record at build time as the baseline (no upstream figure). First `sales.csv` row is `(13, 987, 2019-01-10, 3, 999, 1, 1232.16)`.
* NULL semantics: `SELECT COUNT(*) FROM customers WHERE cust_marital_status IS NULL` must be > 0 and `... = ''` must be 0.

# Tier assignment
**core (medium)** — ≈ 1.06 M rows, 91 MB CSV, estimated 150–250 MB InnoDB: within the "medium core" band of the [tier model](/decisions/tier-model.md) (Employees-class). Downgrade to extended only if the measured loaded size exceeds the band; the compressed dump (~25 MB inferred) is cheap to bake.

# License and attribution
MIT — [MIT record](/licenses/mit.md). The CSVs carry no license header; the per-schema README and the repo LICENSE.txt cover them.

# Open questions
* [SH CSV row counts, padding and NULL handling](/questions/oracle-sh-csv-row-counts-and-padding.md): confirm 918,843 lines, whether `LOAD DATA` tolerates the 80-column padding without pre-processing, and the measured InnoDB size.
