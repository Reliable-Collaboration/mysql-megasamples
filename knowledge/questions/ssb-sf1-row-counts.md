---
type: Open Question
title: Exact ssb-dbgen row counts at SF=1 (lineorder, date), fractional SF behaviour, and lo_commitdate range
description: The paper gives SF×6,000,000, SF×30,000, SF×2,000, 200,000×(1+log2 SF) and "7 years of days"; exact generated counts (6,001,215? 2,556?) are inferred.
resource: /questions/ssb-sf1-row-counts.md
tags: [question, ssb, generator]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://github.com/eyalroz/ssb-dbgen
    accessed: "2026-09-02"
  - resource: https://www.cs.umb.edu/~poneil/StarSchemaB.PDF
    accessed: "2026-09-02"
---

# Question
1. `wc -l` of each `.tbl` at SF=1 (expected customer 30,000, supplier 2,000, part 200,000; lineorder ≈ 6,000,000 — TPC-H's 6,001,215 if the order/line generation is inherited; date 2,556 or 2,557).
2. Does `-s 0.01` work and what does part's `200,000×(1+⌊log2 SF⌋)` give for SF<1 (negative log → clamp?).
3. Are all `lo_commitdate` values present in `date` (needed before declaring the FK)?
4. Magnitudes of lo_extendedprice/lo_revenue/lo_supplycost (integer cents or units?).

# Cheapest experiment
Build ssb-dbgen in the builder stage, run `dbgen -s 1 -T a` and `dbgen -s 0.01 -T a`, `wc -l *.tbl`, `awk -F'|' '{print $16}' lineorder.tbl | sort -u | comm -23 - <(cut -d'|' -f1 date.tbl | sort -u) | head`, and `cut -d'|' -f10,13,14 lineorder.tbl | sort -n | tail -1`. Record in the [SSB record](/datasets/ssb.md).

# Resolves
SSB expected counts, smoke SF, FK on lo_commitdate.
