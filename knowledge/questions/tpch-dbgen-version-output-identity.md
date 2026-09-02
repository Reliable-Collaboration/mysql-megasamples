---
type: Open Question
title: Is dbgen 2.17.3 (tpch-kit, DuckDB) output identical to the official TPC-H_Tools_v3.0.1 dbgen output?
description: The 3.0.0/3.0.1 revision notes list only pricing/metric clauses, suggesting the data generator did not change, but this is inferred.
resource: /questions/tpch-dbgen-version-output-identity.md
tags:
- question
- tpc-h
- generator
status: draft
trust: open
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf
  accessed: "2026-09-02"
- resource: https://github.com/gregrahn/tpch-kit
  accessed: "2026-09-02"
---

# Question
Revision history of the 3.0.1 spec: "10 February 2021 Revision 3.0.0 Change price performance metric … Affected clauses are: 0.1, 4.1.3.1, 5.4, …"; "28 April 2022 Revision 3.0.1 Clarify change log history … Add comment to Clause 9.2.4.3 … 2.4.19.5". None touches Clause 4.2 (population) or dbgen. Is the 3.0.1 tools zip's dbgen source identical to 2.17.3 apart from `release.h`?

# Cheapest experiment
A human registers on the [TPC form](/sources/tpc-tools-download-request-form.md), downloads TPC-H_Tools_v3.0.1.zip (once), and runs `diff -r` between its `dbgen/` and tpch-kit's `dbgen/` excluding release.h/Makefile; then `./dbgen -s 0.01` with both and `cmp` the `.tbl` files. Record the diff summary here and the zip's size/sha256 in the [TPC-H record](/datasets/tpc-h.md).

# Resolves
Whether the README may say "generated with TPC-H dbgen 3.0.1-equivalent" and whether `ref_data` validation applies.
