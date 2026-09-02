---
type: Open Question
title: Loaded InnoDB size and load time of tpch, tpcds, tpcc, ssb per scale factor / warehouse
description: Only raw sizes are documented (TPC-H SF1 956 MB; TPC-DS SF1 ~1.2 GB inferred; TPC-C ~69 MB/warehouse inferred; SSB SF1 ~600 MB inferred); InnoDB with indexes is estimated at 1.5–3× raw.
resource: /questions/benchmark-innodb-size-per-sf.md
tags: [question, sizing, tier]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/specification/TPC-DS_v2.10.0.pdf
    accessed: "2026-09-02"
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/tpc-c_v5.11.0.pdf
    accessed: "2026-09-02"
---

# Question
What are `SUM(data_length+index_length)` from `information_schema.TABLES`, `du -sh` of the tablespaces, and wall-clock generate+load times for: tpch SF 0.01/0.1/1/10; tpcds SF 0.01/0.1/1; tpcc W 1/10/100; ssb SF 0.01/1/10 — on the reference build machine, with the index sets in the dataset records?

# Cheapest experiment
`make gen-<ds> SF=…` for each size on the `mysql-build` service, then `scripts/verify.py sizes` writes the numbers into each dataset record's "Tier assignment" and PLAN.md §7; keep the 1.5–3× estimate marked inferred until then.

# Resolves
Default SF/W documented in README, disk-space warnings, CI smoke sizes for [TPC-H](/datasets/tpc-h.md), [TPC-DS](/datasets/tpc-ds.md), [TPC-C](/datasets/tpc-c.md), [SSB](/datasets/ssb.md).
