---
type: Tool
title: ssb-dbgen (Star Schema Benchmark data generator, eyalroz unified fork)
description: CMake-built C generator derived from TPC-H dbgen that writes the five SSB tables as pipe-delimited .tbl files; no license file, TPC EULA applies by derivation; no query generator.
resource: https://github.com/eyalroz/ssb-dbgen
tags: [tool, ssb, generator, c, tpc-eula]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://github.com/eyalroz/ssb-dbgen
    title: eyalroz/ssb-dbgen (README, CMakeLists.txt, doc/ssb.ddl, doc/ssb.ri, src/driver.c, listing)
    accessed: "2026-09-02"
    version: commit ae1e254aa4d603d8ef1f44078e5abed011634b23 (2025-04-26); no tags
  - resource: https://github.com/electrum/ssb-dbgen
    title: electrum/ssb-dbgen README/CHANGES
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/ClickHouse/clickhouse-docs/main/docs/getting-started/example-datasets/star-schema.md
    title: ClickHouse SSB doc (uses vadimtk/ssb-dbgen)
    accessed: "2026-09-02"
---

# Facts
* Lineage: "based on the TPC-H benchmark's data generation utility, also named dbgen"; the electrum fork's README says "The original TPCH dbgen code stays untouched and all new code related to SSBM dbgen follow the #ifdef SSBM statements". eyalroz's repo unifies the abandoned forks (electrum, vadimtk used by ClickHouse, others) and is the only one with recent commits (2025-04-26). **No LICENSE/EULA/COPYING file in any fork**; the source files carry the TPC SCCS ids (`@(#)driver.c 2.1.8.4`) — the [TPC EULA](/licenses/tpc-eula.md) governs it as a modified TPC-H dbgen (clause 4.b/9), and a redistributor would have to add the EULA copy and legend that the forks omit. Plan: clone at a pinned commit at build time; do not vendor.
* Build: `cmake -B build [-DEOL_HANDLING=ON] [-DYMD_DASH_DATE=ON] [-DCSV_OUTPUT_FORMAT=ON] && cmake --build build` (needs cmake + a C compiler; tested with gcc/clang/MSVC/MinGW). Options: `DATABASE` (qgen only; INFORMIX/DB2/TDAT/SQLSERVER/SYBASE), `WORKLOAD` (SSB default), `EOL_HANDLING` (ON = no trailing `|`), `YMD_DASH_DATE` (ON = `YYYY-MM-DD` dates instead of `YYYYMMDD` integers), `CSV_OUTPUT_FORMAT`.
* Run: `./dbgen -b ../dists.dss -v -s 1` (all tables) or `-T c|p|s|d|l|a`; outputs `customer.tbl, part.tbl, supplier.tbl, date.tbl, lineorder.tbl`; refresh sets with `-r 5 -U 4`. Sample: `1|Customer#000000001|j5JsirBM9P|MOROCCO  0|MOROCCO|AFRICA|25-989-741-2988|BUILDING|`. "At this moment there is no QGEN for SSBM" (electrum README) — the 13 queries come from the paper/ClickHouse doc.
* Cardinalities: customer 30,000×SF (README: 300,000 at SF 10), supplier 2,000×SF (electrum CHANGES: fixed from 10,000×SF on 2010-02-28), part 200,000×(1+⌊log2 SF⌋), date 7 years (1992–1998), lineorder ≈ 6,000,000×SF — exact SF=1 counts to be measured ([open question](/questions/ssb-sf1-row-counts.md)).
* DDL/RI shipped in `doc/ssb.ddl` and `doc/ssb.ri`; the RI file names the date table `date_` and puts a single-column PK on lineorder — both contradict the DDL/paper; use the paper's compound key (lo_orderkey, lo_linenumber).
* DuckDB ships **no SSB generator** (its `extension/` tree has only tpch and tpcds; verified by listing) — **Inferred:** no community DuckDB extension either (not surveyed).

# Limits
* No official releases/tags; pin by commit.
* `d_datekey` is an integer `YYYYMMDD` by default; keep it INTEGER (paper) so `lo_orderdate = d_datekey` joins stay integer, or build with `YMD_DASH_DATE=ON` and use DATE columns (ClickHouse style). The dataset record chooses INTEGER + a generated DATE column.
