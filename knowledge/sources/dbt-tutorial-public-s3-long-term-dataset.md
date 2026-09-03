---
type: Source
title: dbt-tutorial-public S3 "long_term_dataset" (6-year Jaffle Shop CSVs) - HEAD sizes
description: Public, unauthenticated CSV downloads referenced by the jaffle-shop README; raw_orders 297.9 MB and raw_order_items 248.0 MB.
resource: https://dbt-tutorial-public.s3.us-west-2.amazonaws.com/long_term_dataset/raw_orders.csv
tags:
- jaffle-shop
- s3
- sizes
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dbt-tutorial-public.s3.us-west-2.amazonaws.com/long_term_dataset/raw_orders.csv
  title: HEAD on raw_customers, raw_orders, raw_order_items, raw_products, raw_supplies, raw_stores
  accessed: "2026-09-02"
---

# What was read
`curl -sI` on the six objects, accessed 2026-09-02 (HTTP 200, no auth).

# Relevant excerpt
Content-Length (bytes), Last-Modified 2024-08-07: raw_customers.csv 159,115; raw_orders.csv 297,899,240; raw_order_items.csv 247,985,646; raw_products.csv 912; raw_supplies.csv 2,589; raw_stores.csv 470. Note the item file is named `raw_order_items.csv` here versus `raw_items.csv` in the repo seeds.

# What it was used to decide
Extended-tier option (6 years, ~546 MB CSV) in [Jaffle Shop](/datasets/jaffle-shop.md); no license statement accompanies the bucket ([question](/questions/jaffle-shop-new-repo-license.md)).
