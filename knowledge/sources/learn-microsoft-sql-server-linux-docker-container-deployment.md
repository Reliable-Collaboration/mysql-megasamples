---
type: Source
title: Microsoft Learn - Deploy and connect to SQL Server Linux containers
description: Platform support statement (x86-64 only, emulation unsupported), sqlcmd path inside the container, tags, ACCEPT_EULA/MSSQL_SA_PASSWORD/MSSQL_PID usage, and the production-license statement.
resource: https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-deployment
tags: [sql-server, container, docs]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-deployment
    title: Deploy and Connect to SQL Server Linux Containers - SQL Server | Microsoft Learn (canonical linux/containers/deploy)
    accessed: 2026-09-02
    version: ms.date 2026-05-07, updated_at 2026-06-12, git commit 2b0a712a054f0c7f4addacee8956f9eb1019999a
---

# What was read
The full page (view=sql-server-ver17).

# Relevant excerpt
> SQL Server container images are supported only on Linux hosts running on Intel and AMD x86-64 CPUs. Emulation or translation environments (for example, Rosetta 2, Prism, or QEMU) aren't tested or supported.
> Starting with SQL Server 2017 (14.x), the SQL Server command-line tools are included in the container image. ... `/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P '<YourPassword>'`
> Newer versions of **`sqlcmd`** are secure by default. ... you can add the `-No` option to **`sqlcmd`** to specify that encryption is optional, not mandatory.
> You can retrieve a list of all available tags for mssql/server at https://mcr.microsoft.com/v2/mssql/server/tags/list.
> The `SA_PASSWORD` environment variable is deprecated. Use `MSSQL_SA_PASSWORD` instead.
> `docker run -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=<password>' -p 1401:1433 -d mcr.microsoft.com/mssql/server:2025-latest`
> The quickstart in the previous section runs the free Developer edition of SQL Server from the Microsoft Artifact Registry. ... You can only use SQL Server in a production environment if you have a valid license.
> By passing the value `Y` to the environment variable `ACCEPT_EULA` and an edition value to `MSSQL_PID`, you express that you have a valid and existing license for the edition and version of SQL Server that you intend to use.
> Web edition isn't available in SQL Server 2025 (17.x) and later versions.

Also: `docker run -e PAL_PROGRAM_INFO=1 --name sqlver -ti mcr.microsoft.com/mssql/server:2022-latest && docker rm sqlver` prints the build; RHEL images exist under `mcr.microsoft.com/mssql/rhel/server`.

# What it was used to decide
[SQL Server container tool record](/tools/mssql-server-container.md).
