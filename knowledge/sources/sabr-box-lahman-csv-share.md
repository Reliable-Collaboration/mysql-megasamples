---
type: Source
title: SABR Box share for the Lahman CSV version (probe)
description: The CSV download link is a Box shared folder "lahman_1871-2025_csv" (itemID 357532062389) listing individual CSV files; guessed direct .zip URLs return 404.
resource: https://sabr.box.com/s/y1prhc795jk8zvmelfd3jq7tl389y6cd
tags: [lahman, download, box]
status: stable
trust: verified
stale_after: "2027-01-15"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://sabr.box.com/s/y1prhc795jk8zvmelfd3jq7tl389y6cd
    title: Box share page (HTML, 57,742 bytes; final URL sabr.app.box.com/s/...)
    accessed: "2026-09-02"
---

# What was read
`curl -sL` of the share page with a browser user agent, grepped for item names; `curl -sIL` on `https://sabr.box.com/shared/static/<id>.zip` for the three share ids (all HTTP 404), accessed 2026-09-02.

# Relevant excerpt
The share page (HTTP 200) embeds `"itemID":357532062389`, a folder name `lahman_1871-2025_csv`, and entries `Batting.csv, BattingPost.csv, CollegePlaying.csv, Fielding.csv, FieldingPost.csv, HallOfFame.csv, HomeGames.csv, Managers.csv, ManagersHalf.csv, Parks.csv, People.csv, Pitching.csv, PitchingPost.csv, Salaries.csv, Schools.csv, SeriesPost.csv, Teams.csv, ...` (the listing is paginated in the HTML; not all 27 names appeared). No file sizes were extracted. No direct static download URL exists for the folder.

# What it was used to decide
[Box download question](/questions/lahman-box-direct-download.md); the recommendation to vendor the CSVs into the repository under CC BY-SA ([Lahman](/datasets/lahman.md)).
