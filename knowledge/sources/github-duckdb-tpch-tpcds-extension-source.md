---
type: Source
title: duckdb/duckdb extension/tpch and extension/tpcds source tree (license and generator versions)
description: What license notice DuckDB's bundled dbgen/dsdgen ports carry, which TPC tool versions they port, and the stored SF1 Q1 answer.
resource: https://github.com/duckdb/duckdb/tree/main/extension/tpch
tags:
- duckdb
- tpc-h
- tpc-ds
- license
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://raw.githubusercontent.com/duckdb/duckdb/main/extension/tpch/dbgen/LICENSE
  title: extension/tpch/dbgen/LICENSE (17,729 B)
  accessed: "2026-09-02"
  version: main, 2026-09-02; DuckDB latest release v1.5.5 (2026-07-22)
- resource: https://raw.githubusercontent.com/duckdb/duckdb/main/extension/tpch/dbgen/include/dbgen/release.h
  title: extension/tpch/dbgen/include/dbgen/release.h
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/duckdb/duckdb/main/extension/tpcds/dsdgen/include/dsdgen-c/release.h
  title: extension/tpcds/dsdgen/include/dsdgen-c/release.h
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/duckdb/duckdb/main/extension/tpch/dbgen/answers/sf1/q01.csv
  title: extension/tpch/dbgen/answers/sf1/q01.csv
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/duckdb/duckdb/main/LICENSE
  title: DuckDB LICENSE (MIT, "Copyright 2018-2026 Stichting DuckDB Foundation")
  accessed: "2026-09-02"
---

# What was read
Directory listings of `extension/` (autocomplete, core_functions, delta, icu, json, parquet, tpcds, tpch — no SSB), `extension/tpch/dbgen/` (LICENSE, answers/{sf0.01,sf0.1,sf1,sf10,sf100}, queries/, C++ ports bm_utils/build/dbgen/permute/rnd/rng64/speed_seed/text), `extension/tpcds/dsdgen/` (dsdgen-c/, answers/, queries/, schema/, tpcds.idx), the files above.

# Relevant excerpt
* `extension/tpch/dbgen/LICENSE` is the **TPC EULA Version 2.2**, identical to tpc.org's EULA_v2.2.0.txt after whitespace normalisation.
* dbgen release.h header: "Copyright owned by the Transaction Processing Performance Council. A copy of the license is included under extension/tpch/dbgen/LICENSE in this repository. You may not use this file except in compliance with the License. THE TPC SOFTWARE IS AVAILABLE WITHOUT CHARGE FROM TPC." and `VERSION 2 RELEASE 17 PATCH 3` → the port is of dbgen **2.17.3** (same as tpch-kit).
* dsdgen release.h: the TPC "Legal Notice ... The TPC reserves all right, title, and interest to the Work" header and `VERSION 2 RELEASE 10 MODIFICATION 0`, `COPYRIGHT "Transaction Processing Performance Council (TPC)"`, `C_DATES "2001 - 2018"` → dsdgen **2.10.0** (same as tpcds-kit). No separate LICENSE file in the tpcds tree.
* DuckDB's own LICENSE is MIT; the generator subtrees are TPC-licensed islands inside it (EULA clause 8 "Merger or Integration").
* answers/sf1/q01.csv (pipe-delimited): `A|F|37734107|56586554400.73|53758257134.8700|55909065222.827692|25.522005853257337|38273.129734621674|0.049985295838397614|1478493` … `R|F|37719753|56568041380.90|53741292684.6040|55889619119.831932|25.50579361269077|38250.85462609966|0.05000940583012706|1478870` — the same sums/counts as the spec's Q1 validation output and tpch-kit's q1.out, with more decimal places.

# What it was used to decide
[DuckDB extensions tool record](/tools/duckdb-tpch-tpcds-extensions.md); [TPC EULA license record](/licenses/tpc-eula.md) (applies to DuckDB's ports too); fidelity [open question](/questions/duckdb-generator-fidelity.md).
