---
type: Source
title: oracle-samples/db-sample-schemas releases, tags, and file trees (GitHub API)
description: Release list, tag-to-commit mapping, per-file sizes for v23.3 / v19.2 / main, and the v23.3..main diff, read through the GitHub REST API.
resource: https://api.github.com/repos/oracle-samples/db-sample-schemas
tags: [oracle, sample-schemas, github, versions]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://api.github.com/repos/oracle-samples/db-sample-schemas/releases
    title: Releases (gh api)
    accessed: 2026-09-02
  - resource: https://api.github.com/repos/oracle-samples/db-sample-schemas/git/trees/v23.3?recursive=1
    title: Tree at tag v23.3 (gh api)
    accessed: 2026-09-02
    version: v23.3 = commit e3325a83e56c516815844025418a96ecaf219751 (2024-03-28)
  - resource: https://api.github.com/repos/oracle-samples/db-sample-schemas/git/trees/v19.2?recursive=1
    title: Tree at tag v19.2 (gh api)
    accessed: 2026-09-02
    version: v19.2 = commit 5d236bf4178322716963f173f4b8f6a0c987a0dd (2019-08-23)
  - resource: https://api.github.com/repos/oracle-samples/db-sample-schemas/compare/v23.3...main
    title: Compare v23.3...main (gh api)
    accessed: 2026-09-02
    version: main = commit 6660bad68c07bd143430ace58565b3f727e17263 (2025-06-25)
---

# What was read
`gh api` (read-only) against the repository on 2026-09-02: repository metadata, `/releases`, `/tags`, `/branches`, recursive git trees for `main`, `v23.3`, `v19.2`, the `compare/v23.3...main` endpoint, and the commit objects behind the tags.

# Relevant excerpt (facts, not verbatim)
* Repository `oracle-samples/db-sample-schemas`; default branch `main`; only branch `main`; GitHub license detection: `MIT` (`LICENSE.txt`, 1,094 bytes). Last push 2025-06-25.
* Releases (newest first): **v23.3 "Oracle Database Sample Schemas 23c" (published 2023-04-18)**, v21.1 (2021-09-08), v19.2 (2019-11-06), v19c (2019-07-29), v18c (2018-12-04), v12.2.0.1 (2016-12-01), v12.1.0.2 (2015-11-19). Tags additionally include v23.1 and v23.2. There is no v23.4/26ai tag as of the access date.
* The `v23.3` tag now points at commit `e3325a8` dated **2024-03-28** ("Update supplementary demographics data (#24)") — i.e. the tag was moved after the release was published; the executor must pin the commit SHA, not the tag name.
* `main` is 3 commits ahead of v23.3 (f5204d1 "Fix typos (#29)" 2025-04-30; b60ab8d "Update Sample Schema documentation (#32)"; 6660bad "Update README.md (#33)", both 2025-06-25). Files changed: the root and per-schema README.md/README.txt files and `human_resources/hr_create.sql` (two spelling fixes inside `COMMENT ON COLUMN` strings: "deparment_id"→"department_id", "elgible"→"eligible"; 17,112 → 17,114 bytes). No data files changed.
* v23.3 directories: `customer_orders/`, `human_resources/`, `order_entry/`, `product_media/`, `sales_history/` (plus root README.md, README.txt, SECURITY.md, LICENSE.txt, .gitignore). **No `info_exchange/` (IX), `bus_intelligence/` (BI) or `shipping/` (QS) directories.**
* v19.2 directories: `bus_intelligence/`, `customer_orders/` (older scripts: co_ddl.sql, customers.sql, orders.sql, order_items.sql...), `human_resources/` (hr_main.sql, hr_cre.sql, hr_popul.sql...), `info_exchange/` (cix_v3.sql, dix_v3.sql, ix_main.sql, vix_v3.sql), `order_entry/`, `product_media/`, `sales_history/` (SQL*Loader `.dat`/`.ctl`: sale1v3.dat 42,445,678 B; sh_sales.dat 55,180,902 B; cust1v3.dat 13,159,220 B; sh_cust.dat 7,173,460 B; time_v3.dat 544,621 B; ...), `shipping/`, and the old drivers `mksample.sql`, `mkplug.sql`, `mkunplug.sql`, `mkverify.sql`, `drop_sch.sql`.
* v23.3 sizes (bytes) — HR: hr_install.sql 8,275; hr_create.sql 17,112; hr_populate.sql 41,301; hr_code.sql 3,849; hr_uninstall.sql 2,920 (directory 78,765). CO: co_install.sql 8,141; co_create.sql 19,570; co_populate.sql 1,274,129; co_uninstall.sql 2,917 (directory 1,309,608). SH: sh_install.sql 8,412; sh_create.sql 25,051; sh_populate.sql 41,072; sh_uninstall.sql 2,902; **sales.csv 74,426,366; customers.csv 12,615,719; costs.csv 2,658,415; supplementary_demographics.csv 701,892; times.csv 439,487; promotions.csv 56,158** (directory 90,977,907). OE: 216 files, 13,600,128 (70 .sql = 3,572,146; 132 XML purchase orders under `2002/<Mon>/` = 484,971; PurchaseOrders.dmp 9,345,886; POList.json 64,658; bi_oe_*.ctl/.dat ≈ 100 KB). PM: 65 files, 2,763,923 (54 media files = 2,720,743; scripts pm_cre.sql 4,527, pm_main.sql 5,940, pm_p_lob.ctl 7,252, pm_p_lob.dat 3,207, pm_p_lob.sql 2,773, long2lob.*). Whole tree 108,740,575 bytes.

# What it was used to decide
[HR](/datasets/oracle-hr.md), [CO](/datasets/oracle-co.md), [SH](/datasets/oracle-sh.md), [OE/PM/IX](/datasets/oracle-oe-pm-ix.md) source-artifact sections; [conversion path](/decisions/oracle-conversion-path.md).
