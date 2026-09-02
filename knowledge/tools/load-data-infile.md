---
type: Tool
title: MySQL 9.7 LOAD DATA (server-side and LOCAL) and the bulk-load settings
description: "The ingestion primitive for every converted dataset: LOCAL versus server-side semantics, secure_file_priv in the official image, the converter TSV contract (\\N NULLs, backslash escapes), strict-versus-nonrestrictive loading, and the documented InnoDB bulk-load settings; mysqldump --tab as fallback exporter, mysqlpump gone."
resource: https://dev.mysql.com/doc/refman/9.7/en/load-data.html
tags:
- tool
- mysql
- load-data
- bulk-load
- build-time
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
- resource: https://dev.mysql.com/doc/refman/9.7/en/load-data.html
  title: 15.2.9 LOAD DATA Statement
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/load-data-local-security.html
  title: 8.1.6 Security Considerations for LOAD DATA LOCAL
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/optimizing-innodb-bulk-data-loading.html
  title: 10.5.5 Bulk Data Loading for InnoDB Tables
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/insert-optimization.html
  title: 10.2.5.1 Optimizing INSERT Statements
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/innodb-auto-increment-handling.html
  title: 17.6.1.6 AUTO_INCREMENT Handling in InnoDB
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/mysql-command-options.html
  title: 6.5.1.1 mysql Client Options
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/mysqldump.html
  title: 6.5.4 mysqldump
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/8.4/en/mysql-nutshell.html
  title: What Is New in MySQL 8.4 (mysqlpump removal)
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/linux-installation-rpm.html
  title: 2.5.4 RPM installation layout (secure_file_priv)
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/docker-library/mysql/master/9.7/Dockerfile.oracle
  title: docker-library/mysql 9.7/Dockerfile.oracle
  accessed: "2026-09-02"
  version: master @ 2f988f19 (2026-08-19)
- resource: https://raw.githubusercontent.com/docker-library/mysql/master/9.7/docker-entrypoint.sh
  title: docker-library/mysql 9.7/docker-entrypoint.sh
  accessed: "2026-09-02"
  version: master @ 2f988f19 (2026-08-19)
- resource: https://dev.mysql.com/doc/refman/9.7/en/sql-mode.html
  title: 7.1.11 Server SQL Modes
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/create-table-check-constraints.html
  title: 15.1.25.6 CHECK Constraints
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-parallel-table.html
  title: MySQL Shell importTable (sessionInitSql example with sql_log_bin=0)
  accessed: "2026-09-02"
---

# Facts

## LOCAL versus server-side
* Server-side (`LOAD DATA INFILE`): the file is read by mysqld on the server host, relative paths resolve against the data directory or the default database's directory, and the statement "Requires the FILE privilege". LOCAL: "The client program reads the file and sends its contents to the server", which "creates a copy in its temporary files directory"; no FILE privilege ([load-data](/sources/mysql-refman-9-7-load-data.md)).
* `secure_file_priv`: "If the variable value is a nonempty directory name, the file must be located in that directory"; empty means any server-readable file. For Oracle RPM installs the documented value is `/var/lib/mysql-files` ([RPM layout](/sources/mysql-refman-9-7-linux-installation-rpm.md)); the official image installs exactly that RPM (`mysql-community-server-minimal-9.7.2-1.el9`) and its Dockerfile edits `/etc/my.cnf` only for the socket and `!includedir` ([Dockerfile](/sources/docker-library-mysql-9-7-dockerfile-oracle.md)); the entrypoint creates whatever directory `secure-file-priv` resolves to ([entrypoint](/sources/docker-library-mysql-9-7-docker-entrypoint.md)).
* LOCAL is off by default on both sides: "By default, local_infile is disabled." (server); client `--local-infile` Default Value FALSE; failure text "ERROR 3950 (42000): Loading local data is disabled; this must be enabled on both the client and server side" ([security](/sources/mysql-refman-9-7-load-data-local-security.md), [client options](/sources/mysql-refman-9-7-mysql-command-options.md)).

