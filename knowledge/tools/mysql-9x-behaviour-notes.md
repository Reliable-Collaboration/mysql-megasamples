---
type: Tool
title: MySQL 9.7 behaviour notes for conversions
description: "Verified server behaviours that shape every schema port: utf8mb4/utf8mb4_0900_ai_ci defaults, caching_sha2_password only, spatial SRID rules, JSON, CHECK constraints, generated columns, identifier limits and case sensitivity, sql_mode, temporal/decimal/bit ranges, no UUID or datetimeoffset type, FULLTEXT tuning, invisible columns/indexes, partitioning limits, size and integrity statements, and what changed in 9.x."
resource: https://dev.mysql.com/doc/refman/9.7/en/
tags:
- tool
- mysql
- type-mapping
- behaviour
- reference
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:47:28Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:47:28Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/charset-server.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/caching-sha2-pluggable-authentication.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/relnotes/mysql/9.0/en/news-9-0-0.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/mysql-nutshell.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/8.4/en/mysql-nutshell.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/spatial-type-overview.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/gis-wkt-functions.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/creating-spatial-indexes.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/json.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/create-table-check-constraints.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/create-table-generated-columns.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/identifier-length.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/identifier-case-sensitivity.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/sql-mode.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/datetime.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/fixed-point-types.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/bit-type.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/miscellaneous-functions.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/fulltext-search.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/fulltext-fine-tuning.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/invisible-columns.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/invisible-indexes.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/partitioning-limitations.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/information-schema-tables-table.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/checksum-table.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/check-table.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/workbench/en/wb-migration-database-mssql-typemapping.html
  accessed: "2026-09-02"
---

# Facts

## Measured on `mysql:9.7.2` (2026-09-02, task P-02)
`mysqld --verbose --help` and a running server confirm every default the records assumed: `character_set_server=utf8mb4`, `collation_server=utf8mb4_0900_ai_ci`, `local_infile=FALSE`, `secure_file_priv=/var/lib/mysql-files`, `lower_case_table_names=0`, `innodb_autoinc_lock_mode=2`, `log_bin=binlog` (binary logging on), `--init-file` accepted, `group_concat_max_len=1024`, and `sql_mode=ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`. Image size 270,916,394 bytes, amd64, digest `sha256:257388ed…`; bundled `mysqlsh` 9.7.1 and `mysql` client 9.7.2.
Two results that were open questions: **`@@explain_format` defaults to `TREE`**, so every EXPLAIN test must ask for `FORMAT=JSON` explicitly (the plan already does); and `CAST('2021/1/1' AS DATETIME)` yields `2021-01-01 00:00:00` under the strict default, so Chinook's slashed date literals load without rewriting.
**`GROUPING SETS` is not usable**: it parses and then fails with `ERROR 3889 Secondary engine operation failed`, a HeatWave-only feature; `WITH ROLLUP` + `GROUPING()` is the portable form.

## Character set and collation
* "By default, these are utf8mb4 and utf8mb4_0900_ai_ci" ([charset-server](/sources/mysql-refman-9-7-charset-server.md)). `_ai_ci` = accent- and case-insensitive comparisons: `'resume' = 'résumé'` is true, so uniqueness constraints and `DISTINCT` behave differently from SQL Server `_CS_AS`/binary collations and Oracle's case-sensitive default. Converters declare `CHARACTER SET utf8mb4` explicitly and choose `utf8mb4_0900_as_cs` or `utf8mb4_bin` per column only where the source semantics demand it (dataset records list those columns).

## Authentication
* "In MySQL 9.7, caching_sha2_password is the default authentication plugin; mysql_native_password is no longer available." Clients need "either a secure connection or an unencrypted connection that supports password exchange using an RSA key pair" (`--get-server-public-key`) ([caching-sha2](/sources/mysql-refman-9-7-caching-sha2-pluggable-authentication.md)). Removal happened in 9.0: "The mysql_native_password authentication plugin, deprecated in MySQL 8.0, has been removed" ([9.0.0 notes](/sources/mysql-relnotes-9-0-0.md)); 8.4 had already disabled it by default ([8.4 nutshell](/sources/mysql-refman-8-4-mysql-nutshell.md)). Consequence: upstream scripts with `IDENTIFIED WITH mysql_native_password` fail; every client library in the [Python stack](/tools/python-conversion-stack.md) must speak caching_sha2_password.

