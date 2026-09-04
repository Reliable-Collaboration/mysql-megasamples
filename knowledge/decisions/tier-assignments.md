---
type: Decision
title: Final tier assignment per dataset
description: Which datasets are baked into the core image, which are extended (downloaded, generated, or user-fetched), with the size evidence behind each call.
resource: /decisions/tier-assignments.md
tags:
- decision
- tiers
status: stable
trust: inferred
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T21:02:00Z"
sources:
- resource: /decisions/tier-model.md
  accessed: "2026-09-02"
---

# Question
Apply the [tier model](/decisions/tier-model.md) to every dataset record's size evidence.

# Options considered
1. **Apply the thresholds of the tier model dataset by dataset, allowing a small medium band** (chosen).
2. Strict 50 MB cut-off — rejected: it would exclude Employees, Oracle SH and AdventureWorks, the three datasets most users expect in a MySQL sample image.
3. Everything in one image — rejected: extended datasets total tens of GB and several may not be redistributed at all.

# Evidence
Each row of the table links to the dataset record that holds the size evidence; the licensing constraints come from [the Citi Bike/Divvy finding](/questions/citibike-divvy-redistribution.md) and [the Wikidata decision](/decisions/wikidata-vs-wikipedia-simple.md).

# Outcome
| Database | Tier | Loaded size (MB, inferred unless a record says measured) | Evidence |
|---|---|---|---|
| sakila | core | <10 | [record](/datasets/sakila.md) |
| chinook | core | 2–3 | [record](/datasets/chinook.md) |
| northwind | core | <10 | [record](/datasets/northwind.md) |
| pubs | core | <1 | [record](/datasets/pubs.md) |
| employees | core (medium) | 150–250 | [record](/datasets/employees.md) |
| oracle_hr | core | <1 | [record](/datasets/oracle-hr.md) |
| oracle_co | core | 2–3 | [record](/datasets/oracle-co.md) |
| oracle_sh | core (medium) | 150–250 | [record](/datasets/oracle-sh.md) |
| oracle_oe | core | <10 | [record](/datasets/oracle-oe-pm-ix.md) |
| adventureworks_lt | core | <10 | [record](/datasets/adventureworks-lt.md) |
| adventureworks | core (medium) | 180–250 | needs no SQL Server; [record](/datasets/adventureworks-oltp.md) |
| adventureworks_dw | extended (download) | ~150 | [record](/datasets/adventureworks-dw.md) |
| wideworldimporters | extended (SQL Server once, cached export) | 600–900 | [record](/datasets/wideworldimporters.md) |
| wideworldimporters_dw | extended (same) | ~150 | [record](/datasets/wideworldimporters-dw.md) |
| contoso | core (csv-100k) / extended (1m, 10m) | 60–120 core | [record](/datasets/contoso.md) |
| dvdstore | core (DS2 tables) / extended (reviews) | 15–25 core, 300–400 with reviews | [record](/datasets/dell-dvd-store.md) |
| jaffle_shop | core (classic) / extended (jafgen) | <1 core | [record](/datasets/jaffle-shop.md) |
| smallsets | core | <1 | [titanic](/datasets/titanic.md), [iris](/datasets/iris.md), [penguins](/datasets/palmer-penguins.md) |
| lahman | core (release-asset mirror of the CSVs) | ~50 (measure) | [record](/datasets/lahman.md) |
| tpch, tpcds, tpcc, ssb | extended (generated) | SF/W dependent | benchmark records |
| nyc_taxi | core (green 2025-01 + zones) / extended (yellow) | 8–12 core, 500–700 yellow | [record](/datasets/nyc-tlc.md) |
| bts_ontime | extended (download) | 250–400 per month | [record](/datasets/bts-ontime.md) |
| chicago_crimes | core (year 2024, 259,267 rows) / extended (full) | 60–80 core | [record](/datasets/chicago-crimes.md) |
| citibike, divvy | extended, **user-fetched only** (license forbids stand-alone redistribution) | one year each | [finding](/questions/citibike-divvy-redistribution.md) |
| enron | core (deterministic mailbox subset <40 MB) / extended (full) | 2,000–3,000 full | [record](/datasets/enron.md) |
| stackexchange_beer | core | <40 | [record](/datasets/stackexchange.md) |
| stackexchange_dba | extended (download) | 2,000–3,000 | same |
| wikipedia_simple | core (5,000-article deterministic sample) / extended (full) | 2,500–3,000 full | [record](/datasets/wikipedia-simple.md) |
| wikidata | not shipped | — | [decision](/decisions/wikidata-vs-wikipedia-simple.md) |

Core total, inferred: 1.0–1.3 GB of InnoDB pages; compressed image target ≤ 2 GB (base image ≈ 0.6 GB). Task E-01 replaces every inferred figure with a measurement; if the measured core datadir exceeds 3 GB, `adventureworks` and then `contoso` move to extended (in that order).

# Measured outcome (2026-09-03, task E-01)
Every core dataset is now built and measured, and **no tier assignment changed**. The image holds 22
databases, 249 base tables and 9,056,697 rows: 942.8 MB logical, a 1,785 MB data directory, a 3.46 GB
image, ready to serve a query 2.2 seconds after start.

Where measurement differed from the estimate it was in both directions, and none of it crossed a tier
boundary:

| dataset | estimated | measured | note |
|---|---:|---:|---|
| wikipedia_simple (sample) | < 50 MB | 131.3 MB | wikitext and the two link tables; still in the employees band |
| chicago_crimes (2024) | 60–90 MB | 65.7 MB | |
| contoso (100k) | 60–120 MB | 103.3 MB | |
| oracle_sh | 150–250 MB | 160.6 MB | |
| adventureworks | 220 MB | 154.0 MB | |
| employees | 150–250 MB | 146.8 MB | |
| lahman | ~50 MB | 75.6 MB | |
| enron (subset) | < 40 MB | 38.0 MB | the 40 MB rule is on source bytes, and it held |
| dvdstore (no reviews) | 15–25 MB | 16.3 MB | |
| nyc_taxi (green) | ~10 MB | 10.1 MB | |
| stackexchange_beer | ~20 MB | 21.5 MB logical, 74 MB on disk | FULLTEXT over post bodies dominates the on-disk cost |

The last row is the one worth carrying forward: **logical size is not what the disk pays**. Across the
image the ratio is 1.9x, and for a FULLTEXT-heavy dataset it is 3.4x.

# Status
accepted (sizes inferred; revisit after E-01)
