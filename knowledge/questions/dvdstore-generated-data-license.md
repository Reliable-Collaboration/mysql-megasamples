---
type: Open Question
title: What license covers the DS3 Small CSV data files (generator output)?
description: The DS3 kit is GPL-2.0-or-later, but the committed CSVs are the output of the generators; GPL section 0 says output is covered only if it is a "work based on the Program", and Dell never labelled the data separately.
resource: /questions/dvdstore-generated-data-license.md
tags: [dvdstore, license, gpl-2-0, data]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/gpl.txt
    title: gpl.txt section 0 and 2
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/prod/prod.csv
    title: prod.csv (titles/actors embedded from ds2_data.h word lists)
    accessed: "2026-09-02"
---

# Question
The Small CSVs (customers, orders, products, reviews, ...) were produced by GPL'd C programs from word lists compiled into the programs (`ds3/data_files/prod/ds2_data.h`, `reviews/ds_reviews_data.h`). Product titles ("ACADEMY ACADEMY", "PENELOPE GUINESS") and review texts are recombinations of those embedded lists, so the data arguably "contains ... a portion of" the Program. Treating the CSVs as GPL-2.0-or-later is the conservative answer; treating them as uncopyrightable random output is the permissive one.

# Cheapest experiment
No experiment resolves a legal question; the cheapest safe action is to (a) label the DS3 database as GPL-2.0-or-later in the image documentation (it is the same license the DDL already carries, so no extra burden) and (b) e-mail the maintainers (davejaffe7@gmail.com, tmuirhead@vmware.com per the readmes) asking for a statement on the data. Record the answer here.

# Related
[Dell DVD Store](/datasets/dell-dvd-store.md), [GPL-2.0 record](/licenses/gpl-2-0.md).

# Resolves
Records that depend on the answer:
* [dell-dvd-store.md](/datasets/dell-dvd-store.md)
* [gpl-2-0.md](/licenses/gpl-2-0.md)
* [github-dvdstore-ds3-gpl-and-source-headers.md](/sources/github-dvdstore-ds3-gpl-and-source-headers.md)
* PLAN.md §9 risk register (outside the bundle)
