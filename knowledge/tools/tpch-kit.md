---
type: Tool
title: tpch-kit (TPC-H dbgen/qgen 2.17.3, GitHub mirror by gregrahn)
description: Reference C generator for TPC-H data and the 22 query templates with SF=1 answers; built with make in a builder stage; output is pipe-delimited .tbl with a trailing pipe.
resource: https://github.com/gregrahn/tpch-kit
tags: [tool, tpc-h, generator, c, tpc-eula]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://github.com/gregrahn/tpch-kit
    title: gregrahn/tpch-kit (README, Makefile, tpcd.h, dss.ddl, dss.ri, TPC README, release.h, answers/q1.out)
    accessed: "2026-09-02"
    version: commit 852ad0a5ee31ebefeed884cea4188781dd9613a3 (2018-05-07)
  - resource: https://github.com/electrum/tpch-dbgen
    title: electrum/tpch-dbgen (README, makefile.suite, release.h)
    accessed: "2026-09-02"
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf
    title: TPC-H spec 3.0.1
    accessed: "2026-09-02"
---

# Facts
* Version: dbgen/qgen **2.17.3** (`release.h`), i.e. the TPC-H 2.17.3 tools plus macOS/PostgreSQL build fixes. The TPC's current tools are **3.0.1** (click-through only, [download form](/sources/tpc-tools-download-request-form.md)); the 3.0.x spec revisions changed only pricing/metric clauses ([spec record](/sources/tpc-h-specification-v3-0-1.md)) — output identity is an [open question](/questions/tpch-dbgen-version-output-identity.md).
* License: the repository root carries the **TPC EULA v2.2** (`EULA.txt`), no OSI license ([license record](/licenses/tpc-eula.md)). Redistribution of the kit requires the EULA copy plus the "THE TPC SOFTWARE IS AVAILABLE WITHOUT CHARGE FROM TPC." legend; the plan clones it at a pinned commit at build time instead of vendoring.
* Build (Debian/Ubuntu builder stage): `apt-get install gcc make git`; `git clone https://github.com/gregrahn/tpch-kit && cd tpch-kit/dbgen && git checkout 852ad0a && make MACHINE=LINUX DATABASE=POSTGRESQL WORKLOAD=TPCH`. Valid `DATABASE` values: INFORMIX, DB2, TDAT, SQLSERVER, SYBASE, ORACLE, VECTORWISE, POSTGRESQL — **there is no MYSQL value**; use **POSTGRESQL** because its `SET_ROWCOUNT` is `limit %d;` (tpcd.h), which MySQL accepts, whereas INFORMIX gives `FIRST %d` and ORACLE `where rownum <= %d`. (The brief's suggestion of INFORMIX/ORACLE is therefore not the best choice for MySQL; community ports patched SQLSERVER's block to `limit %d` before POSTGRESQL existed in the Makefile — [catarinaribeir0](/sources/github-catarinaribeir0-queries-tpch-dbgen-mysql.md).)
* Data: `DSS_PATH=/out ./dbgen -s 1 -f -v` writes `region.tbl, nation.tbl, supplier.tbl, part.tbl, partsupp.tbl, customer.tbl, orders.tbl, lineitem.tbl`; `-T` letters: p (part+partsupp), c, s, o (orders+lineitem), n, r, l (nation+region), O, L, P, S; `-C n -S k` for parallel chunks; fractional `-s 0.1` works (community-observed, [source](/sources/github-catarinaribeir0-queries-tpch-dbgen-mysql.md)). Format: pipe-delimited, one trailing `|` per line, dates `YYYY-MM-DD`, decimals with two places, ASCII text only (TPC-H text is generated from an English word grammar — **Inferred:** no non-ASCII bytes; verify with `LC_ALL=C grep -P '[\x80-\xff]'`).
* Queries: `DSS_QUERY=../queries ./qgen -v -c -d -s 1 N` (N = 1..22; omit for all) emits query N with the spec's validation ("default", `-d`) substitution parameters, comments kept (`-c`), `limit N;` for the ":n" directive. Variants (8a, 12a, 13a, 14a, 15a) for engines without certain features live in `variants/`.
* Answers: `answers/q1.out … q22.out` are the qualification-database (SF=1) results in pipe-delimited form; `check_answers/cmpq.pl` compares with a precision table (`colprecision.txt`). Q1 first row: `A|F|37734107.00|56586554400.73|53758257134.87|55909065222.83|25.52|38273.13|0.05|1478493` — matches spec Clause 2.4.1.5.
* DDL: `dss.ddl` (portable: INTEGER, CHAR, VARCHAR, DECIMAL(15,2), DATE) and `dss.ri` (DB2 syntax: `CONNECT TO TPCD`, `ALTER TABLE TPCD.x ADD FOREIGN KEY name (col) references TPCD.y` without a column list) — usable as the source of truth but must be rewritten for MySQL (drop schema prefix, add referenced column lists, drop CONNECT/COMMIT).
* MySQL loading: `LOAD DATA LOCAL INFILE '/out/lineitem.tbl' INTO TABLE lineitem FIELDS TERMINATED BY '|' LINES TERMINATED BY '|\n';` — the `'|\n'` line terminator swallows the trailing pipe ([dhuny/tpch](/sources/github-dhuny-tpch.md)); alternatively plain `FIELDS TERMINATED BY '|'` works but logs one "too many fields" warning per row ([LOAD DATA doc](https://dev.mysql.com/doc/refman/9.7/en/load-data.html), [tpcds-kit mysql_setup.sh](/sources/github-gregrahn-tpcds-kit.md)).

# Alternatives considered
* electrum/tpch-dbgen: dbgen 2.14.0, no EULA copy, no POSTGRESQL dialect — reference only ([record](/sources/github-electrum-tpch-dbgen.md)).
* DuckDB's built-in port of the same 2.17.3 code ([record](/tools/duckdb-tpch-tpcds-extensions.md)) — chosen as primary generator in [the decision](/decisions/tpch-generator-path.md); this kit remains the cross-check and the source of qgen/answers.

# Limits
* Needs a C toolchain (not in the runtime image; builder stage only).
* Output size ≈ 1.0 GB per SF (spec: 956 MB "typical" at SF=1).
* Compliant SFs are 1, 10, 30, 100, …; anything else is fine for a sample database but must be described as non-compliant.
