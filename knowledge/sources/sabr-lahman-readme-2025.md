---
type: Source
title: SABR Lahman Baseball Database 1871-2025 readme (readme2025.txt)
description: The release readme - copyright/CC BY-SA 3.0 notice, file list of the CSV version (27 tables), table descriptions and column definitions, revision history, Negro Leagues notes.
resource: https://sabr.app.box.com/public/static/qtgh1olzcaauz5x234wqx8huixizff8l.txt
tags: [lahman, readme, license, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://sabr.app.box.com/public/static/qtgh1olzcaauz5x234wqx8huixizff8l.txt
    title: readme (47,982 bytes; md5 56e80e2c9bd5e27a73891321bf04cc14; CRLF, no BOM)
    accessed: 2026-09-02
    version: "Release Date: Dec 10, 2025"
---

# What was read
The readme text fetched with curl (47,982 bytes), sections 0-2 read, accessed 2026-09-02.

# Relevant excerpt
* Header: "The SABR Lahman Baseball Database 1871-2025 / Release Date: Dec 10, 2025".
* 0.1 Copyright Notice & Limited Use License: "This database is copyright 1996-2025 by SABR, via generious donation from Sean Lahman. This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License. For details see: http://creativecommons.org/licenses/by-sa/3.0/ For licensing information or further information, contact Scott Bush at: sbush@sabr.org".
* 1.0 Release Contents: MS Access `lahman_1871-2025.mdb` + `readme2025.txt`; MSSQL `lahman2025.bak` + readme; Comma Delimited Version: readme.txt, AllStarFull.csv, Appearances.csv, AwardsManagers.csv, AwardsPlayers.csv, AwardsShareManagers.csv, AwardsSharePlayers.csv, Batting.csv, BattingPost.csv, CollegePlaying.csv, Fielding.csv, FieldingOF.csv, FieldingPost.csv, FieldingOFsplit, HallOfFame.csv, HomeGames.csv, Managers.csv, ManagersHalf.csv, Parks.csv, People.csv, Pitching.csv, PitchingPost.csv, readme2025.txt, Salaries.csv, Schools.csv, SeriesPost.csv, Teams.csv, TeamsFranchises.csv, TeamsHalf.csv.
* 1.1: covers 1871-2025, NA/AA/UA/PL/FL and the Negro leagues recognised by SABR; "This database was created by Sean Lahman".
* 1.5 Revision history includes "2024.01 July 2025 Corrected extended characters in Access People table" and "2024u Oct 2025 Added Negro League data".
* 2.0 Data Tables: "Each player is assigned a unique number (playerID) ... The playerIDs are linked to names and birthdates in the People table." Main tables People, Teams, TeamFranchises, Parks, Batting, Pitching, Fielding, FieldingOF, FieldingOFsplit, Appearances, Managers; supplementary AllStarFull, BattingPost, PitchingPost, FieldingPost, SeriesPost, HomeGames, ManagersHalf, TeamsHalf, AwardsManagers, AwardsPlayers, AwardsShareManagers, AwardsSharePlayers, HallofFame, CollegePlaying (last updated 2014), Salaries (last updated 2016), Schools (2014).
* PEOPLE TABLE columns: ID, playerID, birthYear, birthMonth, birthDay, birthCity, birthCountry, birthState, deathYear, deathMonth, deathDay, deathCountry, deathState, deathCity, nameFirst, nameLast, nameGiven, weight, height, bats, throws, debut, bbrefID, finalGame, retroID. BATTING TABLE: playerID, yearID, stint, teamID, lgID, G, AB, R, H, 2B, 3B, HR, RBI, SB, CS, BB, SO, IBB, HBP, SH, SF, GIDP. PITCHING TABLE starts playerID, yearID, stint, teamID, lgID ... TEAMS TABLE: yearID, lgID, teamID, franchID, divID, Rank, G, GHome, W, L, DivWin, WCWin, LgWin, WSWin, R, AB, H, 2B, 3B, HR, BB, SO, SB, CS, HBP, SF, RA, ER, ERA, CG, SHO, SV, IPOuts, HA, HRA, BBA, SOA, E, DP, FP, name, park, attendance, BPF, PPF (and more).
* 2.1 Notes on Negro League data: Seamheads data added per SABR's 2021 and 2024 recommendations.

# What it was used to decide
License, attribution, table inventory and keys in [Lahman](/datasets/lahman.md); [CC BY-SA 3.0](/licenses/cc-by-sa-3-0.md).
