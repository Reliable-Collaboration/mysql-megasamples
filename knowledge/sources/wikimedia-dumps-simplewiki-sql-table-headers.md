---
type: Source
title: CREATE TABLE headers sampled from the simplewiki 20260901 .sql.gz dumps
description: First 16 KB of redirect, page, categorylinks, pagelinks, linktarget, category and page_props dumps (decompressed) — the exact DDL MediaWiki/MariaDB emits, used to plan MySQL 9.7 load fix-ups.
resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-page.sql.gz
tags:
- source
- wikipedia
- mediawiki
- schema
- ddl
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-redirect.sql.gz
  title: redirect.sql.gz (bytes 0-8191)
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-page.sql.gz
  title: page.sql.gz (bytes 0-16383)
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-categorylinks.sql.gz
  title: categorylinks.sql.gz (bytes 0-16383)
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pagelinks.sql.gz
  title: pagelinks.sql.gz (bytes 0-16383)
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-linktarget.sql.gz
  title: linktarget.sql.gz (bytes 0-16383)
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-category.sql.gz
  title: category.sql.gz (bytes 0-16383)
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-page_props.sql.gz
  title: page_props.sql.gz (bytes 0-16383)
  accessed: "2026-09-02"
---

# What was read
HTTP range requests for the first 8-16 KB of each file, piped through `zcat`, on 2026-09-02 (one record for the set because they are partial reads of one dump run; each file is listed above).

# Relevant excerpt (verbatim DDL)
Common preamble: `/*M!999999\- enable the sandbox mode */`, `-- MariaDB dump 10.19  Distrib 10.5.29-MariaDB`, `-- Server version 10.11.13-MariaDB-log`, `/*!40101 SET NAMES utf8mb4 */`, `/*!40103 SET TIME_ZONE='+00:00' */`, `SQL_MODE='NO_AUTO_VALUE_ON_ZERO'`, `DROP TABLE IF EXISTS`, then `CREATE TABLE`, `/*!40000 ALTER TABLE ... DISABLE KEYS */`, multi-row `INSERT INTO ... VALUES (...),(...)`.
```sql
CREATE TABLE `page` (
  `page_id` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `page_namespace` int(11) NOT NULL DEFAULT 0,
  `page_title` varbinary(255) NOT NULL DEFAULT '',
  `page_is_redirect` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `page_is_new` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `page_random` double unsigned NOT NULL DEFAULT 0,
  `page_touched` binary(14) NOT NULL,
  `page_links_updated` binary(14) DEFAULT NULL,
  `page_latest` int(8) unsigned NOT NULL DEFAULT 0,
  `page_len` int(8) unsigned NOT NULL DEFAULT 0,
  `page_content_model` varbinary(32) DEFAULT NULL,
  `page_lang` varbinary(35) DEFAULT NULL,
  PRIMARY KEY (`page_id`),
  UNIQUE KEY `page_name_title` (`page_namespace`,`page_title`),
  KEY `page_random` (`page_random`), KEY `page_len` (`page_len`),
  KEY `page_redirect_namespace_len` (`page_is_redirect`,`page_namespace`,`page_len`)
) ENGINE=InnoDB AUTO_INCREMENT=1281329 DEFAULT CHARSET=binary ROW_FORMAT=COMPRESSED;
-- first row: (1,0,'April',0,0,0.778582929065,'20260901120458','20260901120939',10861257,22079,'wikitext',NULL)

CREATE TABLE `categorylinks` (
  `cl_from` int(8) unsigned NOT NULL DEFAULT 0,
  `cl_sortkey` varbinary(230) NOT NULL DEFAULT '',
  `cl_timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `cl_sortkey_prefix` varbinary(255) NOT NULL DEFAULT '',
  `cl_type` enum('page','subcat','file') NOT NULL DEFAULT 'page',
  `cl_collation_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `cl_target_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`cl_from`,`cl_target_id`),
  KEY `cl_sortkey_id` (`cl_target_id`,`cl_type`,`cl_sortkey`,`cl_from`),
  KEY `cl_timestamp_id` (`cl_target_id`,`cl_timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=binary ROW_FORMAT=COMPRESSED;

CREATE TABLE `pagelinks` (
  `pl_from` int(8) unsigned NOT NULL DEFAULT 0,
  `pl_from_namespace` int(11) NOT NULL DEFAULT 0,
  `pl_target_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`pl_from`,`pl_target_id`),
  KEY `pl_target_id` (`pl_target_id`,`pl_from`),
  KEY `pl_backlinks_namespace_target_id` (`pl_from_namespace`,`pl_target_id`,`pl_from`)
) ENGINE=InnoDB DEFAULT CHARSET=binary ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;

CREATE TABLE `linktarget` (
  `lt_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `lt_namespace` int(11) NOT NULL,
  `lt_title` varbinary(255) NOT NULL,
  PRIMARY KEY (`lt_id`), UNIQUE KEY `lt_namespace_title` (`lt_namespace`,`lt_title`)
) ENGINE=InnoDB AUTO_INCREMENT=3268234 DEFAULT CHARSET=binary;

CREATE TABLE `redirect` ( `rd_from` int(8) unsigned NOT NULL DEFAULT 0, `rd_namespace` int(11) NOT NULL DEFAULT 0, `rd_title` varbinary(255) NOT NULL DEFAULT '', `rd_interwiki` varbinary(32) DEFAULT NULL, `rd_fragment` varbinary(255) DEFAULT NULL, PRIMARY KEY (`rd_from`), KEY `rd_ns_title` (`rd_namespace`,`rd_title`,`rd_from`) ) ENGINE=InnoDB DEFAULT CHARSET=binary ROW_FORMAT=COMPRESSED;

CREATE TABLE `category` ( `cat_id` int(10) unsigned NOT NULL AUTO_INCREMENT, `cat_title` varbinary(255) NOT NULL DEFAULT '', `cat_pages` int(11) NOT NULL DEFAULT 0, `cat_subcats` int(11) NOT NULL DEFAULT 0, `cat_files` int(11) NOT NULL DEFAULT 0, PRIMARY KEY (`cat_id`), UNIQUE KEY `cat_title` (`cat_title`), KEY `cat_pages` (`cat_pages`) ) ENGINE=InnoDB AUTO_INCREMENT=1689294 DEFAULT CHARSET=binary ROW_FORMAT=COMPRESSED;

CREATE TABLE `page_props` ( `pp_page` int(10) unsigned NOT NULL, `pp_propname` varbinary(60) NOT NULL DEFAULT '', `pp_value` blob NOT NULL, `pp_sortkey` float DEFAULT NULL, PRIMARY KEY (`pp_page`,`pp_propname`), UNIQUE KEY `pp_propname_page` (`pp_propname`,`pp_page`), UNIQUE KEY `pp_propname_sortkey_page` (`pp_propname`,`pp_sortkey`,`pp_page`) ) ENGINE=InnoDB DEFAULT CHARSET=binary ROW_FORMAT=COMPRESSED;
```
Observations: `categorylinks` has **no `cl_to`** and `pagelinks` has **no `pl_namespace`/`pl_title`** — both reference `linktarget.lt_id`. `page.AUTO_INCREMENT=1281329` (max page_id ≈ 1.28 M); `linktarget` ≈ 3.27 M ids; `category` ≈ 1.69 M ids allocated (row counts are lower).

# What it was used to decide
DDL fix-up list in [MediaWiki dump parsing](/tools/mediawiki-xml-dump-parsing.md); table selection (must include linktarget) in [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md); [DDL compatibility question](/questions/mediawiki-sql-dump-ddl-compatibility-mysql-9-7.md).
