---
type: Tool
title: DuckDB tpch and tpcds extensions (built-in dbgen 2.17.3 and dsdgen 2.10.0)
description: Generate TPC-H/TPC-DS data at any (fractional) scale factor inside DuckDB without a C toolchain, then COPY to pipe-delimited files for LOAD DATA or ATTACH MySQL directly; the generator code is TPC-EULA-licensed inside an MIT project.
resource: https://duckdb.org/docs/current/core_extensions/tpch.html
tags: [tool, duckdb, tpc-h, tpc-ds, generator]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://duckdb.org/docs/current/core_extensions/tpch.html
    title: DuckDB TPC-H extension docs
    accessed: "2026-09-02"
  - resource: https://duckdb.org/docs/current/core_extensions/tpcds.html
    title: DuckDB TPC-DS extension docs
    accessed: "2026-09-02"
  - resource: https://github.com/duckdb/duckdb/tree/main/extension/tpch
    title: extension/tpch and extension/tpcds source (LICENSE, release.h, answers)
    accessed: "2026-09-02"
    version: main on 2026-09-02; latest release v1.5.5 (2026-07-22)
  - resource: https://duckdb.org/docs/current/sql/statements/copy.html
    title: COPY statement docs
    accessed: "2026-09-02"
  - resource: https://duckdb.org/docs/current/core_extensions/mysql.html
    title: MySQL extension docs
    accessed: "2026-09-02"
---

# Facts
* `INSTALL tpch; LOAD tpch; CALL dbgen(sf = 0.01);` creates the 8 TPC-H tables; `sf` is DOUBLE; `children`/`step` generate one partition at a time (bounded memory); `suffix`/`catalog` place tables. `FROM tpch_queries()` gives the 22 queries with fixed (validation) parameters; `FROM tpch_answers()` has answers for **sf 0.01, 0.1 and 1** (the source tree also has sf10/sf100). Port of dbgen **2.17.3** — identical version to tpch-kit; its `answers/sf1/q01.csv` matches the spec's Q1 validation output.
* `INSTALL tpcds; LOAD tpcds; CALL dsdgen(sf = 0.01, keys = true);` creates the 24 TPC-DS tables (`keys` adds PK/FK); `sf` DOUBLE (fractional SF possible, unlike the C dsdgen); `tpcds_queries()` (99) and `tpcds_answers()` for **sf 1 and 10**. Port of dsdgen **2.10.0** — same as tpcds-kit; DuckDB says the generator "will change in DuckDB version 2.0 to make the generator compatible with TPC-DS version 4".
* License: `extension/tpch/dbgen/LICENSE` is the TPC EULA v2.2; every dbgen header says "Copyright owned by the Transaction Processing Performance Council ... THE TPC SOFTWARE IS AVAILABLE WITHOUT CHARGE FROM TPC."; dsdgen files carry the TPC "Legal Notice". DuckDB itself is MIT ([license](/licenses/mit.md)); the TPC parts stay under the [TPC EULA](/licenses/tpc-eula.md). The extensions are downloaded from DuckDB's extension repository at first use, so the megasamples repo redistributes nothing.
* Export for MySQL: `COPY lineitem TO '/out/lineitem.tbl' (FORMAT csv, DELIMITER '|', HEADER false);` (defaults: delimiter `,`, header true, quote `"`) — produces **no trailing pipe**, so MySQL loads with plain `FIELDS TERMINATED BY '|'`; strings containing `|` or `"` would be quoted by DuckDB (TPC-H text has neither — **Inferred**; verify), NULLs are written as empty fields (DuckDB default `NULLSTR` — **Inferred**; TPC-DS has NULLs, so set `NULLSTR '\\N'` and let LOAD DATA read `\N` as NULL, or use the `SET col = NULLIF(@v,'')` form).
* Direct path: `INSTALL mysql; ATTACH 'host=mysql user=admin password=... database=tpch' AS m (TYPE mysql); INSERT INTO m.lineitem SELECT * FROM lineitem;` — works per docs; throughput vs LOAD DATA unmeasured ([open question](/questions/duckdb-generator-fidelity.md)).
* DuckDB CLI is a single static binary already planned for the loader image ([tier model](/decisions/tier-model.md)).

# Limits / hazards
* Fidelity: the ports are transliterations of the TPC C code; byte-identity of the generated rows with tpch-kit/tpcds-kit output at the same SF is **not documented** — first execution experiment in [fidelity question](/questions/duckdb-generator-fidelity.md) (diff sorted .tbl at SF 0.01 and 1; compare Q1–Q22 results with `tpch_answers()` and the kit's `answers/`).
* Memory: `dbgen(sf=10)` materialises ~10 GB of tables; use a file-backed database (`duckdb /tmp/gen.duckdb`), `SET memory_limit`, and `children/step` partitions, exporting and dropping each step.
* `tpch_queries()`/`tpcds_queries()` are in DuckDB's dialect (PostgreSQL-like); they still need the MySQL edits listed in the dataset records.
* `dsdgen` in DuckDB has no `RNGSEED` parameter exposed (docs list sf, schema, catalog, suffix, keys, overwrite) — output is deterministic per DuckDB version only (**Inferred**).
