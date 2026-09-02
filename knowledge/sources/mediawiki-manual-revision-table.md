---
type: Source
title: MediaWiki Manual:Revision table
description: Revision table columns (≥1.43) used to design the revision table we synthesize from the XML dump.
resource: https://www.mediawiki.org/wiki/Manual:Revision_table
tags: [source, mediawiki, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.mediawiki.org/wiki/Manual:Revision_table
    title: Manual:Revision table
    accessed: "2026-09-02"
---

# What was read
The manual page on 2026-09-02.

# Relevant excerpt
rev_id bigint(20) unsigned PK; rev_page int(10) unsigned → page; rev_comment_id bigint unsigned → comment; rev_actor bigint unsigned → actor; rev_timestamp binary(14) "MW_TS" e.g. `20080326231614`; rev_minor_edit tinyint unsigned; rev_deleted tinyint unsigned (RevisionDelete bitfield); rev_len int unsigned (bytes); rev_parent_id bigint unsigned; rev_sha1 varbinary(32) — "SHA-1 text content hash in base-36" (`Wikimedia\base_convert()`); for multi-slot revisions "a nested hash of hashes of content_sha1 across all slots".

# What it was used to decide
Column names/types of the synthesized `revision` table (denormalising actor and comment) in [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md).
