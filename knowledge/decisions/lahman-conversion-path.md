---
type: Decision
title: Lahman conversion path - vendor SABR's 2025 CSV release, load with explicit DDL
description: Use the SABR Version 2025 CSV set (not the SQL Server .bak, not the Access .mdb, not GitHub mirrors), commit the files under CC BY-SA 3.0, strip BOMs, load with LOAD DATA / generated INSERTs into typed tables with composite keys.
resource: /decisions/lahman-conversion-path.md
tags:
- lahman
- decision
- csv
status: stable
trust: inferred
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://sabr.org/lahman-database/
  title: SABR Lahman page (formats)
  accessed: "2026-09-02"
- resource: https://sabr.app.box.com/public/static/qtgh1olzcaauz5x234wqx8huixizff8l.txt
  title: readme 2025
  accessed: "2026-09-02"
---

# Question
Which of SABR's three formats to use and how to bring it into MySQL.

# Options considered
1. CSV version (27 files) - plain text, needs our DDL; sizes unknown until downloaded.
2. MSSQL `lahman2025.bak` - would need a SQL Server container and a schema-conversion tool (covered by other groups' tool records) for a dataset that is natively flat files; rejected.
3. MS Access `.mdb` - needs mdbtools; rejected.
4. GitHub mirrors (chadwickbureau/baseballdatabank is gone; third-party mirrors unverified) - rejected as non-authoritative ([status](/sources/github-chadwickbureau-baseballdatabank-status.md)).

# Evidence
[SABR page](/sources/sabr-lahman-database-page.md), [readme](/sources/sabr-lahman-readme-2025.md), [Box probe](/sources/sabr-box-lahman-csv-share.md).

# Outcome
Option 1. Because there is no stable download URL, vendor the CSVs (with readme2025.txt and the CC BY-SA notice) in the repository after a one-time manual download; record sha256 per file. DDL: derive column types from the readme (ints for counting stats, `DECIMAL(5,3)` for FP/ERA-like ratios, `VARCHAR` codes, `DATE` for debut/finalGame), composite primary keys Batting/Pitching (playerID, yearID, stint), Fielding (playerID, yearID, stint, POS) - **Inferred** for Fielding, Teams (yearID, teamID), People (playerID) with unique bbrefID/retroID where present. Load empty strings as NULL for numeric columns. Trust is `inferred` until the files are measured.

# Amendment (2026-09-03, on building it)
The outcome said "vendor the CSVs in the repository" because there is no stable download URL. In
practice the same problem is solved without putting 42 MB into git: `manifest.yaml` gained a
`manual: true` flag for artifacts no build can fetch, and `scripts/fetch.py` verifies a
maintainer-placed file against its sha256 and size instead of downloading it, with a message naming
the URL and the exact path if it is missing. That keeps the repository small (a plan constraint),
still pins the exact bytes, and leaves R-02 to republish the set as a release asset under CC BY-SA
3.0. The flag also covers the other artifacts nothing can fetch, such as the citibike and divvy
downloads behind a licence gate.

# Status
accepted (pending size measurement)
