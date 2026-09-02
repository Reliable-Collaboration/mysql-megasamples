---
type: Open Question
title: Iris licensing - accept UCI's CC BY 4.0 with attribution, or ship the scikit-learn/R corrected copy (BSD-3) as facts?
description: UCI labels Iris CC BY 4.0 (not public domain as commonly assumed); the same 150 measurements are shipped by scikit-learn under BSD-3-Clause and by R's datasets package; the data are 1936 facts.
resource: /questions/iris-uci-cc-by-vs-public-domain.md
tags:
- iris
- license
- open
- flag
status: draft
trust: open
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://archive.ics.uci.edu/dataset/53/iris
  title: UCI Iris page (CC BY 4.0 statement)
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/COPYING
  title: scikit-learn COPYING (BSD-3-Clause)
  accessed: "2026-09-02"
---

# Question
FLAG: the brief assumed Iris is public domain; UCI's current page says CC BY 4.0. Both routes are cheap to comply with, but they differ: (a) UCI route = attribution block naming Fisher + UCI + DOI + CC BY 4.0 URI + modification note; (b) scikit-learn route = BSD-3 notice ("Copyright (c) 2007-2026 The scikit-learn developers") for the file, Fisher citation as courtesy. Which one the project standardises on is a policy decision.

# Cheapest experiment
None needed technically. Policy: pick (b) - ship the corrected 150 rows from scikit-learn's `iris.csv` (md5 `d69a16ea6136ccb02a7c37c66375ebba`) with the BSD notice and the Fisher/UCI citation (the citation also satisfies (a) in practice, so include the CC BY URI as well to be safe). Record the choice in [Iris](/datasets/iris.md) and the small-sets decision.

# Related
[Iris](/datasets/iris.md), [CC BY 4.0](/licenses/cc-by-4-0.md).

# Resolves
Records that depend on the answer:
* [iris.md](/datasets/iris.md)
* [cc-by-4-0.md](/licenses/cc-by-4-0.md)
* [uci-iris-dataset-page.md](/sources/uci-iris-dataset-page.md)
* PLAN.md §9 risk register (outside the bundle)
