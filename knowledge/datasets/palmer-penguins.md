---
type: Dataset
title: Palmer Penguins
description: 344 penguins (Adelie, Chinstrap, Gentoo) measured 2007-2009 at Palmer Station, Antarctica; two CSVs (tidy 8 columns, raw 17 columns) from the palmerpenguins R package; CC0.
resource: https://github.com/allisonhorst/palmerpenguins
tags: [tier-core, csv, penguins, smallsets, cc0]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:48:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/README.md
    title: README and DESCRIPTION
    accessed: 2026-09-02
    version: package 0.1.1 (2022-08-12); main @ 8957207 (2024-09-19)
  - resource: https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/LICENSE.md
    title: LICENSE.md (CC0 1.0)
    accessed: 2026-09-02
  - resource: https://github.com/allisonhorst/palmerpenguins/tree/main/inst/extdata
    title: penguins.csv / penguins_raw.csv (measured)
    accessed: 2026-09-02
---

# Identity
Palmer Archipelago penguin size measurements collected by Dr. Kristen Gorman with the Palmer Station Long Term Ecological Research program, packaged by Allison Horst, Alison Hill and Kristen Gorman as the R package `palmerpenguins` (0.1.1) - the modern alternative to Iris ([README](/sources/github-allisonhorst-palmerpenguins-readme.md)).

# Source artifact
* https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv - 15,241 bytes, md5 `a06a0210251465a86fb970018292304d`, sha256 `f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93`.
* https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins_raw.csv - 53,098 bytes, md5 `049da101568e078f9845c8b366481810`.
* Commit `8957207b78d6ccd1b4654a9dd9c9041b657478ab`; no auth ([inspection](/sources/github-allisonhorst-palmerpenguins-extdata-csv.md)). Underlying EDI data packages: DOIs 10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f (Adelie), 10.6073/pasta/7fca67fb28d56ee2ffa3d9370ebda689 (Gentoo) and the Chinstrap package.

# Native format and friendlier forms
CSV with header; `NA` marks missing values. Nothing else needed.

# Shape
* `penguins`: 344 rows x 8 - species (Adelie/Chinstrap/Gentoo), island (Torgersen/Biscoe/Dream), bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex (male/female/NA), year (2007-2009). 11 rows contain NA.
* `penguins_raw`: 344 rows x 17 - studyName, Sample Number, Species (long form "Adelie Penguin (Pygoscelis adeliae)"), Region, Island, Stage, Individual ID, Clutch Completion, Date Egg, Culmen Length/Depth (mm), Flipper Length (mm), Body Mass (g), Sex (MALE/FEMALE/NA), Delta 15 N, Delta 13 C, Comments.
* Encoding: pure ASCII in both CSVs (the species name is "Adelie" without the accent that the README uses); no canary.

# Conversion path
Build-time CSV-to-INSERT into two tables `penguins` and `penguins_raw` ([small-sets decision](/decisions/smallsets-database-layout.md); CSV notes [tool note](/tools/smallcsv-load-data-infile.md)).

# Type-mapping hazards
* `NA` string must become NULL (LOAD DATA `NULLIF(@v,'NA')`); affects DECIMAL/INT and the `sex` column.
* Raw column names with spaces and parentheses -> snake_case (`culmen_length_mm`, `delta_15_n`); document the mapping.
* `Date Egg` -> DATE; `Sample Number` INT; isotopes DECIMAL(8,5); `Clutch Completion` Yes/No -> BOOLEAN or VARCHAR.
* No natural key in `penguins` - add `id` in file order; `penguins_raw` has `Individual ID` (not unique across years? - **Inferred**; use surrogate).
* `bill_length_mm DECIMAL(4,1)`, `body_mass_g SMALLINT`, `flipper_length_mm SMALLINT`, `year SMALLINT` (or YEAR).

# Programmable objects
None.

# Indexing
Surrogate PKs; index on (species, island).

# Tests and expected values
`COUNT(*)` = 344 in both tables; species counts Adelie 152 / Gentoo 124 / Chinstrap 68 (**Inferred** well-known values; verify); `COUNT(*) WHERE sex IS NULL` = 11 (**Inferred** from the 11 NA lines; a row may hold several NAs - verify); row 1 = Adelie, Torgersen, 39.1, 18.7, 181, 3750, male, 2007; file md5s pinned.

# Tier assignment
core (68 KB). Evidence: [inspection](/sources/github-allisonhorst-palmerpenguins-extdata-csv.md).

# License and attribution
[CC0 1.0](/licenses/cc0-1-0.md) - no obligation; include the requested citations: "Horst AM, Hill AP, Gorman KB (2020). palmerpenguins: Palmer Archipelago (Antarctica) penguin data. R package version 0.1.0. https://allisonhorst.github.io/palmerpenguins/. doi: 10.5281/zenodo.3960218." and "Gorman KB, Williams TD, Fraser WR (2014). Ecological sexual dimorphism and environmental variability within a community of Antarctic penguins (genus Pygoscelis). PLoS ONE 9(3):e90081. https://doi.org/10.1371/journal.pone.0090081".

# Database name
`smallsets`, tables `penguins` and `penguins_raw` (per the [naming convention](/decisions/database-naming-convention.md) and [small-sets decision](/decisions/smallsets-database-layout.md)).

# Open questions
None blocking.
