---
type: Source
title: instpubs.sql (pubs install script) - file analysis
description: Structural analysis of the pubs T-SQL install script performed in this session (encoding, tables, insert counts, user-defined types, trigger, view, procedures).
resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/instpubs.sql
tags:
- pubs
- script-analysis
- tsql
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/instpubs.sql
  title: instpubs.sql at master
  accessed: "2026-09-02"
  version: blob d887fd48cb06436a9aa2e988d00ba7b036dfd6d4, 125,718 bytes
---

# What was read
The whole file (125,718 bytes) downloaded with curl and analysed with `file`, `xxd`, `grep`, `iconv`.

# Relevant excerpt
* **Encoding**: no BOM, LF line endings, `file` says "Unicode text, UTF-8 text" but a byte scan finds **0 lines with non-ASCII bytes** (pure ASCII); longest line 1,912 chars. Header: `InstPubs.SQL - Creates the Pubs database`, `Copyright Microsoft, Inc. 1994 - 2000`.
* Unlike Northwind, this script **creates the database**: `USE master`, drops an existing `pubs`, `CREATE DATABASE pubs`, `CHECKPOINT`, `raiserror(...) with nowait` progress messages, `set dateformat mdy`. 75 `GO` batches.
* **User-defined types** via `sp_addtype`: `id varchar(11) NOT NULL`, `tid varchar(6) NOT NULL`, `empid char(9) NOT NULL`.
* **Tables (11)**: authors, publishers, titles, titleauthor, stores, sales, roysched, discounts, jobs, pub_info, employee.
* **INSERT rows per table** (one row per statement, counted): authors 23, publishers 8, titles 18, titleauthor 25, stores 6, sales 21, roysched 86, discounts 3, jobs 14, pub_info 8, employee 43.
* **Types**: varchar (18), char (22), int, smallint, tinyint, money (titles.price, titles.advance), decimal (roysched/discounts), datetime (titles.pubdate, employee.hire_date, sales.ord_date), bit (publishers? no: `employee`/`jobs`... one bit column), text (pub_info.pr_info), image (pub_info.logo). `jobs.job_id SMALLINT IDENTITY(1,1)`; no `IDENTITY_INSERT` is used (job rows are inserted with default identity in order).
* **CHECK constraints** with `LIKE` patterns: `au_id LIKE '[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]'`, `zip LIKE '[0-9][0-9][0-9][0-9][0-9]'`, `pub_id IN ('1389','0736','0877','1622','1756') OR pub_id LIKE '99[0-9][0-9]'`, `min_lvl >= 10`, `max_lvl <= 250`, and a multi-pattern check on `employee.emp_id`. Defaults include `DEFAULT ('UNKNOWN')`, `DEFAULT('USA')`, `DEFAULT (GETDATE())`.
* **Programmable objects**: trigger `employee_insupd` (validates job level against jobs.min_lvl/max_lvl, `raiserror('Job id 1 expects the default level of 10.',16,1)`), view `titleview`, procedures `byroyalty @percentage int`, `reptq1`, `reptq2`, `reptq3 @lolimit money, @hilimit money, @type char(12)`.
* **Binary data**: 8 `pub_info.logo` values are hex literals beginning `0x474946383961` (`GIF89a`), i.e. plain GIF files (no OLE wrapper). `pub_info.pr_info` is `text`.

# What it was used to decide
[pubs](/datasets/pubs.md); [conversion-path decision](/decisions/mssql-northwind-pubs-conversion-path.md).
