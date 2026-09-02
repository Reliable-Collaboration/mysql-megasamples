---
type: Source
title: "pgloader documentation: Migrating a MS SQL Database to PostgreSQL"
description: "mssql:// source syntax; the 'latest' docs describe v4 (JDBC mssql-jdbc, no FreeTDS) while a later section on the same page still documents the FreeTDS/freetds.conf setup of v3; default casting rules."
resource: https://pgloader.readthedocs.io/en/latest/ref/mssql.html
tags: [pgloader, mssql]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://pgloader.readthedocs.io/en/latest/ref/mssql.html
    title: "pgloader documentation: Migrating a MS SQL Database to PostgreSQL"
    accessed: 2026-09-02
    version: "readthedocs 'latest', read 2026-09-02"
---

# What was read
https://pgloader.readthedocs.io/en/latest/ref/mssql.html, accessed 2026-09-02; version: readthedocs 'latest', read 2026-09-02.

# Relevant excerpt
> "This command instructs pgloader to load data from a MS SQL database. Automatic discovery of the schema is supported, including build of the indexes, primary and foreign keys constraints."
> "pgloader v4 uses the official Microsoft JDBC driver (mssql-jdbc) so no FreeTDS or ODBC installation is required." Connection strings: `mssql://[user[:password]@][host][:port][/dbname]` or `jdbc:sqlserver://host[:port][;param=value;...]`; "When using the native mssql:// URI, encrypt=false is set automatically (matching the previous FreeTDS behaviour)."
* Later on the same page ("MS SQL Driver setup and encoding"): "pgloader is using the FreeTDS driver, and internally expects the data to be sent in utf-8. To achieve that, you can configure the FreeTDS driver with those defaults, in the file ~/.freetds.conf: [global] tds version = 7.4 client charset = UTF-8" — i.e. the v3 text was not removed.
* Casting defaults summarised: tinyint→smallint; float/real/numeric/decimal/money→PostgreSQL numerics; char/nchar/varchar/nvarchar/xml→text; binary/varbinary→bytea; datetime/datetime2→timestamptz; bit→boolean; uniqueidentifier→uuid. Target: PostgreSQL only.

# What it was used to decide
[pgloader record](/tools/pgloader.md).
