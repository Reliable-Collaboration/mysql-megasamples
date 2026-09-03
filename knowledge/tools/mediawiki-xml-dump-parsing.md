---
type: Tool
title: MediaWiki dump parsing (pages-articles XML via mwxml or iterparse; .sql.gz tables via mwsql or direct load)
description: How the Simple English Wikipedia dumps get into MySQL — stream the XML for page text and revisions, and load the MediaWiki-produced .sql.gz files directly after DDL fix-ups.
resource: https://github.com/mediawiki-utilities/python-mwxml
tags:
- tool
- mediawiki
- xml
- python
- mysql-load
- text-group
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://github.com/mediawiki-utilities/python-mwxml
  title: python-mwxml README
  accessed: "2026-09-02"
- resource: https://pypi.org/pypi/mwxml/json
  title: PyPI metadata for mwxml
  accessed: "2026-09-02"
  version: 0.3.8 (uploaded 2026-04-08)
- resource: https://github.com/mediawiki-utilities/python-mwsql
  title: python-mwsql README
  accessed: "2026-09-02"
- resource: https://pypi.org/pypi/mwsql/json
  title: PyPI metadata for mwsql
  accessed: "2026-09-02"
  version: 1.0.4 (uploaded 2024-02-19)
- resource: https://www.mediawiki.org/xml/export-0.11.xsd
  title: MediaWiki export schema 0.11
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-redirect.sql.gz
  title: first 8 KB of the redirect SQL dump (header + first INSERT)
  accessed: "2026-09-02"
  version: "20260901"
---

# Two input formats, two paths

## A. `pages-articles.xml.bz2` → `page` text, `revision`, `text` (needs code)
* **mwxml 0.3.8** (MIT; GitHub pushed 2026-04-09; deps `mwtypes>=0.4.0, mwcli, para, jsonschema`; no `requires_python` declared). README usage: `dump = mwxml.Dump.from_file(open("dump.xml")); for page in dump: for revision in page: ...`. It streams, so memory is flat. The README does not state which export schema versions are supported — **Inferred:** 0.3.x handles 0.10/0.11 (the 0.11 additions are `origin`, `model`, `format`, `sha1`, `content` slots, all present in the XSD read today); the executor verifies on the first 1,000 pages.
* **Fallback with zero dependencies:** `xml.etree.ElementTree.iterparse` over `bz2.open(...)`, clearing each `<page>` element after use. The XSD (read 2026-09-02) gives the element order per page: `title, ns, id, [redirect title=], [restrictions], revision*` and per revision: `id, [parentid], timestamp, contributor(username,id | ip), [minor], [comment], origin, model, format, text(bytes=, sha1=, [deleted]), [content*], sha1`. The namespace is `http://www.mediawiki.org/xml/export-0.11/`.
* Write rows with `LOAD DATA LOCAL INFILE` from tab-separated temp files (fastest) or `executemany` batches of 1,000; wikitext contains tabs/newlines, so escape per MySQL LOAD DATA rules (`\t`, `\n`, `\\`) or use CSV with `ENCLOSED BY '"'`.
* Titles in XML use spaces and include the namespace prefix ("Talk:Foo"); the SQL `page_title` uses underscores and no prefix. Join key between XML and SQL is `page.id` = `page_id`.

