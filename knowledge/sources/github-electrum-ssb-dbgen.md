---
type: Source
title: electrum/ssb-dbgen (original SSBM dbgen README and CHANGES)
description: The older SSB generator fork carrying the original UMass README; documents -T table letters and the supplier-cardinality fix.
resource: https://github.com/electrum/ssb-dbgen
tags: [ssb, dbgen, github]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/electrum/ssb-dbgen/master/README
    title: README (SSBM dbgen readme)
    accessed: "2026-09-02"
    version: master; pushed_at 2024-03-11; GitHub license null; 124 stars
---

# What was read
Root listing (README, TPCH_README, CHANGES, makefile.suite, makefile_win, C sources; no LICENSE) and README.

# Relevant excerpt (verbatim)
* "Version of 2/28/10: Cardinality of supplier fixed to follow benchmark spec: now 2000*SF (previously was 10000*SF, in error)".
* "SSBM is based on TPC-H dbgen source. ... all new code related to SSBM dbgen follow the "#ifdef SSBM" statements."
* Generation: `dbgen -s 1 -T c` (customer.tbl), `-T p` (part.tbl), `-T s` (supplier.tbl), `-T d` (date.tbl), `-T l` (lineorder.tbl), `-T a` (all); refresh sets `dbgen -s 1 -r 5 -U 4`. "At this moment there is no QGEN for SSBM."

# What it was used to decide
[ssb-dbgen tool record](/tools/ssb-dbgen.md).
