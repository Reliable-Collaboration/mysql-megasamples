---
type: License
title: BSD 3-Clause (generic, for build-time Python packages)
description: Permissive licence of lxml (declared BSD-3-Clause per PyPI metadata) and of scikit-learn's corrected Iris copy; both are build-time inputs and are not shipped in the image.
resource: https://opensource.org/license/bsd-3-clause
tags:
- license
- permissive
- bsd
status: stable
trust: inferred
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:51:18Z"
sources:
- resource: https://pypi.org/pypi/lxml/json
  accessed: "2026-09-02"
  version: 6.1.3
- resource: https://opensource.org/license/bsd-3-clause
  title: The 3-Clause BSD License (OSI)
  accessed: "2026-09-02"
---

# Where the text lives
The generic text is at https://opensource.org/license/bsd-3-clause ([OSI source record](/sources/opensource-org-bsd-3-clause.md), read 2026-09-02); the Sakila-specific variant is in [bsd-3-clause-sakila](/licenses/bsd-3-clause-sakila.md). **Inferred:** lxml's licence file matches the OSI text; verify by reading `LICENSE.txt` in the sdist when the lock file is first generated.

# Obligations
Retain copyright notice, licence text and disclaimer in source and binary redistributions; no endorsement using contributor names. Not triggered: the packages are build-time dependencies only.

# Attribution
Reproduce the copyright notice, the three conditions and the disclaimer of each BSD-licensed package if it is ever redistributed; for build-time-only use (lxml, scikit-learn's Iris copy) NOTICE lists the package name, version and "BSD-3-Clause".

# Applied to
* lxml 6.1.3 in the [Python conversion stack](/tools/python-conversion-stack.md); sqlparse was evaluated and rejected ([source](/sources/pypi-sqlparse.md)).
* [Iris](/datasets/iris.md) - the corrected values as shipped by scikit-learn.
