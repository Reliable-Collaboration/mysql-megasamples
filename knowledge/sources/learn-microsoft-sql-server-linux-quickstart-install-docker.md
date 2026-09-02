---
type: Source
title: "Microsoft Learn - Quickstart: run SQL Server Linux container images with Docker"
description: Prerequisites (2 GB RAM, 2 GB disk, x86-64 only), docker pull/run commands, ACCEPT_EULA and MSSQL_SA_PASSWORD parameter table, Developer edition default, and the go-sqlcmd `sqlcmd create mssql --accept-eula` alternative.
resource: https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker
tags: [sql-server, container, docs]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver17
    title: "Docker: Run Containers for SQL Server on Linux - SQL Server | Microsoft Learn (canonical linux/install-upgrade/quickstart-install-docker)"
    accessed: 2026-09-02
    version: ms.date 2026-05-07, updated_at 2026-07-20, git commit e3d58b450af7ac2150dd72e0fbdaeaaabf5dc6ad
---

# What was read
The full page (71.6 KB of markdown, saved by the tool and grepped).

# Relevant excerpt
> SQL Server container images are supported only on Linux hosts running on Intel and AMD x86-64 CPUs. Emulation or translation environments (for example, Rosetta 2, Prism, or QEMU) aren't tested or supported.
> - At least 2 GB of disk space. - At least 2 GB of RAM.
> `docker pull mcr.microsoft.com/mssql/server:2022-latest`
> `docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<password>" ... mcr.microsoft.com/mssql/server:2022-latest`
> | `-e "ACCEPT_EULA=Y"` | Set the `ACCEPT_EULA` variable to any value to confirm your acceptance of the End-User Licensing Agreement. Required setting for the SQL Server image. |
> | `-e "MSSQL_SA_PASSWORD=<password>"` | Specify your own strong password that is at least eight characters and meets the Password policy. Required setting for the SQL Server image. |
> By default, this quickstart creates a container with the Developer edition of SQL Server. The process for running production editions in containers is slightly different.
> **`sqlcmd`** doesn't currently support the `MSSQL_PID` parameter when creating containers. If you use the **`sqlcmd`** instructions in this quickstart, you create a container with the Developer edition
> `sqlcmd create mssql --tag 2019-latest --hostname sql1 --name sql1 --port 1433 --accept-eula`
> As a final step, change your SA password in a production environment, because the `MSSQL_SA_PASSWORD` is visible in `ps -eax` output

# What it was used to decide
[SQL Server container tool record](/tools/mssql-server-container.md).
