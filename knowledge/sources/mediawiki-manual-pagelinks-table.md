---
type: Source
title: MediaWiki Manual:Pagelinks table
description: Confirms pl_target_id → linktarget and the removal of pl_namespace/pl_title in 1.43.
resource: https://www.mediawiki.org/wiki/Manual:Pagelinks_table
tags:
- source
- mediawiki
- schema
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://www.mediawiki.org/wiki/Manual:Pagelinks_table
  title: Manual:Pagelinks table
  accessed: "2026-09-02"
---

# What was read
The manual page on 2026-09-02.

# Relevant excerpt
pl_from int unsigned "The page_id of the page containing the link"; pl_from_namespace int "The page_namespace of the page containing the link"; pl_target_id bigint unsigned "Foreign key to linktarget" (added 1.41+); pl_namespace and pl_title removed in 1.43. Links are recorded whether or not the target page exists.

# What it was used to decide
Link resolution in [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md).
