---
type: Source
title: electrum/tpch-dbgen (TPC-H dbgen 2.14.0 mirror)
description: Older GitHub mirror of the TPC-H tools (2.14.0); no license file; kept for reference only.
resource: https://github.com/electrum/tpch-dbgen
tags:
- tpc-h
- dbgen
- github
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://raw.githubusercontent.com/electrum/tpch-dbgen/master/README
  title: README (the TPC README, "@(#)README 2.4.0")
  accessed: "2026-09-02"
  version: master; repo pushed_at 2023-09-03; 342 stars; GitHub license field null
- resource: https://raw.githubusercontent.com/electrum/tpch-dbgen/master/makefile.suite
  title: makefile.suite
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/electrum/tpch-dbgen/master/release.h
  title: release.h
  accessed: "2026-09-02"
---

# What was read
Repository listing (README, BUGS, HISTORY, PORTING.NOTES, answers/, queries/, variants/, dss.ddl, dss.ri, makefile.suite, C sources; **no EULA or LICENSE file**), README, makefile.suite, release.h.

# Relevant excerpt
* release.h: `VERSION 2 RELEASE 14 PATCH 0` → 2.14.0 (older than tpch-kit's 2.17.3).
* makefile.suite: "Current values for DATABASE are: INFORMIX, DB2, TDAT (Teradata) SQLSERVER, SYBASE, ORACLE" (no POSTGRESQL/VECTORWISE here), "MACHINE are: ATT, DOS, HP, IBM, ICL, MVS, SGI, SUN, U2200, VMS, LINUX, WIN32"; `CC`, `DATABASE`, `MACHINE` left blank for the user to fill.
* README is the TPC's own text (identical section list to tpch-kit's dbgen/README); it contains no license notice.

# What it was used to decide
Rejected as the primary mirror in [tpch-kit tool record](/tools/tpch-kit.md): older version, no EULA copy, no POSTGRESQL dialect.