## What changed in 9.x that matters
* 9.0: VECTOR column type (default 2048 entries, max 16383); JavaScript stored programs are Enterprise-only ([9.0.0 notes](/sources/mysql-relnotes-9-0-0.md)). 9.7 itself: `innodb_log_writer_threads` default logic, `binlog_transaction_dependency_history_size` default, SCRAM-SHA-1 deprecation, two replication variables removed — nothing affecting conversions ([9.7 nutshell](/sources/mysql-refman-9-7-mysql-nutshell.md)). 8.4: mysqlpump and mysql_upgrade removed, `innodb_change_buffering` default `none` ([8.4 nutshell](/sources/mysql-refman-8-4-mysql-nutshell.md)).

## Spatial
* Types GEOMETRY, POINT, LINESTRING, POLYGON, MULTI*, GEOMETRYCOLLECTION; `col GEOMETRY NOT NULL SRID 4326` makes the column SRID-restricted ("Attempts to insert values with a different SRID produce an error"; "The optimizer can use SPATIAL indexes on the column") ([spatial overview](/sources/mysql-refman-9-7-spatial-type-overview.md)). SPATIAL indexes: InnoDB/MyISAM only, "Indexed columns must be declared NOT NULL", R-tree, optimizer uses them only on SRID-restricted columns ([creating spatial indexes](/sources/mysql-refman-9-7-creating-spatial-indexes.md)).
* `ST_GeomFromText(wkt [, srid [, options]])` with `axis-order=lat-long|long-lat|srid-defined` (default srid-defined); for geographic SRSs coordinates "are interpreted in the order specified by the spatial reference system" and out-of-range values raise ER_LONGITUDE_OUT_OF_RANGE (−180, 180] / ER_LATITUDE_OUT_OF_RANGE [−90, 90] ([WKT functions](/sources/mysql-refman-9-7-gis-wkt-functions.md)). Rule: every converter writing longitude-first WKT (SQL Server geography `.STAsText()`, GeoJSON, shapefiles) loads with `ST_GeomFromText(@wkt, 4326, 'axis-order=long-lat')`; nullable source columns cannot carry a SPATIAL index ([indexing strategy](/decisions/indexing-strategy.md) rule 5).

## JSON
* Validated on write ("Invalid documents produce an error"), binary storage, size bounded by `max_allowed_packet`, "not indexed directly" (generated columns / multi-valued indexes), duplicate keys "last duplicate key wins", key order "subject to change and not guaranteed to be consistent across releases" ([json](/sources/mysql-refman-9-7-json.md)). SQL Server `nvarchar` JSON payloads that are not strictly valid JSON must stay TEXT; JSON columns are compared through a normalised form in tests ([checksum method](/decisions/test-checksum-method.md)).

## CHECK constraints
* Enforced since 8.0.16 ("Prior to MySQL 8.0.16 ... parsed and ignored" — [8.0 page](/sources/mysql-refman-8-0-create-table-check-constraints.md)); not permitted: nondeterministic functions, subqueries, stored/loadable functions, variables, AUTO_INCREMENT columns, other tables, FK actions; evaluated for INSERT/UPDATE/REPLACE/LOAD DATA (warning + skipped row under IGNORE); `NOT ENFORCED` available ([check constraints](/sources/mysql-refman-9-7-create-table-check-constraints.md)). Port rule: keep expressible constraints (comparison, IN, LIKE, REGEXP), rewrite T-SQL/PL-SQL function calls, and mark anything referencing other rows/tables as dropped with the reason in the dataset record.

## Generated (computed/virtual) columns
* `AS (expr) [VIRTUAL | STORED]`, VIRTUAL default; only deterministic built-ins, no stored functions, no subqueries, no variables, no AUTO_INCREMENT interplay; explicit values not allowed (`DEFAULT` only); STORED may be PK/indexed, VIRTUAL gets secondary indexes only ([generated columns](/sources/mysql-refman-9-7-create-table-generated-columns.md)). SQL Server `PERSISTED` → STORED, non-persisted → VIRTUAL; Oracle virtual columns likewise; the loader column list omits them.

