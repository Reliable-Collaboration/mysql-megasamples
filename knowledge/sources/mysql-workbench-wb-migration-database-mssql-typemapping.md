---
type: Source
title: "MySQL Workbench Manual: 10.5.4 Microsoft SQL Server Type Mapping"
description: "Workbench's documented SQL Server → MySQL type map (MONEY→DECIMAL, UNIQUEIDENTIFIER→VARCHAR(64), XML→TEXT, DATETIMEOFFSET→DATETIME, HIERARCHYID/SQL_VARIANT not migrated)."
resource: https://dev.mysql.com/doc/workbench/en/wb-migration-database-mssql-typemapping.html
tags: [workbench, migration, type-mapping, mssql]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://dev.mysql.com/doc/workbench/en/wb-migration-database-mssql-typemapping.html
    title: "MySQL Workbench Manual: 10.5.4 Microsoft SQL Server Type Mapping"
    accessed: 2026-09-02
    version: "MySQL Workbench 8.0 manual"
---

# What was read
https://dev.mysql.com/doc/workbench/en/wb-migration-database-mssql-typemapping.html, accessed 2026-09-02; version: MySQL Workbench 8.0 manual.

# Relevant excerpt
> "The following table shows the mapping between Microsoft SQL Server (source) data types and MySQL data types."
* INT→INT; TINYINT→TINYINT ("UNSIGNED flag set in MySQL."); SMALLINT→SMALLINT; BIGINT→BIGINT; BIT→TINYINT(1); FLOAT→FLOAT ("Precision value is used for storage size in both."); REAL→FLOAT; NUMERIC→DECIMAL; DECIMAL→DECIMAL; MONEY→DECIMAL; SMALLMONEY→DECIMAL; CHAR→CHAR/LONGTEXT (up to 255 chars else LONGTEXT); NCHAR→CHAR/LONGTEXT; VARCHAR/NVARCHAR→VARCHAR/MEDIUMTEXT/LONGTEXT ("Depending on its length ... up to 65535 characters. Anything larger is migrated to one of the TEXT blob types"); DATE→DATE; DATETIME→DATETIME; DATETIME2→DATETIME ("Date range in MySQL is '1000-01-01 00:00:00.000000' to '9999-12-31 23:59:59.999999'"); SMALLDATETIME→DATETIME; DATETIMEOFFSET→DATETIME; TIME→TIME; TIMESTAMP→TIMESTAMP; ROWVERSION→TIMESTAMP; BINARY→BINARY/MEDIUMBLOB/LONGBLOB; VARBINARY→VARBINARY/MEDIUMBLOB/LONGBLOB; TEXT/NTEXT→VARCHAR/MEDIUMTEXT/LONGTEXT; IMAGE→TINYBLOB/MEDIUMBLOB/LONGBLOB; SQL_VARIANT, TABLE, HIERARCHYID: "not migrated" ("There is not specific support for this data type."); UNIQUEIDENTIFIER→VARCHAR(64) ("A unique flag set in MySQL. There is not specific support for inserting unique identifier values."); SYSNAME→VARCHAR(160); XML→TEXT. GEOMETRY/GEOGRAPHY are absent from the table.

# What it was used to decide
[Workbench Migration Wizard record](/tools/mysql-workbench-migration-wizard.md): the table is a useful published baseline, but the project's own map deviates (MONEY→DECIMAL(19,4), UNIQUEIDENTIFIER→BINARY(16), DATETIMEOFFSET→DATETIME(7→6) + offset column, ROWVERSION→BINARY(8), XML→LONGTEXT or JSON, geography→GEOMETRY SRID 4326) as recorded in [MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md).
