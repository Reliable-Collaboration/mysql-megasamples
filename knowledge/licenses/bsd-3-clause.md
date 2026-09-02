---
type: License
title: "BSD 3-Clause (generic, for build-time Python packages)"
description: "Permissive licence of lxml (declared BSD-3-Clause) and sqlparse (BSD classifier) as reported by PyPI metadata; these run only at build time and are not shipped in the image."
resource: https://opensource.org/license/bsd-3-clause
tags: [license, permissive, bsd]
status: stable
trust: inferred
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:51:18Z" }
sources:
  - resource: https://pypi.org/pypi/lxml/json
    accessed: "2026-09-02"
    version: "6.1.3"
  - resource: https://pypi.org/pypi/sqlparse/json
    accessed: "2026-09-02"
    version: "0.6.0"
---

# Where the text lives
The generic text is at https://opensource.org/license/bsd-3-clause (not opened this session; the Sakila-specific variant is in [bsd-3-clause-sakila](/licenses/bsd-3-clause-sakila.md), whose source record quotes the OSI text). **Inferred:** lxml's and sqlparse's licence files match the OSI text; verify by reading `LICENSE.txt` in each sdist when the lock file is first generated.

# Obligations
Retain copyright notice, licence text and disclaimer in source and binary redistributions; no endorsement using contributor names. Not triggered: the packages are build-time dependencies only.

# Attribution
Reproduce the copyright notice, the three conditions and the disclaimer of each BSD-licensed package if it is ever redistributed; for build-time-only use (lxml, sqlparse, scikit-learn's Iris copy) NOTICE lists the package name, version and "BSD-3-Clause".

# Applied to
* lxml 6.1.3 and sqlparse 0.6.0 in the [Python conversion stack](/tools/python-conversion-stack.md).
