---
type: License
title: GNU General Public License v2.0 (or later) - Dell DVD Store 3
description: Copyleft license of the DS3 kit (generators, drivers, build scripts); the data CSVs are program output whose status is an open question.
resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/gpl.txt
tags: [license, gpl-2-0, copyleft, dvdstore]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/gpl.txt
    title: gpl.txt (GPL v2, June 1991)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/cust/ds3_create_cust.c
    title: source header "version 2 ... or (at your option) any later version"
    accessed: "2026-09-02"
---

# Where the text lives
* Verbatim GPL v2 text: `ds3/gpl.txt` in the repository (18,013 bytes; identical copies under mysqlds3/ and oracleds3/) - canonical https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt (returned HTTP 429 during this session; not re-verified there).
* Grant: each generator/driver source header says "either version 2 of the License, or (at your option) any later version" - SPDX `GPL-2.0-or-later` ([source](/sources/github-dvdstore-ds3-gpl-and-source-headers.md)). No repository-level LICENSE file; GitHub shows no license.

# Key clauses (verbatim)
* Section 1: copies of source must keep "an appropriate copyright notice and disclaimer of warranty; keep intact all the notices that refer to this License ... and give any other recipients of the Program a copy of this License along with the Program."
* Section 2(b): any distributed work "that in whole or in part contains or is derived from the Program ... to be licensed as a whole at no charge to all third parties under the terms of this License."
* Section 2 (aggregation): "mere aggregation of another work not based on the Program with the Program ... on a volume of a storage or distribution medium does not bring the other work under the scope of this License."
* Section 0 (output): "the output from the Program is covered only if its contents constitute a work based on the Program".

# Obligations
* Redistributing the DS3 DDL/index/procedure scripts (even edited) = distributing a GPL work: ship `gpl.txt`, keep Dell/VMware notices, mark modified files with a change notice (Section 2(a)), and license the modified scripts GPL-2.0-or-later.
* Because of the aggregation clause, including the DS3 scripts in the image does not force the other datasets or the project's own build code under the GPL, provided they are separate works on the same medium.
* The generated CSV data: see [open question](/questions/dvdstore-generated-data-license.md).

# Attribution
Ship `gpl.txt` (GPL-2.0-or-later) next to the DVD Store scripts, keep the Dell (2005) and VMware (2014) copyright headers, and mark every modified script with a dated change note. Wording used in NOTICE: "Dell DVD Store 3 kit © 2005 Dell, Inc. and © 2014 VMware, Inc., GNU GPL v2 or later; MySQL scripts adapted (InnoDB, utf8mb4, lower-case identifiers) by this project." sysbench (GPL-2.0) is executed at load time only and is not redistributed.

# Applied to
* [Dell DVD Store 3](/datasets/dell-dvd-store.md) - `ds3/mysqlds3/build/*.sql`, `ds3/mysqlds3/load/**/*.sql`, generators and drivers.
* [TPC-C](/datasets/tpc-c.md) — the `sysbench` binary (Debian package 1.0.20+ds-7; **Inferred:** GPL-2.0 per GitHub's license detection, the license file itself was not opened — confirm at task B-03) executes the Apache-2.0 sysbench-tpcc scripts at load time; nothing GPL is redistributed. See [TPC-C implementations](/tools/tpcc-implementations.md).
