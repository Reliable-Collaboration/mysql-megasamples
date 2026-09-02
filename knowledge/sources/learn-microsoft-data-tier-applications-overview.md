---
type: Source
title: Microsoft Learn - Data-tier applications (DAC) overview (.bacpac / .dacpac)
description: Defines .bacpac as an encapsulation of schema plus data ("compressed but not encrypted"), importable only into a new database via SqlPackage/SSMS/VS Code; no documented way to read the data without a SQL engine.
resource: https://learn.microsoft.com/en-us/sql/relational-databases/data-tier-applications/data-tier-applications
tags: [bacpac, dacfx, docs]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/relational-databases/data-tier-applications/data-tier-applications
    title: Data-Tier Applications (DAC) Overview - SQL Server | Microsoft Learn (canonical tools/sql-database-projects/concepts/data-tier-applications/overview)
    accessed: "2026-09-02"
    version: ms.date 2026-03-13, updated_at 2026-07-21, git commit 4f43f815712bfe38231ce50021bfd788a7269693
---

# What was read
The full page.

# Relevant excerpt
> The `.bacpac` file format is a related artifact that by default encapsulates the database schema and the data stored in the database. Objects in the `.bacpac` database model are limited to the surface area of Azure SQL Database. The primary use case for a `.bacpac` is to move a database from one server to another ... and archiving an existing database in an open format.
> **Import** - the user can import a `.bacpac` file into a new database. For more information, see SqlPackage import
> The data contained in these files is compressed but not encrypted.
> The following tools support the `.dacpac` and `.bacpac` formats: SqlPackage CLI, SQL Server Management Studio, Data-tier Application (DACPAC and BACPAC) import and export (VS Code mssql extension)

The page does not describe the internal layout (zip with model.xml and per-table data files) - that remains inferred; see the open question.

# What it was used to decide
[bacpac readability open question](/questions/mssql-bacpac-readable-without-sql-server.md); [WideWorldImporters](/datasets/wideworldimporters.md) "friendlier forms" section.
