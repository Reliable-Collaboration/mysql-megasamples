---
type: Source
title: Microsoft Artifact Registry - mssql/server image catalog entry, tag list and manifests
description: The MCR "About" text for mcr.microsoft.com/mssql/server (featured tags, requirements, environment variables, EULA link, MSSQL_PID values) read via the MCR catalog API, plus the live tag list and the image manifests/configs for 2022-latest and 2025-latest.
resource: https://mcr.microsoft.com/en-us/artifact/mar/mssql/server/about
tags: [sql-server, container, mcr]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://mcr.microsoft.com/api/v1/catalog/mssql/server/details?reg=mar
    title: MCR catalog details API (the JSON behind the About page; lastModifiedDate 2026-08-13)
    accessed: 2026-09-02
  - resource: https://mcr.microsoft.com/v2/mssql/server/tags/list
    title: OCI/Docker registry tags list (274 tags on 2026-09-02)
    accessed: 2026-09-02
  - resource: https://mcr.microsoft.com/v2/mssql/server/manifests/2022-latest
    title: manifests for 2022-latest and 2025-latest plus their config blobs
    accessed: 2026-09-02
stale_after: 2027-03-01
---

# What was read
The HTML About page is JavaScript-rendered (WebFetch returned only the footer), so the same content was read from the catalog API, and the registry v2 API was queried for tags and manifests.

# Relevant excerpt (catalog "About" text)
> Official Ubuntu-based container images for Microsoft SQL Server for Docker Engine.
> | SQL Server 2025 (17.x) | `2025-latest` | `docker pull mcr.microsoft.com/mssql/server:2025-latest` | ... | SQL Server 2022 (16.x) | `2022-latest` | ... | SQL Server 2019 (15.x) | `2019-latest` | ... | SQL Server 2017 (14.x) | `2017-latest` |
> Starting with **SQL Server 2022 (16.x) CU 14** and **SQL Server 2019 (15.x) CU 28**, container images include the mssql-tools18 package. The previous directory `/opt/mssql-tools/bin` is being phased out. The directory for Microsoft ODBC 18 tools is `/opt/mssql-tools18/bin`
> ODBC driver version 18 is designed with an *encryption-first* approach ... To connect without encryption, the sample command is: `sqlcmd -S <ip address,port> -U <login_name> -P <password> -No`
> This image requires Docker Engine 1.8 or later ... At least 2 GB of RAM (3.25 GB before SQL Server 2017 CU2).
> Set the following environment flags: `"ACCEPT_EULA=Y"`, `"MSSQL_SA_PASSWORD=<password>"`, `"MSSQL_PID=<your_product_id | edition_name> (default: Developer)"`
> `ACCEPT_EULA` confirms your acceptance of the End-User Licensing Agreement (https://go.microsoft.com/fwlink/?linkid=857698).
> `MSSQL_PID` ... Acceptable values for SQL Server 2025: 1. Evaluation (free, no production use rights, 180-day limit) 1. EnterpriseDeveloper (free, no production use rights) 1. StandardDeveloper (free, no production use rights) 1. Express (free) 1. Standard (PAID) 1. Enterprise (PAID) ... 1. Enterprise Core (PAID) ...
> Password ... at least eight characters from at least three of these four categories: uppercase letters, lowercase letters, numbers, and non-alphanumeric symbols.
> `docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<password>" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest`

Catalog metadata: publisher Microsoft; licenseUrl `https://www.microsoft.com/licensing/terms/productoffering/SQLServer/EAEAS#LicenseModel`; documentationLink `https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-deployment`; `architectures: []` (not populated).

# Tags and manifests (measured 2026-09-02)
* Floating tags present: `2017-latest`, `2017-latest-ubuntu`, `2019-latest`, `2022-latest`, `2025-latest`, `latest`, `latest-ubuntu`.
* Pinned CU tags: 71 for 2022 (newest `2022-CU26-ubuntu-20.04`, `2022-CU26-ubuntu-22.04`); 24 for 2025 (newest `2025-CU8-ubuntu-22.04`, `2025-CU8-ubuntu-24.04`); 77 for 2019 (newest `2019-CU32-GDR8-ubuntu-20.04`).
* `2022-latest` manifest is a single-platform Docker v2 manifest; config blob says `architecture: amd64`, `os: linux`, label `com.microsoft.version` = `16.0.4265.3`, created 2026-07-08; compressed layers total 624,870,837 bytes.
* `2025-latest`: `amd64`/`linux`, version `17.0.4075.5`, created 2026-07-23; compressed layers 632,528,872 bytes.
* No arm64 manifest exists for either tag (no manifest list at all).

# What it was used to decide
[SQL Server container tool record](/tools/mssql-server-container.md); [sqlcmd/bcp tool record](/tools/sqlcmd-bcp.md).
