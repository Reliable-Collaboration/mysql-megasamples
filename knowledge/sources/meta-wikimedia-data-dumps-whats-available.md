---
type: Source
title: meta.wikimedia.org "Data dumps/What's available for download"
description: Official description of the XML/stub/SQL dump files, confirming which tables ship as SQL and that pages-articles carries current revisions of non-talk pages.
resource: https://meta.wikimedia.org/wiki/Data_dumps/What%27s_available_for_download
tags:
- source
- wikipedia
- dumps
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://meta.wikimedia.org/wiki/Data_dumps/What%27s_available_for_download
  title: Data dumps/What's available for download
  accessed: "2026-09-02"
---

# What was read
The page on 2026-09-02 (WebFetch summary plus a curl grep for the exact lines).

# Relevant excerpt
* Page files pages-articles / pages-meta-current / pages-meta-history: "Page metadata, revision metadata, including complete page content."
* Stubs: "Page metadata and revision metadata, without page content." — "stub-articles: all subject pages (i.e. "articles", but not talk pages), current revisions only." "stub-meta-current: all pages, current revision only." "stub-meta-history: all pages, all revisions." (pages-articles is the content-bearing counterpart of stub-articles.)
* Abstracts: "Short excerpts of the current revision of each page in the main namespace (i.e. "articles", but not project pages or talk pages)."
* SQL tables listed (`<wikiname>-YYYYMMDD-<table>.sql.gz`): categorylinks, category, change_tag, externallinks, flaggedpages, flaggedrevs, geo_tags, image, imagelinks, iwlinks, langlinks, page, pagelinks, page_props, page_restrictions, protected_titles, redirect, sites, site_stats, templatelinks, user_groups, wbc_entity_usage. **No revision or text table in SQL form.**

# What it was used to decide
Scope of `pages-articles` (one current revision per page; subject pages excluding talk) in [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md).
