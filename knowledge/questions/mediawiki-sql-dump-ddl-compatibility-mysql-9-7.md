---
type: Open Question
title: Do the MariaDB-generated simplewiki .sql.gz dumps load unchanged into MySQL 9.7?
description: Four constructs in the dump headers are MariaDB-isms or deprecated MySQL syntax; each needs a one-minute test on the target server before the build script is written.
resource: /questions/mediawiki-sql-dump-ddl-compatibility-mysql-9-7.md
tags: [question, wikipedia, mediawiki, ddl, mysql-9-7, text-group]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-redirect.sql.gz
    accessed: "2026-09-02"
  - resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-page.sql.gz
    accessed: "2026-09-02"
---

# Question
Observed in the 20260901 headers ([source](/sources/wikimedia-dumps-simplewiki-sql-table-headers.md)):
1. First line `/*M!999999\- enable the sandbox mode */` — does Oracle's `mysql` 9.7 client reject `\-` as an unknown command?
2. `page_random double unsigned` — accepted (with warning) or rejected on 9.7?
3. Integer display widths `int(8) unsigned`, `tinyint(1) unsigned` — warnings only?
4. `cl_timestamp timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()` and `ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8` — accepted by InnoDB on 9.7 defaults?

# Cheapest experiment
`docker run --rm -e MYSQL_ALLOW_EMPTY_PASSWORD=1 mysql:9.7.2` then `curl -r 0-16383 .../simplewiki-latest-redirect.sql.gz | zcat | head -40 | mysql -h127.0.0.1 -uroot test` — once as-is, once with `tail -n +2`, once with `sed -E 's/double unsigned/double/; s/ROW_FORMAT=COMPRESSED( KEY_BLOCK_SIZE=[0-9]+)?//'`. Takes under five minutes and produces the exact filter the loader needs. Repeat for the `page` header.

# Resolves
The fix-up list in [MediaWiki dump parsing](/tools/mediawiki-xml-dump-parsing.md) and [decision](/decisions/wikipedia-simple-conversion-path.md).
