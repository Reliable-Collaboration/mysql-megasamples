---
type: Source
title: dbt-labs/jaffle-shop seeds/jaffle-data (1-year jafgen output) - inspection
description: Six CSVs (customers 935, orders 61,948, items 90,900, products 10, stores 6, supplies 65 rows; 16.4 MB) with UUID keys and ISO timestamps.
resource: https://github.com/dbt-labs/jaffle-shop/tree/main/seeds/jaffle-data
tags:
- jaffle-shop
- csv
- measurement
- jafgen
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://api.github.com/repos/dbt-labs/jaffle-shop/contents/seeds/jaffle-data
  title: directory listing with sizes
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop/main/seeds/jaffle-data/raw_orders.csv
  title: raw_*.csv (streamed through wc -l / head)
  accessed: "2026-09-02"
---

# What was read
Directory listing and each CSV streamed to `wc -l`/`head`, accessed 2026-09-02.

# Relevant excerpt (measurements)
| file | bytes | data rows | header / sample |
|---|---|---|---|
| raw_customers.csv | 48,928 | 935 | `id,name` / `50a2d1c4-...,Stephanie Love` |
| raw_orders.csv | 8,837,334 | 61,948 | `id,customer,ordered_at,store_id,subtotal,tax_paid,order_total` / `...,2024-09-01T15:01:00,...,700,42,742` |
| raw_items.csv | 7,544,717 | 90,900 | `id,order_id,sku` / `...,BEV-004` |
| raw_products.csv | 923 | 10 | `sku,name,type,price,description` / `JAF-001,nutellaphone who dis?,jaffle,1100,nutella and banana jaffle` |
| raw_stores.csv | 477 | 6 | `id,name,opened_at,tax_rate` / `...,Philadelphia,2016-09-01T00:00:00,0.06` |
| raw_supplies.csv | 2,655 | 65 | `id,name,cost,perishable,sku` / `SUP-001,compostable cutlery - knife,7,False,JAF-001` |

All ASCII (0 non-ASCII lines in customers/products/stores/supplies); UUID v4 keys; prices in cents; `perishable` is `True`/`False`; quoted description fields with commas. Stores: Philadelphia, Brooklyn, Chicago, San Francisco, New Orleans, Los Angeles.

# What it was used to decide
Optional larger core payload and schema for the new-style tables in [Jaffle Shop](/datasets/jaffle-shop.md).
