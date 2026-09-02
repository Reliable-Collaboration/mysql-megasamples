---
type: Source
title: Microsoft ODBC Driver 18 for SQL Server - license terms (LICENSE18.TXT)
description: The proprietary Microsoft license accepted with ACCEPT_EULA=Y when installing msodbcsql18/mssql-tools18; permits install/use for development and test, contains distributable-code clauses, no production-use prohibition stated.
resource: https://aka.ms/odbc18eula
tags: [license, eula, odbc, mssql-tools18]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://download.microsoft.com/download/1/7/c/17c9447c-dfa6-49e0-abdf-90095a85d986/odbc/eula18/LICENSE18.TXT
    title: LICENSE18.TXT (301 redirect target of https://aka.ms/odbc18eula), 11.9 KB
    accessed: 2026-09-02
stale_after: 2027-03-01
---

# What was read
The license text via WebFetch summary (binary/octet-stream response, 11.9 KB).

# Relevant excerpt (as summarised by the fetch; title verbatim)
> MICROSOFT SOFTWARE LICENSE TERMS  MICROSOFT ODBC DRIVER 18 FOR SQL SERVER
> You may install and use any number of copies of the software to develop and test your applications.
Distributable-code section present (object code may be distributed if the application adds "significant primary functionality"); no explicit prohibition on production use; no version/date stated; **bcp and sqlcmd (mssql-tools18) are not named in this document** - the tools package carries its own EULA prompt at install time whose text was not located (open question in the tool record).

# What it was used to decide
[sqlcmd/bcp tool record](/tools/sqlcmd-bcp.md): the ODBC-based tools are proprietary and must not be redistributed inside the public MySQL image; they are build-time only. The MIT go-sqlcmd is the redistributable alternative for queries (not for bulk export).
