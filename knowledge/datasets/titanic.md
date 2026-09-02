---
type: Dataset
title: Titanic (titanic3, Vanderbilt Biostatistics)
description: Thomas Cason's 1,309-passenger Titanic survival dataset (14 columns) hosted by Frank Harrell's hbiostat.org under a blanket permission with acknowledgement; chosen over Kaggle's login-gated 891-row train set.
resource: https://hbiostat.org/data/repo/titanic3.csv
tags: [tier-core, csv, titanic, smallsets, permission]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:48:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://hbiostat.org/data/
    title: Vanderbilt Biostatistics Datasets (permission statement)
    accessed: "2026-09-02"
  - resource: https://hbiostat.org/data/repo/titanic.html
    title: Titanic Data description
    accessed: "2026-09-02"
  - resource: https://hbiostat.org/data/repo/titanic3.csv
    title: titanic3.csv (measured)
    accessed: "2026-09-02"
    version: "md5 01b027be0a49ab8538efbd60a8c43288"
  - resource: https://hbiostat.org/data/repo/titanic5.html
    title: titanic5 notes
    accessed: "2026-09-02"
---

# Identity
"titanic3": survival status of 1,309 Titanic passengers (no crew), compiled from the Encyclopedia Titanica and Eaton & Haas (1994) by Thomas Cason (University of Virginia) as of 2 August 1999 and distributed by Frank Harrell's Vanderbilt Biostatistics data repository ([description](/sources/hbiostat-titanic-description.md)). Kaggle's "Titanic - Machine Learning from Disaster" train.csv (891 rows) is a subset of this data behind a login and competition terms - not used. A 2016 revision "titanic5" (fewer missing ages) exists but titanic3 is the widely cited form ([csv inspection](/sources/hbiostat-titanic3-csv.md)).

# Source artifact
https://hbiostat.org/data/repo/titanic3.csv - 116,752 bytes, md5 `01b027be0a49ab8538efbd60a8c43288`, sha256 `db6df9666818c69a753cd85d743e01502c8518b00579b6aada0d4fc5a66ccb9d`; no auth; no snapshot/version label (page last modified 2002 for the description; the data reflects 1999-08-02). Also available as .sav/.dta/.xls and via R `Hmisc::getHdata(titanic3)`. Vendor the CSV (small; permission allows).

# Native format and friendlier forms
CSV with quoted strings, header row, empty fields for missing values. Nothing else needed.

# Shape
1,309 rows; columns: pclass (1-3), survived (0/1), name, sex, age (years, fractional for infants e.g. 0.92; 263 missing), sibsp, parch, ticket, fare (4 decimals, e.g. 211.3375), cabin (may hold several codes "C22 C26"), embarked (C/Q/S), boat (lifeboat id, may be non-numeric), body (body id number), home.dest. Encoding: pure ASCII, LF - no encoding canary. Loaded size negligible (<1 MB).

# Conversion path
Build-time CSV-to-INSERT conversion (or LOAD DATA) into explicit DDL ([small-sets decision](/decisions/smallsets-database-layout.md); CSV notes [tool note](/tools/smallcsv-load-data-infile.md)).

# Type-mapping hazards
* Column `home.dest` contains a dot - rename to `home_dest` (document the rename).
* `age DECIMAL(5,2)`, `fare DECIMAL(9,4)`, `pclass TINYINT`, `survived BOOLEAN/TINYINT`, `sibsp/parch TINYINT`, `body SMALLINT NULL`, `boat VARCHAR(8)` (values like "13 15 B" exist - **Inferred** from the known dataset; verify max length), `cabin VARCHAR(20)`, `name VARCHAR(100)`, `ticket VARCHAR(20)`.
* Empty strings -> NULL for numeric columns (`NULLIF`).
* No natural primary key (names are not unique) - add `passenger_id INT AUTO_INCREMENT` in file order.

# Programmable objects
None. Optional view `survival_by_class` (**Inferred**, nice-to-have).

# Indexing
Surrogate PK; index on (pclass, sex) for the classic aggregation queries.

# Tests and expected values
`COUNT(*)` = 1309; `SUM(survived)` = 500 (**Inferred** from the well-known dataset; verify at load); `COUNT(*) WHERE age IS NULL` = 263 (stated in titanic5 notes as "263" missing in titanic3); `SELECT name FROM titanic WHERE passenger_id=1` = `Allen, Miss. Elisabeth Walton`; file md5 pinned.

# Tier assignment
core (117 KB). Evidence: [csv inspection](/sources/hbiostat-titanic3-csv.md).

# License and attribution
[hbiostat permission](/licenses/hbiostat-data-permission.md): include "Data obtained from http://hbiostat.org/data courtesy of the Vanderbilt University Department of Biostatistics." and cite Encyclopedia Titanica / Eaton & Haas (1994) / Thomas Cason. Not a formal open license - [open question](/questions/titanic-hbiostat-license-status.md).

# Database name
`smallsets`, table `titanic` (per the [naming convention](/decisions/database-naming-convention.md) and [small-sets decision](/decisions/smallsets-database-layout.md)); the alternative of a separate `titanic` database was not adopted.

# Open questions
* [Formal license status](/questions/titanic-hbiostat-license-status.md).
