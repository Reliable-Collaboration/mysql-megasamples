---
type: Source
title: Oracle SQLcl 26.2 User's Guide — LOAD / SET LOAD / SET LOADFORMAT and SET SQLFORMAT; SQLcl download endpoint
description: The SQLcl commands the SH installer depends on, their defaults (comma-delimited, double-quote enclosed, UTF-8, header row), the csv/json/insert/loader output formats usable for export, and the direct download URL and size.
resource: https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.2/sqcug/loading-file.html
tags: [oracle, sqlcl, csv, export]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://docs.oracle.com/en/database/oracle/sql-developer-command-line/index.html
    title: SQLcl documentation index (latest 26.2)
    accessed: "2026-09-02"
  - resource: https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.2/sqcug/loading-file.html
    title: LOAD command, SET LOAD, SET LOADFORMAT
    accessed: "2026-09-02"
    version: SQLcl 26.2
  - resource: https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.2/sqcug/set-system_variable-value.html
    title: SET system_variable value (SQLFORMAT, ENCODING)
    accessed: "2026-09-02"
  - resource: https://download.oracle.com/otn_software/java/sqldeveloper/sqlcl-latest.zip
    title: sqlcl-latest.zip (HTTP HEAD only)
    accessed: "2026-09-02"
  - resource: https://www.oracle.com/tools/downloads/sqlcl-downloads.html
    title: SQLcl download page
    accessed: "2026-09-02"
---

# What was read
The SQLcl doc index and two 26.2 guide pages, an HTTP HEAD of the direct download, and the download page text (curl), 2026-09-02.

# Relevant excerpt
* `LOAD [TABLE] [schema.]table_name { <file-specification> | <cloud-storage-specification> } [NEW | SHOW | SHOW_DDL | CREATE | CREATE_DDL]`.
* `SET LOAD` options: `BATCH_ROWS`, `BATCHES_PER_COMMIT`, `CLEAN_NAMES`, `COLUMN_SIZE`, `COMMIT {ON|OFF}`, `DATE|DATE_FORMAT format_mask`, `ERRORS {n|UNLIMITED}`, `LOCALE`, `MAP_COLUMN_NAMES`, `METHOD INSERT`, `SCAN_ROWS`, `TIMESTAMP_FORMAT`, `TIMESTAMPTZ_FORMAT`, `TRUNCATE`, `UNKNOWN_COLUMNS_FAIL`.
* `SET LOADFORMAT [default|csv|delimited|html|insert|json|json-formatted|loader|t2|xml]` with `COLUMN_NAMES {ON|OFF}`, `DELIMITER`, `DOUBLE`, `ENCLOSURES`, `ENCODING`, `LEFT/RIGHT`, `ROW_LIMIT`, `SKIP_ROWS`, `SKIP_AFTER_NAMES`, `ROW_TERMINATOR {CR|CRLF|LF}`; html/insert/json/loader/t2/xml "For `UNLOAD` command only". Defaults: "Columns delimited by comma, optionally enclosed in double quotes; Lines terminated with standard line terminators (Windows, UNIX, Mac); File encoded UTF8; 50 rows per batch; Commit every 10 batches (if AUTOCOMMIT set); Load terminates if more than 50 errors found".
* `SET SQLFORMAT {csv | html | xml | json | ansiconsole | insert | loader | fixed | default}`; `SET ENCODING <encoding>`.
* Download: `sqlcl-latest.zip` HEAD → `HTTP/1.1 200 OK`, `Content-Length: 121421628` (≈121 MB), `Last-Modified: Mon, 31 Aug 2026`; no authentication challenge on the HEAD. The download page states "All software downloads are free, and most come with a Developer License ..." and links to the [Oracle Technology Network License Agreement](/sources/oracle-otn-license-agreement.md); the page did not expose the SQLcl version string in the fetched HTML.

# What it was used to decide
[SQLcl and python-oracledb tool record](/tools/sqlcl-and-python-oracledb.md); the SH CSV format description in the [SH dataset record](/datasets/oracle-sh.md) (the SQLcl defaults are exactly what the `.csv` files follow, so any RFC-4180 CSV reader can read them).
