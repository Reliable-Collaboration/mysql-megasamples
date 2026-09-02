---
type: Source
title: dbt-labs/jaffle-shop README (new project, main @ 7d0d8de)
description: The current Jaffle Shop dbt Cloud sandbox - 1-year jafgen seeds in seeds/jaffle-data, a 6-year public S3 dataset, and instructions to generate up to 10 years with jafgen; no LICENSE file in the repository.
resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop/main/README.md
tags: [jaffle-shop, dbt, readme, jafgen]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop/main/README.md
    title: README.md (23,543 bytes)
    accessed: 2026-09-02
    version: main @ 7d0d8de (2026-07-27); dbt_project.yml version 3.0.0
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop/main/dbt_project.yml
    title: dbt_project.yml
    accessed: 2026-09-02
  - resource: https://api.github.com/repos/dbt-labs/jaffle-shop
    title: repository metadata (license null; /license endpoint 404)
    accessed: 2026-09-02
---

# What was read
README head and grep for jafgen/license/years/seed lines; dbt_project.yml; API metadata; accessed 2026-09-02.

# Relevant excerpt
* "This is a sandbox project for exploring the basic functionality and latest features of dbt. It's based on a fictional restaurant called the Jaffle Shop". The main branch targets dbt Fusion and dbt Core >= 1.12.
* Loading options: "Using the sample data in the repo. Seeds are static data files in CSV format ... in this case the feature is hacked to do some data ingestion ... `dbt seed --full-refresh --vars '{"load_source_data": true}'`"; "Load the data via S3. If you'd prefer a larger dataset (6 years instead of 1) ... copy the data from a public S3 bucket" with download links `https://dbt-tutorial-public.s3.us-west-2.amazonaws.com/long_term_dataset/raw_{customers,orders,order_items,products,supplies,stores}.csv` and column types `raw_orders (id text, customer text, ordered_at datetime, store_id text, subtotal int, tax_paid int, order_total int)`, `raw_products (sku text, name text, type text, price int, description text)`, `raw_supplies (id text, name text, cost int, perishable boolean, sku text)`, `raw_stores (id text, name text, opened_at datetime, tax_rate float)`; "Generate a larger dataset on the command line ... as many years of data as you'd like (up to 10)" with `jafgen 6; rm -rf seeds/jaffle-data; mv jaffle-data seeds`.
* dbt_project.yml: `name: "jaffle_shop"`, `version: "3.0.0"`, seeds `jaffle-data: +enabled: "{{ var('load_source_data', false) }}"`, `+schema: raw`.
* No LICENSE file; GitHub reports no license.

# What it was used to decide
Extended-tier options and the license gap in [Jaffle Shop](/datasets/jaffle-shop.md) / [question](/questions/jaffle-shop-new-repo-license.md).
