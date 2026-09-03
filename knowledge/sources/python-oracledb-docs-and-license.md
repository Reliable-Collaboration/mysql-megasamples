---
type: Source
title: python-oracledb documentation (introduction, installation) and LICENSE.txt
description: Thin-mode driver that needs no Oracle Client; dual UPL 1.0 / Apache 2.0 license; supported Python and Oracle versions; wheels for Linux x86-64 and aarch64.
resource: https://python-oracledb.readthedocs.io/en/latest/
tags:
- oracle
- python
- driver
- license
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
- resource: https://python-oracledb.readthedocs.io/en/latest/user_guide/introduction.html
  title: Introduction to python-oracledb
  accessed: "2026-09-02"
- resource: https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html
  title: Installing python-oracledb
  accessed: "2026-09-02"
- resource: https://python-oracledb.readthedocs.io/en/latest/license.html
  title: License
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/oracle/python-oracledb/main/LICENSE.txt
  title: LICENSE.txt (repo); latest release v4.0.2 published 2026-07-14 (GitHub releases API)
  accessed: "2026-09-02"
  version: v4.0.2
---

# What was read
The three documentation pages, the repository LICENSE.txt and the releases API, 2026-09-02.

# Relevant excerpt
* "By default, python-oracledb allows connecting directly to Oracle Database 12.1 or later. This Thin mode does not need Oracle Client libraries." / "By default, python-oracledb runs in a 'Thin' mode which connects directly to Oracle Database. This mode does not need Oracle Client libraries."
* "This module is currently tested with Python 3.10, 3.11, 3.12, 3.13, 3.14 and 3.15 against Oracle Database version 26, 21, and 19."; install: `python -m pip install oracledb --upgrade`; pre-built wheels for "Linux 64-bit (x86-64)" and "Linux Arm 64-bit (aarch64)".
* LICENSE.txt: "Copyright (c) 2016, 2026 Oracle and/or its affiliates. This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl and Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license."

# What it was used to decide
[SQLcl and python-oracledb tool record](/tools/sqlcl-and-python-oracledb.md): python-oracledb Thin mode is the export tool for the optional Oracle verification profile (no Instant Client, permissive license).
