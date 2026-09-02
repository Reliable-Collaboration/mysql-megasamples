---
type: Source
title: lerocha/chinook-database release v1.4.5 (GitHub API)
description: Latest release (2024-02-12) with 16 assets including Chinook_MySql.sql (616,450 B) and Chinook_MySql_AutoIncrementPKs.sql (578,950 B); master is 23 commits ahead with tooling changes only.
resource: https://github.com/lerocha/chinook-database/releases/tag/v1.4.5
tags: [chinook, release, github-api]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://api.github.com/repos/lerocha/chinook-database/releases/latest
    title: releases/latest, /releases, /compare/v1.4.5...master, /contents/ChinookDatabase/DataSources
    accessed: 2026-09-02
---

# What was read
`gh api` on 2026-09-02.

# Relevant excerpt
* Latest release `v1.4.5`, published 2024-02-12T04:50:23Z; body: "feat: updating SQL scripts to insert multiple rows with a single insert statement (#45)". Release history v1.0.0 ... v1.4.5 all created 2024-01-22..2024-02-12.
* Assets (bytes): ChinookData.json 1,897,482; Chinook_Db2.sql 604,388; **Chinook_MySql.sql 616,450** (https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_MySql.sql); **Chinook_MySql_AutoIncrementPKs.sql 578,950**; Chinook_Oracle.sql 629,968; Chinook_PostgreSql.sql 600,200; Chinook_PostgreSql_AutoIncrementPKs.sql 578,730; Chinook_PostgreSql_SerialPKs.sql 562,563; Chinook_Sqlite.sql 611,447; Chinook_Sqlite.sqlite 1,067,008; Chinook_Sqlite_AutoIncrementPKs.sql/.sqlite; Chinook_SqlServer.sql 601,344; Chinook_SqlServerCompact.sqlce; Chinook_SqlServer_AutoIncrementPKs.sql 563,826.
* Repository: default branch master, pushed 2025-10-05; `compare/v1.4.5...master` = 23 commits ahead (dependabot, dotnet-t4 generation, .NET 9 upgrade reverted, Docker test infrastructure for Oracle/SQL Server/DB2, "Removing SQL Server Compact"). The in-repo `ChinookDatabase/DataSources/Chinook_MySql.sql` (600,574 B, LF) is byte-identical to the release asset after CR removal (`diff <(tr -d '\r' < release) master` = empty).
* No Chinook 2.x release exists on this repository.

# What it was used to decide
Artifact pin and size in [Chinook dataset](/datasets/chinook.md).
