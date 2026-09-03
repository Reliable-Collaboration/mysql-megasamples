---
type: Source
title: "MySQL Shell 9.7: Dump Loading Utility (util.loadDump)"
description: "util.loadDump(): expects DDL .sql + .tsv(.zst) data + .json metadata; local_infile=ON required; loadIndexes/deferTableIndexes, loadUsers, ignoreVersion, resetProgress, threads, skipBinlog, createInvisiblePKs."
resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-load-dump.html
tags:
- mysql-shell
- dump
- load
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:41:13Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:41:13Z"
sources:
- resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-load-dump.html
  title: "MySQL Shell 9.7: Dump Loading Utility (util.loadDump)"
  accessed: "2026-09-02"
  version: MySQL Shell 9.7 manual, section 12.6
---

# What was read
https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-load-dump.html, accessed 2026-09-02; version: MySQL Shell 9.7 manual, section 12.6.

# Relevant excerpt
> "The dump loading utility uses the LOAD DATA LOCAL INFILE statement, so the global setting of the local_infile system variable on the target MySQL instance must be ON for the duration of the import."
> "MySQL Shell's dump loading utility uses the DDL files and tab-separated .tsv data files to set up the server instance or schema in the target MySQL instance, then loads the data." Compressed dumps are decompressed by the utility. "MySQL 5.7 or later is required for the destination MySQL instance".
* `loadDdl`/`loadData` (default true); `loadUsers` default false ("If a user already exists in the target MySQL instance, an error is returned").
* `loadIndexes` default true: "When this option is set to false, secondary indexes are not created during the import, and you must create them afterwards."
* `deferTableIndexes: [ off | fulltext | all ]`: "Defer the creation of secondary indexes until after the table data is loaded. This can reduce loading times. off means all indexes are created during the table load. The default setting fulltext defers full-text indexes only. all defers all secondary indexes and only creates primary indexes during the table load, and also indexes defined on columns containing auto-increment values."
* `analyzeTables: off|on|histogram` (default off); `ignoreVersion` ("Import the dump even if the major version number of the MySQL instance from which the data was dumped is non-consecutive"; not needed between consecutive majors); `ignoreExistingObjects`; `resetProgress` ("you must first manually remove from the target MySQL instance all previously loaded objects"); `progressFile`; `threads` default 4 (chunked dumps let several threads load one table); `backgroundThreads`; `skipBinlog` (issues `SET sql_log_bin=0`); `characterSet` (default from dump metadata, utf8mb4); `schema` (load into a differently named schema); include/exclude schemas and tables; `dryRun`; `updateGtidSet`; `createInvisiblePKs` (adds invisible `my_row_id` PKs, target must be 8.0.24+); `handleGrantErrors: abort|drop_account|ignore`; `sessionInitSql`; `waitDumpTimeout`.
> "The LOAD DATA LOCAL INFILE statement uses nonrestrictive data interpretation, which turns errors into warnings and continues with the load operation."
* Dumps made by Shell >= 8.0.27 cannot be loaded by older Shells.

# What it was used to decide
[MySQL Shell utilities](/tools/mysql-shell-utilities.md): `deferTableIndexes: "all"` matches the load-first-index-second rule in [indexing strategy](/decisions/indexing-strategy.md); the nonrestrictive-interpretation warning drives the row-count and digest tests.
