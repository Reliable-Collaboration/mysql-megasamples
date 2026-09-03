---
type: Source
title: Status of github.com/chadwickbureau/baseballdatabank (GitHub API, 2026-09-02)
description: The historical GitHub mirror of the Lahman data returns 404 from the API; the chadwickbureau org lists chadwick, register, retrosheet, retrosplits, data-boxscores only; third-party mirrors exist.
resource: https://api.github.com/repos/chadwickbureau/baseballdatabank
tags:
- lahman
- baseballdatabank
- chadwick
- mirror
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://api.github.com/repos/chadwickbureau/baseballdatabank
  title: repos/chadwickbureau/baseballdatabank (HTTP 404), users/chadwickbureau/repos, search/repositories?q=baseballdatabank
  accessed: "2026-09-02"
---

# What was read
`gh api repos/chadwickbureau/baseballdatabank` -> "Not Found" (also /commits, /contents/core); `gh api users/chadwickbureau/repos` -> chadwick (GPL-2.0), chadwickbureau.github.io, data-boxscores, register, retrosheet, retrosplits; `gh api search/repositories?q=baseballdatabank` -> forks/mirrors such as `xorq-labs/baseballdatabank` ("Mirror of the Baseball Databank (CC BY-SA 3.0) by Chadwick Baseball Bureau", NOASSERTION), `cbwinslow/baseballdatabank`, `orrski/baseballdatabank` (2017). Accessed 2026-09-02.

# Relevant excerpt
The canonical Chadwick repository is not reachable at its historical URL; a web search (2026-09-02) still returned pages describing it as active, which are stale relative to the API result. **Inferred:** the repository was removed or made private after SABR took over distribution; no announcement was read.

# What it was used to decide
Pick SABR's release as the authoritative artifact and treat GitHub mirrors as unverified ([Lahman](/datasets/lahman.md)).
