---
type: Source
title: mediawiki-utilities/python-mwsql README and repo metadata
description: GPL-3.0 library that parses Wikimedia .sql.gz dumps into Python rows; README example read; repo last pushed 2024-02-19.
resource: https://github.com/mediawiki-utilities/python-mwsql
tags:
- source
- tool
- mediawiki
- python
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://github.com/mediawiki-utilities/python-mwsql
  title: README (WebFetch)
  accessed: "2026-09-02"
- resource: https://api.github.com/repos/mediawiki-utilities/python-mwsql
  title: GitHub API repo metadata (pushed_at 2024-02-19T08:47Z, license GPL-3.0, 20 stars, default branch main)
  accessed: "2026-09-02"
---

# What was read
README and repository metadata on 2026-09-02.

# Relevant excerpt
"mwsql" converts Wikimedia SQL dump files into Python objects with lazy-loading generators; `Dump.from_file('simplewiki-latest-change_tag_def.sql.gz')`, `dump.head(5)`, `dump.dtypes`, `dump.rows(convert_dtypes=True)`; one table per dump file; license GPLv3; Python 3.9+.

# What it was used to decide
Optional row-level path in [MediaWiki dump parsing tool](/tools/mediawiki-xml-dump-parsing.md) (GPL: build-time only).
