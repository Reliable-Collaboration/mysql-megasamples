---
type: Source
title: TPC Fair Use Quick Reference v1.0.0 (2019-06-05)
description: The TPC's summary of how non-TPC (derived, unaudited) benchmark uses must be named and disclaimed.
resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/Fair_Use_Quick_Reference_v1.0.0.pdf
tags: [tpc, fair-use, trademark]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/Fair_Use_Quick_Reference_v1.0.0.pdf
    title: Fair Use of TPC Benchmarks
    accessed: 2026-09-02
    version: dated 2019-06-05, 108 KB PDF (text extracted locally with a zlib stream parser; one phrase set in a different font was lost, noted below)
---

# What was read
The 2-page quick reference, extracted to text locally (no PDF tools installed; a pure-Python FlateDecode extractor was used).

# Relevant excerpt (verbatim)
* "The TPC label may be applied to only fully legitimate Results, used in a fair manner." Restated: "Any use of the TPC name in conjunction with published results must ONLY be used with official published results, available on the TPC web site."
* Non-TPC Benchmarks: "Any use of a TPC benchmark outside of official published results is considered a non-TPC benchmark and is subject to certain conditions": 1) Copyright (Policies 8.1.1); 2) License (8.1.2) "In all cases, the TPC Copyright Notice and License Agreement must be maintained."; 3) Benchmark Name and Metrics (8.1.3): "Any use of the TPC Benchmark Name in a derived work must be prefixed with the phrase [phrase lost in extraction — **Inferred:** "derived from", which is the wording HammerDB and Bexhoma use, see below]"; "The use of any Primary Metric or Optional Metric of a TPC Benchmark is not allowed" (e.g. use tps, not tpsE); 4) Disclaimer (8.1.4): "A disclaimer ... needs to be present wherever derived results are presented"; the template as recovered: "<...> is derived from the <TPC Benchmark name> and as such is not comparable to published <TPC Benchmark name> results, as the <name of ...> results do not comply with the <TPC Benchmark name> Specification" (the HammerDB docs instantiate it as "derived from the TPC-C Benchmark Standard and as such is not comparable to published TPC-C results, as the results comply with a subset rather than the full TPC-C Benchmark Standard", [HammerDB ch03s02](/sources/hammerdb-docs-ch03s02-tproc-c.md); Bexhoma as "The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS Specification", [Bexhoma](/sources/bexhoma-docs-tpc-ds.md)); 6) Deviations must be noted (schema, query text, ...); 7) "Any comparison between official TPC Results with non-TPC workloads is prohibited."
* Member fines "up to $10,000 per infraction" apply to TPC members; the naming/disclaimer rules are the conditions under which non-members may use the material.

# What it was used to decide
Naming and README disclaimer wording in [TPC-H](/datasets/tpc-h.md), [TPC-DS](/datasets/tpc-ds.md), [TPC-C](/datasets/tpc-c.md), [SSB](/datasets/ssb.md); [TPC EULA](/licenses/tpc-eula.md).
