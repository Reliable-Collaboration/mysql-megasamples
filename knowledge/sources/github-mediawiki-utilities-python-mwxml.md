---
type: Source
title: mediawiki-utilities/python-mwxml README and repo metadata
description: MIT-licensed streaming reader for MediaWiki XML dumps; README example and license read; repo pushed 2026-04-09.
resource: https://github.com/mediawiki-utilities/python-mwxml
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
- resource: https://github.com/mediawiki-utilities/python-mwxml
  title: README (WebFetch)
  accessed: "2026-09-02"
- resource: https://api.github.com/repos/mediawiki-utilities/python-mwxml
  title: GitHub API repo metadata (pushed_at 2026-04-09T20:39Z, license MIT, 63 stars, not archived, default branch master)
  accessed: "2026-09-02"
---

# What was read
README and the repository metadata on 2026-09-02.

# Relevant excerpt
README: memory-efficient iteration over pages and revisions — `dump = mwxml.Dump.from_file(open("dump.xml")); for page in dump: for revision in page: print(revision.id)`; `pip install mwxml`; license MIT; docs at pythonhosted.org/mwxml. The README does not state supported export-schema versions or Python versions.

# What it was used to decide
[MediaWiki dump parsing tool](/tools/mediawiki-xml-dump-parsing.md).
