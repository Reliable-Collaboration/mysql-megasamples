---
type: Source
title: Microsoft Learn - AdventureWorks sample databases (install and configure)
description: Official download table of AdventureWorks OLTP/DW/LT .bak files by SQL Server version (2008R2-2025), restore instructions, and the pointer to the OLTP/DW install-script zips.
resource: https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure
tags: [adventureworks, docs]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure
    title: AdventureWorks sample databases - SQL Server | Microsoft Learn
    accessed: "2026-09-02"
    version: ms.date 2026-03-16, updated_at 2026-08-27, git commit 0e15016bdadf2052263550047d86e9d8eef54be5
---

# What was read
The full page (view=sql-server-ver17).

# Relevant excerpt
> - **OLTP** data works for most typical online transaction processing workloads. - **Data Warehouse (DW)** data works for data warehousing workloads. - **Lightweight (LT)** data is a lightweight and pared down version of the **OLTP** sample.

Download table rows: 2025, 2022, 2019, 2017, 2016, 2016_EXT (OLTP/DW only), 2014, 2012, 2008R2 (OLTP/DW only; LT "N/A" for 2008R2 in the table although the 2008r2 release has an lt .bak). Links go to the GitHub releases `adventureworks`, `adventureworks2012`, `adventureworks2008r2`. No file sizes and no checksums are listed on the page.

> ## Scripts for creating a database  Instead of restoring a database, you can use scripts to create the `AdventureWorks` databases, regardless of version. - AdventureWorks OLTP scripts zip - AdventureWorks DW scripts zip

Linux restore example: `RESTORE DATABASE [AdventureWorks2025] FROM DISK = '/var/opt/mssql/backup/AdventureWorks2025.bak' WITH MOVE 'AdventureWorks2025' TO '/var/opt/mssql/data/AdventureWorks2025_Data.mdf', MOVE 'AdventureWorks2025_log' TO '/var/opt/mssql/data/AdventureWorks2025_log.ldf', FILE = 1, NOUNLOAD, STATS = 5;`. No LT script is offered; no license statement on the page.

# What it was used to decide
[AdventureWorks OLTP](/datasets/adventureworks-oltp.md), [DW](/datasets/adventureworks-dw.md), [LT](/datasets/adventureworks-lt.md); [conversion-path decision](/decisions/mssql-adventureworks-conversion-path.md).
