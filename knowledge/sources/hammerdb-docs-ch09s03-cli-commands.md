---
type: Source
title: HammerDB docs 9.3 — CLI commands (dbset, diset, buildschema, vuset)
description: The CLI verbs needed to script a MySQL TPROC-C schema build without the GUI.
resource: https://www.hammerdb.com/docs/ch09s03.html
tags:
- hammerdb
- cli
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://www.hammerdb.com/docs/ch09s03.html
  title: CLI Commands
  accessed: "2026-09-02"
---

# What was read
The command reference.

# Relevant excerpt (verbatim)
* "Usage: dbset [db|bm] value. Sets the database (db) or benchmark (bm)."
* "Usage: diset dict key value. Set the dictionary variables for the current database."
* "Usage: buildschema. Runs the schema build for the database and benchmark selected with dbset and variables selected with diset."
* "Usage: vuset [vu|delay|repeat|iterations|showoutput|logtotemp|unique|nobuff|timestamps]".
* The exact non-interactive invocation (`hammerdbcli auto <script>`) is not shown on this page — **Inferred** from the launcher accepting arguments; verify in execution.

# What it was used to decide
[TPC-C implementations tool record](/tools/tpcc-implementations.md).
