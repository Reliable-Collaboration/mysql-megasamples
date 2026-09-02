---
type: Source
title: scikit-learn iris copy (sklearn/datasets/data/iris.csv, descr/iris.rst, COPYING) and load_iris docs
description: scikit-learn ships a corrected Iris (same as R, not as UCI) under BSD-3-Clause; 150 rows with numeric class codes 0/1/2.
resource: https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/datasets/data/iris.csv
tags: [iris, scikit-learn, bsd-3-clause, alternative-source]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/datasets/data/iris.csv
    title: iris.csv (md5 d69a16ea6136ccb02a7c37c66375ebba)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/datasets/descr/iris.rst
    title: descr/iris.rst
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/COPYING
    title: COPYING (BSD 3-Clause License, Copyright (c) 2007-2026 The scikit-learn developers)
    accessed: 2026-09-02
  - resource: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html
    title: sklearn.datasets.load_iris documentation
    accessed: 2026-09-02
---

# What was read
The three repository files and the API doc page, accessed 2026-09-02.

# Relevant excerpt
* iris.csv: first line `150,4,setosa,versicolor,virginica` (count, n_features, target names), then 150 rows `5.1,3.5,1.4,0.2,0`; rows 35 and 38 are `4.9,3.1,1.5,0.2,0` and `4.9,3.6,1.4,0.1,0` (corrected).
* iris.rst: "The famous Iris database, first used by Sir R.A. Fisher. The dataset is taken from Fisher's paper. Note that it's the same as in R, but not as in the UCI Machine Learning Repository, which has two wrong data points."; summary statistics (sepal length min 4.3 max 7.9 mean 5.84 SD 0.83; sepal width 2.0/4.4/3.05/0.43; petal length 1.0/6.9/3.76/1.76; petal width 0.1/2.5/1.20/0.76); reference Fisher, R.A. "The use of multiple measurements in taxonomic problems", Annual Eugenics 7 Part II 179-188 (1936).
* load_iris docs: "Changed in version 0.20: Fixed two wrong data points according to Fisher's paper. The new version is the same as in R, but not as in the UCI Machine Learning Repository."
* COPYING: "BSD 3-Clause License, Copyright (c) 2007-2026 The scikit-learn developers."

# What it was used to decide
Alternative BSD-licensed source and the summary-statistics tests in [Iris](/datasets/iris.md).
