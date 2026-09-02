---
type: Source
title: Networks-Learning/stackexchange-dump-to-postgres README and repo metadata
description: MIT Python/lxml/psycopg2 loader for the Stack Exchange dumps into PostgreSQL; reviewed as prior art, not reused.
resource: https://github.com/Networks-Learning/stackexchange-dump-to-postgres
tags: [source, tool, stackexchange, python]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://github.com/Networks-Learning/stackexchange-dump-to-postgres
    title: README (WebFetch)
    accessed: "2026-09-02"
  - resource: https://api.github.com/repos/Networks-Learning/stackexchange-dump-to-postgres
    title: GitHub API repo metadata (pushed_at 2026-04-21T21:02Z, license MIT, 92 stars, default branch master)
    accessed: "2026-09-02"
---

# What was read
README and repository metadata on 2026-09-02.

# Relevant excerpt
Loads "Badges, Posts, Tags, Users, Votes, PostLinks, PostHistory, and Comments" (Tags may be missing in old dumps); dependencies `psycopg2-binary`, `lxml`; downloads from archive.org; "The Body field in Posts table is NOT populated by default" unless `--with-post-body`; EmailHash not populated; empty `ViewCount` → NULL; optional indexes and views; license MIT.

# What it was used to decide
[Stack Exchange XML parsing tool](/tools/stackexchange-xml-parsing.md): we write our own MySQL loader but keep familiar table names.
