---
type: Dataset
title: Simple English Wikipedia (simplewiki dump 20260901)
description: Current-revision article text plus MediaWiki link tables of the Simple English Wikipedia, loaded as page/revision/text/categorylinks/pagelinks/linktarget/redirect/category with FULLTEXT on wikitext.
resource: https://dumps.wikimedia.org/simplewiki/20260901/
tags: [tier-core, tier-extended, dataset, text-corpus, wiki, cc-by-sa, gfdl, mysql-native-dumps, text-group]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
stale_after: "2026-12-01"
sources:
  - resource: https://dumps.wikimedia.org/simplewiki/latest/
    title: latest/ listing (20260901)
    accessed: "2026-09-02"
  - resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-sha1sums.txt
    title: sha1sums / md5sums
    accessed: "2026-09-02"
  - resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-page.sql.gz
    title: DDL headers of page/categorylinks/pagelinks/linktarget/redirect/category/page_props
    accessed: "2026-09-02"
  - resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-site_stats.sql.gz
    title: site_stats (complete)
    accessed: "2026-09-02"
  - resource: https://meta.wikimedia.org/wiki/Data_dumps/What%27s_available_for_download
    title: What's available for download
    accessed: "2026-09-02"
  - resource: https://www.mediawiki.org/xml/export-0.11.xsd
    title: export schema 0.11
    accessed: "2026-09-02"
  - resource: https://www.mediawiki.org/wiki/Manual:Page_table
    title: Manual:Page table
    accessed: "2026-09-02"
  - resource: https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use
    title: Terms of Use §7
    accessed: "2026-09-02"
  - resource: https://dumps.wikimedia.org/legal.html
    title: dumps legal notice
    accessed: "2026-09-02"
  - resource: https://simple.wikipedia.org/wiki/Special:Statistics
    title: Special:Statistics
    accessed: "2026-09-02"
---

# Identity
Simple English Wikipedia (`simplewiki`), dump run **20260901** (the `latest/` symlinks point to it; dated directories are kept for a few months — the index showed 20260101..20260901 on 2026-09-02, so pin the dated URL and re-pin quarterly). Proposed MySQL database name: **`wikipedia_simple`**.

# Source artifact
Base URL `https://dumps.wikimedia.org/simplewiki/20260901/simplewiki-20260901-<file>` ([listing](/sources/wikimedia-dumps-simplewiki-latest-listing.md), [checksums](/sources/wikimedia-dumps-simplewiki-checksums.md)); no auth, no click-through.
| file | bytes | md5 | sha1 |
|---|---|---|---|
| pages-articles.xml.bz2 | 356,186,307 | 066f0b2e8d6cf5504abf26b8b86027bb | 1bdd97642b5f511def336cce8afd34996db52d49 |
| page.sql.gz | 33,064,269 | f48dc42e43e50c5e31a5641118de2a6d | c2b88ecbc7e0e440cf541e54f5cf53c1129b9468 |
| categorylinks.sql.gz | 28,305,762 | 49218fc0877e3568eabbd0d5c62252e8 | 3139fe67ba6105ba0829b321bf80f552b4f26466 |
| pagelinks.sql.gz | 82,424,067 | 2e07c9e1b90e16c3cf00a814b55ec448 | b900518ce197c72f01cdf2f38f8e2514d8e7c6af |
| linktarget.sql.gz | 37,519,370 | ee227cfc6d3e28a004080eb86ea56fe4 | 3b84a923cb157f4d4cbcc538516aa866b53d27f0 |
| redirect.sql.gz | 1,463,928 | 7cd7c35b7aaa6f8f861e42b29de5f8f3 | 46fabd49fc5a18c0ce2e2338743b596806279b92 |
| category.sql.gz | 1,199,048 | 073743f17b4d7391e98d34070b873be2 | c57b1f2b8d32e0a5ad1bf90ded1f0a87f7825dc5 |
| site_stats.sql.gz | 862 | af0898a45c9e589153ac523030654fa3 | (in sha1sums) |
Not carried: pages-meta-current (483 MB, adds talk/user pages), pages-meta-history (4.3 GB), templatelinks, imagelinks, externallinks (56 MB), langlinks (122 MB), iwlinks, change_tag*, geo_tags, page_props (10.7 MB — optional), page_restrictions, protected_titles, sites, user_groups, babel, wbc_entity_usage (9.9 MB — useful only for a Wikidata subset, see [Wikidata](/datasets/wikidata.md)).

