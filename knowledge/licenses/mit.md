---
type: License
title: MIT License
description: Permissive license requiring only that the copyright notice and permission notice accompany copies; used by Chinook and the Contoso Data Generator V2 (tool and data).
resource: https://opensource.org/license/mit
tags:
- license
- mit
- permissive
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://opensource.org/license/mit
  title: The MIT License (OSI)
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/lerocha/chinook-database/master/LICENSE.md
  title: Chinook LICENSE.md
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/LICENSE
  title: Contoso-Data-Generator-V2 LICENSE
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2-Data/main/LICENSE
  title: Contoso-Data-Generator-V2-Data LICENSE
  accessed: "2026-09-02"
---

# Where the text lives
Template: https://opensource.org/license/mit ([source](/sources/opensource-org-mit.md)). Each project's file carries the same operative text with its own copyright line.

# Obligations
"The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software." - ship each project's copyright line plus the permission paragraph and disclaimer with the converted database and in the repository. No share-alike, no attribution beyond the notice.

# Attribution
Reproduce the copyright line and the MIT permission notice for each MIT-licensed dataset in its `LICENSE` and in NOTICE: "Copyright (c) Microsoft Corporation" (Northwind, Pubs, AdventureWorks, WideWorldImporters, plus the scripts' own "Copyright Microsoft, Inc. 1994 - 2000" lines), "Copyright (c) 2023 Oracle and/or its affiliates" (HR, CO, SH, OE), "Chinook Database, Copyright (c) 2008-2024 Luis Rocha", "Copyright (c) 2024 SQLBI" (Contoso data) and "Copyright (c) 2022 SQLBI" (generator), each followed by the standard MIT permission and disclaimer paragraphs.

# Applied to
* [Chinook](/datasets/chinook.md) - "Chinook Database / Copyright (c) 2008-2024 Luis Rocha" ([LICENSE.md](/sources/github-lerocha-chinook-license.md)). GitHub shows NOASSERTION only because of the custom heading.
* [Contoso (SQLBI Contoso Data Generator V2)](/datasets/contoso.md) - generator "Copyright (c) 2022 SQLBI"; ready-to-use data repository "Copyright (c) 2024 SQLBI" ([data license](/sources/github-sql-bi-contoso-v2-data-license.md)).
* [Oracle HR](/datasets/oracle-hr.md), [Oracle CO](/datasets/oracle-co.md), [Oracle SH](/datasets/oracle-sh.md), [Oracle OE/PM/IX (archived)](/datasets/oracle-oe-pm-ix.md) - `LICENSE.txt` of oracle-samples/db-sample-schemas at tag v23.3 is the MIT text with "Copyright (c) 2023 Oracle and/or its affiliates. All rights reserved." ([source](/sources/github-oracle-samples-db-sample-schemas-readme-and-license.md)). Verified MIT, **not** UPL (Oracle's tooling repos python-oracledb/docker-images are UPL/Apache; the sample-schema repo is not). Every `.sql` file and per-schema README repeats the notice; the SH `.csv` data files carry no header but are covered as "associated documentation files". Attribution string: "Oracle Database Sample Schemas (HR/CO/SH/OE) - Copyright (c) 2023 Oracle and/or its affiliates. MIT License. https://github.com/oracle-samples/db-sample-schemas". Ship the upstream LICENSE.txt verbatim next to each converted dataset.

## microsoft/sql-server-samples, appended by claude-code/claude-fable-5-1 2026-09-02
* [Northwind](/datasets/northwind.md) - `samples/databases/northwind-pubs/instnwnd.sql`
* [pubs](/datasets/pubs.md) - `samples/databases/northwind-pubs/instpubs.sql`
* [AdventureWorks OLTP](/datasets/adventureworks-oltp.md) - `samples/databases/adventure-works/oltp-install-script/` and the `adventureworks` release .bak files
* [AdventureWorksDW](/datasets/adventureworks-dw.md) - `samples/databases/adventure-works/data-warehouse-install-script/`
* [AdventureWorksLT](/datasets/adventureworks-lt.md) - `adventureworks`/`adventureworks2012` release assets
* [WideWorldImporters](/datasets/wideworldimporters.md) - `wide-world-importers-v1.0` release .bak/.bacpac (Microsoft Learn "Terms of use" links this file); geodata inside is additionally public-domain Natural Earth / data.gov
* [WideWorldImportersDW](/datasets/wideworldimporters-dw.md) - same release

## DuckDB tpch/tpcds generators, appended by claude-code/claude-fable-5-1 2026-09-02
* [TPC-H](/datasets/tpc-h.md) and [TPC-DS](/datasets/tpc-ds.md) — DuckDB (MIT, "Copyright 2018-2026 Stichting DuckDB Foundation") runs the generators; its `extension/tpch/dbgen` and `extension/tpcds/dsdgen` subtrees are TPC-EULA-licensed, not MIT ([tool record](/tools/duckdb-tpch-tpcds-extensions.md), [TPC EULA](/licenses/tpc-eula.md)).
