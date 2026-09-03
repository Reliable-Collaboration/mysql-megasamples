---
type: Tool
title: tpcds-kit (TPC-DS dsdgen/dsqgen 2.10.0, GitHub mirror by gregrahn)
description: Reference C generator for the 24 TPC-DS tables and the 99 query templates with dialect files; integer scale factors only; deterministic RNG seed; ships a MySQL test script.
resource: https://github.com/gregrahn/tpcds-kit
tags:
- tool
- tpc-ds
- generator
- c
- tpc-eula
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
- resource: https://github.com/gregrahn/tpcds-kit
  title: gregrahn/tpcds-kit (README, EULA, tools/params.h, tools/release.h, tools/tpcds.sql, query_templates/*.tpl, tests/mysql_setup.sh)
  accessed: "2026-09-02"
  version: commit 5a3a81796992b725c2a8b216767e142609966752 (2020-03-11)
- resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/specification/TPC-DS_v2.10.0.pdf
  title: TPC-DS spec 2.10.0
  accessed: "2026-09-02"
---

# Facts
* Version: dsdgen/dsqgen **2.10.0** (`tools/release.h`); the TPC's current tools are **4.0.0** (click-through). DuckDB's port is also 2.10.0. What changed in the generator between 2.10 and 4.0 is unknown ([open question](/questions/tpcds-dsdgen-version-output-identity.md)).
* License: TPC EULA v2.2 (`EULA.txt` at root; TPC "Legal Notice" header on every template and `tpcds.sql`) — [license record](/licenses/tpc-eula.md).
* Build: `apt-get install gcc make flex bison byacc git`; `cd tools && make OS=LINUX` (produces `dsdgen`, `dsqgen`, `mkheader`, `checksum`, `distcomp`).
* dsdgen options (`tools/params.h`, defaults): `-SCALE n` **integer GB only** (default 1; SF=1 ≈ 1 GB raw, the qualification size); `-DIR d` (must exist); `-DELIMITER '|'`; `-SUFFIX .dat`; **`-TERMINATE Y`** (trailing delimiter, like dbgen; pass `-TERMINATE N` to omit); `-TABLE name`; `-PARALLEL n -CHILD k` for chunked generation; `-FORCE Y`; `-DISTRIBUTIONS tools/tpcds.idx` when not run from tools/; **`-RNGSEED` default 19620718** — output is deterministic for a given scale/seed; `-UPDATE n` for data-maintenance sets.
* Output: 24 `.dat` files (plus `dbgen_version.dat`), pipe-delimited, dates `YYYY-MM-DD`, times `HH:MM:SS`, NULLs as empty fields (**Inferred** from the kit's own MySQL script using plain LOAD DATA; verify NULL rendering — the Bexhoma project reports "the treatment of NULL during INSERT is complicated" for MySQL).
* DDL: `tools/tpcds.sql` (25 CREATE TABLEs incl. `dbgen_version`; types integer/char/varchar/decimal(7,2)/decimal(15,2)/date/time — all MySQL-native) and `tools/tpcds_ri.sql` (foreign keys). `tools/tpcds_source.sql` is the staging schema for data maintenance (not needed).
* Queries: `dsqgen -DIRECTORY ../query_templates -INPUT ../query_templates/templates.lst -DIALECT <d> -SCALE 1 -QUALIFY Y -VERBOSE Y -OUTPUT_DIR out` writes `query_0.sql` with all 99 queries; `-QUALIFY Y` uses the qualification parameters that match `answer_sets/`. Dialects shipped: **ansi, db2, netezza, oracle, sqlserver — no mysql**. A `mysql.tpl` is three lines: `define __LIMITA = ""; define __LIMITB = ""; define __LIMITC = "limit %d";` plus the two `_BEGIN/_END` defines copied from `netezza.tpl` (whose LIMITC is exactly this).
* MySQL harness inside the kit: `tests/mysql_setup.sh` loads with `load data infile '<file>' replace into table <t> fields terminated by '|'` (server-side file; needs FILE privilege) — proof the TPC's own test flow targets MySQL with plain LOAD DATA.
* Answer sets: `answer_sets/1.ans … 99.ans` (with `14_NULLS_FIRST.ans`/`14_NULLS_LAST.ans` style variants for NULL-ordering differences); their scale factor is not stated in the kit (**Inferred:** qualification DB = SF 1, per spec 3.3.1).

# Limits
* Integer SF → the smallest dataset is ~1 GB raw, ~3 GB in InnoDB (**Inferred**); smoke tests need DuckDB's fractional `dsdgen(sf=0.01)` instead ([DuckDB record](/tools/duckdb-tpch-tpcds-extensions.md)).
* The 99 queries need MySQL edits: FULL OUTER JOIN (q51, q97), `+ N days` arithmetic (18 templates), and the `[_LIMITC]` dialect — see [TPC-DS dataset](/datasets/tpc-ds.md).
