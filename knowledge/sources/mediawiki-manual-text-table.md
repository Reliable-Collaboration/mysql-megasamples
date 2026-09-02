---
type: Source
title: MediaWiki Manual:Text table
description: The text table (old_id, old_text mediumblob, old_flags) and its flag semantics; basis for our utf8mb4 MEDIUMTEXT variant.
resource: https://www.mediawiki.org/wiki/Manual:Text_table
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
- resource: https://www.mediawiki.org/wiki/Manual:Text_table
  title: Manual:Text table
  accessed: "2026-09-02"
---

# What was read
The manual page on 2026-09-02.

# Relevant excerpt
old_id int unsigned PK (referenced by `content.content_address` as `tt:<id>` since 1.35); old_text mediumblob (wikitext or an external pointer `DB://cluster/id`); old_flags tinyblob, comma-separated: "gzip" ("Text is compressed with PHP's gzdeflate() function"), "utf-8", "external" ("Text was stored in an external location specified by old_text"), "object".

# What it was used to decide
Our `text` table stores plain utf8mb4 `MEDIUMTEXT` with `old_flags='utf-8'` and a FULLTEXT index — [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md).
