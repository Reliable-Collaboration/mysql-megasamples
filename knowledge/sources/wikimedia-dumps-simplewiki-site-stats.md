---
type: Source
title: simplewiki-20260901-site_stats.sql.gz (complete file)
description: The one-row site_stats table from the 20260901 dump — authoritative page/article/edit/user counts for that exact snapshot.
resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-site_stats.sql.gz
tags: [source, wikipedia, row-counts]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-site_stats.sql.gz
    title: site_stats.sql.gz (862 bytes, md5 af0898a45c9e589153ac523030654fa3)
    accessed: 2026-09-02
    version: 20260901
---

# What was read
The whole file, decompressed, on 2026-09-02.

# Relevant excerpt
```sql
CREATE TABLE `site_stats` ( `ss_row_id` int(8) unsigned NOT NULL DEFAULT 0, `ss_total_edits` bigint(20) unsigned DEFAULT NULL, `ss_good_articles` bigint(20) unsigned DEFAULT NULL, `ss_total_pages` bigint(20) unsigned DEFAULT NULL, `ss_users` bigint(20) unsigned DEFAULT NULL, `ss_images` bigint(20) unsigned DEFAULT NULL, `ss_active_users` bigint(20) unsigned DEFAULT NULL, `ss_temp_users` bigint(20) unsigned DEFAULT NULL, `ss_active_temp_users` bigint(20) unsigned DEFAULT NULL, PRIMARY KEY (`ss_row_id`) ...
INSERT INTO `site_stats` VALUES (1,10957060,284761,947771,1840585,36,3219,NULL,NULL);
```
So at snapshot 20260901: total edits 10,957,060; good ("content") articles **284,761**; total pages **947,771**; users 1,840,585; images 36; active users 3,219.

# What it was used to decide
Expected row count of `page` (947,771) and the ns0 content-page count in [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md).
