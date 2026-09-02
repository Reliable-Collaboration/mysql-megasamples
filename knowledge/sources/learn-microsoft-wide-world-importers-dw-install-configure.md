---
type: Source
title: Microsoft Learn - Install and configure WideWorldImportersDW
description: Prerequisites (SQL Server 2016 SP1+; full version needs Developer/Enterprise), download pointer, restore/bacpac steps, PolyBase configuration.
resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-dw-install-configure
tags: [wideworldimporters-dw, docs, install]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-dw-install-configure
    title: Install & configure WideWorldImportersDW sample database - SQL Server | Microsoft Learn
    accessed: "2026-09-02"
    version: ms.date 2023-08-01, updated_at 2026-07-20, git commit 2ceb7c07640735a9c49dbb6ff1de511aceead449
---

# What was read
The full page.

# Relevant excerpt
> SQL Server 2016 with Service Pack 1 (and later versions), or Azure SQL Database. To use the full version of the sample, use SQL Server Developer or Enterprise editions.
> Source code to recreate the sample database is available from wide-world-importers-source. Data population is based on ETL from the OLTP database (`WideWorldImporters`).
> ## Configure PolyBase ... `EXECUTE [Application].[Configuration_ApplyPolyBase];`

# What it was used to decide
[WideWorldImportersDW](/datasets/wideworldimporters-dw.md); [conversion-path decision](/decisions/mssql-wideworldimporters-conversion-path.md).
