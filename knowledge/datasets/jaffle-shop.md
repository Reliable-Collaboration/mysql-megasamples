---
type: Dataset
title: Jaffle Shop
description: dbt Labs' fictional jaffle (toasted sandwich) shop - classic seeds (customers 100, orders 99, payments 113) under Apache-2.0, plus the newer jafgen-generated multi-table data (1 year = 62K orders; 6 years public on S3).
resource: https://github.com/dbt-labs/jaffle-shop-classic
tags: [tier-core, tier-generated, csv, jaffle-shop, dbt, apache-2-0, generator]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:48:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/main/README.md
    title: jaffle-shop-classic README
    accessed: "2026-09-02"
    version: main @ fd7bfac (archived)
  - resource: https://github.com/dbt-labs/jaffle-shop-classic/tree/main/seeds
    title: classic seeds (measured)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/main/LICENSE
    title: Apache-2.0 LICENSE
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop/main/README.md
    title: dbt-labs/jaffle-shop README
    accessed: "2026-09-02"
    version: main @ 7d0d8de (2026-07-27)
  - resource: https://github.com/dbt-labs/jaffle-shop/tree/main/seeds/jaffle-data
    title: jaffle-data seeds (measured)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-generator/main/README.md
    title: jafgen README
    accessed: "2026-09-02"
  - resource: https://dbt-tutorial-public.s3.us-west-2.amazonaws.com/long_term_dataset/raw_orders.csv
    title: S3 long_term_dataset (HEAD)
    accessed: "2026-09-02"
---

# Identity
Two generations of the same fictional business ([classic README](/sources/github-dbt-labs-jaffle-shop-classic-readme.md), [new README](/sources/github-dbt-labs-jaffle-shop-readme.md)):
* **Classic** (dbt-labs/jaffle-shop-classic, archived 2024): three raw tables - customers, orders, payments - the data behind every "dbt tutorial".
* **New** (dbt-labs/jaffle-shop v3.0.0): customers, orders, items, products, stores, supplies (+ tweets) produced by the `jafgen` simulator ([tool](/tools/jafgen.md)).

# Source artifact
* Classic seeds: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/main/seeds/{raw_customers,raw_orders,raw_payments}.csv at commit `fd7bfacae4f497ff044a6a0275268676bf1b64c3`; 1,302 / 2,723 / 2,560 bytes; md5 `c07b5acaaab79acc27a00ad489ab4150`, `7deaec91356accb3cf8908934a8af81c`, `8e525f53c0858fba7660598144549edf` ([inspection](/sources/github-dbt-labs-jaffle-shop-classic-seeds.md)). No auth.
* New 1-year seeds: dbt-labs/jaffle-shop `seeds/jaffle-data/` at `7d0d8de` - 16.4 MB, six files ([inspection](/sources/github-dbt-labs-jaffle-shop-seeds-jaffle-data.md)); 6-year snapshot on S3 (`raw_orders.csv` 297,899,240 B, `raw_order_items.csv` 247,985,646 B, 2024-08-07) ([S3](/sources/dbt-tutorial-public-s3-long-term-dataset.md)). Both lack a license statement.
* Generator: `pip install jafgen==0.4.14` (Apache-2.0).

# Native format and friendlier forms
CSV with header rows (dbt seeds); no database product involved. Types must be assigned by us (dbt infers them).

# Shape
* Classic: raw_customers (id, first_name, last_name) 100 rows; raw_orders (id, user_id, order_date 2018-01-01.., status in returned/completed/placed/...) 99 rows; raw_payments (id, order_id, payment_method e.g. credit_card, amount integer cents) 113 rows. ASCII, LF.
* New (1 year): raw_customers 935; raw_orders 61,948 (UUID id/customer/store_id, `ordered_at` ISO `2024-09-01T15:01:00`, subtotal/tax_paid/order_total cents); raw_items 90,900; raw_products 10 (sku JAF-00x/BEV-00x, price cents, quoted descriptions); raw_stores 6 (Philadelphia ... Los Angeles, tax_rate 0.04-0.08); raw_supplies 65 (perishable True/False). ASCII.
* jafgen scale: about 62K orders per simulated year; README allows up to 10 years.

# Conversion path
Classic seeds -> build-time INSERT script with explicit DDL (core). Larger data -> `jafgen N` at build time, CSV load (extended) ([decision](/decisions/jaffle-shop-conversion-path.md)). CSV notes: [tool note](/tools/smallcsv-load-data-infile.md).

# Type-mapping hazards
* No types in the source: choose `INT` ids (classic), `CHAR(36)` UUIDs (new), `DATE` vs `DATETIME` (`ordered_at` has seconds), `INT` cents (do not convert to DECIMAL - the dbt models divide by 100), `BOOLEAN` for `perishable` (`True`/`False` strings need mapping), `DECIMAL(5,4)` for tax_rate.
* Header row must be skipped; quoted fields with embedded commas in `raw_products.description`.
* Table name collision between generations (`raw_customers`, `raw_orders`).

# Programmable objects
None upstream (dbt models are SQL SELECTs materialised by dbt, not database objects). Optionally port the classic `customers`/`orders` marts as MySQL views - **Inferred** feasibility; not required.

# Indexing
Primary keys on ids; FK `raw_orders.user_id -> raw_customers.id`, `raw_payments.order_id -> raw_orders.id` (classic); `raw_orders.customer -> raw_customers.id`, `raw_items.order_id -> raw_orders.id`, `raw_items.sku -> raw_products.sku` (new). Add explicitly (source has none).

# Tests and expected values
Classic: 100 / 99 / 113 rows; `SELECT SUM(amount) FROM raw_payments` recorded at first load; `SELECT status, COUNT(*) FROM raw_orders GROUP BY status` recorded; file md5s pinned. New/generated: counts recorded per build (non-deterministic generator) or fixed if a snapshot is vendored.

# Tier assignment
core: classic seeds (6.6 KB). extended: jafgen 3-6 years (16 MB per year of CSV) loaded into `jaffle_shop_gen` or the 546 MB S3 snapshot once licensed. Evidence: [seed sizes](/sources/github-dbt-labs-jaffle-shop-classic-seeds.md), [S3 sizes](/sources/dbt-tutorial-public-s3-long-term-dataset.md).

# License and attribution
Classic seeds and jafgen: [Apache-2.0](/licenses/apache-2-0.md) (copyright holder not filled in upstream; attribute to dbt Labs, Inc.). New-repo seeds and S3 data: no license - [open question](/questions/jaffle-shop-new-repo-license.md); not vendored until resolved.

# Database name
`jaffle_shop` (classic) as listed in the [naming convention](/decisions/database-naming-convention.md); generated multi-year data in `jaffle_shop_gen` (this group's recommendation, not yet in the convention list) to avoid the `raw_customers`/`raw_orders` clash.

# Open questions
* [License of new-repo seeds / S3 data](/questions/jaffle-shop-new-repo-license.md).
* Deterministic jafgen output (seed patch) - see [tool record](/tools/jafgen.md).