# Native format and friendlier forms
* `pages-articles.xml.bz2`: MediaWiki export XML 0.11 ([XSD](/sources/mediawiki-xml-export-0-11-xsd.md)); **one (current) revision per page**, covering subject pages (articles, templates, categories, project pages) but **not talk pages** ("stub-articles: all subject pages (i.e. "articles", but not talk pages), current revisions only" — [What's available](/sources/meta-wikimedia-data-dumps-whats-available.md)). Full-history dumps are not used.
* `*.sql.gz`: **already MySQL-dialect dumps** produced by MariaDB 10.11 `mysqldump` — each contains `DROP TABLE`, `CREATE TABLE`, and multi-row `INSERT`s ([DDL headers](/sources/wikimedia-dumps-simplewiki-sql-table-headers.md)). The `revision`, `text`, `slots`, `content`, `actor`, `comment`, `user` tables are **not** published as SQL — page text and revision metadata come only from the XML.

# Shape
* Counts at 20260901 from [site_stats](/sources/wikimedia-dumps-simplewiki-site-stats.md): `page` = **947,771** rows (all namespaces); content ("good") articles **284,761**; edits 10,957,060; users 1,840,585; images 36. Live Special:Statistics a day later: 284,784 / 947,842 ([source](/sources/simple-wikipedia-special-statistics.md)). `page.AUTO_INCREMENT=1281329`, `linktarget` 3,268,234 ids, `category` 1,689,294 ids allocated (upper bounds on row counts).
* Pages in `pages-articles.xml`: not published; **Inferred:** between 284,761 (ns0) and ~600k (ns0 + templates/categories/project/user? pages); the executor counts `<page>` elements ([question](/questions/simplewiki-pages-articles-page-count.md)). `revision` and `text` rows = that count.
* Tables carried (types verbatim from the dump DDL unless noted):
  * `page` (as dumped: `page_id int unsigned PK, page_namespace int, page_title varbinary(255), page_is_redirect, page_is_new, page_random double unsigned, page_touched binary(14), page_links_updated binary(14), page_latest int unsigned, page_len int unsigned, page_content_model varbinary(32), page_lang varbinary(35)`; `DEFAULT CHARSET=binary`).
  * `revision` (synthesized from XML): `rev_id BIGINT UNSIGNED PK, rev_page INT UNSIGNED, rev_parent_id BIGINT UNSIGNED NULL, rev_timestamp DATETIME, rev_minor_edit TINYINT, rev_len INT UNSIGNED (text@bytes), rev_sha1 VARBINARY(32) (base-36), rev_user_id INT UNSIGNED NULL, rev_user_text VARBINARY(255) (username or IP), rev_comment TEXT NULL, rev_content_model VARBINARY(32), rev_content_format VARBINARY(64)` — actor/comment tables denormalised ([revision manual](/sources/mediawiki-manual-revision-table.md)).
  * `text` (synthesized): `old_id BIGINT UNSIGNED PK (= rev_id), old_text MEDIUMTEXT CHARACTER SET utf8mb4, old_flags VARBINARY(255) DEFAULT 'utf-8'` ([text manual](/sources/mediawiki-manual-text-table.md)); FULLTEXT on `old_text`.
  * `categorylinks` (`cl_from, cl_sortkey varbinary(230), cl_timestamp, cl_sortkey_prefix, cl_type enum, cl_collation_id, cl_target_id bigint unsigned`), `pagelinks` (`pl_from, pl_from_namespace, pl_target_id`), `linktarget` (`lt_id, lt_namespace, lt_title varbinary(255)`), `redirect` (`rd_from, rd_namespace, rd_title, rd_interwiki, rd_fragment`), `category` (`cat_id, cat_title, cat_pages, cat_subcats, cat_files`), `site_stats` (1 row) — all as dumped.
* Encoding: SQL tables are `binary`/`varbinary` (MediaWiki convention, [page manual](/sources/mediawiki-manual-page-table.md)); XML is UTF-8 with the full Unicode repertoire (page titles in non-Latin scripts, emoji in wikitext) — `text.old_text` must be utf8mb4. Titles: SQL uses underscores without namespace prefix; XML `<title>` uses spaces and includes the prefix.

# Conversion path
Load the seven `.sql.gz` files directly with `mysql` after DDL fix-ups, and stream the XML with mwxml/iterparse into `revision` + `text` (+ verify `page` linkage). See [decision](/decisions/wikipedia-simple-conversion-path.md) and [tool](/tools/mediawiki-xml-dump-parsing.md).

# Type-mapping hazards
1. Dump line 1 `/*M!999999\- enable the sandbox mode */` (MariaDB sandbox directive) — strip before piping to `mysql` ([question](/questions/mediawiki-sql-dump-ddl-compatibility-mysql-9-7.md)).
2. `double unsigned` (`page_random`), integer display widths (`int(8)`), `DEFAULT current_timestamp()` spelling, `ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8` — verify on 9.7; sed fallbacks listed in the question.
3. Binary vs utf8mb4: **keep the binary schema** (lossless, byte-identical to upstream, documented on mediawiki.org) and add views `v_page`, `v_linktarget`, `v_category`, `v_redirect` exposing `CONVERT(x USING utf8mb4)` titles with underscores→spaces; do not convert in place (`page_name_title` unique index semantics would change under a collation).
4. `binary(14)` timestamps (`20260901120458`) — keep; views expose `STR_TO_DATE(page_touched,'%Y%m%d%H%i%s')`.
5. `categorylinks`/`pagelinks` no longer carry titles: category name = `linktarget.lt_title` via `cl_target_id` where `lt_namespace=14` ([categorylinks manual](/sources/mediawiki-manual-categorylinks-table.md), [pagelinks manual](/sources/mediawiki-manual-pagelinks-table.md)); `linktarget` is mandatory.
6. `cl_sortkey` is a binary collation key ("may not be readable"); do not convert it.
7. Some pages have `model` ≠ `wikitext` (Scribunto modules, CSS/JS, JSON); keep `rev_content_model`; FULLTEXT still indexes them.
8. FULLTEXT on ~1 GB of wikitext: build after load; expect the index to be a large share of the tablespace (**Inferred:** +40-60%).

# Programmable objects
None upstream (MediaWiki logic lives in PHP). We add the utf8mb4 views above and `v_article_text (page_id, title, old_text)` for ns0 non-redirects. No triggers/procedures.

# Indexing
Upstream keys as dumped (`page_name_title`, `page_random`, `page_len`, `page_redirect_namespace_len`, `cl_sortkey_id`, `cl_timestamp_id`, `pl_target_id`, `pl_backlinks_namespace_target_id`, `lt_namespace_title`, `rd_ns_title`, `cat_title`, `cat_pages`); add `revision(rev_page)`, `revision(rev_timestamp)`, `FULLTEXT text(old_text)`.

# Tests and expected values
* `COUNT(*) FROM page` = 947,771; `site_stats.ss_good_articles` = 284,761.
* `page_id=1` → (`page_namespace` 0, `page_title` 'April', `page_latest` 10861257, `page_len` 22079, `page_content_model` 'wikitext') — from the first INSERT row of page.sql.gz; `redirect.rd_from=24` → `rd_title` 'Catharism'.
* `COUNT(*) FROM revision` = `COUNT(*) FROM text` = number of `<page>` elements; every `page.page_latest` for pages present in the XML equals its `revision.rev_id`; `page_len` equals `rev_len` for those pages.
* `SELECT COUNT(*) FROM categorylinks c LEFT JOIN linktarget l ON l.lt_id=c.cl_target_id WHERE l.lt_id IS NULL` = 0.
* File sha1 values equal the table above.

# Tier assignment
**Extended.** Evidence: 356 MB bz2 XML (**Inferred:** ~1.3 GB wikitext), 33 + 28 + 82 + 37.5 MB gz link tables (**Inferred:** ~0.8-1 GB InnoDB), plus FULLTEXT → ~2.5-3 GB loaded. Core option: a deterministic ns0 sample (e.g., the 5,000 lowest `page_id` non-redirect articles with their text and the link rows among them, **Inferred** < 50 MB) shipped as `wikipedia_simple`, with the full load at start.

# License and attribution
Text: [CC BY-SA 4.0](/licenses/cc-by-sa-4-0.md) **and** [GFDL 1.3](/licenses/gfdl-1-3.md) (dumps legal notice; Terms of Use §7 effective 2023-06-07). Link tables are facts/metadata with the same terms. README wording: "Text from Simple English Wikipedia (https://simple.wikipedia.org/), dump 2026-09-01, available under the Creative Commons Attribution-ShareAlike 4.0 License (https://creativecommons.org/licenses/by-sa/4.0/) and, for most pages, the GNU Free Documentation License. Authors: each `revision.rev_user_text` row and the full history at https://simple.wikipedia.org/w/index.php?title=<page_title>&action=history (attribution "Through hyperlink (where possible) or URL to the article" per the Wikimedia Terms of Use). Modified: converted to MySQL; wikitext unchanged; talk pages and history omitted." Images are excluded ("many images are NOT released under this license"). The converted database is redistributed under CC BY-SA 4.0.

# Open questions
* [Page count of pages-articles](/questions/simplewiki-pages-articles-page-count.md)
* [DDL compatibility of MariaDB dumps with MySQL 9.7](/questions/mediawiki-sql-dump-ddl-compatibility-mysql-9-7.md)
