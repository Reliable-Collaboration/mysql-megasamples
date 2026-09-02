---
type: Decision
title: Chinook conversion path - run the upstream MySQL script with a NVARCHAR-to-utf8mb4 rewrite
description: Use Chinook_MySql.sql v1.4.5 as-is except for replacing NVARCHAR with VARCHAR CHARACTER SET utf8mb4, an explicit utf8mb4 CREATE DATABASE, and (optionally) the lowercase database name.
resource: /decisions/chinook-conversion-path.md
tags: [chinook, decision, mysql-native]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:48:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_MySql.sql
    title: Chinook_MySql.sql v1.4.5
    accessed: "2026-09-02"
  - resource: https://dev.mysql.com/doc/refman/9.7/en/charset-national.html
    title: The National Character Set (9.7)
    accessed: "2026-09-02"
---

# Question
How to load Chinook into the 9.7 image without inheriting deprecated utf8mb3 columns.

# Options considered
1. Run `Chinook_MySql.sql` verbatim - works, but every `NVARCHAR` column becomes `utf8mb3` and the server emits deprecation warnings ([manual](/sources/mysql-refman-9-7-charset-national.md)).
2. `sed` rewrite at build time: `NVARCHAR(` -> `VARCHAR(` and add `CHARACTER SET utf8mb4` (or set `DEFAULT CHARSET=utf8mb4` on `CREATE DATABASE`), keep the `N'...'` literals (they are `_utf8mb3` introducers that convert losslessly into utf8mb4 columns - **Inferred**, verify with a round-trip test on `90’s Music`).
3. Use `Chinook_MySql_AutoIncrementPKs.sql` instead (AUTO_INCREMENT PKs) - changes upstream semantics; not chosen.
4. Convert from the SQLite asset or ChinookData.json with a tool - unnecessary.

# Evidence
[Script inspection](/sources/github-lerocha-chinook-mysql-script.md): CRLF UTF-8 without BOM, 11 tables, no routines, 15,607 rows, accented Latin text only (no supplementary-plane characters, so utf8mb3 would not truncate, but is deprecated).

# Outcome
Option 2, applied by a build script with an md5 pin on the release asset (`75acf33f91aebf8bf0d79f4458d43b79`). Database name: upstream creates `Chinook`; the project uses `chinook` and, following the [naming convention](/decisions/database-naming-convention.md), lower-cases all table and column identifiers (`album`, `invoiceline`, `albumid`) in the same build-time rewrite (identifiers are backticked in the upstream script, so a token-level replacement is safe). Record the rewrite as a documented deviation from upstream.

# Status
accepted
