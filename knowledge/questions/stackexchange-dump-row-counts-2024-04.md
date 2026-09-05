---
type: Open Question
title: Row counts per XML file in dba.stackexchange.com.7z (2024-04-02 snapshot) and the small core site
description: Only live 2026 totals exist; the exact April 2024 counts must be measured once and pinned as the test baseline.
resource: /questions/stackexchange-dump-row-counts-2024-04.md
tags:
- question
- stackexchange
- row-counts
- text-group
status: deprecated
trust: verified
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-04T00:00:00Z"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://api.stackexchange.com/2.3/info?site=dba
  accessed: "2026-09-02"
- resource: https://archive.org/metadata/stackexchange
  accessed: "2026-09-02"
---

# Question
How many rows do Posts/Users/Comments/Votes/Badges/Tags/PostLinks/PostHistory have in the 2024-04 dba and beer dumps, what is the uncompressed size, and is `ContentLicense` present on every post row (it should be, but this snapshot predates the schema doc's latest edits)?

# Cheapest experiment
`curl -O https://archive.org/download/stackexchange/beer.stackexchange.com.7z && md5sum ... && 7z x ... && for f in *.xml; do echo $f $(grep -c '<row ' $f) $(stat -c %s $f); done; grep -c 'ContentLicense=' Posts.xml` (minutes for beer; ~15 minutes for dba). Record in [Stack Exchange dataset](/datasets/stackexchange.md).

# Resolves
Test baseline and the core/extended size estimates (compression ratio) in [Stack Exchange](/datasets/stackexchange.md).

# Answer (2026-09-04, tasks M-06 and X-05)

**Counted, and pinned.** Both dumps were loaded and every table's count recorded in
`datasets/stackexchange_*/tests/expected_counts.yaml`, which the S3 test asserts on every build.

`dba.stackexchange.com` (2024-04-02): posts 243,410 · comments 347,838 · users 248,141 ·
votes 911,783 · badges 429,421 · posthistory 833,657 · postlinks 20,194 · tags 1,242 ·
posttypes 15 · votetypes 14 · linktypes 2 — **3,035,686 rows over 1,751.7 MB loaded**.

`beer.stackexchange.com` (same snapshot): posts 3,924 · comments 4,007 · users 10,168 ·
badges 12,901 · posthistory 10,423 · postlinks 152 · tags 152 · posttypes 15 · linktypes 2.

These numbers are fixed for good rather than merely current: the project reads the archive.org
snapshot, whose upstream md5 matches what the record pins, so unlike the live site they cannot move.
The per-row `contentlicense` column is populated for every post, which is what the CC BY-SA
attribution requires.
