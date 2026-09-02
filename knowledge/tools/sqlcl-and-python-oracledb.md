---
type: Tool
title: SQLcl and python-oracledb as Oracle-side load/export tools
description: SQLcl (Java CLI, OTN developer license) provides the LOAD command the SH installer requires and csv/json/insert SQLFORMAT spooling; python-oracledb (UPL/Apache, Thin mode, no Instant Client) is the preferred programmatic exporter for the optional Oracle verification profile.
resource: https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.2/sqcug/
tags: [oracle, sqlcl, python-oracledb, export, oracle-group]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: /sources/oracle-docs-sqlcl-26-2-load-and-sqlformat.md
    title: SQLcl 26.2 LOAD / SET LOADFORMAT / SET SQLFORMAT, download HEAD
    accessed: "2026-09-02"
  - resource: /sources/oracle-otn-license-agreement.md
    title: OTN License Agreement (SQLcl download license)
    accessed: "2026-09-02"
  - resource: /sources/python-oracledb-docs-and-license.md
    title: python-oracledb docs and LICENSE
    accessed: "2026-09-02"
  - resource: /sources/oracle-database-free-faq-and-get-started.md
    title: "FAQ: SQLcl not part of Database Free"
    accessed: "2026-09-02"
---

# Facts

## SQLcl
* Latest documented release 26.2; direct download `https://download.oracle.com/otn_software/java/sqldeveloper/sqlcl-latest.zip` answers HTTP 200 with `Content-Length: 121421628` (≈121 MB) to an unauthenticated HEAD; the download page links the **Oracle Technology Network License Agreement** ("internally use the Programs ... only for the purpose of developing, testing, prototyping, and demonstrating Your application ... not ... for any data processing, business, commercial, or production purposes"). Consequence: SQLcl may run inside our build/verification container but must never be packaged into the published image. Java requirement not captured from the page (**inferred:** a JDK 17+ is needed; verify from the zip's README).
* `LOAD [TABLE] table file [NEW|CREATE]` reads CSV with defaults "comma, optionally enclosed in double quotes, UTF8, header row, 50 rows per batch, commit every 10 batches, abort after 50 errors"; the SH installer sets `SET LOAD BATCH_ROWS 10000 BATCHES_PER_COMMIT 1 DATE_FORMAT YYYY-MM-DD`. `SET LOADFORMAT` exposes `DELIMITER`, `ENCLOSURES`, `ENCODING`, `ROW_TERMINATOR`, `SKIP_ROWS`.
* Export: `SET SQLFORMAT csv` (also `json`, `insert`, `loader`, `xml`, `html`, `fixed`) + `SPOOL file` + `SELECT ...` writes a delimited file; the `UNLOAD` command uses the same format list. The CSV quoting/NULL/date rendering rules were not found on the SET page (**inferred:** strings are double-quoted, NULL is empty, dates follow `NLS_DATE_FORMAT` — set it explicitly to `YYYY-MM-DD HH24:MI:SS` before spooling; verify on first run).
* SQLcl is **not** shipped inside Oracle Database Free ([FAQ](/sources/oracle-database-free-faq-and-get-started.md)); a `build-oracle` profile must add it.

## python-oracledb
* v4.0.2 (2026-07-14); `python -m pip install oracledb`; Thin mode "does not need Oracle Client libraries"; wheels for Linux x86-64 and aarch64; Python 3.10–3.15; tested against Oracle 19/21/26.
* License: dual **UPL 1.0 / Apache 2.0** ("You may choose either license") — no distribution restriction, so it can live in the shared `work` loader image ([build orchestration](/decisions/build-orchestration.md)).
* Recommended export pattern for the verification profile: connect `oracledb.connect(user="hr", password=..., dsn="oracle:1521/FREEPDB1")`, iterate `SELECT * FROM <table> ORDER BY <pk>`, write CSV with Python's `csv` module (`QUOTE_MINIMAL`, `\n`, ISO timestamps rendered from `datetime` objects, `None` → empty), and compute the same per-table checksums the converter computes from the scripts. `TIMESTAMP WITH LOCAL TIME ZONE` comes back as naive `datetime` in the session time zone — set `ALTER SESSION SET TIME_ZONE='UTC'` first ([Oracle data types](/sources/oracle-docs-sql-language-reference-23-data-types.md)). `NVARCHAR2`/`UNISTR` text arrives as Python `str` (UTF-8 out of the box with `AL32UTF8`). Object columns (`cust_address_typ`, `phone_list_typ`) come back as `oracledb.Object` and need attribute access — the same flattening the script parser performs.

# Limits
* SQLcl is distributed under the OTN license (development/test use only) and is therefore confined to the opt-in verification profile; nothing from it is redistributed.
* python-oracledb Thin mode needs no Oracle client but cannot read `.dmp` Data Pump files; the XML purchase-order dump stays out of scope.

# Where each is used
* Primary path (no Oracle at all): neither tool is needed — see [conversion path decision](/decisions/oracle-conversion-path.md).
* Verification profile: python-oracledb (preferred) or SQLcl `SET SQLFORMAT csv` spooling to produce an independent CSV per table for row-count/checksum comparison against the script-parsed conversion.
