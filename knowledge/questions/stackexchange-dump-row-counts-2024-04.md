---
type: Open Question
title: Row counts per XML file in dba.stackexchange.com.7z (2024-04-02 snapshot) and the small core site
description: Only live 2026 totals exist; the exact April 2024 counts must be measured once and pinned as the test baseline.
resource: /questions/stackexchange-dump-row-counts-2024-04.md
tags: [question, stackexchange, row-counts, text-group]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://api.stackexchange.com/2.3/info?site=dba
    accessed: 2026-09-02
  - resource: https://archive.org/metadata/stackexchange
    accessed: 2026-09-02
---

# Question
How many rows do Posts/Users/Comments/Votes/Badges/Tags/PostLinks/PostHistory have in the 2024-04 dba and beer dumps, what is the uncompressed size, and is `ContentLicense` present on every post row (it should be, but this snapshot predates the schema doc's latest edits)?

# Cheapest experiment
`curl -O https://archive.org/download/stackexchange/beer.stackexchange.com.7z && md5sum ... && 7z x ... && for f in *.xml; do echo $f $(grep -c '<row ' $f) $(stat -c %s $f); done; grep -c 'ContentLicense=' Posts.xml` (minutes for beer; ~15 minutes for dba). Record in [Stack Exchange dataset](/datasets/stackexchange.md).

# Resolves
Test baseline and the core/extended size estimates (compression ratio) in [Stack Exchange](/datasets/stackexchange.md).
