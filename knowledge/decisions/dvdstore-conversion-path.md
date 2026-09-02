---
type: Decision
title: Dell DVD Store 3 conversion path - upstream MySQL DDL plus server-side LOAD DATA of the committed Small CSVs; reviews split to extended
description: Reuse mysqlds3_create_db/ind/sp with InnoDB and utf8mb4 fixes, load the ~6.5 MB DS2-part CSVs into the build server during `make dvdstore`, defer the 190 MB reviews CSVs to the extended tier, drop the broken RESTOCK trigger.
resource: /decisions/dvdstore-conversion-path.md
tags: [dvdstore, decision, csv, load-data]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/build/mysqlds3_create_db.sql
    title: mysqlds3_create_db.sql
    accessed: "2026-09-02"
  - resource: https://github.com/dvdstore/ds3/tree/master/ds3/data_files
    title: Small CSV inspection
    accessed: "2026-09-02"
---

# Question
How to build the DS3 database for the image, and which parts belong in core.

# Options considered
1. Run the upstream kit verbatim (`mysqlds3_create_all.sh`): needs user `web`, `LOAD DATA LOCAL INFILE` with relative paths, MyISAM PRODUCTS - not suitable for the entrypoint.
2. Keep the upstream DDL (edited: `ENGINE=InnoDB` for PRODUCTS, `CHARACTER SET utf8mb4` on the database, lowercase database name `dvdstore`), and load the CSVs with server-side `LOAD DATA INFILE` from a staging directory allowed by `secure_file_priv`, or pre-convert CSV to multi-row INSERT `.sql.zst` at build time (no server settings needed).
3. Regenerate data with the C generators (Linux build) at image build time - non-deterministic (`rand()` without a fixed seed documented), adds a compiler to the build; rejected for core, viable for custom sizes in extended.

# Evidence
* DDL/index/procedure scripts ([create_db](/sources/github-dvdstore-ds3-mysql-create-db.md), [create_ind](/sources/github-dvdstore-ds3-mysql-create-ind.md), [create_sp](/sources/github-dvdstore-ds3-mysql-create-sp.md)); loaders ([readme and loaders](/sources/github-dvdstore-ds3-mysql-readme-and-loaders.md)).
* Small CSV sizes: DS2-part tables about 6.5 MB total; reviews.csv 101 MB + review_helpfulness.csv 89 MB = 200,000 + 4,106,382 rows ([inspection](/sources/github-dvdstore-ds3-small-csv-files.md)).
* InnoDB supports the two FULLTEXT indexes on PRODUCTS (Sakila already relies on InnoDB FULLTEXT).

# Outcome
Option 2: the CSVs are converted to the project's contract TSV (with `build/baseline.json` computed from the parsed rows) and loaded into the build server with server-side `LOAD DATA`, exactly like every other dataset ([bake decision](/decisions/bake-data-vs-initdb.md)); the runtime image carries the baked result. Core tier: CUSTOMERS, ORDERS, ORDERLINES, CUST_HIST, PRODUCTS, INVENTORY, CATEGORIES, MEMBERSHIP, REORDER (empty) and the four procedures. Extended tier: REVIEWS and REVIEWS_HELPFULNESS loaded from the same repository at build/start when enabled. Drop `mysqlds3_create_trigger2.sql` (upstream marks it "Doesn't work yet"). Pin commit `8226cc06584fde1688a37184c2bd9fbc6faf7282`.

# Status
accepted
