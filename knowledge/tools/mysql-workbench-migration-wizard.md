---
type: Tool
title: "MySQL Workbench Migration Wizard (8.0.47)"
description: "GUI wizard for ODBC-reachable sources (SQL Server, PostgreSQL, Sybase ASE, SQLite, Access, SQL Anywhere, generic ODBC); copies data with the bundled wbcopytables helper; rejected for the unattended build because schema conversion is interactive and non-MySQL programmable objects are only copied as comments."
resource: https://dev.mysql.com/doc/workbench/en/wb-migration.html
tags: [tool, workbench, migration, gui, rejected]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:43:49Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:43:49Z" }
sources:
  - resource: https://dev.mysql.com/doc/workbench/en/wb-migration.html
    title: "Chapter 10 Database Migration Wizard"
    accessed: "2026-09-02"
  - resource: https://dev.mysql.com/doc/workbench/en/wb-migration-overview.html
    title: "10.2 Migration Overview"
    accessed: "2026-09-02"
  - resource: https://dev.mysql.com/doc/workbench/en/wb-migration-overview-supported.html
    title: "10.2.2 Migrating from Supported Databases"
    accessed: "2026-09-02"
  - resource: https://dev.mysql.com/doc/workbench/en/wb-migration-wizard.html
    title: "10.8 Using the MySQL Workbench Migration Wizard"
    accessed: "2026-09-02"
  - resource: https://dev.mysql.com/doc/workbench/en/wb-migration-wizard-data-migration-setup.html
    title: "10.8.10 Data Transfer and Migration Setup"
    accessed: "2026-09-02"
  - resource: https://dev.mysql.com/doc/workbench/en/wb-migration-wizard-data-migration-transfer.html
    title: "10.8.11 Bulk Data Transfer"
    accessed: "2026-09-02"
  - resource: https://dev.mysql.com/doc/workbench/en/wb-migration-database-mssql-typemapping.html
    title: "10.5.4 Microsoft SQL Server Type Mapping"
    accessed: "2026-09-02"
  - resource: https://dev.mysql.com/doc/workbench/en/wb-preface.html
    title: "Preface and Legal Notices"
    accessed: "2026-09-02"
  - resource: https://dev.mysql.com/doc/workbench/en/
    title: "MySQL Workbench Manual (8.0 through 8.0.47)"
    accessed: "2026-09-02"
    version: "8.0.47"
  - resource: https://github.com/mysql/mysql-workbench/tree/8.0.47/plugins/migration
    title: "mysql/mysql-workbench plugins/migration sources and License.txt"
    accessed: "2026-09-02"
    version: "8.0.47"
---

