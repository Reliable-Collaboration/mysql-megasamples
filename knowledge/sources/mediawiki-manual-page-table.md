---
type: Source
title: MediaWiki Manual:Page table
description: Column-by-column documentation of the page table (matches the 20260901 dump DDL) and the underscore/varbinary title convention.
resource: https://www.mediawiki.org/wiki/Manual:Page_table
tags: [source, mediawiki, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.mediawiki.org/wiki/Manual:Page_table
    title: Manual:Page table
    accessed: 2026-09-02
---

# What was read
The manual page on 2026-09-02.

# Relevant excerpt
| column | type | meaning (quoted/paraphrased) |
|---|---|---|
| page_id | int(10) unsigned | "Uniquely identifying primary key" preserved across edits |
| page_namespace | int(11) | namespace number (0-99 core; 100+ custom) |
| page_title | varbinary(255) | "Sanitized page title, without the namespace" with "spaces replaced by underscores" |
| page_is_redirect | tinyint(3) unsigned | 1 if redirect |
| page_is_new | tinyint(3) unsigned | only one revision or recently restored |
| page_random | double unsigned | "Random decimal value, between 0 and 1, used for Special:Random" |
| page_touched | binary(14) | timestamp when re-rendering is needed |
| page_links_updated | binary(14) | last link-table refresh (1.23+) |
| page_latest | int(10) unsigned | "Foreign key to rev_id for the current revision" |
| page_len | int(10) unsigned | "Uncompressed length in bytes of the page's current source text" |
| page_content_model | varbinary(32) | content model (1.21+) |
| page_lang | varbinary(35) | "Page content language" (1.24+) |

# What it was used to decide
Keep the binary schema as-is and add utf8mb4 views — [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md).
