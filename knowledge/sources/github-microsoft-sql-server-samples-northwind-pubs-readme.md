---
type: Source
title: sql-server-samples northwind-pubs readme.md
description: Directory readme for the Northwind and pubs install scripts; states they were created for SQL Server 2000 and lists the directory contents.
resource: https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/northwind-pubs
tags:
- northwind
- pubs
- sql-server-samples
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/readme.md
  title: readme.md (northwind-pubs)
  accessed: "2026-09-02"
  version: master; directory last changed by commit c6f4e6fb7a 2024-06-27 "Made tables script more readable for northwind-pubs"
- resource: https://api.github.com/repos/microsoft/sql-server-samples/contents/samples/databases/northwind-pubs
  title: GitHub contents API listing (sizes and blob SHAs)
  accessed: "2026-09-02"
---

# What was read
The directory readme (1,514 bytes; note lowercase `readme.md`, `README.md` 404s) and the GitHub contents API listing of `samples/databases/northwind-pubs/`.

Directory contents (name, size in bytes, blob SHA):
* `instnwnd.sql` 1,049,720 (ae61e5631d7f03029ec15213ce672b45ceb7e629)
* `instnwnd (Azure SQL Database).sql` 1,049,643 (f9121728b14864f1ed3dda42bc741db10d88d30b) - differs from `instnwnd.sql` only in trailing whitespace on constraint lines (verified by `diff`).
* `instpubs.sql` 125,718 (d887fd48cb06436a9aa2e988d00ba7b036dfd6d4)
* `readme.md` 1,514

# Relevant excerpt
> This folder contains scripts to create and load the *Northwind* (`instnwnd.sql`) and *pubs* (`instpubs.sql`) sample databases.
> These scripts were originally created for SQL Server 2000.

The readme only says how to run them in SSMS/SSDT; it carries no row counts, no data dictionary and no license statement of its own (the repo-level `license.txt` applies).

# What it was used to decide
[Northwind](/datasets/northwind.md), [pubs](/datasets/pubs.md), [conversion-path decision](/decisions/mssql-northwind-pubs-conversion-path.md).