## Identifiers
* 64-character limit for database/table/column/index/constraint/routine names (aliases 256); generated `_ibfk_`/`_chk_` names can overflow when the table name is near 64 ([identifier length](/sources/mysql-refman-9-7-identifier-length.md)). SQL Server allows 128 → converters truncate deterministically and record renames.
* `lower_case_table_names`: Unix default 0 (case-sensitive database and table names), "can only be configured when initializing the server. Changing the lower_case_table_names setting after the server is initialized is prohibited."; the manual recommends 1 "on all platforms" for InnoDB portability; column, index, routine, event names are case-insensitive everywhere, trigger names are case-sensitive ([case sensitivity](/sources/mysql-refman-9-7-identifier-case-sensitivity.md)). Decision input: either pass `--lower-case-table-names=1` to `mysqld --initialize` in the build stage **and** to every later start (via `/etc/mysql/conf.d/`), or keep 0 and emit lowercase names everywhere ([naming convention](/decisions/database-naming-convention.md)); the executor must not change it after the datadir exists.

## sql_mode and syntax
* Default: ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_ENGINE_SUBSTITUTION; ANSI_QUOTES/PIPES_AS_CONCAT/NO_BACKSLASH_ESCAPES exist but are not defaults ([sql-mode](/sources/mysql-refman-9-7-sql-mode.md)). Ported SQL uses backticks, single quotes, `CONCAT()`; ONLY_FULL_GROUP_BY breaks many tutorial queries copied from other engines — the smoke queries are written to comply.

## Temporal, decimal, bit
* DATETIME '1000-01-01 00:00:00' to '9999-12-31 23:59:59[.499999]'; TIMESTAMP '1970-01-01 00:00:01' to '2038-01-19 03:14:07' UTC (no extension in 9.7); DATE '1000-01-01'..'9999-12-31'; 6 fractional digits; TIMESTAMP converts through the session time zone, DATETIME does not; invalid values become the zero date under permissive modes ([datetime](/sources/mysql-refman-9-7-datetime.md)). Hazards: SQL Server temporal-table end date `9999-12-31 23:59:59.9999999` must be truncated (not rounded) to `.999999`; `datetime2`/Oracle `DATE` values before year 1000 (e.g. `0001-01-01` sentinels) have no representation — dataset records choose NULL or a documented sentinel; never use TIMESTAMP for source values past 2038.
* DECIMAL max 65 digits, scale ≤ 30 and ≤ precision, defaults (10,0), excess fractional digits rounded on load ([fixed-point](/sources/mysql-refman-9-7-fixed-point-types.md)); BIT(M) 1..64 with `b'...'` literals ([bit](/sources/mysql-refman-9-7-bit-type.md)).

## No UUID type, no datetimeoffset
* `UUID_TO_BIN(str[, swap])` returns VARBINARY(16); swapping helps only version-1 UUIDs; `BIN_TO_UUID` inverts; `IS_UUID` accepts dashed/undashed/braced text ([misc functions](/sources/mysql-refman-9-7-miscellaneous-functions-uuid.md)). Mapping: `uniqueidentifier` → `BINARY(16)` loaded with `UUID_TO_BIN(@v)` (no swap), with a `BIN_TO_UUID` view column for readability; CHAR(36) only where the dataset's canonical queries compare against literal GUID strings.
* No offset-bearing type exists: `datetimeoffset` → `DATETIME(6)` normalised to UTC plus a `SMALLINT` offset-minutes column when the offset varies (dataset records say which).

## FULLTEXT
* InnoDB/MyISAM, CHAR/VARCHAR/TEXT, three modes, create after load ([fulltext](/sources/mysql-refman-9-7-fulltext-search.md)); `innodb_ft_min_token_size` 3, `innodb_ft_max_token_size` 84, stopword list in `INFORMATION_SCHEMA.INNODB_FT_DEFAULT_STOPWORD`, rebuild required after tuning ([fine-tuning](/sources/mysql-refman-9-7-fulltext-fine-tuning.md)).

## Invisible columns and indexes
* Invisible columns are hidden from `SELECT *`, loadable by name, at least one column must stay visible ([invisible columns](/sources/mysql-refman-9-7-invisible-columns.md)); invisible indexes are maintained but ignored unless `use_invisible_indexes=on`, primary keys cannot be invisible ([invisible indexes](/sources/mysql-refman-9-7-invisible-indexes.md)).

