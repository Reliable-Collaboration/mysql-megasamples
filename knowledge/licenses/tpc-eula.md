---
type: License
title: TPC End User License Agreement v2.2 (dbgen, qgen, dsdgen, dsqgen and derivatives)
description: The license on every TPC benchmark tool and on anything merged with it; permits use, modification and no-fee redistribution with the full agreement and a legend, restricts performance-result publication and TPC name use, and is silent about generated data.
resource: https://www.tpc.org/TPC_Documents_Current_Versions/txt/EULA_v2.2.0.txt
tags: [license, tpc, eula, proprietary]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/txt/EULA_v2.2.0.txt
    title: END USER LICENSE AGREEMENT VERSION 2.2
    accessed: "2026-09-02"
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/Fair_Use_Quick_Reference_v1.0.0.pdf
    title: Fair Use of TPC Benchmarks (2019-06-05)
    accessed: "2026-09-02"
---

# Where the text lives
https://www.tpc.org/TPC_Documents_Current_Versions/txt/EULA_v2.2.0.txt (18,323 bytes, plain text) — full excerpt in [the EULA source record](/sources/tpc-eula-v2-2.md). Identical copies: `EULA.txt` in gregrahn/tpch-kit and gregrahn/tpcds-kit; `extension/tpch/dbgen/LICENSE` in duckdb/duckdb. This is **not** an OSI license; SPDX has no identifier for it (use `LicenseRef-TPC-EULA-2.2` in SBOMs — **Inferred** naming convention).

# Obligations
| Question | Answer from the text |
|---|---|
| May we run the tools in our build? | Yes: clause 3 grants a "restricted, non-exclusive, revocable license to install and use"; clause 4.b "You may modify the Software." |
| May we redistribute dbgen/dsdgen source (vendor it in the repo)? | Yes, under clause 9, if **all** of: (a) unmodified copies ship "a complete copy of this Agreement"; modified copies ship under a license "that at a minimum provides all of the protections and conditions of use contained within this Agreement"; (b) each copy carries, in all caps, ≥12-point, no less prominent than other printing: **"THE TPC SOFTWARE IS AVAILABLE WITHOUT CHARGE FROM TPC."**; (c) all copyright/patent/trademark/attribution notices retained; (d) no fee for distribution. Clause 8: anything merged with the Software stays under this Agreement. |
| May we redistribute the generated .tbl/.dat data? | **Not addressed.** The Agreement defines Software as "source code, scripts, executable programs, drivers, libraries and data files associated with such programs" — the distribution files (dists.dss, tpcds.idx) are clearly covered; the *output* of running the generator is neither granted nor restricted. The TPC-H spec only requires that a compliant population "must exactly match the output of DBGEN". Treat as an open question ([record](/questions/tpc-eula-generated-data-redistribution.md)); the plan ships no generated data. |
| Performance numbers | Clause 4.c: may only be disclosed as an official TPC Result, as academic/research work, or "clearly identified as not being comparable to TPC Benchmark Results". |
| Names/trademarks | Clause 7 + TPC Fair Use: a derived work must be described as *derived from* TPC-x and carry the disclaimer "<work> is derived from the TPC-x Benchmark and as such is not comparable to published TPC-x results, as the <work> results do not comply with the TPC-x Specification"; primary metrics (QphH, tpmC, QphDS) may not be used. "TPC Benchmark, TPC-H, QppH, QthH, and QphH are trademarks" (TPC-H spec); "TPC Benchmark, TPC-C, and tpmC are trademarks" (TPC-C spec). |
| Warranty/liability | "AS IS", liability capped at US $100; US export (EAR) clause 13. |
| Removing the license | Clause 5: "You may not remove or modify this license without permission." |

# Attribution
1. A complete copy of the EULA next to any TPC-derived code or query text we ship (`datasets/tpch/LICENSE`, `datasets/tpcds/LICENSE`, `datasets/ssb/LICENSE`).
2. The legend, in caps at the top of the license/label: `THE TPC SOFTWARE IS AVAILABLE WITHOUT CHARGE FROM TPC.`
3. The original TPC copyright headers on any TPC file or excerpt (e.g. "Copyright owned by the Transaction Processing Performance Council"; the TPC-DS "Legal Notice" block).
4. The Fair Use disclaimer in README wherever the databases are described, using "derived from TPC-H/TPC-DS/TPC-C" and never the metric names; e.g. "The `tpch`, `tpcds`, `tpcc` and `ssb` databases are derived from the TPC-H, TPC-DS and TPC-C Benchmark Standards and as such are not comparable to published TPC results, as they do not comply with the TPC specifications."
5. The TPC spec copying notice when we quote table definitions from a spec: "copying is by permission of the Transaction Processing Performance Council", with the spec title and date.

# Share-alike / compatibility
Not copyleft in the GPL sense, but clause 9.a makes modified redistribution require at least the same conditions, and clause 8 propagates the terms into merged works. It is not compatible with relicensing under MIT/Apache; keep TPC-derived files in their own directories with their own LICENSE, and prefer **cloning the kits at build time (pinned commit) over vendoring**, so the repository itself redistributes no TPC Software (see [decision](/decisions/tpch-generator-path.md)).

# Applied to
* [TPC-H](/datasets/tpc-h.md) — dbgen/qgen 2.17.3 (tpch-kit) and DuckDB's port.
* [TPC-DS](/datasets/tpc-ds.md) — dsdgen/dsqgen 2.10.0 (tpcds-kit) and DuckDB's port.
* [SSB](/datasets/ssb.md) — ssb-dbgen is a modified TPC-H dbgen ("all new code ... follow the #ifdef SSBM statements"); clause 8/9 apply even though the fork ships no license file.
* Not applied to TPC-C: the TPC publishes no TPC-C software; only the spec's copying notice and trademark/fair-use rules apply ([TPC-C](/datasets/tpc-c.md)).
