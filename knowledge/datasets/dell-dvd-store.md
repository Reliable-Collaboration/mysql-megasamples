---
type: Dataset
title: Dell DVD Store 3 (DS3)
description: Dell/VMware's open-source OLTP benchmark schema (DVD e-commerce with reviews and memberships); Small size = 20,000 customers, 12,000 orders, 10,000 products, plus 200,000 reviews; MySQL kit; GPL-2.0-or-later.
resource: https://github.com/dvdstore/ds3
tags: [tier-core, tier-extended, csv, dvdstore, gpl-2-0, benchmark]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:48:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/readme.md
    title: root readme
    accessed: 2026-09-02
    version: master @ 8226cc0 (2021-11-08)
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/ds3_readme.txt
    title: ds3_readme.txt
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/ds3_schema.txt
    title: ds3_schema.txt
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/ds3_Documentation.txt
    title: ds3_Documentation.txt
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/build/mysqlds3_create_db.sql
    title: MySQL build scripts (create_db, create_ind, create_sp, trigger2, cleanup, loaders)
    accessed: 2026-09-02
  - resource: https://github.com/dvdstore/ds3/tree/master/ds3/data_files
    title: Small CSV files (measured)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/gpl.txt
    title: gpl.txt and source headers
    accessed: 2026-09-02
---