## Partitioning
* "Partitioned tables using the InnoDB storage engine do not support foreign keys." (both directions); unique keys must include the partitioning columns; no FULLTEXT, no spatial columns; 8192 partitions max ([partitioning limitations](/sources/mysql-refman-9-7-partitioning-limitations.md)).

## Size and integrity statements used by tests
* `information_schema.TABLES`: InnoDB `TABLE_ROWS` "may vary from the actual value by as much as 40% to 50%"; `DATA_LENGTH` = clustered index pages × page size, `INDEX_LENGTH` = secondary index pages × page size; cached for `information_schema_stats_expiry` (86400 s) unless set to 0 ([TABLES](/sources/mysql-refman-9-7-information-schema-tables.md)).
* `CHECKSUM TABLE`: "The checksum value depends on the table row format"; QUICK is MyISAM-only; EXTENDED reads every row under a read lock ([CHECKSUM TABLE](/sources/mysql-refman-9-7-checksum-table.md)) — same-image fingerprint only ([checksum method](/decisions/test-checksum-method.md)).
* `CHECK TABLE t QUICK` is the InnoDB-meaningful form (FAST/MEDIUM/EXTENDED/CHANGED are ignored for InnoDB); it can mark corruption and even exit the server on a corrupt page ([CHECK TABLE](/sources/mysql-refman-9-7-check-table.md)).

# Inferred: the project type map versus Workbench's published map
Workbench documents MONEY→DECIMAL, UNIQUEIDENTIFIER→VARCHAR(64), XML→TEXT, DATETIMEOFFSET→DATETIME, ROWVERSION→TIMESTAMP, HIERARCHYID not migrated ([Workbench map](/sources/mysql-workbench-wb-migration-database-mssql-typemapping.md)). **Inferred** project choices, each justified by a verified fact above: MONEY→DECIMAL(19,4) (exact, 65-digit cap irrelevant); SMALLMONEY→DECIMAL(10,4); UNIQUEIDENTIFIER→BINARY(16); XML→LONGTEXT (or JSON only when converted); DATETIMEOFFSET→DATETIME(6)+offset; ROWVERSION→BINARY(8) (a TIMESTAMP would silently rewrite on update); HIERARCHYID→VARCHAR(4000) path string via `.ToString()`; SQL_VARIANT→LONGTEXT with a type tag column; geography/geometry→GEOMETRY SRID 4326 / SRID 0; BIT→TINYINT(1); NVARCHAR(MAX)→LONGTEXT; VARBINARY(MAX)→LONGBLOB; Oracle NUMBER(p,s)→DECIMAL(p,s), unconstrained NUMBER→DECIMAL(38,10) or DOUBLE per column statistics, CLOB→LONGTEXT, RAW(16)→BINARY(16), TIMESTAMP WITH TIME ZONE→DATETIME(6) UTC + offset, INTERVAL→VARCHAR ISO-8601 text; PostgreSQL uuid→BINARY(16), jsonb→JSON, arrays→JSON, timestamptz→DATETIME(6) UTC, boolean→TINYINT(1), serial→AUTO_INCREMENT, text→LONGTEXT, numeric without precision→DECIMAL(38,10), inet/cidr→VARCHAR(45), tsvector→dropped + FULLTEXT. Dataset records override per column.

# Limits
1. `lower_case_table_names` is an initialization-time choice for the baked datadir — decide before P-03.
2. Accent/case-insensitive default collation changes uniqueness semantics; expect duplicate-key failures on sources with case-variant keys (dataset records flag them).
3. No year-0/year-10000 temporal values, no TIMESTAMP past 2038, no UUID/offset types — all handled in converters, none at load time.
4. SPATIAL indexes need NOT NULL + SRID; FULLTEXT and FKs are incompatible with partitioning.
5. Nonrestrictive LOCAL loading ([LOAD DATA record](/tools/load-data-infile.md)) can mask every hazard above; tests are the safety net.

# Open questions
* Whether to pass `--lower-case-table-names=1` at `--initialize` (portability) or keep 0 (fidelity to upstream mixed-case names): decide in [naming convention](/decisions/database-naming-convention.md); experiment = initialise twice and diff `SHOW VARIABLES` and `SHOW TABLES` behaviour (5 minutes).
