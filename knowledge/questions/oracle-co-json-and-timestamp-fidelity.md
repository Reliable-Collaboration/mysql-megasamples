---
type: Open Question
title: CO fidelity — 9-digit timestamps, JSON key normalisation, and GROUPING SETS in MySQL 9.7
description: Three details where MySQL may render CO data or views differently from Oracle; each is a one-command experiment.
resource: /questions/oracle-co-json-and-timestamp-fidelity.md
tags: [question, oracle, co, json, datetime]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: /sources/github-oracle-samples-db-sample-schemas-co-scripts.md
    title: CO scripts
    accessed: 2026-09-02
  - resource: /sources/mysql-refman-9-7-fractional-seconds.md
    title: MySQL fractional seconds rounding
    accessed: 2026-09-02
  - resource: /sources/mysql-refman-9-7-json.md
    title: MySQL JSON normalisation
    accessed: 2026-09-02
---

# Question
1. All 1,950 `orders.order_tms` literals have 9 fractional digits (`13.20.22.245676861`). Oracle `TIMESTAMP` defaults to precision 6 — does Oracle round or truncate the 7th digit? MySQL rounds unless `TIME_TRUNCATE_FRACTIONAL`. Which rule should the converter apply so both engines agree (and the baseline is stable)?
2. Do any `product_details` JSON documents contain duplicate keys or rely on key order (MySQL keeps the last duplicate and sorts keys)? Is any document larger than a conservative `max_allowed_packet`? (Longest seen ≈ 1,350 chars, so size is not an issue.)
3. Does MySQL 9.7 accept `GROUP BY GROUPING SETS (...)` and `GROUPING_ID()` as used by the `store_orders` view, or must it be rewritten with `WITH ROLLUP` + `GROUPING()` / `UNION ALL`?
4. `LISTAGG ... ON OVERFLOW TRUNCATE '...' WITH COUNT` → `GROUP_CONCAT`: is any order's concatenated product list longer than 1,024 bytes (default `group_concat_max_len`)?

# Cheapest experiment
* (1) `python3 -c "import re;print(sorted({len(m) for m in re.findall(r'\.(\d+)\',\'DD-MON', open('co_populate.sql').read())}))"` confirms 9 digits; then on the Oracle verification profile `SELECT TO_CHAR(order_tms,'FF9') FROM co.orders WHERE order_id=1` (expect `245676861` → stored as `245676` or `245677`). Without Oracle: choose **truncation** (documented) and set `sql_mode` to include `TIME_TRUNCATE_FRACTIONAL` in the converter's load session.
* (2) `python3` script: extract each JSON literal, `json.loads(..., object_pairs_hook=<detect duplicates>)`; compare `json.dumps(sort_keys=True)` with MySQL `JSON_EXTRACT(product_details,'$')` output.
* (3) `mysql -e "SELECT a,b,SUM(x) FROM (SELECT 1 a,2 b,3 x) t GROUP BY GROUPING SETS ((a),(b),())"` on `mysql:9.7`.
* (4) `SELECT MAX(LENGTH(GROUP_CONCAT(product_name SEPARATOR ', '))) FROM order_items JOIN products USING (product_id) GROUP BY order_id`.

# Resolves
[CO dataset record](/datasets/oracle-co.md) hazards and view ports.
