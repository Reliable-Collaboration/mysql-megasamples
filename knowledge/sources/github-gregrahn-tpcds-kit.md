---
type: Source
title: gregrahn/tpcds-kit (TPC-DS dsdgen/dsqgen 2.10.0 mirror with fixes)
description: GitHub mirror of the TPC-DS tools based on v2.10.0; read README, EULA presence, query_templates (dialect files), tools/tpcds.sql, tools/params.h, tools/release.h, tests/mysql_setup.sh, answer_sets listing, and a feature survey of the 99 templates.
resource: https://github.com/gregrahn/tpcds-kit
tags: [tpc-ds, dsdgen, dsqgen, github]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/README.md
    title: tpcds-kit README
    accessed: 2026-09-02
    version: master @ 5a3a81796992b725c2a8b216767e142609966752 (2020-03-11, latest commit); pushed_at 2024-04-16; 365 stars; GitHub license field null
  - resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/query_templates/ansi.tpl
    title: query_templates/ansi.tpl (+ netezza.tpl, sqlserver.tpl, db2.tpl, oracle.tpl, README, templates.lst)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/tools/tpcds.sql
    title: tools/tpcds.sql
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/tools/params.h
    title: tools/params.h (dsdgen option table)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/tools/release.h
    title: tools/release.h
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/tests/mysql_setup.sh
    title: tests/mysql_setup.sh
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/query_templates/query16.tpl
    title: query_templates/query1..99.tpl (all 99 downloaded and grepped; query5, 16, 36, 51, 97, 8, 14, 38, 87 read in part)
    accessed: 2026-09-02
---

# What was read
Root: `EULA.txt` (17,730 B, TPC EULA v2.2), `README.md`, `answer_sets/` (1.ans … 99.ans, with `14_NULLS_FIRST.ans`/`14_NULLS_LAST.ans` style variants), `query_templates/`, `query_variants/`, `specification/` (TPC-DS_v2.10.0.pdf/.docx), `tests/`, `tools/`.

# Relevant excerpt
* README: "This version is based on v2.10.0 and has been modified to: Allow compilation under macOS; Address obvious query template bugs like query22a, query77a; Rename s_web_returns column wret_web_site_id to wret_web_page_id". Build deps (Ubuntu): `gcc make flex bison byacc git`; `cd tpcds-kit/tools && make OS=LINUX`. "If you do not run dsdgen from the tools/ directory then you will need to use the option -DISTRIBUTIONS /.../tpcds-kit/tools/tpcds.idx. The output directory (specified via the -DIR option) must exist prior to running dsdgen." dsqgen example: `dsqgen -DIRECTORY ../query_templates -INPUT ../query_templates/templates.lst -VERBOSE Y -QUALIFY Y -SCALE 10000 -DIALECT netezza -OUTPUT_DIR /tmp`.
* tools/release.h: `VERSION 2 RELEASE 10 MODIFICATION 0`.
* tools/params.h (dsdgen options, defaults in quotes): DELIMITER "use <s> as output field separator" "|"; DIR "."; DISTRIBUTIONS "tpcds.idx"; FORCE; **SCALE is OPT_INT "volume of data to generate in GB" "1"** (integers only); SUFFIX ".dat"; TABLE "ALL"; **TERMINATE "end each record with a field delimiter" default "Y"** (trailing pipe like dbgen); UPDATE; PARALLEL "build data in <n> separate chunks"; CHILD; VALIDATE; **RNGSEED "set RNG seed" default "19620718"** (deterministic).
* Dialect templates: `ansi.tpl`: `__LIMITA=""; __LIMITB="top %d"; __LIMITC=""`; `netezza.tpl`: `__LIMITC="limit %d"` (the MySQL-compatible form); `sqlserver.tpl`: `__LIMITB="top %d"`; `db2.tpl`: `__LIMITC=" fetch first %d rows only"`; `oracle.tpl`: `__LIMITA="select * from ("; __LIMITC=" ) where rownum <= %d"`. Shipped dialects: ansi, db2, netezza, oracle, sqlserver — no mysql.
* tools/tpcds.sql: 25 `create table` statements (24 benchmark tables + `dbgen_version`), types used: integer (189 columns), date (12), time (1), plus char/varchar/decimal(7,2)/decimal(15,2). Legal header: "This document and associated source code (the "Work") is a part of a benchmark specification maintained by the TPC ... TPC reserves all right, title, and interest".
* tests/mysql_setup.sh (the kit's own MySQL test harness): `mysql -utpcds -ptpcds -D$V_DATABASE -e "load data infile '$1' replace into table $2 fields terminated by '|'"` and index creation via awk over the RI file; requires the global FILE privilege.
* Template feature survey (grep over query1..99.tpl): ROLLUP in 11 (q5, 14, 18, 22, 27, 36, 67, 70, 77, 80, 86); GROUPING() in 4 (q27, 36, 70, 86); FULL OUTER JOIN in 2 (q51, q97); EXCEPT in 1 (q87); INTERSECT in 3 (q8, 14, 38); "+ N days" date arithmetic (e.g. q16: `(cast('[YEAR]-[MONTH]-01' as date) + 60 days)`) in 18 (q5, 12, 16, 20, 21, 32, 37, 40, 50, 62, 77, 80, 82, 92, 94, 95, 98, 99); window functions in 9; `[_LIMITC]` in 84; SUBSTR in 9; STDDEV_SAMP in 6; NULLS FIRST/LAST in 0; WITH RECURSIVE in 0.

# What it was used to decide
[tpcds-kit tool record](/tools/tpcds-kit.md); [TPC-DS dataset](/datasets/tpc-ds.md); [TPC-DS generator decision](/decisions/tpcds-generator-path.md).
