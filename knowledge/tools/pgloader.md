---
type: Tool
title: pgloader (v3.6.x SBCL, v4 Clojure rewrite in progress)
description: Loads CSV/fixed/dBase/IXF/archives and MySQL/SQLite/MS SQL Server/PostgreSQL/Redshift into PostgreSQL only; PostgreSQL-licensed; rejected for this project because MySQL is never a target and DuckDB/bcp cover the MSSQL-to-CSV step directly.
resource: https://pgloader.readthedocs.io/
tags:
- tool
- pgloader
- postgresql
- rejected
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:43:49Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:43:49Z"
sources:
- resource: https://pgloader.readthedocs.io/en/latest/
  title: pgloader documentation index
  accessed: "2026-09-02"
- resource: https://pgloader.readthedocs.io/en/latest/intro.html
  title: pgloader Introduction
  accessed: "2026-09-02"
- resource: https://pgloader.readthedocs.io/en/latest/ref/mssql.html
  title: Migrating a MS SQL Database to PostgreSQL
  accessed: "2026-09-02"
- resource: https://github.com/dimitri/pgloader
  title: dimitri/pgloader README, LICENSE, releases and tags
  accessed: "2026-09-02"
  version: latest release v3.6.9 (2022-10-24); tag v4-dev; master pushed 2026-07-24
---

# Facts
* Direction: "pgloader loads data from various sources into PostgreSQL. It can transform the data it reads on the fly and submit raw SQL before and after the loading." and "It uses the COPY PostgreSQL protocol to stream the data into the server" ([index](/sources/pgloader-readthedocs-index.md)). Sources per the Introduction: files CSV, Fixed Format, Postgres COPY text, DBF, IXF; databases SQLite, MySQL, MS SQL Server, PostgreSQL, Redshift ([intro](/sources/pgloader-readthedocs-intro.md)). **There is no MySQL target.**
* MS SQL Server source: "This command instructs pgloader to load data from a MS SQL database. Automatic discovery of the schema is supported, including build of the indexes, primary and foreign keys constraints." Connection `mssql://[user[:password]@][host][:port][/dbname]`. The current "latest" docs say "pgloader v4 uses the official Microsoft JDBC driver (mssql-jdbc) so no FreeTDS or ODBC installation is required." while a later section of the same page still says "pgloader is using the FreeTDS driver, and internally expects the data to be sent in utf-8" with a `~/.freetds.conf` example (`tds version = 7.4`, `client charset = UTF-8`) — the v3 text survives ([mssql page](/sources/pgloader-readthedocs-mssql.md)). Default casts include `uniqueidentifier→uuid`, `bit→boolean`, `datetime/datetime2→timestamptz`, `money→numeric`, `xml→text`.
* Release state: GitHub's latest release is v3.6.9 (2022-10-24) with a v3.6.10 tag; the README on master describes "pgloader v4 is a full rewrite in Clojure, distributed as a single self-contained JAR requiring Java 21 or later", downloaded from the `v4-dev` pre-release tag, "A v4 Debian package is planned." ([repo record](/sources/github-dimitri-pgloader-repo.md)).
* License: the PostgreSQL licence text, "Copyright (c) 2005-2017, The PostgreSQL Global Development Group ... Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted" ([repo record](/sources/github-dimitri-pgloader-repo.md); [license record](/licenses/postgresql.md)).

# Inferred
* **Inferred:** the only way pgloader could participate is as a staging hop MSSQL → PostgreSQL, followed by a PostgreSQL → CSV/MySQL export (DuckDB's postgres extension reads PostgreSQL with binary COPY, [DuckDB record](/tools/duckdb.md)). That adds a PostgreSQL container, a second type-mapping layer (T-SQL → PostgreSQL → MySQL) and a JVM or SBCL runtime, and yields nothing that `bcp`/`sqlcmd` or DuckDB reading the source container cannot produce directly.
* **Inferred:** the docs/README/release skew (docs describe v4-JDBC, releases are v3.6.9-FreeTDS) means any pin would be either a 2022 binary with FreeTDS caveats or an unreleased development JAR — neither is acceptable for a reproducible build.

# Limits
1. Target is PostgreSQL only — cannot write to MySQL under any option.
2. Its MySQL support is a *source* reader (MySQL → PostgreSQL), the opposite of what we need.
3. Type casting rules target PostgreSQL types (uuid, timestamptz, boolean) that would have to be re-mapped to MySQL afterwards.
4. Unreleased v4; v3.6.x depends on FreeTDS configuration for encoding correctness.

# Decision
**Not used.** No dataset in the inventory benefits: SQL Server sources are exported with the SQL Server tools or DuckDB from the source container ([mssql-server-container](/tools/mssql-server-container.md), [sqlcmd-bcp](/tools/sqlcmd-bcp.md), dataset-group records), CSV/SQLite/Parquet sources go through DuckDB, MySQL-native sources through MySQL Shell. Recorded so the question is not reopened.

# Open questions
* None.