## Syntax elements the converters rely on
* Defaults with no FIELDS/LINES clause: `FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\' LINES TERMINATED BY '\n' STARTING BY ''`.
* NULL: "a field value of \N is read as NULL for input (assuming that the ESCAPED BY character is \)"; with a non-empty `ENCLOSED BY`, an unquoted literal `NULL` is NULL while a quoted `"NULL"` is the string.
* `CHARACTER SET charset_name` overrides `character_set_database`; `binary` = no conversion; "It is not possible to load data files that use the ucs2, utf16, utf16le, or utf32 character set."
* `IGNORE 1 LINES` skips a header; column list may name user variables and `SET col = expr` transforms them (`(column1, @var1) SET column2 = @var1/100`); `@dummy` discards a field; Windows files need `LINES TERMINATED BY '\r\n'`.
* `REPLACE` overwrites and `IGNORE` drops duplicate-unique-key rows.

## Strict versus nonrestrictive — the correctness trap
* "When IGNORE or LOCAL without REPLACE is specified, data interpretation errors become warnings and the load operation continues, even if the SQL mode is restrictive": too many fields are dropped, too few get defaults, NULL into NOT NULL becomes the implicit default, invalid values become the "closest" valid value ([load-data](/sources/mysql-refman-9-7-load-data.md)). The default sql_mode is strict (`STRICT_TRANS_TABLES` among ONLY_FULL_GROUP_BY, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_ENGINE_SUBSTITUTION) ([sql-mode](/sources/mysql-refman-9-7-sql-mode.md)), so **only server-side LOAD DATA without IGNORE aborts on bad data**; every LOCAL path (mysql `--local-infile`, `util.importTable`, `util.loadDump`) coerces silently.
* CHECK constraints are evaluated by LOAD DATA (error) and with `LOAD DATA ... IGNORE` become warnings with the row skipped ([check constraints](/sources/mysql-refman-9-7-create-table-check-constraints.md)).

## Documented bulk-load settings ([InnoDB bulk loading](/sources/mysql-refman-9-7-optimizing-innodb-bulk-data-loading.md))
* "turn off autocommit mode, because it performs a log flush to disk for every insert" (`SET autocommit=0; ... COMMIT;`).
* `SET unique_checks=0`: "InnoDB can use its change buffer to write secondary index records in a batch" (note the change-buffer default is `none` since 8.4, [8.4 nutshell](/sources/mysql-refman-8-4-mysql-nutshell.md), so the benefit is mostly the skipped uniqueness check — **Inferred**).
* `SET foreign_key_checks=0`: "For big tables, this can save a lot of disk I/O."
* "set innodb_autoinc_lock_mode to 2 (interleaved)" — already the default in 9.7 ([autoinc](/sources/mysql-refman-9-7-innodb-auto-increment-handling.md)).
* "it is faster to insert rows in PRIMARY KEY order ... particularly important for tables that do not fit entirely within the buffer pool."
* "Create the FULLTEXT index after the data is loaded."
* "If loading data into a new MySQL instance, consider disabling redo logging using ALTER INSTANCE {ENABLE|DISABLE} INNODB REDO_LOG syntax."
* Speed reference: "When loading a table from a text file, use LOAD DATA. This is usually 20 times faster than using INSERT statements." ([insert-optimization](/sources/mysql-refman-9-7-insert-optimization.md)). `bulk_insert_buffer_size` is mentioned there for nonempty tables (MyISAM-oriented; not used).
* `sql_log_bin=0` per session is the documented Shell example (`sessionInitSql: ["SET SESSION sql_log_bin=0;", ...]`) and `loadDump`'s `skipBinlog` ([Shell importTable](/sources/mysql-shell-9-7-parallel-table-import.md)).

