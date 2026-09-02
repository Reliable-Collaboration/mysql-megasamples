---
type: Source
title: "python.org Downloads: active Python releases"
description: Latest release 3.14.7; 3.14 and 3.13 in bugfix status, 3.12 security-only until 2028-10, 3.10 security ends 2026-10.
resource: https://www.python.org/downloads/
tags:
- python
- versions
status: stable
trust: verified
stale_after: "2026-12-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
sources:
- resource: https://www.python.org/downloads/
  title: "python.org Downloads: active Python releases"
  accessed: "2026-09-02"
---

# What was read
https://www.python.org/downloads/, accessed 2026-09-02.

# Relevant excerpt
* "Download Python 3.14.7" is the current release. Active releases: 3.15 pre-release (EOL 2031-10), 3.14 bugfix (2030-10), 3.13 bugfix (2029-10), 3.12 security (2028-10), 3.11 security (2027-10), 3.10 security (2026-10), 3.9 end-of-life 2025-10-31.

# What it was used to decide
[Python conversion stack](/tools/python-conversion-stack.md): pin Python 3.13 (bugfix, widest wheel coverage) with 3.14 as the upgrade candidate once every pinned wheel ships cp314 builds.
