---
type: Tool
title: "MySQL Shell 9.7 utilities: importTable, dump/loadDump, copy"
description: "mysqlsh 9.7.1 is already in the official mysql:9.7 image; util.importTable is the parallel LOAD DATA LOCAL loader, util.dumpSchemas/loadDump is the interchange format with deferred secondary indexes, util.copy* streams between servers; all need local_infile=ON."
resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/
tags: [tool, mysql-shell, bulk-load, dump, build-time, ships-in-image]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:43:49Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:43:49Z" }
sources:
  - resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-parallel-table.html
    title: "12.4 Parallel Table Import Utility"
    accessed: 2026-09-02
    version: "MySQL Shell 9.7"
  - resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-load-dump.html
    title: "12.6 Dump Loading Utility"
    accessed: 2026-09-02
    version: "MySQL Shell 9.7"
  - resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-dump-instance-schema.html
    title: "12.5 Instance Dump Utility, Schema Dump Utility, and Table Dump Utility"
    accessed: 2026-09-02
    version: "MySQL Shell 9.7"
  - resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utils-copy.html
    title: "12.8 Copy Instance, Schemas, and Tables"
    accessed: 2026-09-02
    version: "MySQL Shell 9.7"
  - resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/command-line-integration-overview.html
    title: "5.8.1 Command Line Integration Overview"
    accessed: 2026-09-02
  - resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-batch-code-execution.html
    title: "5.6 Batch Code Execution"
    accessed: 2026-09-02
  - resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/
    title: "MySQL Shell 9.7 manual front page (preface license links)"
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/mysql/mysql-shell/9.7.1/LICENSE
    title: "mysql/mysql-shell LICENSE at 9.7.1"
    accessed: 2026-09-02
    version: "9.7.1"
  - resource: https://raw.githubusercontent.com/docker-library/mysql/master/9.7/Dockerfile.oracle
    title: "docker-library/mysql 9.7/Dockerfile.oracle"
    accessed: 2026-09-02
    version: "master @ 2f988f19 (2026-08-19)"
  - resource: https://dev.mysql.com/doc/refman/9.7/en/load-data-local-security.html
    title: "8.1.6 Security Considerations for LOAD DATA LOCAL"
    accessed: 2026-09-02
---

# Facts (verified)

