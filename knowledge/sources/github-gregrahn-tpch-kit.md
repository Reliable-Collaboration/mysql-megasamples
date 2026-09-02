---
type: Source
title: gregrahn/tpch-kit (TPC-H dbgen/qgen 2.17.3 mirror with fixes)
description: The most-used GitHub mirror of the TPC-H tools; read its README, Makefile, tpcd.h, dss.ddl, dss.ri, the TPC README, release.h, queries/1.sql, answers/q1.out and the repository listing.
resource: https://github.com/gregrahn/tpch-kit
tags: [tpc-h, dbgen, qgen, github]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/gregrahn/tpch-kit/master/README.md
    title: tpch-kit README
    accessed: "2026-09-02"
    version: master @ 852ad0a5ee31ebefeed884cea4188781dd9613a3 (2018-05-07, latest commit); repo pushed_at 2022-07-20; 217 stars; GitHub license field null
  - resource: https://raw.githubusercontent.com/gregrahn/tpch-kit/master/dbgen/Makefile
    title: dbgen/Makefile
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/gregrahn/tpch-kit/master/dbgen/tpcd.h
    title: dbgen/tpcd.h
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/gregrahn/tpch-kit/master/dbgen/dss.ddl
    title: dbgen/dss.ddl
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/gregrahn/tpch-kit/master/dbgen/dss.ri
    title: dbgen/dss.ri
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/gregrahn/tpch-kit/master/dbgen/README
    title: dbgen/README (the TPC's own DBGEN/QGEN README, "@(#)README 2.4.0")
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/gregrahn/tpch-kit/master/dbgen/release.h
    title: dbgen/release.h
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/gregrahn/tpch-kit/master/dbgen/queries/1.sql
    title: dbgen/queries/1.sql
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/gregrahn/tpch-kit/master/dbgen/answers/q1.out
    title: dbgen/answers/q1.out
    accessed: "2026-09-02"
---

# What was read
Repository metadata via GitHub API and the files listed above. Root files: `.gitattributes`, `.gitignore`, `EULA.txt` (17,809 B, TPC EULA v2.2), `README.md`, `dbgen/`, `doc/` (tpc-h_v2.17.3.pdf/.docx), `ref_data/` (subdirs 1, 100, 300, 1000, 3000, 10000, 30000, 100000 holding reference `customer.tbl.N`, `delete.u1.N`... sample files). `dbgen/` contains the C sources, `answers/` (q1.out … q22.out), `queries/` (1.sql … 22.sql templates), `variants/` (8a, 12a, 13a, 14a, 15a), `check_answers/` (cmpq.pl), `dists.dss`, `dss.ddl`, `dss.ri`, `update_release.sh`.

# Relevant excerpt
* README: build `cd tpch-kit/dbgen && make MACHINE=LINUX DATABASE=POSTGRESQL` (or MACHINE=MACOS); env vars `DSS_CONFIG` (dbgen dir), `DSS_QUERY` (queries dir), `DSS_PATH` (output dir); "See `dbgen -h` for all options"; "`qgen -v -c -d -s 1 > tpch-stream.sql`" produces all 22 queries at 1 GB scale.
* Makefile: "Current values for DATABASE are: INFORMIX, DB2, TDAT (Teradata) SQLSERVER, SYBASE, ORACLE, VECTORWISE, POSTGRESQL"; "MACHINE are: ATT, DOS, HP, IBM, ICL, MVS, MACOS SGI, SUN, U2200, VMS, LINUX, WIN32"; "WORKLOAD are: TPCH"; defaults `DATABASE = POSTGRESQL`, `MACHINE = LINUX`, `WORKLOAD = TPCH`; `CFLAGS = -g -DDBNAME=\"dss\" -D$(MACHINE) -D$(DATABASE) -D$(WORKLOAD) -DRNG_TEST -D_FILE_OFFSET_BITS=64`. There is no MYSQL value.
* tpcd.h: `#ifdef POSTGRESQL ... #define SET_ROWCOUNT "limit %d;\n"`; INFORMIX → "FIRST %d"; ORACLE → "where rownum <= %d;"; SQLSERVER/SYBASE → "set rowcount %d\ngo"; DB2 → "--#SET ROWS_FETCH %d"; VECTORWISE → "first %d". So `DATABASE=POSTGRESQL` makes qgen emit MySQL-compatible `limit N` for the ":n" directives.
* release.h: `VERSION 2 RELEASE 17 PATCH 3` → dbgen/qgen 2.17.3.
* TPC README: "Without any command line options, DBGEN will generate 8 separate ascii files. Each file will contain pipe-delimited load data ... named <table>.tbl"; options `-s <scale>` ("Scale 1.0 represents ~1 GB of data"), `-T <table>` ("p -- part/partuspp, c -- customer, s -- supplier, o -- orders/lineitem, n -- nation, r -- region, l -- code (same as n and r), O -- orders, L -- lineitem, P -- part, S -- partsupp"), `-C <children>`, `-S <n>`, `-f` force, `-v` verbose, `-U`/`-r` refresh sets; "TPC-H runs are only compliant when run against SF's of 1, 10, 100, 300, 1000, 3000, 10000, 30000, 100000"; "the resultant population must exactly match the output of DBGEN".
* dss.ddl (8 tables, upper-case names, `INTEGER`, `CHAR(n)`, `VARCHAR(n)`, `DECIMAL(15,2)`, `DATE`) and dss.ri (DB2-flavoured `ALTER TABLE TPCD.x ADD PRIMARY KEY` / `ADD FOREIGN KEY name (cols) references TPCD.y`, with `CONNECT TO TPCD;` and `COMMIT WORK;`) — see the DDL reproduced in [TPC-H dataset](/datasets/tpc-h.md).
* queries/1.sql template: `where l_shipdate <= date '1998-12-01' - interval ':1' day (3)` with directives `:x :o ... :n -1`.
* answers/q1.out (pipe-delimited): `A|F|37734107.00|56586554400.73|53758257134.87|55909065222.83|25.52|38273.13|0.05|1478493`, `N|F|991417.00|1487504710.38|1413082168.05|1469649223.19|25.52|38284.47|0.05|38854`, `N|O|74476040.00|111701729697.74|106118230307.61|110367043872.50|25.50|38249.12|0.05|2920374`, `R|F|37719753.00|56568041380.90|53741292684.60|55889619119.83|25.51|38250.85|0.05|1478870`.

# What it was used to decide
[tpch-kit tool record](/tools/tpch-kit.md); [TPC-H dataset](/datasets/tpc-h.md); [TPC-H generator decision](/decisions/tpch-generator-path.md).
