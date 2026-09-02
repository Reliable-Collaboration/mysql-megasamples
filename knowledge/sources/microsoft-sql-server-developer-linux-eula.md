---
type: Source
title: Microsoft SQL Server Developer (Linux) EULA - License_Dev_Linux.rtf
description: The End-User License Agreement that ACCEPT_EULA=Y accepts for the mssql/server container image (fwlink 857698); Developer edition may be used to design, develop, test and demonstrate only, not in a production environment.
resource: https://go.microsoft.com/fwlink/?linkid=857698
tags: [license, eula, sql-server, container]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://download.microsoft.com/download/4/F/7/4F7E81B0-7CEB-401D-BCFA-BF8BF73D868C/EULAs/License_Dev_Linux.rtf
    title: License_Dev_Linux.rtf (302 redirect target of https://go.microsoft.com/fwlink/?linkid=857698), 132,035 bytes, RTF
    accessed: "2026-09-02"
stale_after: "2027-03-01"
---

# What was read
The fwlink (linked from the MCR About text and the Learn container pages as "End-User Licensing Agreement") redirects (HTTP 302) to an RTF file; it was downloaded and de-RTF'd with a small Python script to read the text.

# Relevant excerpt
> MICROSOFT SOFTWARE LICENSE TERMS ... MICROSOFT SQL SERVER 2017 DEVELOPER
> BY USING THE SOFTWARE, YOU ACCEPT THESE TERMS. IF YOU DO NOT ACCEPT THEM, DO NOT USE THE SOFTWARE.
> ... to design, develop, test and demonstrate your programs. You may not use the software on a device or server in a production environment.
> Your end users may access the software to perform acceptance tests on your programs.

Observation: the document served today is titled for **SQL Server 2017 Developer** even though the same link is used by the 2019/2022/2025 images; the MCR catalog additionally links the general SQL Server product terms (`https://www.microsoft.com/licensing/terms/productoffering/SQLServer/EAEAS#LicenseModel`). **Inferred:** the edition-specific terms for 2022/2025 Developer are materially the same ("no production use rights" per the MSSQL_PID table), but the executor should not quote this RTF as the 2025 EULA without checking the product-terms page.

# What it was used to decide
[SQL Server container tool record](/tools/mssql-server-container.md); [SQL Server Developer EULA license record](/licenses/microsoft-sql-server-developer-eula.md). Build-time use of the container to convert sample data is development/test use, which the terms permit; the resulting MySQL image must not contain or run SQL Server.
