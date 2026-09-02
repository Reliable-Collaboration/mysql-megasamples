---
type: Source
title: Stack Exchange API /info for dba and datascience (live totals on 2026-09-02)
description: Live site totals used as an upper bound for the 2024-04-02 dump row counts.
resource: https://api.stackexchange.com/2.3/info?site=dba
tags:
- source
- stackexchange
- row-counts
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
stale_after: "2026-12-01"
sources:
- resource: https://api.stackexchange.com/2.3/info?site=dba
  title: /info site=dba
  accessed: "2026-09-02"
- resource: https://api.stackexchange.com/2.3/info?site=datascience
  title: /info site=datascience
  accessed: "2026-09-02"
---

# What was read
API v2.3 `/info` responses on 2026-09-02.

# Relevant excerpt
* dba: total_questions 105,698; total_answers 142,723; total_users 321,367; total_comments 472,821; total_votes 823,419; total_badges 458,592; total_accepted 51,433.
* datascience: total_questions 36,319; total_answers 43,054; total_users 165,848; total_comments 105,865; total_votes 207,033; total_badges 166,567.
These are live 2026 numbers; the April 2024 dump will have fewer rows (**Inferred:** ~85-90%).

# What it was used to decide
Row-count expectations in [Stack Exchange dataset](/datasets/stackexchange.md).
