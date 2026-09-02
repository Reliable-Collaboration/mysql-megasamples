---
type: Decision
title: Contoso conversion path - published csv-100k archive in core, csv-1m/10m in extended, MySQL DDL derived from SQLBI's SQL Server scripts
description: Download SQLBI's ready-to-use CSV 7z (no generator run), map the Data-schema DDL to MySQL, load with LOAD DATA; the old Microsoft ContosoRetailDW .bak is not used.
resource: /decisions/contoso-conversion-path.md
tags:
- contoso
- decision
- csv
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://api.github.com/repos/sql-bi/Contoso-Data-Generator-V2-Data/releases
  title: ready-to-use-data assets
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/sql/CreateTablesCommon.sql
  title: SQL Server DDL
  accessed: "2026-09-02"
---

# Question
Which Contoso artifact to ship and how to convert it.

# Options considered
1. SQLBI ready-to-use CSV archives (MIT): csv-10k 5.4 MB, csv-100k 9.8 MB, csv-1m 48.9 MB, csv-10m 512 MB, csv-100m 4.46 GB.
2. Run the generator at build time (.NET 8, network for static files) - flexible but adds a runtime and a determinism question.
3. SQLBI's `bak-ContosoV2-*.7z` SQL Server backups - needs SQL Server; pointless when CSV exists.
4. Microsoft's legacy ContosoRetailDW `.bak` (2009 SQL Server BI sample) - different, older schema, Microsoft sample license; explicitly NOT used.

# Evidence
[data releases](/sources/github-sql-bi-contoso-v2-data-releases.md), [SQL DDL](/sources/github-sql-bi-contoso-v2-sql-scripts.md), [build parameters](/sources/github-sql-bi-contoso-v2-config-and-build-scripts.md).

# Outcome
Option 1: core = `csv-100k.7z` from release `ready-to-use-data` (2025-09-21; sha256 to be recorded at first download, GitHub release assets are immutable per tag but the tag was re-used for the 2025 refresh - pin the asset URL plus checksum). Extended = `csv-1m.7z` (48.9 MB) and optionally `csv-10m.7z`. DDL: translate `nvarchar(n)` -> `VARCHAR(n) CHARACTER SET utf8mb4`, `money` -> `DECIMAL(19,4)`, `float` -> `DOUBLE`, `bit` -> `BOOLEAN`, `date` -> `DATE`, `bigint` -> `BIGINT`; keep PKs/FKs/indexes; skip the dbo renaming views or port them as MySQL views. Unpack with `7z x`. Load both `sales` and `orders`/`orderrows` if the archive contains both (SalesOrders=BOTH in the build config).

# Status
accepted
