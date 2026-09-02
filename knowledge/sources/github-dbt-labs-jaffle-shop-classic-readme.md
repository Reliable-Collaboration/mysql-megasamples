---
type: Source
title: dbt-labs/jaffle-shop-classic README
description: The archived classic Jaffle Shop dbt project - seeds for customers, orders, payments loaded with `dbt seed`; superseded by dbt-labs/jaffle-shop and jaffle_shop_duckdb.
resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/main/README.md
tags: [jaffle-shop, dbt, readme]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/main/README.md
    title: README.md
    accessed: "2026-09-02"
    version: main @ fd7bfac (2024-04-18); repository archived
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/main/dbt_project.yml
    title: dbt_project.yml
    accessed: "2026-09-02"
---

# What was read
README.md (4,568 bytes) and dbt_project.yml, accessed 2026-09-02.

# Relevant excerpt
The repository "is no longer actively maintained" and points to `jaffle-shop` (dbt Cloud) and `jaffle_shop_duckdb` (local). jaffle_shop is "a fictional ecommerce store" whose "raw data from an app database" is transformed "into a customers and orders model ready for analytics". Seed files hold fake raw data for customers, orders and payments; `dbt seed` "materializes the CSVs as tables in your target schema". dbt_project.yml: `name: 'jaffle_shop'`, `seed-paths: ["seeds"]`, `require-dbt-version: [">=1.0.0", "<2.0.0"]`. A jaffle is an Australian toasted sandwich.

# What it was used to decide
[Jaffle Shop dataset](/datasets/jaffle-shop.md) - the classic seeds are the shipped core.
