---
type: Open Question
title: May the MySQL-ported TPC-H (22) and TPC-DS (99) query texts be committed to the public repository?
description: Query templates are TPC Software under the EULA; modified redistribution requires the EULA copy, the caps legend and retained TPC headers; the alternative is generating and patching them at build time.
resource: /questions/tpc-query-text-redistribution.md
tags: [question, tpc, license]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/txt/EULA_v2.2.0.txt
    accessed: "2026-09-02"
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf
    accessed: "2026-09-02"
---

# Question
Two routes exist: (a) commit `datasets/tpch/queries/*.sql` and `datasets/tpcds/queries/*.sql` (ported text, ~130 KB) under the EULA terms of clause 9 (EULA copy + "THE TPC SOFTWARE IS AVAILABLE WITHOUT CHARGE FROM TPC." legend + TPC headers retained, no fee — all satisfiable in a public repo); (b) commit only a patch/sed script and generate the text at build time from the pinned kits (nothing TPC-authored is redistributed, but users cannot read the queries in the repo and the patch file itself contains TPC context lines). The TPC-H spec separately permits copying spec material "for the primary purpose of disseminating TPC material" with notice — the functional query definitions are in the spec, which suggests (a) is acceptable with the notices.

# Cheapest experiment
Ask the same info@tpc.org question as [the data question](/questions/tpc-eula-generated-data-redistribution.md) (one e-mail). Default until answered: route (b) for TPC-DS (99 files), route (a) for TPC-H only if the maintainers accept the notices in `datasets/tpch/LICENSE`; the [TPC-H](/datasets/tpc-h.md) and [TPC-DS](/datasets/tpc-ds.md) records assume route (b).

# Resolves
Repository layout for the two datasets' `queries/` directories and LICENSES.md wording.
