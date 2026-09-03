---
type: Open Question
title: What did the ISI Shetty/Adibi Enron MySQL page offer, and is any copy still authoritative?
description: The live page is blocked (403) and Wayback rate-limited the 2013 snapshot; only a third-party "repaired" copy is reachable.
resource: /questions/enron-isi-mysql-dump-availability.md
tags:
- question
- enron
- relational-versions
- text-group
status: draft
trust: open
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: http://archive.org/wayback/available?url=isi.edu/~adibi/Enron/Enron.htm
  accessed: "2026-09-02"
- resource: https://www.ah-ruhe.de/enron-email-data/
  accessed: "2026-09-02"
---

# Question
For the README's "related work" paragraph only: what schema/statistics did the 2004 ISI page publish (the tech report "The Enron Email Dataset Database Schema and Brief Statistical Report")? Not needed for the build.

# Cheapest experiment
Later (rate limit): `curl -A Mozilla http://web.archive.org/web/20131213191703id_/http://www.isi.edu/~adibi/Enron/Enron.htm` and record a source file. If it fails again, cite ah-ruhe.de's description alone.

# Resolves
Completeness of the "known relational versions" note in [Enron dataset](/datasets/enron.md).
