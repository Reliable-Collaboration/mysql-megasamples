---
type: License
title: Microsoft SQL Server Developer edition EULA (Linux container, ACCEPT_EULA)
description: Proprietary end-user terms accepted by ACCEPT_EULA=Y for mcr.microsoft.com/mssql/server; permits design/develop/test/demonstrate use and forbids production use; governs build-time use only, nothing licensed under it is redistributed.
resource: https://go.microsoft.com/fwlink/?linkid=857698
tags:
- license
- eula
- proprietary
- sql-server
- build-time-only
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://download.microsoft.com/download/4/F/7/4F7E81B0-7CEB-401D-BCFA-BF8BF73D868C/EULAs/License_Dev_Linux.rtf
  title: License_Dev_Linux.rtf (redirect target of fwlink 857698), 132,035 bytes
  accessed: "2026-09-02"
- resource: https://mcr.microsoft.com/api/v1/catalog/mssql/server/details?reg=mar
  title: MCR catalog text naming this link as the End-User Licensing Agreement and listing MSSQL_PID editions with "no production use rights"
  accessed: "2026-09-02"
stale_after: "2027-03-01"
---

# Where the text lives
`https://go.microsoft.com/fwlink/?linkid=857698` -> `License_Dev_Linux.rtf` ([source record](/sources/microsoft-sql-server-developer-linux-eula.md)); the served document is titled "MICROSOFT SOFTWARE LICENSE TERMS - MICROSOFT SQL SERVER 2017 DEVELOPER". The MCR catalog also links the general SQL Server product terms `https://www.microsoft.com/licensing/terms/productoffering/SQLServer/EAEAS#LicenseModel`.

# Key terms (verbatim)
> BY USING THE SOFTWARE, YOU ACCEPT THESE TERMS. IF YOU DO NOT ACCEPT THEM, DO NOT USE THE SOFTWARE.
> ... to design, develop, test and demonstrate your programs. You may not use the software on a device or server in a production environment.
> Your end users may access the software to perform acceptance tests on your programs.

# Obligations
* Acceptance is expressed by `ACCEPT_EULA=Y` in the build job only (a development/test conversion run), never in the published image.
* No SQL Server binaries, tools (`mssql-tools18`, `msodbcsql18`) or container layers are copied into the MySQL image; only the exported sample data (MIT) is.
* Not a data license: it does not affect the redistribution of Northwind/AdventureWorks/WWI data.

# Attribution
None: the software is used at build time only and never redistributed. The `native.yaml` workflow log and `PROVENANCE.md` for WideWorldImporters record "Exported from Microsoft SQL Server 2022 Developer Edition (mcr.microsoft.com/mssql/server) under its EULA (ACCEPT_EULA=Y), non-production build-time use."

# Applied to
* [SQL Server container tool](/tools/mssql-server-container.md) (build-time use for [WideWorldImporters](/datasets/wideworldimporters.md), [WideWorldImportersDW](/datasets/wideworldimporters-dw.md), optional validation for [AdventureWorks](/datasets/adventureworks-oltp.md)).
* Related proprietary tool terms: ODBC Driver 18 license for bcp/sqlcmd ([source](/sources/microsoft-odbc-driver-18-license.md), [tool](/tools/sqlcmd-bcp.md)).