## Companion client tools
* `mysql --default-character-set=utf8mb4 --local-infile=1`; `--binary-mode` stops `\r\n`→`\n` translation and `\0` termination for scripts carrying binary literals ([client options](/sources/mysql-refman-9-7-mysql-command-options.md)).
* `mysqldump`: `--default-character-set` defaults to utf8mb4; `--tab=path` writes per-table `.sql` + `.txt` (tab-separated, needs `secure_file_priv` and FILE); `--hex-blob` for BINARY/VARBINARY/BLOB/BIT/spatial; `--single-transaction`; the manual itself recommends MySQL Shell dump utilities ([mysqldump](/sources/mysql-refman-9-7-mysqldump.md)).
* `mysqlpump` "deprecated in MySQL 8.0.34, were removed" in 8.4 — not available on 9.7 ([8.4 nutshell](/sources/mysql-refman-8-4-mysql-nutshell.md)).

# Inferred
* **Inferred:** inside the `mysql:9.7.2` container the effective values are `secure_file_priv=/var/lib/mysql-files` and `local_infile=OFF`; verify with `docker run --rm mysql:9.7.2 mysqld --verbose --help 2>/dev/null | grep -E '^(secure-file-priv|local-infile) '` (the entrypoint itself reads config this way).
* **Inferred:** the build stage should prefer **server-side** `LOAD DATA INFILE '/var/lib/mysql-files/<dataset>/<table>.tsv'` (files bind-mounted or copied there) because strict mode then aborts on any coercion, turning silent data damage into a failed build; `util.importTable` (LOCAL, parallel, nonrestrictive) is reserved for the largest tables, with `SHOW WARNINGS`/`warning_count` required to be zero per chunk.
* **Inferred:** binary logging is on by default in 8.0+ servers; the temporary build server should be started with `--disable-log-bin` (verify the option name against `mysqld --verbose --help`) so `sql_log_bin` handling is moot and disk use halves.
* **Inferred:** `ALTER INSTANCE DISABLE INNODB REDO_LOG` is safe in the build stage only if `ENABLE` is issued before the clean shutdown that produces the baked datadir; the runbook step is DISABLE → load → ENABLE → `mysqladmin shutdown`.

# The converter TSV contract (what every converter must emit; verified elements cite the LOAD DATA page)
| Aspect | Rule |
|---|---|
| Encoding | UTF-8, no BOM; SQL Server `bcp -w` UTF-16 output must be transcoded first (utf16 cannot be loaded) |
| Line / field terminators | `\n` / `\t` (server defaults); no enclosure; header absent (or `IGNORE 1 LINES`) |
| Escaping | backslash-escape `\t`, `\n`, `\r`, `\\` and `\0` inside values; NULL is the bare two characters `\N` |
| Booleans / bits | `0`/`1` into TINYINT(1) |
| Temporal | `YYYY-MM-DD HH:MM:SS.ffffff` (6 fractional digits max); dates outside 1000-01-01..9999-12-31 handled per dataset record |
| Binary | hex text loaded via `(..., @b) SET col = UNHEX(@b)` |
| Geometry | WKT loaded via `SET col = ST_GeomFromText(@g, 4326, 'axis-order=long-lat')` (see [9.x notes](/tools/mysql-9x-behaviour-notes.md)) |
| Order | rows sorted by the target primary key (bulk-load recommendation) |

# Limits
1. LOCAL implies nonrestrictive interpretation; correctness must be proven by counts and digests ([checksum method](/decisions/test-checksum-method.md)), never assumed.
2. Server-side loading is confined to `secure_file_priv`; the build stage must place files there (or set the variable in `/etc/mysql/conf.d/` for the temporary server only).
3. UTF-16 inputs are rejected outright.
4. No mysqlpump; mysqldump `--tab` is the only Oracle-shipped TSV exporter besides MySQL Shell.
5. Loading in PK order with FKs and secondary indexes deferred is not optional for the multi-GB extended tier ([indexing strategy](/decisions/indexing-strategy.md)).

# Open questions
* Confirm the effective `secure_file_priv` and `local_infile` in `mysql:9.7.2` (command above) — 1 minute, task P-01.
* Confirm the redo-log disable/enable sequence leaves `CHECK TABLE ... QUICK` clean after shutdown and restart — part of task P-03.
