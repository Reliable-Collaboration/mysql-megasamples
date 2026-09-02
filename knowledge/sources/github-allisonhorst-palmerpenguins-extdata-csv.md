---
type: Source
title: palmerpenguins inst/extdata/penguins.csv and penguins_raw.csv - inspection
description: penguins.csv 15,241 B / 344 rows / 8 columns; penguins_raw.csv 53,098 B / 344 rows / 17 columns; ASCII, "NA" tokens for missing values.
resource: https://github.com/allisonhorst/palmerpenguins/tree/main/inst/extdata
tags: [penguins, csv, measurement]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv
    title: penguins.csv (md5 a06a0210251465a86fb970018292304d; sha256 f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins_raw.csv
    title: penguins_raw.csv (md5 049da101568e078f9845c8b366481810)
    accessed: "2026-09-02"
---

# What was read
Both files fetched and measured, accessed 2026-09-02 (commit 8957207).

# Relevant excerpt (measurements)
* penguins.csv: 15,241 bytes, 345 lines (header + 344), 0 non-ASCII, LF. Header `species,island,bill_length_mm,bill_depth_mm,flipper_length_mm,body_mass_g,sex,year`; row `Adelie,Torgersen,39.1,18.7,181,3750,male,2007`; 11 lines contain `NA` (missing measurements/sex).
* penguins_raw.csv: 53,098 bytes, 344 rows, 0 non-ASCII. Header `studyName,Sample Number,Species,Region,Island,Stage,Individual ID,Clutch Completion,Date Egg,Culmen Length (mm),Culmen Depth (mm),Flipper Length (mm),Body Mass (g),Sex,Delta 15 N (o/oo),Delta 13 C (o/oo),Comments`; row `PAL0708,1,Adelie Penguin (Pygoscelis adeliae),Anvers,Torgersen,"Adult, 1 Egg Stage",N1A1,Yes,2007-11-11,39.1,18.7,181,3750,MALE,NA,NA,Not enough blood for isotopes.` - quoted fields with commas, column names with spaces/parentheses, `NA` tokens.
* Species is spelled `Adelie` in the CSVs (the README/DESCRIPTION write "Adélie").

# What it was used to decide
Shape, hazards and tests in [Palmer Penguins](/datasets/palmer-penguins.md).
