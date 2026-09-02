---
type: Source
title: HammerDB docs 3.2 — What is the TPC and the TPROC-C workload derived from TPC-C?
description: HammerDB's own statement of the "derived from" naming and the non-comparability disclaimer.
resource: https://www.hammerdb.com/docs/ch03s02.html
tags: [hammerdb, tpc-c, fair-use]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.hammerdb.com/docs/ch03s02.html
    title: What is the TPC and the TPROC-C workload derived from TPC-C?
    accessed: "2026-09-02"
---

# What was read
The section (chapter 3 index at https://www.hammerdb.com/docs/ch03.html lists sections 1–8 including "TPROC-C key similarities and differences from TPC-C" and "Publishing database performance results").

# Relevant excerpt (verbatim)
* "TPROC-C is the OLTP workload implemented in HammerDB derived from the TPC-C specification."
* "The name for the HammerDB workload TPROC-C means 'Transaction Processing Benchmark derived from the TPC "C" specification'."
* "The TPC Policies allow for derivations of TPC Benchmark Standards that comply with the TPC Fair Use rules."
* "The HammerDB TPROC-C workload is an open source workload derived from the TPC-C Benchmark Standard and as such is not comparable to published TPC-C results, as the results comply with a subset rather than the full TPC-C Benchmark Standard."

# What it was used to decide
Naming/disclaimer wording in [TPC-C dataset](/datasets/tpc-c.md) and the fair-use interpretation in [TPC EULA](/licenses/tpc-eula.md).
