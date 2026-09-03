---
type: Source
title: dumps.wikimedia.org/wikidatawiki/latest/ SQL/XML listing (run 20260801, files dated 06-11 Aug 2026)
description: Sizes of the wikidatawiki MediaWiki-table dumps (page, page_props, pagelinks, ...) showing that even metadata-only tables are multi-gigabyte.
resource: https://dumps.wikimedia.org/wikidatawiki/latest/
tags:
- source
- wikidata
- size-evidence
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
stale_after: "2026-10-05"
sources:
- resource: https://dumps.wikimedia.org/wikidatawiki/latest/
  title: latest/ listing (grep of page*, md5sums, pages-articles-multistream*)
  accessed: "2026-09-02"
---

# What was read
A grep of the listing on 2026-09-02.

# Relevant excerpt (bytes)
wikidatawiki-latest-page.sql.gz **3,609,252,694** (06-Aug-2026); page_props.sql.gz 1,563,614,282; pagelinks.sql.gz 9,421,690,726; page_restrictions.sql.gz 472,294; md5sums.txt 55,722 (11-Aug); pages-articles-multistream is split into many numbered parts (first part index files 1.4-5.4 MB each; the first content part seen was 429,737,511 bytes).

# What it was used to decide
Rules out "wikidatawiki-latest-page.sql.gz as a small metadata dump" in [Wikidata dataset](/datasets/wikidata.md).
