---
type: Source
title: ISI Shetty/Adibi Enron page — live 403 and Wayback availability check
description: Evidence that http://www.isi.edu/~adibi/Enron/Enron.htm is offline behind a Cloudflare block and that a 2013-12-13 Wayback snapshot exists (content not read due to rate limiting).
resource: http://www.isi.edu/~adibi/Enron/Enron.htm
tags: [source, enron, relational-versions, offline]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: http://archive.org/wayback/available?url=isi.edu/~adibi/Enron/Enron.htm
    title: Wayback availability API response
    accessed: 2026-09-02
  - resource: https://www.isi.edu/~adibi/Enron/Enron.htm
    title: live page (HTTP 403, Cloudflare "Sorry, you have been blocked")
    accessed: 2026-09-02
---

# What was read
* Live URL: `HTTP/1.1 403 Forbidden`, body is a Cloudflare block page ("You are unable to access wpewaf.com").
* Wayback availability API: `{"archived_snapshots": {"closest": {"status": "200", "available": true, "url": "http://web.archive.org/web/20131213191703/http://www.isi.edu:80/~adibi/Enron/Enron.htm", "timestamp": "20131213191703"}}}`. Three attempts to fetch the snapshot itself returned HTTP 429 from web.archive.org.

# What it was used to decide
The ISI MySQL dump (Shetty and Adibi 2004) is recorded as historically important but offline in [Enron dataset](/datasets/enron.md); reading the snapshot is an [open question](/questions/enron-isi-mysql-dump-availability.md).
