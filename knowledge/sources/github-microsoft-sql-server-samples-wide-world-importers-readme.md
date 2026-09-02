---
type: Source
title: sql-server-samples wide-world-importers README.md
description: "Upstream readme for the WideWorldImporters sample: what it is, authors, update history, and that the databases are built from SSDT projects (wwi-ssdt, wwi-dw-ssdt) with an SSIS ETL project."
resource: https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/wide-world-importers
tags: [wideworldimporters, sql-server-samples]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/wide-world-importers/README.md
    title: README.md (wide-world-importers), 5,079 bytes
    accessed: 2026-09-02
    version: master (directory last touched 2026-08-31 by dependabot merges)
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/contents/samples/databases/wide-world-importers
    title: directory listing
    accessed: 2026-09-02
---

# What was read
The readme and the directory listing: `README.md`, `power-bi-dashboards/`, `sample-scripts/`, `workload-drivers/`, `wwi-app/`, `wwi-azure-functions/`, `wwi-dw-ssdt/`, `wwi-sample.sln`, `wwi-ssasmd/`, `wwi-ssdt/`, `wwi-ssis/`. There is **no `wwi-database-scripts/` directory** (the Learn catalog page links that name to `sample-scripts/`, which holds feature demos: always-encrypted, dynamic-data-masking, in-memory-oltp, load-sample-data-using-polybase, operational-analytics, polybase, row-level-security).

# Relevant excerpt
> WideWorldImporters is a wholesale company. Transactions and real-time analytics are performed in the database WideWorldImporters. The database WideWorldImportersDW is an OLAP database, focused on analytics.
> **Applies to:** SQL Server 2016 (or higher), Azure SQL Database ... **Authors:** Greg Low, Denzil Ribeiro, Jos de Bruijn, Robert Cain ... **Update history:** 21 June 2017 - restructure using SSDT; 25 May 2016 - initial revision
> The sample databases are created through SQL Server Data Tools projects in Visual Studio. ... To load all project in the solution, SQL Server Integration Services and SQL Server Analysis Services need to be installed on the machine.
> ## Disclaimers  The code included in this sample is not intended to be used for production purposes.

# What it was used to decide
[WideWorldImporters](/datasets/wideworldimporters.md), [WideWorldImportersDW](/datasets/wideworldimporters-dw.md), [conversion-path decision](/decisions/mssql-wideworldimporters-conversion-path.md).