# Identity
DVD Store Version 3 by Dave Jaffe (Dell) and Todd Muirhead (VMware), DS2.1 features by Girish Khadke; a complete e-commerce benchmark (database + PHP web tier + C# driver). DS3 (2015) adds REVIEWS, REVIEWS_HELPFULNESS and MEMBERSHIP to DS2. Originally distributed from linux.dell.com/dvdstore, now at github.com/dvdstore/ds3 ([readme](/sources/github-dvdstore-ds3-readme.md), [documentation](/sources/github-dvdstore-ds3-documentation-txt.md)). Sakila borrowed its film/actor naming from DS2's predecessor.

# Source artifact
* Repository https://github.com/dvdstore/ds3 at commit `8226cc06584fde1688a37184c2bd9fbc6faf7282` (2021-11-08); no releases, no tags, no root LICENSE (320,941 KB repo). No auth.
* MySQL kit: `ds3/mysqlds3/build/mysqlds3_create_db.sql` (4,038 B), `mysqlds3_create_ind.sql` (2,437 B), `mysqlds3_create_sp.sql` (3,629 B), `mysqlds3_create_trigger2.sql` (197 B, broken), `mysqlds3_cleanup_*.sql`, `ds3/mysqlds3/load/**/mysqlds3_load_*.sql`, `mysqlds3_create_all.sh`.
* Small data (committed CSVs, see Shape) - total about 197 MB, of which reviews are 190.6 MB ([inspection](/sources/github-dvdstore-ds3-small-csv-files.md)). Checksums: none published; record blob SHAs from the git tree at build time.
* Generators: `ds3/data_files/{cust,orders,prod,reviews,membership}/ds3_create_*.c` (+ prebuilt Linux/Windows binaries), `ds3/Install_DVDStore.pl` (interactive, last updated 2021-10-25) for Medium (1 GB), Large (100 GB) or any custom size ([generators](/sources/github-dvdstore-ds3-data-files-and-generators.md)).

# Native format and friendlier forms
Native = MySQL DDL scripts + header-less CSV files loaded with `LOAD DATA LOCAL INFILE ... FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'` ([loaders](/sources/github-dvdstore-ds3-mysql-readme-and-loaders.md)). Oracle, SQL Server and PostgreSQL kits exist but are not needed.

# Shape
| table | rows (Small) | source |
|---|---|---|
| CUSTOMERS | 20,000 | us_cust.csv + row_cust.csv |
| ORDERS | 12,000 | 12 monthly files, 2013 |
| ORDERLINES | 60,350 | 12 monthly files |
| CUST_HIST | 60,350 | 12 monthly files |
| PRODUCTS | 10,000 | prod.csv |
| INVENTORY | 10,000 | inv.csv |
| CATEGORIES | 16 | INSERTs in create_db.sql |
| MEMBERSHIP | 2,000 | membership.csv |
| REORDER | 0 | (filled by the driver) |
| REVIEWS | 200,000 | reviews.csv (101.4 MB) |
| REVIEWS_HELPFULNESS | 4,106,382 | review_helpfulness.csv (89.2 MB) |

Upstream's "Small = 10 MB" label predates the review tables; the DS2-part CSVs total about 6.5 MB, the review CSVs 190 MB. Encoding: all sampled files pure ASCII, LF, no header, no quotes needed (names are random uppercase letters, e-mails `X@dell.com`, dates `YYYY/MM/DD`). No encoding canary exists in this dataset. **Inferred:** loaded InnoDB size about 15-25 MB without reviews, 300-400 MB with reviews and their indexes.

# Conversion path
Upstream DDL (InnoDB/utf8mb4-adjusted) + build-time CSV-to-SQL conversion; reviews deferred to the extended tier ([decision](/decisions/dvdstore-conversion-path.md)). Generic CSV loading notes: [tool note](/tools/smallcsv-load-data-infile.md).

# Type-mapping hazards
* `PRODUCTS ... ENGINE = MyISAM` with two FULLTEXT indexes - switch to InnoDB (FULLTEXT supported).
* Dates in CSV are `2013/01/27` (DATE) and `2019/03` (VARCHAR expiry) - **Inferred:** MySQL accepts `/` as a date delimiter in LOAD DATA; verify one row.
* `ZIP INT` receives `00000` (row_cust) -> 0; `CUSTOMERID` explicit in CSV although AUTO_INCREMENT; `ORDERS.CUSTOMERID` nullable with FK `ON DELETE SET NULL`.
* No character set on `CREATE DATABASE DS3`; all identifiers uppercase (`CUSTOMERS`, `CUST_HIST`) - case-sensitive on Linux; the project lower-cases them (`customers`, `cust_hist`, `reviews_helpfulness`) per the [naming convention](/decisions/database-naming-convention.md), so the upstream PHP/C# drivers would need the same rename if ever run against this image (documented deviation).
* `NUMERIC(12,2)` -> DECIMAL; `TINYINT` category/age; `VARCHAR(1000)` review text.
* Plaintext `PASSWORD` column ("password") and synthetic credit-card numbers - fake data, but document that it is synthetic.
* Loaders disable `UNIQUE_CHECKS`/`FOREIGN_KEY_CHECKS`; ORDERS must load before ORDERLINES/CUST_HIST if FKs are enforced.

# Programmable objects
* Ported (4 procedures, MySQL kit): `NEW_CUSTOMER`, `NEW_MEMBER`, `NEW_PROD_REVIEW`, `NEW_REVIEW_HELPFULNESS` ([create_sp](/sources/github-dvdstore-ds3-mysql-create-sp.md)); they use `SYSDATE()` and explicit `COMMIT` (fine in procedures; note non-deterministic for binlog).
* Not present in the MySQL kit (only described for Oracle/SQL Server): LOGIN, BROWSE_BY_CATEGORY/ACTOR/TITLE, GET_PROD_REVIEWS*, PURCHASE - the MySQL web tier implements them in PHP. Do not stub.
* Dropped: trigger `RESTOCK` (upstream comment "Doesn't work yet!!!", hard-coded values).

# Indexing
Port `mysqlds3_create_ind.sql` unchanged ([create_ind](/sources/github-dvdstore-ds3-mysql-create-ind.md)): unique username, FKs with CASCADE/SET NULL, FULLTEXT `IX_PROD_ACTOR`, `IX_PROD_TITLE`, review composite indexes. Create indexes after the bulk load.

# Tests and expected values
Row counts above (core: 9 tables; extended: + REVIEWS 200,000, REVIEWS_HELPFULNESS 4,106,382). Spot checks: `SELECT TITLE, ACTOR FROM PRODUCTS WHERE PROD_ID=1` = `ACADEMY ACADEMY`, `PENELOPE GUINESS`; `SELECT TOTALAMOUNT FROM ORDERS WHERE ORDERID=1` = 339.08; `SELECT COUNT(*) FROM CATEGORIES` = 16; `SELECT MAX(ORDERDATE) FROM ORDERS` within 2013 (**Inferred**). Record `CHECKSUM TABLE` after the first load; `mysqlds3_cleanup_small.sql` documents the baseline (customers <= 20000, orders <= 12000).

# Tier assignment
core for the DS2-part tables (about 6.5 MB CSV); extended for REVIEWS/REVIEWS_HELPFULNESS (190 MB CSV, 4.3 M rows) and for Medium/Large regenerated sizes. Evidence: [CSV inspection](/sources/github-dvdstore-ds3-small-csv-files.md).

# License and attribution
[GPL-2.0-or-later](/licenses/gpl-2-0.md): "Copyright (C) 2005 Dell, Inc." / "Copyright (C) 2014 VMware, Inc." with GPL v2-or-later headers on generators and drivers; `ds3/gpl.txt` shipped in the kit. Ship gpl.txt and the notices; mark modified scripts. Data-file status: [open question](/questions/dvdstore-generated-data-license.md).

# Database name
`dvdstore` (upstream: `DS3`), tables lower-cased per the [naming convention](/decisions/database-naming-convention.md).

# Open questions
* [License of the generated CSVs](/questions/dvdstore-generated-data-license.md).
* Whether to regenerate a deterministic Medium size at build time (needs a fixed seed patch to the C generators - `srand` usage not read in this session).
