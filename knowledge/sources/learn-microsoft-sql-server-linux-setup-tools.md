---
type: Source
title: Microsoft Learn - Install sqlcmd and bcp command-line tools on Linux
description: Package names (mssql-tools18, msodbcsql18, unixodbc-dev), install commands, the ACCEPT_EULA=Y install requirement, x64/arm64 availability, /opt/mssql-tools18/bin path, and the pointer to go-sqlcmd.
resource: https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools
tags: [sqlcmd, bcp, mssql-tools18, docs]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools
    title: Install the sqlcmd and bcp SQL Server Command-Line Tools on Linux - SQL Server | Microsoft Learn (canonical linux/install-upgrade/setup-tools)
    accessed: "2026-09-02"
    version: ms.date 2026-05-07, updated_at 2026-08-21, git commit 5f29d7e8dd0206c096d3274256be8b1fbe5a38b0
---

# What was read
The full page.

# Relevant excerpt
> The **mssql-tools** package contains: **`sqlcmd`**: Command-line query utility. **`bcp`**: Bulk import-export utility.
> **`sqlcmd`** and **`bcp`** are available in **mssql-tools18** for `x64` and `arm64` architectures. For a modern alternative across Linux, macOS, and Windows, see go-sqlcmd utility.
> Ubuntu 24.04 is supported starting with SQL Server 2025 (17.x) CU 1. Ubuntu 22.04 is supported starting with SQL Server 2022 (16.x) CU 10.
> `sudo apt-get update` / `sudo apt-get install mssql-tools18 unixodbc-dev`
> If you run SQL Server in a Docker container, the SQL Server command-line tools are already included in the SQL Server Linux container image.
> If you're creating a container with the SQL Server command-line tools, you should add `ACCEPT_EULA=Y` to the installation command to silently accept the EULA, and not interrupt image creation. ... `sudo ACCEPT_EULA=Y apt-get install mssql-tools18 unixodbc-dev`
> Also locate and copy the **msodbcsql18** package, which is a dependency. The **msodbcsql18** package also has a dependency on **unixodbc-dev**.

The page gives no license URL for mssql-tools18 itself; the ODBC driver EULA is at aka.ms/odbc18eula (see its source record).

# What it was used to decide
[sqlcmd/bcp tool record](/tools/sqlcmd-bcp.md).
