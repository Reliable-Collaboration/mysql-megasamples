---
type: License
title: Creative Commons Attribution 4.0 International (CC BY 4.0) - UCI Iris
description: Attribution-only license that UCI applies to its Iris distribution; requires creator credit, license notice and modification notice; no share-alike.
resource: https://creativecommons.org/licenses/by/4.0/legalcode
tags:
- license
- cc-by-4-0
- attribution
- iris
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://creativecommons.org/licenses/by/4.0/legalcode
  title: Attribution 4.0 International legal code
  accessed: "2026-09-02"
- resource: https://archive.ics.uci.edu/dataset/53/iris
  title: UCI Iris page license statement
  accessed: "2026-09-02"
---

# Where the text lives
https://creativecommons.org/licenses/by/4.0/legalcode ([source](/sources/creativecommons-by-4-0-legalcode.md)); UCI's statement: "This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license." ([UCI page](/sources/uci-iris-dataset-page.md)).

# Obligations (Section 3(a)(1))
Retain creator identification (R. A. Fisher; UCI as distributor), a link to the material (https://doi.org/10.24432/C56C76), a notice that it is CC BY 4.0 with the license URI, and "indicate if You modified the Licensed Material" (e.g. if the two erroneous rows are corrected). No share-alike.

# Licensing finding
Iris is a 1936 table of measurements; UCI's CC BY claim can only attach to UCI's compilation/packaging, not to the facts. Using the scikit-learn/R corrected copy (BSD-3-Clause for scikit-learn's files) avoids the CC BY obligation but not the courtesy citation of Fisher. See [question](/questions/iris-uci-cc-by-vs-public-domain.md).

# Attribution
Wording used for Iris: "Iris data set: Fisher, R. A. (1936), The use of multiple measurements in taxonomic problems, Annals of Eugenics 7(2):179–188. Distributed via the UCI Machine Learning Repository, https://doi.org/10.24432/C56C76, under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Two values corrected per Fisher's paper, as in R and scikit-learn (BSD-3-Clause)." Section 3(a)(1) requires the creator credit, the license notice and an indication of modifications; all three are present.

# Applied to
* [Iris](/datasets/iris.md) - only if the UCI files (`iris.data`/`bezdekIris.data`) are the shipped source.
