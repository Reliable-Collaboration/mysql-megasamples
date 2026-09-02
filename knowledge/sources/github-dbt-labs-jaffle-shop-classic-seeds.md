---
type: Source
title: jaffle-shop-classic seeds (raw_customers.csv, raw_orders.csv, raw_payments.csv) - inspection
description: Sizes, row counts, headers and sample rows of the three classic seed files.
resource: https://github.com/dbt-labs/jaffle-shop-classic/tree/main/seeds
tags: [jaffle-shop, csv, measurement]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/main/seeds/raw_customers.csv
    title: raw_customers.csv (md5 c07b5acaaab79acc27a00ad489ab4150)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/main/seeds/raw_orders.csv
    title: raw_orders.csv (md5 7deaec91356accb3cf8908934a8af81c)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/main/seeds/raw_payments.csv
    title: raw_payments.csv (md5 8e525f53c0858fba7660598144549edf)
    accessed: 2026-09-02
---

# What was read
The three files fetched and measured (`wc`, `head`, `tail`, non-ASCII grep), accessed 2026-09-02.

# Relevant excerpt (measurements)
* raw_customers.csv: 1,302 bytes, header `id,first_name,last_name`, 100 data rows (`1,Michael,P.` ... `100,Jean,M.`), ASCII.
* raw_orders.csv: 2,723 bytes, header `id,user_id,order_date,status`, 99 data rows (`1,1,2018-01-01,returned` ... `99,85,2018-04-09,placed`), ASCII; status values include returned, completed, placed (others not enumerated).
* raw_payments.csv: 2,560 bytes, header `id,order_id,payment_method,amount`, 113 data rows (`1,1,credit_card,1000` ... `113,99,credit_card,2400`), amounts are integer cents, ASCII.
* All LF, one header line each.

# What it was used to decide
Row-count baseline and schema in [Jaffle Shop](/datasets/jaffle-shop.md).
