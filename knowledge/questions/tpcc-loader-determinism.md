---
type: Open Question
title: Can sysbench-tpcc produce an identical tpcc population on two runs (seed coverage, threads, Lua math.random, MySQL 9.7 client auth)?
description: sysbench has --rand-seed, but tpcc_common.lua also uses Lua's math.random for the customer permutation and multi-threaded loads interleave RNG streams; HammerDB/tpcc-mysql are unseeded.
resource: /questions/tpcc-loader-determinism.md
tags:
- question
- tpc-c
- sysbench
- determinism
status: draft
trust: open
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://github.com/Percona-Lab/sysbench-tpcc
  accessed: "2026-09-02"
- resource: https://github.com/akopytov/sysbench
  accessed: "2026-09-02"
---

# Question
1. Does `sysbench … --rand-seed=42 --threads=1 prepare` yield identical digests (excluding NOW() columns) on two runs? Does `--threads=4`?
2. Is Lua `math.random` seeded by sysbench (it is used for the O_C_ID permutation)? If not, patch the script (Apache-2.0 allows) to use `sysbench.rand.uniform`.
3. Does the Debian `sysbench` (libmariadb3) connect to MySQL 9.7 with `caching_sha2_password`?
4. If any answer is no: switch to a seeded Python populator writing `.tbl` files per spec Clause 4.3.3 (option 4 in the [decision](/decisions/tpcc-implementation-choice.md)).

# Cheapest experiment
Loader image: `apt-get install sysbench`; run W=1 twice with the same seed and threads=1, compute the per-table digests with `scripts/canon.py` excluding c_since/h_date/o_entry_d/ol_delivery_d; repeat with threads=4; grep `math.random` seeding in sysbench's Lua bootstrap (`src/lua/internal/sysbench.rand.lua`).

# Resolves
[TPC-C record](/datasets/tpc-c.md) tests section; whether `baseline.json` for tpcc can be pre-committed.
