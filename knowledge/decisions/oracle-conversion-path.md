---
type: Decision
title: Oracle sample schemas — convert from the plain scripts/CSVs with a Python converter; Oracle Database Free only as an optional verification profile
description: For HR, CO, SH and OE the upstream artifacts are plain INSERT scripts and RFC-4180 CSV files, so no Oracle product is needed; an opt-in build-oracle Compose profile (Oracle Database Free + python-oracledb) is reserved for cross-checking row counts and checksums.
resource: /decisions/oracle-conversion-path.md
tags:
- decision
- oracle
- conversion-path
- oracle-group
status: stable
trust: inferred
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: /sources/github-oracle-samples-db-sample-schemas-hr-scripts.md
  title: HR scripts
  accessed: "2026-09-02"
- resource: /sources/github-oracle-samples-db-sample-schemas-co-scripts.md
  title: CO scripts
  accessed: "2026-09-02"
- resource: /sources/github-oracle-samples-db-sample-schemas-sh-scripts.md
  title: SH scripts and CSV samples
  accessed: "2026-09-02"
- resource: /sources/github-oracle-samples-db-sample-schemas-oe-pm-ix-scripts.md
  title: OE/PM/IX scripts
  accessed: "2026-09-02"
- resource: /sources/oracle-container-registry-database-free-api-probe.md
  title: Oracle Free image sizes and anonymous pull
  accessed: "2026-09-02"
- resource: /sources/oracle-free-use-terms-and-conditions.md
  title: Oracle Free Use Terms
  accessed: "2026-09-02"
- resource: /sources/oracle-otn-license-agreement.md
  title: OTN license (SQLcl)
  accessed: "2026-09-02"
---

# Question
How do we turn the four Oracle sample schemas (HR, CO, SH, OE) into MySQL databases: (a) parse the upstream SQL/CSV artifacts directly, or (b) run Oracle Database Free in the build, install the schemas with their own scripts, and export?

# Options considered
1. **(a) Direct conversion with a Python converter (`datasets/oracle_*/convert/oracle_scripts.py (one shared parser module, `scripts/oracle_scripts.py`)`)** — chosen for all four schemas.
   * HR: 7 tables / 216 rows of `INSERT ... VALUES` with `TO_DATE` — trivial grammar ([HR source](/sources/github-oracle-samples-db-sample-schemas-hr-scripts.md)).
   * CO: one 1.27 MB script of column-list INSERTs with `TO_TIMESTAMP` and `UTL_RAW.CAST_TO_RAW('{json}')`; multi-line literals ([CO source](/sources/github-oracle-samples-db-sample-schemas-co-scripts.md)).
   * SH: three tiny INSERT dimensions plus **six plain CSV files with header rows** (SQLcl `LOAD` defaults = comma, double-quote enclosure, UTF-8); only quirks are 80-column space padding in sales.csv and `""`-as-NULL ([SH source](/sources/github-oracle-samples-db-sample-schemas-sh-scripts.md)). `LOAD DATA LOCAL INFILE` handles 918,843 rows in seconds.
   * OE: object constructors (`cust_address_typ(...)`, `PHONE_LIST_TYP(...)`, `MDSYS.SDO_GEOMETRY(...)`), `UNISTR` escapes, `to_yminterval`, XML literals — a few extra token types in the same parser; the archived installer needs SYS/HR passwords, `perl`, XML DB and `sqlldr`, and targets "19c and lower", so it is *less* likely to run unattended on 26ai Free ([OE source](/sources/github-oracle-samples-db-sample-schemas-oe-pm-ix-scripts.md)).
   * Cost: one converter module with ~10 token types; runs on the `work` image with no extra downloads beyond the 108 MB repo tree (of which 91 MB are SH CSVs).
2. **(b) Oracle Database Free container + install scripts + export** — kept as an optional `build-oracle` Compose profile for verification only.
   * Image `container-registry.oracle.com/database/free:latest` pulls anonymously, is multi-arch (amd64/arm64) and 3.7 GB compressed (0.9 GB `-lite`); gvenzl/oracle-free is 1.2 GB; 2–5 min database creation; RAM capped at 2 GB by the product; SQLcl (≈121 MB, OTN developer license, must not be redistributed) plus a JDK are needed to run `sh_install.sql` at all; the export needs python-oracledb (UPL/Apache) or SQLcl `SET SQLFORMAT csv` ([container tool](/tools/oracle-database-free-container.md), [SQLcl/python-oracledb tool](/tools/sqlcl-and-python-oracledb.md)).
   * Licensing is fine for internal build use (Oracle Free Use Terms), but it adds gigabytes, minutes and a second source of truth to every build for data that is already plain text.
   * What (b) would give that (a) cannot: Oracle's own interpretation of ambiguous literals (TSLTZ session zone, 9-digit timestamp rounding, `''`→NULL) and a second row-count/checksum witness.
3. MySQL Workbench Migration Wizard / ora2pg style tools — rejected: both require a live Oracle connection, so they inherit all of (b)'s costs without its verification value.

# Evidence
* Data-format facts and row counts: the four `sources/github-oracle-samples-db-sample-schemas-*-scripts.md` records.
* Image size / login / arm64: [registry probe](/sources/oracle-container-registry-database-free-api-probe.md); limits and license: [FAQ](/sources/oracle-database-free-faq-and-get-started.md), [Free Use Terms](/sources/oracle-free-use-terms-and-conditions.md); SQLcl requirement for SH: [Sample Schemas guide](/sources/oracle-docs-database-sample-schemas-guide-23-comsc.md).

# Outcome (recommendation, per schema)
| schema | path | reason |
|---|---|---|
| HR → `oracle_hr` | (a) | trivial script; port procedures/trigger by hand ([record](/datasets/oracle-hr.md)) |
| CO → `oracle_co` | (a) | one script; converter truncates timestamps to 6 digits and passes JSON through ([record](/datasets/oracle-co.md)) |
| SH → `oracle_sh` | (a) | CSV + `LOAD DATA`; partitions/bitmap/MV/dimension DDL rewritten by the converter ([record](/datasets/oracle-sh.md)) |
| OE → `oracle_oe` | (a) with flattening | object columns → scalar columns/child table, XMLType → TEXT, UNISTR → UTF-8; PM/IX/OC dropped ([record](/datasets/oracle-oe-pm-ix.md)) |
| verification | (b), opt-in `make verify-oracle` | HR/CO/SH installed on `gvenzl/oracle-free:23.26.3` (or the official image) + SQLcl for SH; python-oracledb exports per-table CSV in UTC; compare counts and canonical checksums with the (a) output; OE excluded unless its archived installer proves to run on 26ai |

# Status
accepted by the coordinator on 2026-09-02: path (a) for HR, CO, SH and OE; path (b) is the opt-in `make verify-oracle` cross-check (profile `build-oracle`), run once before the first release and after any converter change.
