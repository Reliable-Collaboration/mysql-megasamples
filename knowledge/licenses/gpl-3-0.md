---
type: License
title: GNU General Public License v3.0 (HammerDB)
description: Copyleft license of HammerDB; relevant only if HammerDB code is redistributed or linked, not for merely running it or shipping data it loaded.
resource: https://raw.githubusercontent.com/TPC-Council/HammerDB/master/LICENSE
tags:
- license
- gpl
- copyleft
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://raw.githubusercontent.com/TPC-Council/HammerDB/master/LICENSE
  title: HammerDB LICENSE (35,149 bytes; header "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007")
  accessed: "2026-09-02"
---

# Where the text lives
https://www.gnu.org/licenses/gpl-3.0.txt; HammerDB's copy at the resource URL (header verified: "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007 Copyright (C) 2007 Free Software Foundation, Inc."). SPDX: GPL-3.0-only (HammerDB's own file headers say "either version 3 of the License, or (at your option) any later version" → GPL-3.0-or-later).

# Obligations
Running HammerDB (from its official Docker image) to populate a database creates no obligation on the database contents; copying HammerDB Tcl code or its DDL text into the repository would require GPL-3.0 terms on that file. If HammerDB's MySQL DDL is reused, rewrite it from the TPC-C spec table layouts rather than copying (the DDL is also derived from the spec, whose copying notice applies).

# Attribution
None required by this project: HammerDB is executed from its official image only and nothing from it is redistributed. If HammerDB code were ever included, the full GPL-3.0 text and source offer would be required.

# Applied to
* [TPC-C](/datasets/tpc-c.md) via [TPC-C implementations](/tools/tpcc-implementations.md) (HammerDB, reference/fallback loader).
