---
type: Source
title: MediaWiki Manual:Categorylinks table
description: Confirms cl_target_id → linktarget.lt_id (introduced 1.44) and the removal of cl_to in 1.45, matching the 20260901 dump.
resource: https://www.mediawiki.org/wiki/Manual:Categorylinks_table
tags: [source, mediawiki, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.mediawiki.org/wiki/Manual:Categorylinks_table
    title: Manual:Categorylinks table
    accessed: 2026-09-02
---

# What was read
The manual page on 2026-09-02.

# Relevant excerpt
cl_from int unsigned "Stores the page.page_id of the article where the link was placed."; cl_sortkey varbinary(230); cl_sortkey_prefix varbinary(255); cl_timestamp; cl_type enum('page','subcat','file'); cl_collation_id smallint unsigned "Foreign key to collation.collation_id"; **cl_target_id bigint unsigned "Foreign key to linktarget.lt_id giving the target of the category link."** — introduced in MediaWiki 1.44; cl_to and cl_collation removed in 1.45.

# What it was used to decide
Category name resolution (`JOIN linktarget ON lt_id = cl_target_id`, `lt_namespace = 14`) in [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md).
