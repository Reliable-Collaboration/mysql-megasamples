---
type: Open Question
title: Does the TPC EULA restrict redistribution of dbgen/dsdgen OUTPUT (the generated rows)?
description: The EULA licenses "the Software … and data files associated with such programs" but never mentions generated output; we ship none, but users and CI caches will.
resource: /questions/tpc-eula-generated-data-redistribution.md
tags: [question, tpc, license]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/txt/EULA_v2.2.0.txt
    accessed: 2026-09-02
---

# Question
Clause 3/9 of the [TPC EULA](/licenses/tpc-eula.md) cover copying/distributing the *Software* ("source code, scripts, executable programs, drivers, libraries and data files associated with such programs"). The `.tbl`/`.dat` rows produced by running dbgen/dsdgen are not named. Are tiny pre-generated scale factors (e.g. SF 0.01 ≈ 10 MB) redistributable in a public repo or as GitHub release assets? DuckDB publicly distributes pre-generated TPC-DS SF10–SF300 database files ([DuckDB docs](/sources/duckdb-docs-tpcds-extension.md)), which is evidence of an industry reading that output is unrestricted, but not a legal statement.

# Cheapest experiment
1. E-mail info@tpc.org (the address the EULA clause 5 gives for license questions) asking whether generated populations may be redistributed with the disclaimer; record the answer here.
2. Until answered: ship no generated data (all four benchmark datasets are generated on demand); CI caches of generated files stay private to the runner.

# Resolves
[TPC-H](/datasets/tpc-h.md), [TPC-DS](/datasets/tpc-ds.md), [SSB](/datasets/ssb.md) tier/packaging; whether a "smoke" SF 0.01 dump may be published as a release asset.
