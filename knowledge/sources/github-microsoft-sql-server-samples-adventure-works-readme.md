---
type: Source
title: sql-server-samples adventure-works README.md
description: Upstream readme describing the AdventureWorks install scripts versus version-specific .bak files, the 2012-2022 "no significant changes" statement and the 2025 changes (Query Store, ADR, optimized locking, adjusted dates).
resource: https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/adventure-works
tags: [adventureworks, sql-server-samples]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/README.md
    title: README.md (adventure-works)
    accessed: "2026-09-02"
    version: master, 7,158 bytes; directory last substantively changed by commit b47eadc852 "AdventureWorks 2025 updates" 2025-11-14
---

# What was read
`samples/databases/adventure-works/README.md` (7,158 bytes) and the GitHub contents listing of the directory (`README.md`, `data-warehouse-install-script/`, `oltp-install-script/`). Commit history of the two script directories was read through the GitHub commits API: `b47eadc852` (2025-11-14, "AdventureWorks 2025 updates"), `f23ab4cf85` (2024-06-27), `9179a8e432` (2023-08-04, "Update line endings for UTF-16 LE encoded files"), `378a9a04af` (2023-08-03, "Fix missing characters").

# Relevant excerpt
> `AdventureWorks` has not seen any significant changes since the 2012 version. The only differences between the various versions of `AdventureWorks` are the name of the database and the database compatibility level.

> ### Changes in SQL Server 2025
> To coincide with the release of SQL Server 2025, the `AdventureWorks` database has been modified to take advantage of recent Database Engine features:
> - Query Store is enabled
> - Accelerated database recovery (ADR) is enabled
> - Optimized locking is enabled
> - Dates have been adjusted

> ## Prerequisites
> FILESTREAM must be installed in your SQL Server instance.

> The install scripts create the sample database to have the database compatibility of your current version of SQL Server. ... you can use either the `AdventureWorks` or `AdventureWorksDW` install script on any version of SQL Server including preview versions ...

> When installing from a script, the default database name is `AdventureWorks` or `AdventureWorksDW`.

Install instructions point at `oltp-install-script/instawdb.sql` (or the release asset `AdventureWorks-oltp-install-script.zip`) and `data-warehouse-install-script/instawdbdw.sql` (or `AdventureWorksDW-data-warehouse-install-script.zip`). Backups are "version-specific. You can restore each backup to its respective version of SQL Server, or a later version."

# What it was used to decide
[AdventureWorks OLTP](/datasets/adventureworks-oltp.md), [AdventureWorks DW](/datasets/adventureworks-dw.md), [AdventureWorks LT](/datasets/adventureworks-lt.md), [conversion-path decision](/decisions/mssql-adventureworks-conversion-path.md). The "dates have been adjusted" statement explains why the current CSVs carry 2018-2025 dates instead of the classic 2011-2014 ones.
