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

# Implementation (2026-09-02, S-03)
`megasamples/sources/tsql.py` is the shared translator; both datasets use it. Constructs it handles, each found by a real load failure rather than by reading the script:

| Construct | Handling |
|---|---|
| `GO` batches, many statements per batch with no separator | split into batches, then into statements; a routine body is never split |
| `"Quoted"` and `[Bracketed]` identifiers, `dbo.` prefixes | mapped to lower-case backticked names, spaces to underscores |
| Types written as `"int"`, `nvarchar`, `ntext`, `image`, `money` | mapped; **`tinyint` becomes `TINYINT UNSIGNED`** because SQL Server's is 0–255 while MySQL's is signed and silently rejects values above 127 |
| `IDENTITY(1,1)`, `PRIMARY KEY CLUSTERED`, `ON [PRIMARY]` | `AUTO_INCREMENT`, plain key, filegroup dropped |
| `CONSTRAINT name DEFAULT (0)` and named column-level PK | MySQL supports neither; the name is stripped |
| inline `REFERENCES t(c)` | hoisted to table-level `FOREIGN KEY`, because MySQL parses and ignores the inline form |
| `INSERT t VALUES(...)` omitting an identity column | an explicit column list is generated |
| `LIKE '[0-9][0-9]...'` | rewritten to `REGEXP`, since MySQL's LIKE has no character classes and would match nothing |
| `$20.00` money literals, `'MM/DD/YYYY'` and two-digit-year dates | stripped/converted outside string data, with SQL Server's 2049 century pivot |
| `getdate()`, `isnull()`, `len()`, `CONVERT(type, expr)` | mapped, with CONVERT's argument order reversed and balanced-paren parsing |
| `sp_addtype` user-defined types | expanded to their base type |
| `--comment` with no space | MySQL requires whitespace after `--`; normalised |
| `UPDATE STATISTICS`, `DBCC`, `RAISERROR`, `PRINT` | skipped; the pipeline runs its own `ANALYZE TABLE` |

Every transformation runs on a scanner that tracks string literals, so none can reach into data. The one deliberate exception is the date rewrite, which is anchored to a whole quoted value in exactly `MM/DD/YYYY` shape.

# Status
accepted (executor may revisit if the translator proves brittle; coordinator owns tier/name choices).
