---
type: Dataset
title: Iris (Fisher 1936)
description: The 150-row, 4-feature iris classification table; UCI distributes it under CC BY 4.0 (licensing flag), scikit-learn/R ship a corrected copy under BSD-3; ship the corrected data with dual attribution.
resource: https://archive.ics.uci.edu/dataset/53/iris
tags:
- tier-core
- csv
- iris
- smallsets
- cc-by-4-0
- licensing-flag
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:48:59Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://archive.ics.uci.edu/dataset/53/iris
  title: UCI Iris page
  accessed: "2026-09-02"
- resource: https://archive.ics.uci.edu/static/public/53/iris.zip
  title: iris.zip (measured)
  accessed: "2026-09-02"
  version: md5 7a07b2b4163b650dc451aca467d4fb58
- resource: https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/datasets/data/iris.csv
  title: scikit-learn iris.csv, iris.rst, COPYING
  accessed: "2026-09-02"
- resource: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html
  title: load_iris docs
  accessed: "2026-09-02"
---

# Identity
R. A. Fisher's 1936 iris measurements (Anderson's data): 50 samples each of Iris setosa, versicolor, virginica with sepal/petal length and width in cm ([UCI page](/sources/uci-iris-dataset-page.md)).

# Source artifact
* UCI: https://archive.ics.uci.edu/static/public/53/iris.zip - 3,738 bytes (md5 `7a07b2b4163b650dc451aca467d4fb58`), containing `iris.data` (historical, two wrong values; md5 `42615765a885ddf54427f12c34a0a070`), `bezdekIris.data` (corrected; md5 `7352471c39afdf2dad640df6dd867b72`), `iris.names` ([zip inspection](/sources/uci-iris-zip.md)). No auth. DOI 10.24432/C56C76.
* scikit-learn ([BSD-3-Clause](/licenses/bsd-3-clause.md)): https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/datasets/data/iris.csv - corrected data, md5 `d69a16ea6136ccb02a7c37c66375ebba`, BSD-3-Clause ([files](/sources/scikit-learn-iris-files.md)).
* Chosen: the corrected values (= `bezdekIris.data` = scikit-learn = R), vendored as a 150-row CSV in the repository.

# Native format and friendlier forms
Header-less CSV (`5.1,3.5,1.4,0.2,Iris-setosa`), trailing blank line in UCI's file; scikit-learn's variant has a metadata first line and numeric class codes.

# Shape
150 rows, columns sepal_length, sepal_width, petal_length, petal_width (DECIMAL(3,1) cm), species (setosa/versicolor/virginica, 50 each). Pure ASCII. Summary statistics (scikit-learn descr): sepal length min 4.3 max 7.9 mean 5.84; sepal width 2.0-4.4 mean 3.05; petal length 1.0-6.9 mean 3.76; petal width 0.1-2.5 mean 1.20.

# Conversion path
Build-time CSV-to-INSERT into explicit DDL; add `id INT` in file order so the known rows 35/38 stay addressable ([small-sets decision](/decisions/smallsets-database-layout.md)).

# Type-mapping hazards
* Keep `DECIMAL(3,1)` (not FLOAT) so `4.9` compares exactly.
* Class label normalisation: UCI uses `Iris-setosa`, scikit-learn `setosa`, R `setosa` - store `species VARCHAR(20)` as `setosa` etc. (document the mapping) or an ENUM.
* Trailing empty line in UCI's file must be ignored by the loader.

# Programmable objects
None.

# Indexing
PK `id`; index on `species`.

# Tests and expected values
`COUNT(*)` = 150; `COUNT(*) GROUP BY species` = 50/50/50; row 35 = (4.9, 3.1, 1.5, 0.2, setosa) and row 38 = (4.9, 3.6, 1.4, 0.1, setosa) (corrected values); `ROUND(AVG(sepal_length),2)` = 5.84, `MIN(petal_width)` = 0.1, `MAX(petal_length)` = 6.9; source-file md5 pinned.

# Tier assignment
core (under 5 KB). Evidence: [zip inspection](/sources/uci-iris-zip.md).

# License and attribution
FLAG: UCI's page states CC BY 4.0, not public domain ([CC BY 4.0 record](/licenses/cc-by-4-0.md)). Attribution to include regardless of route: "Fisher, R. A. (1936). The use of multiple measurements in taxonomic problems. Annals of Eugenics 7(2):179-188; dataset via UCI Machine Learning Repository, https://doi.org/10.24432/C56C76 (CC BY 4.0); values corrected per Fisher's paper as in R and scikit-learn (BSD-3-Clause, Copyright (c) 2007-2026 The scikit-learn developers)." Policy choice in [question](/questions/iris-uci-cc-by-vs-public-domain.md).

# Database name
`smallsets`, table `iris` (per the [naming convention](/decisions/database-naming-convention.md) and [small-sets decision](/decisions/smallsets-database-layout.md)).

# Open questions
* [License route](/questions/iris-uci-cc-by-vs-public-domain.md).
