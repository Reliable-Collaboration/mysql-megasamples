---
type: Dataset
title: pubs
description: Microsoft's tiny 11-table publishers/authors sample (SQL Server 2000 era) shipped as a 126 KB T-SQL script with inline data; MIT licensed.
resource: https://github.com/microsoft/sql-server-samples/blob/master/samples/databases/northwind-pubs/instpubs.sql
tags:
- tier-core
- mssql-origin
- script-translation
- mit
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
  title: instpubs.sql (blob d887fd48cb06436a9aa2e988d00ba7b036dfd6d4)
  accessed: "2026-09-02"
  version: master, 125,718 bytes
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/license.txt
  title: sql-server-samples license.txt (MIT)
  accessed: "2026-09-02"
stale_after: "2027-03-01"
---

# Identity
`pubs`, the book-publisher sample from SQL Server 6.5-2000. Upstream: `samples/databases/northwind-pubs/instpubs.sql`. Proposed MySQL database name: **`pubs`**. Single `dbo` schema.

# Source artifact
* URL `https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/instpubs.sql`, blob SHA `d887fd48cb06436a9aa2e988d00ba7b036dfd6d4`, 125,718 bytes, plain ASCII (no BOM, LF), no auth. No checksum published upstream. **Verified 2026-09-02** at first fetch: sha256 `c66479d429f482ef788290dd94bb315f2277327765f480b2b21be6f359eb4bad`, 125,718 bytes, pinned in `manifest.yaml` ([source record](/sources/github-microsoft-sql-server-samples-instpubs-sql.md)).

# Native format and friendlier forms
The T-SQL script is the only and friendliest form: it creates the database (`USE master`, `DROP`/`CREATE DATABASE pubs`), defines three UDTs with `sp_addtype`, creates 11 tables and inserts all rows inline. No SQL Server needed.

# Shape
11 tables, 255 rows total (INSERT counts, verified): authors 23, publishers 8, titles 18, titleauthor 25, stores 6, sales 21, roysched 86, discounts 3, jobs 14, pub_info 8, employee 43. `pub_info.logo` holds 8 GIF images (hex literals starting `GIF89a`), `pub_info.pr_info` is `text`. **No non-ASCII bytes anywhere** - pubs cannot expose encoding mistakes; Northwind does.

# Conversion path
Script translation without SQL Server, together with Northwind: [decision](/decisions/mssql-northwind-pubs-conversion-path.md).

# Type-mapping hazards
* UDTs `id varchar(11)`, `tid varchar(6)`, `empid char(9)` -> inline the base types.
* `money` (titles.price, advance) -> `DECIMAL(19,4)`; `decimal` in roysched/discounts; `tinyint`, `smallint`, `int`; `datetime` -> `DATETIME`; `bit` -> `TINYINT(1)`; `text` -> `TEXT`; `image` -> `BLOB`.
* CHECK constraints use T-SQL `LIKE '[0-9][0-9][0-9]-...'` character-class patterns - MySQL `LIKE` has no classes; rewrite as `REGEXP '^[0-9]{3}-[0-9]{2}-[0-9]{4}$'` (MySQL 8.0.16+ enforces CHECK) or drop with a note. `pub_id IN (...) OR pub_id LIKE '99[0-9][0-9]'` likewise -> `REGEXP '^99[0-9]{2}$'`. `employee.emp_id` has a multi-pattern CHECK.
* `DEFAULT (GETDATE())` -> `DEFAULT CURRENT_TIMESTAMP`; `jobs.job_id SMALLINT IDENTITY(1,1) PRIMARY KEY CLUSTERED` -> `AUTO_INCREMENT`.
* `set dateformat mdy` + `'mm/dd/yyyy'` literals -> ISO dates.

# Programmable objects
* Trigger `employee_insupd` (INSERT/UPDATE, checks job_lvl within jobs.min_lvl..max_lvl, raises error) -> port as two MySQL triggers (BEFORE INSERT, BEFORE UPDATE) using `SIGNAL SQLSTATE '45000'`.
* View `titleview` -> port.
* Procedures `byroyalty`, `reptq1`, `reptq2`, `reptq3` -> port (`reptq*` use `COMPUTE`/`compute by`? **Inferred** - the SQL Server 2000 versions use `COMPUTE BY` which has no MySQL equivalent; if so, stub them as plain grouped selects and note the deviation).

# Indexing
PKs on all tables (composite on titleauthor, sales, roysched? roysched has none - keep as in script), FKs as in script (`REFERENCES` inline), nonclustered indexes `auidind`, `titleidind` on titleauthor.

# Tests and expected values
Row counts above; `SELECT COUNT(*) FROM sales` = 21; `SELECT SUM(qty) FROM sales` = 493 (**inferred**, verify); `SELECT LENGTH(logo) FROM pub_info WHERE pub_id='0736'` equals the hex literal length/2 from the script; trigger test: inserting an employee with `job_lvl` outside the job's range must fail.

# Tier assignment
**core** - 126 KB source, <1 MB loaded.

# License and attribution
MIT via repository `license.txt` ([license record](/licenses/mit.md)); the script header says `Copyright Microsoft, Inc. 1994 - 2000`. No personal data (fictional), no share-alike.

# Open questions
None blocking. Whether `reptq1-3` use `COMPUTE BY` should be checked when the executor reads the procedure bodies (research grep did not extract them).
