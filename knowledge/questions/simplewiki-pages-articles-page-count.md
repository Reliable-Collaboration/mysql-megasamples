---
type: Open Question
title: How many <page> elements are in simplewiki-20260901-pages-articles.xml.bz2 and which namespaces?
description: site_stats gives 947,771 pages in the page table and 284,761 content articles, but the pages-articles file (subject pages, no talk) has an unpublished count that sets the revision/text row baseline.
resource: /questions/simplewiki-pages-articles-page-count.md
tags: [question, wikipedia, row-counts, text-group]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-site_stats.sql.gz
    accessed: 2026-09-02
  - resource: https://meta.wikimedia.org/wiki/Data_dumps/What%27s_available_for_download
    accessed: 2026-09-02
---

# Question
Expected somewhere between 284,761 (ns0) and ~600k; which namespaces are included (does it include User: pages? Category:? Template:?) and does every included page_id exist in page.sql.gz?

# Cheapest experiment
Without a full download: `curl .../simplewiki-20260901-stub-articles.xml.gz | zcat | grep -c '<page>'` (64 MB) and `... | grep -oP '<ns>\K[0-9]+' | sort | uniq -c` — stubs have the same page set as pages-articles. Record in [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md) `# Tests and expected values`.

# Resolves
Row baseline for `revision`/`text` and the namespace filter for the core sample.
