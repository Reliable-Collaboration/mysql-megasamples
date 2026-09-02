---
type: Source
title: catarinaribeir0/queries-tpch-dbgen-mysql (TPC-H 22 queries hand-ported to MySQL)
description: Community port of the TPC-H queries to MySQL; shows the SQLSERVER-dialect tpcd.h edit (limit %d) and the Q1 text as run on MySQL.
resource: https://github.com/catarinaribeir0/queries-tpch-dbgen-mysql
tags: [tpc-h, mysql, community, github]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/catarinaribeir0/queries-tpch-dbgen-mysql/master/README.md
    title: README.md (+ 1.sql)
    accessed: 2026-09-02
    version: master; pushed_at 2019-12-16; license null; 49 stars
---

# Relevant excerpt
* README: uses TPC-H 2.16.0 dbgen; edits makefile to `DATABASE=SQLSERVER MACHINE=LINUX WORKLOAD=TPCH` and tpcd.h's SQLSERVER block to `START_TRAN "BEGIN WORK;" END_TRAN "COMMIT WORK;" SET_ROWCOUNT "limit %d;\n\n" SET_DBASE "use %s;\n"`; generates with `./dbgen -s 0.1` ("0.1 (=100MB)") — evidence that fractional `-s` works.
* 1.sql as run on MySQL: `... from LINEITEM where l_shipdate <= date '1998-12-01' - interval '108' day group by l_returnflag, l_linestatus order by l_returnflag, l_linestatus;` — the template's trailing `(3)` interval precision is removed; `date '...'` and `interval '108' day` are kept.

# What it was used to decide
[TPC-H dataset](/datasets/tpc-h.md) query-porting rules; [MySQL query syntax question](/questions/mysql-tpch-query-port-syntax.md).
