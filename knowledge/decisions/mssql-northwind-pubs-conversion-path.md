---
type: Decision
title: Conversion path for Northwind and pubs - translate the T-SQL install scripts directly
description: Both datasets are single self-contained T-SQL scripts with inline data, so the build translates them to MySQL DDL/DML with a script (no SQL Server, no bcp).
resource: /decisions/mssql-northwind-pubs-conversion-path.md
tags:
- decision
- northwind
- pubs
- conversion-path
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/instnwnd.sql
  title: instnwnd.sql analysis
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/instpubs.sql
  title: instpubs.sql analysis
  accessed: "2026-09-02"
---

# Question
How do we turn `instnwnd.sql` (1 MB) and `instpubs.sql` (126 KB) into MySQL 9.7 databases reproducibly?

# Options considered
1. **Deterministic text translation of the scripts** (sed/Python: strip `GO`/`SET`/`if exists ... drop`, map types, backtick identifiers, rewrite date literals, keep `0x` hex literals, emit MySQL DDL + INSERTs; hand-port the 16+7 and 1+4 programmable objects into a checked-in `.sql`).
2. Restore into the [SQL Server container](/tools/mssql-server-container.md) and export with bcp - needless (no BULK INSERT/binary format involved) and amd64-only.
3. MySQL Workbench Migration Wizard / pgloader-style tools - GUI or foreign-DB dependent, not reproducible in CI for a script source.
4. Reuse a community "Northwind for MySQL" port - unknown provenance/licensing and known divergences; rejected as the primary source (may be used to cross-check row counts).

# Evidence
[instnwnd.sql source record](/sources/github-microsoft-sql-server-samples-instnwnd-sql.md): 3,308 single-row INSERTs, UTF-8, 13 tables, no BULK INSERT; [instpubs.sql source record](/sources/github-microsoft-sql-server-samples-instpubs-sql.md): 255 rows, ASCII, `sp_addtype` UDTs, one trigger, `LIKE '[0-9]...'` CHECKs. Dataset records: [Northwind](/datasets/northwind.md), [pubs](/datasets/pubs.md).

# Outcome
Option 1. Pin the two blobs by SHA (`ae61e5631d7f...`, `d887fd48cb06...`), commit the translated MySQL scripts plus the translator, and verify with the INSERT-derived row counts. Known deviations to document: dropped `CK_Birthdate` (non-deterministic), `LIKE` character classes rewritten to `REGEXP`, OLE-wrapped pictures kept as-is, `COMPUTE BY` procedures (if present in pubs `reptq*`) simplified.

# Status
accepted (executor may revisit if the translator proves brittle; coordinator owns tier/name choices).
