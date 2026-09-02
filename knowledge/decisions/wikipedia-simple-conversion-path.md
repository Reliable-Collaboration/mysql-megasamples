---
type: Decision
title: Simple English Wikipedia — load the MediaWiki .sql.gz tables directly and synthesize revision/text from pages-articles XML, keeping the binary schema
description: Choose direct SQL loading with DDL fix-ups plus a streaming XML parse, and keep MediaWiki's varbinary/binary columns with utf8mb4 views rather than converting in place.
resource: /decisions/wikipedia-simple-conversion-path.md
tags:
- decision
- wikipedia
- mediawiki
- conversion-path
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
- resource: https://dumps.wikimedia.org/simplewiki/latest/
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-page.sql.gz
  accessed: "2026-09-02"
- resource: https://www.mediawiki.org/wiki/Manual:Page_table
  accessed: "2026-09-02"
- resource: https://github.com/mediawiki-utilities/python-mwxml
  accessed: "2026-09-02"
---

# Question
How to load Simple English Wikipedia into MySQL 9.7 with the least bespoke code and no loss of fidelity, and whether to keep MediaWiki's binary charset convention.

# Options considered
1. **Direct `mysql < *.sql.gz` for page/categorylinks/pagelinks/linktarget/redirect/category/site_stats (after stripping the MariaDB sandbox line and testing three DDL constructs), plus mwxml/iterparse for revision+text; keep `CHARSET=binary`, add utf8mb4 views.**
2. Parse everything with mwsql/mwxml and re-emit our own utf8mb4 schema — more code, GPL tool at build time, and titles would acquire a collation that changes uniqueness semantics.
3. Run MediaWiki's `importDump.php` in a PHP container — heavy, slow, and would rebuild link tables instead of loading the published ones.
4. Use pages-meta-current (adds talk/user pages) or full history — larger, no benefit for a sample.

# Evidence
[DDL headers](/sources/wikimedia-dumps-simplewiki-sql-table-headers.md) show complete MySQL-dialect dumps with `linktarget` normalisation; [page table manual](/sources/mediawiki-manual-page-table.md) documents the varbinary convention; [XSD](/sources/mediawiki-xml-export-0-11-xsd.md) gives the revision fields; [tool record](/tools/mediawiki-xml-dump-parsing.md); [What's available](/sources/meta-wikimedia-data-dumps-whats-available.md) confirms no revision/text SQL and one current revision per page in pages-articles.

# Outcome
Option 1. `text.old_text` is utf8mb4 MEDIUMTEXT with FULLTEXT (the one deliberate departure from MediaWiki's mediumblob). Pin the dated 20260901 URLs and sha1s. Dataset record: [Simple English Wikipedia](/datasets/wikipedia-simple.md). Blocking verification: [DDL compatibility question](/questions/mediawiki-sql-dump-ddl-compatibility-mysql-9-7.md).

# Status
accepted
