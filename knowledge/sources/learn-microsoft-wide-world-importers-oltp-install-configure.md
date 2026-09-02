---
type: Source
title: Microsoft Learn - Install and configure WideWorldImporters (OLTP)
description: Prerequisites (SQL Server 2016+; Full version needs Evaluation/Developer/Enterprise), download pointer, restore/bacpac import steps, and the post-install procedures for full-text, audit and RLS.
resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-oltp-install-configure
tags: [wideworldimporters, docs, install]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-oltp-install-configure
    title: Install and configure WideWorldImporters sample database - SQL Server | Microsoft Learn
    accessed: "2026-09-02"
    version: ms.date 2018-04-04, updated_at 2025-11-25, git commit 46e3eed3e68637ec3da44585e2871a0f33bf0dad
---

# What was read
The full page.

# Relevant excerpt
> SQL Server 2016 (or higher) or Azure SQL Database. For the Full version of the sample, use SQL Server Evaluation/Developer/Enterprise Edition.
> Download the sample WideWorldImporters database backup/bacpac that corresponds to your edition of SQL Server or Azure SQL Database.
> Source code to recreate the sample database is available from the following location. Note that recreating the sample will result in slight differences in the data, since there is a random factor in the data generation
> Row-Level Security is not enabled by default in the bacpac download of WideWorldImporters. To enable Row-Level Security in the database, run ... `EXECUTE [Application].[Configuration_ApplyRowLevelSecurity]`
> The sample database can make use of Full-Text Indexing. However, that feature is not installed by default ... `EXECUTE Application.Configuration_ApplyFullTextIndexing`

# What it was used to decide
[WideWorldImporters](/datasets/wideworldimporters.md); [conversion-path decision](/decisions/mssql-wideworldimporters-conversion-path.md) (Standard .bak restores on the Developer-edition container without needing Enterprise-only features; the Full .bak also restores because Developer edition has Enterprise features - the page ties "Full" to Evaluation/Developer/Enterprise).
