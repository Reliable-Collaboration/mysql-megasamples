---
type: Open Question
title: Is the hbiostat.org permission statement sufficient for redistributing titanic3 in a public image, or should a CC0/PD-labelled copy be preferred?
description: hbiostat grants blanket permission with an acknowledgement request but names no license; Kaggle's copy needs login and terms; the R `titanic` CRAN package and OpenML copies were not read in this session.
resource: /questions/titanic-hbiostat-license-status.md
tags:
- titanic
- license
- open
status: draft
trust: open
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://hbiostat.org/data/
  title: permission statement
  accessed: "2026-09-02"
---

# Question
The permission ("Permission is granted to anyone wishing to use the data sets provided here") plainly allows use and, by reasonable reading, redistribution with the acknowledgement; but it is not CC0 and the brief asked for a public-domain/CC0 source. The passenger list itself is a compilation of historical facts (Encyclopedia Titanica, Eaton & Haas 1994) with thin copyright.

# Cheapest experiment
1. E-mail Frank Harrell (address on the page) asking whether the hbiostat datasets may be labelled CC0 or CC BY 4.0 for redistribution; record the reply.
2. Meanwhile ship titanic3 with the hbiostat acknowledgement and the original-source references, which satisfies the stated request. Alternatives to evaluate if a formal license is required: OpenML dataset 40945 "titanic" (same 1309-row data, OpenML labels most datasets Public/CC-BY - **not verified**), CRAN package `titanic` (Kaggle-derived 891+418 rows; license not verified).

# Related
[Titanic](/datasets/titanic.md), [permission record](/licenses/hbiostat-data-permission.md).

# Resolves
Records that depend on the answer:
* [titanic.md](/datasets/titanic.md)
* [hbiostat-data-permission.md](/licenses/hbiostat-data-permission.md)
