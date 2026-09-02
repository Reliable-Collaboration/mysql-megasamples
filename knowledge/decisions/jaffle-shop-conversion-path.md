---
type: Decision
title: Jaffle Shop conversion path - ship the classic Apache-2.0 seeds as generated INSERTs; jafgen run for larger data in extended
description: Core = three classic CSVs (312 rows) converted to SQL at build time with explicit DDL; extended = jafgen-generated multi-year data loaded from CSV; do not vendor the unlicensed new-repo seeds.
resource: /decisions/jaffle-shop-conversion-path.md
tags: [jaffle-shop, decision, csv]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://github.com/dbt-labs/jaffle-shop-classic/tree/main/seeds
    title: classic seeds inspection
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-generator/main/README.md
    title: jafgen README
    accessed: "2026-09-02"
---

# Question
Which Jaffle Shop data to ship and how to load it, given two generations of the project.

# Options considered
1. Classic seeds only (100 customers / 99 orders / 113 payments, 6.6 KB) - tiny, Apache-2.0, matches every dbt tutorial.
2. Also vendor the 1-year `seeds/jaffle-data` from dbt-labs/jaffle-shop (16.4 MB, 935 customers / 61,948 orders / 90,900 items) - richer, but the repository has no license.
3. Download the 6-year S3 snapshot (546 MB) - extended-size, same license gap.
4. Run `jafgen N` at build time - our own output, Apache-2.0 tool, but non-deterministic run to run.

# Evidence
[classic seeds](/sources/github-dbt-labs-jaffle-shop-classic-seeds.md), [new seeds](/sources/github-dbt-labs-jaffle-shop-seeds-jaffle-data.md), [S3 sizes](/sources/dbt-tutorial-public-s3-long-term-dataset.md), [jafgen](/tools/jafgen.md), [license question](/questions/jaffle-shop-new-repo-license.md).

# Outcome
Core: option 1, converted at build time into `CREATE TABLE` + INSERT statements (types: id INT PK, first_name/last_name VARCHAR(50), order_date DATE, status VARCHAR(20), payment_method VARCHAR(20), amount INT cents) - **Inferred** DDL, since dbt seeds carry no types. Extended: option 4 (`jafgen 3`, tables customers/orders/items/products/stores/supplies with UUID CHAR(36) keys, DATETIME timestamps, price INT cents, perishable BOOLEAN) loaded via CSV; revisit options 2/3 if dbt Labs adds a license. Both generations live in one database `jaffle_shop` with the classic tables named `raw_customers`, `raw_orders`, `raw_payments` and the jafgen tables prefixed `raw_` as generated (name clash on `raw_customers`/`raw_orders`: put the jafgen set in a second database `jaffle_shop_gen` or a table prefix `jaf_` - coordinator's call; recommendation: second database).

# Status
accepted: core is option 1 in `jaffle_shop`; extended jafgen output goes into `jaffle_shop_gen` (named in the [naming convention](/decisions/database-naming-convention.md)), non-reproducible by design
