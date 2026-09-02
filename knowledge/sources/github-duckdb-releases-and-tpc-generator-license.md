---
type: Source
title: "duckdb/duckdb: releases (API), extension/tpch/dbgen/LICENSE (TPC EULA 2.2) and extension/tpcds/dsdgen-c source headers (TPC Legal Notice)"
description: "Latest release v1.5.5 (2026-07-22), LTS 1.4.5; the TPC-H generator carries the TPC End User License Agreement v2.2; the TPC-DS generator files carry the TPC 'Legal Notice ... maintained by the TPC' header; the DuckDB repository itself is MIT."
resource: https://github.com/duckdb/duckdb
tags: [duckdb, tpch, tpcds, license, release]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://github.com/duckdb/duckdb
    title: "duckdb/duckdb: releases (API), extension/tpch/dbgen/LICENSE (TPC EULA 2.2) and extension/tpcds/dsdgen-c source headers (TPC Legal Notice)"
    accessed: 2026-09-02
    version: "main branch and releases read via GitHub API/raw on 2026-09-02"
---

# What was read
https://github.com/duckdb/duckdb, accessed 2026-09-02; version: main branch and releases read via GitHub API/raw on 2026-09-02.

# Relevant excerpt
* Releases: v1.5.5 "DuckDB v1.5.5 Bugfix Release" 2026-07-22; v1.5.4 2026-06-17; v1.4.5 2026-06-17; v1.5.3 2026-05-20; v1.5.2 2026-04-13; v1.5.1 2026-03-23; repo license MIT.
* `extension/tpch/dbgen/LICENSE`: "END USER LICENSE AGREEMENT VERSION 2.2 ... This is a legal agreement between you ... and the Transaction Processing Performance Council ("TPC"). This Agreement states the terms and conditions upon which TPC offers to license the Software, including, but not limited to, the source code, scripts, executable programs, drivers, libraries and data files associated with such programs"; "2. Ownership. The Materials are licensed, not sold"; "3. License Grant. Subject to Your compliance ... TPC grants You a restricted, non-exclusive, revocable license to install and use the" Software (text continues; export-control clause 13 referenced).
* `extension/tpcds/dsdgen/dsdgen-c/address.cpp` header: "Legal Notice — This document and associated source code (the "Work") is a part of a benchmark specification maintained by the TPC. The TPC reserves all right, title, and interest to the Work as provided under U.S. and international laws, including without limitation all patent and trademark rights therein." followed by a no-warranty clause; "Contributors: Gradient Systems". No LICENSE file in `extension/tpcds/dsdgen/`.

# What it was used to decide
[DuckDB record](/tools/duckdb.md) and [TPC EULA license record](/licenses/tpc-eula.md): generated TPC-H/TPC-DS data is redistributable only under the TPC terms, which the dataset group must resolve before shipping generated rows (ship the generator invocation, not the rows, is the safe default).
