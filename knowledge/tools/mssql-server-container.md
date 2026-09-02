---
type: Tool
title: SQL Server Linux container (mcr.microsoft.com/mssql/server)
description: Microsoft's official Ubuntu-based SQL Server image, used only at build time to restore WideWorldImporters .bak files (and optionally AdventureWorks .bak) before exporting to MySQL; Developer edition by default, EULA acceptance required, amd64 only, 2 GB RAM minimum.
resource: https://mcr.microsoft.com/en-us/artifact/mar/mssql/server/about
tags: [tool, sql-server, container, build-time-only, proprietary]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://mcr.microsoft.com/api/v1/catalog/mssql/server/details?reg=mar
    title: MCR catalog "About" text, tags list and manifests (see source record)
    accessed: "2026-09-02"
  - resource: https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-deployment
    title: Deploy and connect to SQL Server Linux containers (Learn)
    accessed: "2026-09-02"
  - resource: https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver17
    title: "Quickstart: run SQL Server Linux container images with Docker (Learn)"
    accessed: "2026-09-02"
  - resource: https://go.microsoft.com/fwlink/?linkid=857698
    title: End-User License Agreement (License_Dev_Linux.rtf)
    accessed: "2026-09-02"
stale_after: "2027-03-01"
---

# What it is
`mcr.microsoft.com/mssql/server`, "Official Ubuntu-based container images for Microsoft SQL Server for Docker Engine" ([MCR source](/sources/mcr-microsoft-mssql-server-catalog.md)). Used in this project only inside the build pipeline for datasets that exist solely as `.bak` files ([WideWorldImporters](/datasets/wideworldimporters.md), [WideWorldImportersDW](/datasets/wideworldimporters-dw.md); optionally to validate hierarchyid/geography decoding for [AdventureWorks](/datasets/adventureworks-oltp.md)). It is never part of the shipped MySQL image.

# Facts
* **Tags** (2026-09-02): floating `2025-latest`, `2022-latest`, `2019-latest`, `2017-latest`, `latest`; pinned examples `2022-CU26-ubuntu-22.04`, `2025-CU8-ubuntu-24.04`, `2019-CU32-GDR8-ubuntu-20.04`. `2022-latest` config = version `16.0.4265.3` (built 2026-07-08), `2025-latest` = `17.0.4075.5` (2026-07-23). Full list at `https://mcr.microsoft.com/v2/mssql/server/tags/list`. Recommend pinning a CU tag (e.g. `2022-CU26-ubuntu-22.04`) in the build.
* **Platform**: manifests are single-platform `linux/amd64`; no arm64 image exists. Learn: "SQL Server container images are supported only on Linux hosts running on Intel and AMD x86-64 CPUs. Emulation or translation environments (for example, Rosetta 2, Prism, or QEMU) aren't tested or supported." Consequence: the WWI conversion step must run on an amd64 builder (GitHub-hosted ubuntu runners are amd64); Apple-silicon developers cannot run it natively.
* **Size**: compressed layers ~625 MB (2022) / ~633 MB (2025).
* **Requirements**: "At least 2 GB of RAM" and "At least 2 GB of disk space" (quickstart); Docker Engine 1.8+.
* **Mandatory environment**: `ACCEPT_EULA=Y` ("Set the ACCEPT_EULA variable to any value to confirm your acceptance of the End-User Licensing Agreement. Required setting"), `MSSQL_SA_PASSWORD=<password>` (>= 8 chars from 3 of 4 classes; `SA_PASSWORD` deprecated), optional `MSSQL_PID` (default Developer; 2025 values include `EnterpriseDeveloper`/`StandardDeveloper` "free, no production use rights", `Express` free, `Evaluation` 180-day). Example: `docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<password>" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest`.
* **License**: EULA fwlink 857698 -> `License_Dev_Linux.rtf` ("MICROSOFT SQL SERVER 2017 DEVELOPER" terms): "to design, develop, test and demonstrate your programs. You may not use the software on a device or server in a production environment." Learn: "You can only use SQL Server in a production environment if you have a valid license." A one-off conversion job in CI is development/test use. See [EULA license record](/licenses/microsoft-sql-server-developer-eula.md).
* **Tools inside the image**: `/opt/mssql-tools18/bin/sqlcmd` and `bcp` (mssql-tools18) are included from 2022 CU14 / 2019 CU28 onward; ODBC 18 tools default to encrypted connections - use `sqlcmd -No` / `bcp -Yo` (bcp 18) or `-C`/`-u` trust-server-certificate flags against the self-signed container certificate ([sqlcmd/bcp record](/tools/sqlcmd-bcp.md)).
* **Restore pattern** (Learn): copy the .bak to `/var/opt/mssql/backup/`, then `RESTORE DATABASE [WideWorldImporters] FROM DISK='/var/opt/mssql/backup/WideWorldImporters-Standard.bak' WITH MOVE 'WWI_Primary' TO '/var/opt/mssql/data/WideWorldImporters.mdf', MOVE 'WWI_UserData' TO '...UserData.ndf', MOVE 'WWI_Log' TO '...ldf', FILE=1, NOUNLOAD, STATS=5` (logical file names **inferred**; list them first with `RESTORE FILELISTONLY`). The Full .bak additionally has an `WWI_InMemory_Data_1` filestream container (inferred) - prefer the Standard .bak.

# Limits
* amd64-only; ~1.3 GB image pull per build unless cached; 2 GB RAM.
* `MSSQL_SA_PASSWORD` visible in `ps`; use a throwaway password in CI.
* The EULA document served is titled for SQL Server 2017 even for 2022/2025 images (inferred to be equivalent; do not quote it as the 2025 text).
* Startup takes ~10-30 s; poll with `sqlcmd -Q "SELECT 1"` before restoring (inferred practice).

# Used by
[WideWorldImporters conversion decision](/decisions/mssql-wideworldimporters-conversion-path.md); fallback in [AdventureWorks decision](/decisions/mssql-adventureworks-conversion-path.md).