## Availability and license
* `mysqlsh` **is in the official image**: `9.7/Dockerfile.oracle` installs `mysql-shell-9.7.1-1.el9` from `repo.mysql.com/yum/mysql-tools-9.7-community` and runs `mysqlsh --version` during the build ([Dockerfile record](/sources/docker-library-mysql-9-7-dockerfile-oracle.md)). No extra package is needed in the final stage or in a builder stage derived from `mysql:9.7.2`.
* The manual front page states: "MySQL Shell 9.7.0 is highly recommended for use with any GA version of MySQL 8.0, or later." ([front page](/sources/mysql-shell-9-7-front-page.md)).
* License: "This software is released under version 2 of the GNU General Public License (GPLv2), as set forth below, with the following additional permissions" — the additional permission is the right to link with separately licensed software such as OpenSSL; "Oracle elects to use only the General Public License version 2 (GPLv2)" ([LICENSE at 9.7.1](/sources/github-mysql-shell-license.md); the preface links the same text as https://downloads.mysql.com/docs/licenses/mysql-shell-9.7-gpl-en.pdf). See [GPL-2.0 license record](/licenses/gpl-2-0.md).

## Common requirement: `local_infile=ON`
* importTable: "The parallel table import utility uses LOAD DATA LOCAL INFILE statements to upload data, so the local_infile system variable must be set to ON on the target server." loadDump: "the global setting of the local_infile system variable on the target MySQL instance must be ON for the duration of the import." copy utilities: same sentence for the target server.
* The server default is OFF: "By default, local_infile is disabled." ([load-data-local-security](/sources/mysql-refman-9-7-load-data-local-security.md)). Build stages therefore start the temporary server with `--local-infile=1` (or issue `SET GLOBAL local_infile=1`) before any utility runs; the shipped image does **not** need it on at runtime.

## util.importTable()
* "The utility analyzes an input data file, distributes it into chunks, and uploads the chunks to the target MySQL server using parallel connections. The utility is capable of completing a large data import many times faster than a standard single-threaded upload using a LOAD DATA statement."
* Dialects (lines / fields / enclosed / optionally / escape): `default` LF, TAB, none, false, `\`; `csv` CRLF, `,`, `"`, true, `\`; `csv-unix` LF, `,`, `"`, false, `\`; `tsv` CRLF, TAB, `"`, true, `\`; `json` LF-separated documents. Each element can be overridden with `linesTerminatedBy`, `fieldsTerminatedBy`, `fieldsEnclosedBy`, `fieldsOptionallyEnclosed`, `fieldsEscapedBy`.
* `columns`: names in file order; an integer captures the field as `@N`. `decodeColumns`: dictionary that assigns expressions to target columns "in the same way as the SET clause of a LOAD DATA statement" (e.g. `{'power': 'POW(@1, @2)'}`).
* `threads` default max 8, effective `min{max{1, threads}, chunks}`; `bytesPerChunk` default 50M, minimum 131072 bytes (single-file only); `skipRows` (per file); `characterSet` (default `character_set_database`; `binary` = no conversion); `replaceDuplicates` default false; `maxRate`; `showProgress`; `sessionInitSql` (documented example: `["SET SESSION sql_log_bin=0;", "SET SESSION innodb_ddl_threads=8,"]`).
* Input may be `.gz`/`.zst` compressed ("detecting the format automatically based on the file extension") but "Compressed files cannot be distributed into chunks"; parallelism then comes only from multiple files. Lists and `*`/`?` globs are accepted and all land in one table.
* Not documented on the page: `maxBytesPerTransaction`, `onDuplicateKey`.

## util.dumpInstance / dumpSchemas / dumpTables and util.loadDump
* Dump layout: DDL `.sql` files, data as chunked `schema@table@@N.tsv.zst` with `.idx` files, metadata `@.json`, `@.done.json`, `schema.json`, `schema@table.json`, plus `@.sql`/`@.post.sql`. Compression `zstd` (default, level 1) / `gzip` / `none`; `chunking` on, `bytesPerChunk` 64 MB, `threads` 4, `consistent` true; `ddlOnly`, `dataOnly`, `dryRun`. `compatibility` modifiers include `strip_definers` (removes DEFINER and sets SQL SECURITY INVOKER), `force_innodb`, `strip_tablespaces`, `ignore_missing_pks`, `create_invisible_pks`, `strip_restricted_grants`, `skip_invalid_accounts` ([dump record](/sources/mysql-shell-9-7-dump-utilities.md)).
* loadDump: "uses the DDL files and tab-separated .tsv data files to set up the server instance or schema in the target MySQL instance, then loads the data." Destination must be MySQL 5.7+.
* **Index deferral** (the fact behind the load-first/index-second strategy): `deferTableIndexes: [ off | fulltext | all ]` — "Defer the creation of secondary indexes until after the table data is loaded. This can reduce loading times. off means all indexes are created during the table load. The default setting fulltext defers full-text indexes only. all defers all secondary indexes and only creates primary indexes during the table load, and also indexes defined on columns containing auto-increment values." `loadIndexes: false` skips secondary indexes entirely ("you must create them afterwards").
* Other options: `loadUsers` (default false; error if the user exists), `ignoreVersion` (needed only when major versions are non-consecutive), `ignoreExistingObjects`, `resetProgress` (requires manual cleanup first), `progressFile`, `threads` (default 4; chunked dumps let several threads load one table), `skipBinlog` (`SET sql_log_bin=0`), `characterSet` (default from metadata, utf8mb4), `schema` (rename on load), include/exclude schemas/tables, `analyzeTables`, `createInvisiblePKs` (target >= 8.0.24), `handleGrantErrors`, `sessionInitSql`, `waitDumpTimeout`, `dryRun`, `updateGtidSet` ([loadDump record](/sources/mysql-shell-9-7-load-dump.md)).
* "The LOAD DATA LOCAL INFILE statement uses nonrestrictive data interpretation, which turns errors into warnings and continues with the load operation." Dumps from Shell >= 8.0.27 cannot be loaded by older Shells.

## util.copyInstance / copySchemas / copyTables
* "copy DDL and data between MySQL instances, without the need for intermediate storage. The data is streamed from source to destination." Options mirror dump+load (`threads` 4, `compatibility`, `deferTableIndexes` default fulltext, `dryRun`, `ignoreVersion`); "Progress resumption is not supported"; consistency only for InnoDB; object names must be latin1 or utf8 ([copy record](/sources/mysql-shell-9-7-copy-utilities.md)).

## Unattended invocation
* CLI form: `mysqlsh [options] -- [shell_object]+ object_method [arguments]`; camelCase becomes hyphenated (`check-for-server-upgrade`); `mysqlsh -- util --help`; unknown object/method exits with status 10; Shell reads option files and login paths unless `--no-defaults` ([CLI overview](/sources/mysql-shell-9-7-command-line-integration-overview.md)).
* Batch form: `mysqlsh --py --file load.py`, `mysqlsh < script.js`, `echo "..." | mysqlsh --sql --uri ...`; in batch mode only language code runs, no interactive commands ([batch record](/sources/mysql-shell-9-7-batch-code-execution.md)).

# Inferred
* **Inferred:** because the builder stage runs inside the `mysql:9.7.2` image, the socket path is `/var/run/mysqld/mysqld.sock` (Dockerfile patches `/etc/my.cnf`), so loaders connect with `mysqlsh --no-defaults -uroot --socket=/var/run/mysqld/mysqld.sock --py --file ...`; the entrypoint's own `mysql_socket_fix` comment notes that "`mysqlsh --mysql` doesn't read the [client] config", so the socket must be passed explicitly.
* **Inferred:** `importTable` with `bytesPerChunk` 50M and 8 threads is I/O-bound on the WSL2 disk; the plan's default is `threads: 4` matching the image's 4-vCPU CI target, tuned by task E-02.
* **Inferred:** the `.tsv.zst` chunk format written by `dumpSchemas` is also a good *publishing* format for extended-tier bundles (zstd, chunked, self-describing, loadable with `deferTableIndexes:"all"`), at the cost of requiring mysqlsh on the consumer side, which the image provides.

# Limits that matter for this project
1. Every Shell loader needs `local_infile=ON` on the temporary build server; forgetting it fails with ERROR 3950.
2. Compressed inputs to `importTable` are single-threaded per file — keep converter output uncompressed (or split into many files) when speed matters; compress only for publishing.
3. `importTable` is strictly one target table per invocation and cannot express foreign-key order; the Makefile orders calls.
4. `loadDump` is for dumps produced by Shell's own dump utilities; it does not load arbitrary CSV directories (use importTable for those).
5. Nonrestrictive interpretation means silent coercion: counts and digests ([checksum method](/decisions/test-checksum-method.md)) are the only proof of a lossless load; `SHOW WARNINGS` output should be captured per table.
6. GPLv2 tooling inside the image is unchanged from the base image; the project redistributes unmodified Oracle binaries, so the obligation is Oracle's source offer, nothing new ([GPL record](/licenses/gpl-2-0.md)).

# Role in the plan
* Primary loader for converter output (`util.importTable`, dialect `default` TSV with `\N` NULLs), invoked in `.py` batch scripts.
* `util.dumpSchemas` + `util.loadDump(deferTableIndexes:"all")` for MySQL-native sources (Sakila, Employees, World, Menagerie) and for extended-tier bundles.
* `copy*` utilities: only if a dataset is available solely as a running MySQL server (none in the inventory so far).

# Open questions
* Whether `mysqlsh -- util import-table` accepts `--decode-columns` as a JSON dictionary on the command line is not shown on the overview page; the batch `.py` form avoids the question.
