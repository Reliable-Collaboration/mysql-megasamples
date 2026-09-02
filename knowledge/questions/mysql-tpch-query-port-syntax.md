---
type: Open Question
title: Exactly which of the 22 qgen-generated TPC-H queries need MySQL edits, and does utf8mb4_bin reproduce the reference ordering?
description: Community ports show Q1 needs the interval precision "(3)" removed; the rest is inferred to run unchanged with the POSTGRESQL dialect's "limit N".
resource: /questions/mysql-tpch-query-port-syntax.md
tags:
- question
- tpc-h
- mysql
- sql
status: draft
trust: open
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://github.com/catarinaribeir0/queries-tpch-dbgen-mysql
  accessed: "2026-09-02"
- resource: https://github.com/gregrahn/tpch-kit
  accessed: "2026-09-02"
---

# Question
Known: `date '1998-12-01' - interval '90' day (3)` → drop `(3)`; `limit N` from `DATABASE=POSTGRESQL`; `extract(year from …)`, `substring(x from 1 for 2)`, `create view … drop view` (Q15) are MySQL-valid. Unknown until run: implicit DECIMAL arithmetic precision in Q1/Q6 aggregates versus the reference decimals; whether `utf8mb4_0900_ai_ci` (MySQL default) changes ORDER BY on p_brand/p_type/n_name/s_name results compared with the ASCII-ordered `answers/`; CHAR padding effects in `where p_type like '%BRASS'`.

# Cheapest experiment
Load SF 0.01 and SF 1, run the 22 queries once under `utf8mb4_bin` and once under `utf8mb4_0900_ai_ci`, compare with `tpch_answers()` using `check_answers/cmpq.pl` precision rules; list every edit in `datasets/tpch/convert/patch_queries.py` and copy the list into the [TPC-H record](/datasets/tpc-h.md) hazard 4.

# Resolves
The collation of the `tpch`/`tpcds`/`ssb` databases and the query patch script.