## B. `*.sql.gz` → load directly into MySQL (no parser needed, but DDL fix-ups)
Observed header of `simplewiki-latest-redirect.sql.gz` (20260901):
```
/*M!999999\- enable the sandbox mode */
-- MariaDB dump 10.19  Distrib 10.5.29-MariaDB, for debian-linux-gnu (x86_64)
-- Host: dbstore1007.eqiad.wmnet    Database: simplewiki
-- Server version 10.11.13-MariaDB-log
/*!40101 SET NAMES utf8mb4 */;
DROP TABLE IF EXISTS `redirect`;
CREATE TABLE `redirect` ( `rd_from` int(8) unsigned NOT NULL DEFAULT 0, `rd_namespace` int(11) NOT NULL DEFAULT 0, `rd_title` varbinary(255) NOT NULL DEFAULT '', `rd_interwiki` varbinary(32) DEFAULT NULL, `rd_fragment` varbinary(255) DEFAULT NULL, PRIMARY KEY (`rd_from`), KEY `rd_ns_title` (`rd_namespace`,`rd_title`,`rd_from`) ) ENGINE=InnoDB DEFAULT CHARSET=binary ROW_FORMAT=COMPRESSED;
/*!40000 ALTER TABLE `redirect` DISABLE KEYS */;
INSERT INTO `redirect` VALUES (24,0,'Catharism','',''),(41,0,'United_States_customary_units','',''),...
```
So: **yes, every .sql.gz includes `DROP TABLE` + `CREATE TABLE` + multi-row `INSERT`s** — `zcat file.sql.gz | mysql db` is the load path. Things the executor must handle (each is an open question until tested on 9.7 — see [DDL compatibility question](/questions/mediawiki-sql-dump-ddl-compatibility-mysql-9-7.md)):
1. Line 1 `/*M!999999\- enable the sandbox mode */` is a MariaDB-only executable comment. **Inferred:** Oracle's `mysql` client may reject the `\-` as an unknown client command; strip line 1 with `tail -n +2` or `sed '1{/^\/\*M!999999/d}'`.
2. Integer display widths (`int(8) unsigned`, `tinyint(1)`) — deprecated syntax; expected to load with warnings.
3. `page_random double unsigned` — `UNSIGNED` on DOUBLE is deprecated in MySQL 8.0.17+; whether 9.7 still accepts it must be tested; fallback `sed 's/double unsigned/double/'`.
4. `ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8` — legal in InnoDB with file-per-table; consider stripping for load speed.
5. `DEFAULT current_timestamp() ON UPDATE current_timestamp()` (MariaDB spelling with parentheses) on `categorylinks.cl_timestamp`.
6. `DEFAULT CHARSET=binary` + `varbinary` titles: keep as-is (lossless, matches MediaWiki docs); add `_utf8` views with `CONVERT(col USING utf8mb4)` for humans.
* **mwsql 1.0.4** (GPL-3.0-or-later; Python >=3.9; deps requests, tqdm; last push 2024-02-19) parses these files into Python rows (`Dump.from_file(...).rows(convert_dtypes=True)`) — useful only if we want to re-emit rows (e.g., to convert binary titles to utf8mb4 or subset rows); its GPL license is fine for a build-time tool but keep it out of the shipped image.

# Facts
* `linktarget` is required: 20260901 `categorylinks` has `cl_target_id` and no `cl_to`; `pagelinks` has `pl_target_id` and no `pl_namespace/pl_title` (headers read 2026-09-02). Category names = `linktarget.lt_title WHERE lt_namespace = 14`.
* Dumps are produced by MariaDB 10.11 `mysqldump`, `SET NAMES utf8mb4`, `TIME_ZONE='+00:00'`, `SQL_MODE='NO_AUTO_VALUE_ON_ZERO'`, and disable FK/unique checks during load.
* Checksums: `simplewiki-latest-md5sums.txt` and `-sha1sums.txt` list every file by its dated name (`simplewiki-20260901-...`).

# Limits
* The `.sql.gz` dumps are MariaDB `mysqldump` output and need the fix-ups listed above before MySQL 9.7 accepts them ([question](/questions/mediawiki-sql-dump-ddl-compatibility-mysql-9-7.md)).
* `revision` and `text` are not published as SQL; they are synthesized from the XML, so their row counts are only known after parsing ([question](/questions/simplewiki-pages-articles-page-count.md)).
* From the 2025 schema on, `categorylinks`/`pagelinks` carry no title columns; every title join must go through `linktarget`.
