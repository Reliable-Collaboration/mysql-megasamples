---
type: Dataset
title: Lahman Baseball Database (SABR, Version 2025)
description: Sean Lahman's historical MLB statistics 1871-2025, now published by SABR as 27 CSV tables (plus Access and SQL Server forms) under CC BY-SA 3.0; sizes and encoding still to be measured because the download is a Box share.
resource: https://sabr.org/lahman-database/
tags: [tier-core, csv, lahman, baseball, cc-by-sa-3-0]
status: stable
trust: inferred
stale_after: "2027-01-15"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:48:59Z" }
sources:
  - resource: https://sabr.org/lahman-database/
    title: SABR Lahman Baseball Database page
    accessed: "2026-09-02"
    version: Version 2025 (released 2026-01-02; BOM update 2026-02-18)
  - resource: https://sabr.app.box.com/public/static/qtgh1olzcaauz5x234wqx8huixizff8l.txt
    title: readme2025.txt
    accessed: "2026-09-02"
    version: "Release Date: Dec 10, 2025"
  - resource: https://sabr.box.com/s/y1prhc795jk8zvmelfd3jq7tl389y6cd
    title: Box share for the CSV version (probe only)
    accessed: "2026-09-02"
  - resource: https://api.github.com/repos/chadwickbureau/baseballdatabank
    title: former GitHub mirror (404)
    accessed: "2026-09-02"
---

# Identity
The Lahman Baseball Database: batting, pitching, fielding, team, manager, award, Hall of Fame, salary and biographical tables for Major League Baseball 1871-2025 (including SABR-recognised Negro Leagues, Seamheads data added Oct 2025). Created by Sean Lahman (first release 1995); since the 2024/2025 releases published by SABR ("copyright 1996-2025 by SABR, via generious donation from Sean Lahman") ([readme](/sources/sabr-lahman-readme-2025.md)). The Chadwick Bureau's "Baseball Databank" GitHub repository, historically the sibling/mirror, is no longer reachable ([status](/sources/github-chadwickbureau-baseballdatabank-status.md)); SABR's release is authoritative.

# Source artifact
* Page https://sabr.org/lahman-database/ ; Version 2025 released 2026-01-02, "byte order markers updated February 18, 2026" ([page](/sources/sabr-lahman-database-page.md)).
* Formats: CSV (Box folder https://sabr.box.com/s/y1prhc795jk8zvmelfd3jq7tl389y6cd, folder `lahman_1871-2025_csv`), MS Access `lahman_1871-2025.mdb`, SQL Server `lahman2025.bak`; documentation readme (47,982 bytes, md5 `56e80e2c9bd5e27a73891321bf04cc14`). No login, but the CSV folder has no static URL (guessed `shared/static/<id>.zip` -> 404) ([probe](/sources/sabr-box-lahman-csv-share.md)). **Inferred:** total CSV size in the tens of MB (People.csv alone lists 20,000+ players; Batting.csv 110,000+ rows in earlier releases) - measure.
* No published checksums.

# Native format and friendlier forms
CSV with header rows is the native "friendly" form; the .bak/.mdb are conveniences. No product needed.

# Shape
27 tables ([readme section 1.0/2.0](/sources/sabr-lahman-readme-2025.md)): main - People, Teams, TeamsFranchises, Parks, Batting, Pitching, Fielding, FieldingOF, FieldingOFsplit, Appearances, Managers; supplementary - AllStarFull, BattingPost, PitchingPost, FieldingPost, SeriesPost, HomeGames, ManagersHalf, TeamsHalf, AwardsManagers, AwardsPlayers, AwardsShareManagers, AwardsSharePlayers, HallOfFame, CollegePlaying (frozen 2014), Salaries (frozen 2016), Schools (2014). Row counts: not published - executor derives `wc -l` minus header per file at vendoring time and records them here.
* Keys: `playerID` (People) links everything; Batting/Pitching rows are (playerID, yearID, stint); Teams rows are (yearID, teamID) with lgID/franchID; People also carries `ID` (numeric, "not used anywhere else"), `bbrefID`, `retroID`.
* Encoding: **Inferred** UTF-8 with BOM (SABR explicitly updated "byte order markers" in Feb 2026; revision 2024.01 "Corrected extended characters in Access People table" implies accented names such as in birthCity/nameGiven). Verify with `head -c 3` and a non-ASCII grep on People.csv; BOM must be stripped or the first header column becomes `﻿playerID`.

# Conversion path
Vendor the CSVs, strip BOMs, load into explicit DDL ([decision](/decisions/lahman-conversion-path.md)); CSV handling notes in [tool note](/tools/smallcsv-load-data-infile.md).

# Type-mapping hazards
* Column names starting with digits (`2B`, `3B`) need backticks; `Rank` and `name` are fine. Tables and columns are lower-cased per the [naming convention](/decisions/database-naming-convention.md) (`people`, `batting`, `playerid`, `yearid`).
* Many empty cells for early years (e.g. SO, CS, IBB, HBP, SF, GIDP not recorded) -> NULL, not 0; use `NULLIF(@col,'')` in LOAD DATA.
* `debut`/`finalGame` dates; `ERA`, `FP`, `BPF/PPF` decimals; `DivWin/WCWin/LgWin/WSWin` are Y/N.
* `stint` composite keys; Fielding has `POS`; HallOfFame has `yearid, votedBy` keys (**Inferred**).
* Negro League rows may have leagues/teams that do not join to Teams for all years (readme 2.1 warns datasets differ) - keep FKs off or non-enforced for Batting->Teams.

# Programmable objects
None upstream (flat files). Views could be added later (e.g. career batting totals) - not planned.

# Indexing
PK/unique per table as listed; secondary indexes on (yearID, teamID) for Batting/Pitching/Fielding and on People(nameLast, nameFirst).

# Tests and expected values
Derive at vendoring: per-file row counts and sha256; `SELECT COUNT(DISTINCT playerid) FROM people`; a known player e.g. `SELECT namefirst, namelast FROM people WHERE playerid='ruthba01'` = Babe Ruth (**Inferred** id, well-known convention - verify); presence of Negro League lgID values (e.g. 'NNL', 'NAL' - **Inferred**) in Teams.

# Tier assignment
core candidate if the loaded size is under ~50 MB (expected; measure), otherwise extended. Evidence pending ([question](/questions/lahman-box-direct-download.md)).

# License and attribution
[CC BY-SA 3.0](/licenses/cc-by-sa-3-0.md). Required notice (verbatim): "This database is copyright 1996-2025 by SABR, via generious donation from Sean Lahman. This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License. For details see: http://creativecommons.org/licenses/by-sa/3.0/". Share-alike applies to the MySQL conversion. Note the Negro Leagues data is "licensed from Seamheads.com" - included in SABR's release under the same notice; keep the readme's section 2.1 text with the data.

# Database name
`lahman`.

# Open questions
* [Non-interactive download / vendoring and sizes](/questions/lahman-box-direct-download.md).
* Actual encoding/BOM state of the 2025 CSVs (verify on download).
* Whether SABR publishes the MySQL-compatible SQL (the "SQL version" is a SQL Server .bak per the readme) - confirm by opening that share.