# Facts
* Version and license: the manual "documents the MySQL Workbench Community and MySQL Workbench Commercial releases for versions 8.0 through 8.0.47" ([front page](/sources/mysql-workbench-manual-front-page.md)); repository tags 8.0.47/8.0.46/8.0.45, last push 2026-04-23. `License.txt` at 8.0.47: "released under version 2 of the GNU General Public License (GPLv2) ... with the following additional permissions" (OpenSSL-style linking permission), "Last updated: March 2026" ([plugin sources record](/sources/github-mysql-workbench-migration-plugin.md); preface links the same text as `workbench-8.0-gpl-en.pdf`, [preface](/sources/mysql-workbench-wb-preface.md)). See [GPL-2.0](/licenses/gpl-2-0.md).
* Supported sources ("currently tested and supported"): Microsoft SQL Server 2000 and later; Microsoft Access 2007 and later; MySQL 5.6+; PostgreSQL 8.0 and later; SQL Anywhere; SQLite; Sybase Adaptive Server Enterprise 15.x and later; other products through "Generic database support, as long as you have an ODBC driver for it" ([supported](/sources/mysql-workbench-wb-migration-overview-supported.md), [overview](/sources/mysql-workbench-wb-migration-overview.md)).
* It is a wizard inside the Workbench GUI: chapter 10.8 is twelve sequential wizard pages (Connecting, Schema Retrieval, Reverse Engineering, Object Selection, Migration, **Manual Editing**, Target Creation Options, Schema Creation, Create Target Results, Data Transfer Setup, Bulk Data Transfer, Migration Report) ([wizard](/sources/mysql-workbench-wb-migration-wizard.md)). The chapter opens with "Setup may be the most challenging aspect of using the MySQL Workbench Migration Wizard" (ODBC libraries and drivers per platform) ([chapter](/sources/mysql-workbench-wb-migration.md)).
* Programmable objects are **not** ported: "Triggers are copied, and commented out if the source is not MySQL"; "View objects are copied, and commented out if the source is not MySQL"; "Stored Procedure and Function objects are copied, and commented out if the source is not MySQL" ([overview](/sources/mysql-workbench-wb-migration-overview.md)).
* Data copy method: three modes — "Online copy of table data to target RDBMS" (default, through Workbench), "Create a batch file to copy the data at another time" ("This script uses a MySQL connection to transfer the data"), and "Create a shell script to use native server dump and load abilities for fast migration" (source-host script → Zip → "import the data into MySQL using a LOAD DATA call"). Default "Worker tasks" is 2 connections ([setup](/sources/mysql-workbench-wb-migration-wizard-data-migration-setup.md), [transfer](/sources/mysql-workbench-wb-migration-wizard-data-migration-transfer.md)).
* The helper the manual does not name is `wbcopytables`: a C++ program (`plugins/migration/copytable/main.cpp`) wrapped by `wbcopytables.in` (sets `LD_LIBRARY_PATH` to the Workbench lib dir and execs `wbcopytables-bin`). Usage: `copytable --*-source=<source db> --target=<target db> <options>` with `--odbc-source=<odbc connstring>` or `--pythondbapi-source=<python connstring>`, `--target=<mysql connstring>`, `--table-file=<filename>`, `--thread-count=<count>`, `--truncate-target`, `--source-charset`, `--log-file`, `--log-level`, SSH tunnelling flags. The wizard's frontend (`migration_data_transfer.py`) writes `copy_migrated_tables.sh/.cmd` and `bulk_copy_tables.sh/.cmd` to the Desktop and warns "You should edit this file to add the source and target server passwords before running it." ([plugin sources](/sources/github-mysql-workbench-migration-plugin.md)).
* Documented SQL Server type map ([typemapping](/sources/mysql-workbench-wb-migration-database-mssql-typemapping.md)): BIT→TINYINT(1); MONEY/SMALLMONEY→DECIMAL (no precision stated); UNIQUEIDENTIFIER→VARCHAR(64) ("There is not specific support for inserting unique identifier values"); XML→TEXT; DATETIME2/DATETIMEOFFSET/SMALLDATETIME→DATETIME; ROWVERSION/TIMESTAMP→TIMESTAMP; NVARCHAR→VARCHAR/MEDIUMTEXT/LONGTEXT by length; SYSNAME→VARCHAR(160); HIERARCHYID, SQL_VARIANT, TABLE "not migrated"; GEOMETRY/GEOGRAPHY absent from the table.

# Inferred
* **Inferred:** `wbcopytables` is scriptable (all inputs are flags and a table file) but it is only built and installed as part of a full Workbench package with GUI toolkit dependencies; there is no standalone package, no Docker image, and it needs an ODBC DSN or Python DB-API connection string to the *running* source product — so it saves nothing over talking to that product directly.
* **Inferred:** the type map is a reasonable published baseline for reviewers, but the project's map is stricter (MONEY→DECIMAL(19,4), UNIQUEIDENTIFIER→BINARY(16) with UUID_TO_BIN, DATETIMEOFFSET→DATETIME(6)+offset column, ROWVERSION→BINARY(8), XML→LONGTEXT/JSON, geography→GEOMETRY SRID 4326) — see [MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md).

# Limits
1. Schema conversion requires clicking through the wizard; the "Manual Editing" step is where every type-mapping decision would be taken by hand — not reproducible, not diffable, not runnable in CI.
2. Views, procedures, functions and triggers arrive as commented-out text, so the hardest part of each port (programmable objects) is not done at all.
3. Requires a live ODBC connection to the source product; the project already needs the source container for SQL Server/Oracle sources, and from there bcp/sqlcmd or DuckDB exports are simpler.
4. Data copy is row-oriented over ODBC/MySQL connections (2 workers by default); the only fast path generates LOAD DATA scripts — which the project generates itself without Workbench.

# Decision
**Rejected** for the unattended Docker build. Kept as a reference for reviewers comparing type maps. Any dataset whose only viable path were Workbench would instead be converted with the source product's own export plus sqlglot/DuckDB ([Python stack](/tools/python-conversion-stack.md), [DuckDB](/tools/duckdb.md)).

# Open questions
* None blocking; if a reviewer wants an independent cross-check of the AdventureWorks type map, a one-off manual Workbench run on a workstation is acceptable but its output must not enter the repository.
