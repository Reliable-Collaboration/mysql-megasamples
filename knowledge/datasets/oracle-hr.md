---
type: Dataset
title: Oracle HR (Human Resources) sample schema
description: The 7-table, 216-row teaching schema from Oracle's db-sample-schemas v23.3, converted from its plain INSERT scripts; the foundation OE depends on.
resource: https://github.com/oracle-samples/db-sample-schemas/tree/v23.3/human_resources
tags:
- tier-core
- oracle
- hr
- small
- mit
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: /sources/github-oracle-samples-db-sample-schemas-releases-and-tree.md
  title: Releases, tags, tree sizes
  accessed: "2026-09-02"
- resource: /sources/github-oracle-samples-db-sample-schemas-hr-scripts.md
  title: hr_install/hr_create/hr_populate/hr_code scripts
  accessed: "2026-09-02"
- resource: /sources/github-oracle-samples-db-sample-schemas-readme-and-license.md
  title: README and LICENSE.txt
  accessed: "2026-09-02"
- resource: /sources/oracle-docs-database-sample-schemas-guide-23-comsc.md
  title: Oracle Sample Schemas guide (HR pages)
  accessed: "2026-09-02"
- resource: /sources/oracle-docs-sql-language-reference-23-data-types.md
  title: Oracle data types
  accessed: "2026-09-02"
- resource: /sources/mysql-refman-9-7-char.md
  title: MySQL CHAR semantics
  accessed: "2026-09-02"
---

# Identity
Oracle "HR" — employees, departments, jobs, locations, countries, regions, job history. Current (not archived) in the v23.3 release and in the 26ai documentation. Proposed MySQL database name: **`oracle_hr`** (per [naming decision](/decisions/database-naming-convention.md)).

# Source artifact
* Repository `oracle-samples/db-sample-schemas`, tag **v23.3** ("Oracle Database Sample Schemas 23c", release published 2023-04-18). Pin the **commit `e3325a83e56c516815844025418a96ecaf219751`** (the tag was moved to it on 2024-03-28); `main` (`6660bad`, 2025-06-25) differs from v23.3 only in README files and two spelling fixes in `hr_create.sql` column comments ([releases source](/sources/github-oracle-samples-db-sample-schemas-releases-and-tree.md)).
* Files (bytes): `human_resources/hr_install.sql` 8,275; `hr_create.sql` 17,112; `hr_populate.sql` 41,301; `hr_code.sql` 3,849; `hr_uninstall.sql` 2,920; README.md 2,642. Directory total 78,765 bytes. Fetch the four `.sql` files individually from `https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/<sha>/human_resources/<file>` or the release zip. No auth, no click-through.
* Checksums: none published upstream; the executor records the sha256 of each fetched file in `build/baseline.json`. Schema version string inside the README: "21.1", release date 03-FEB-2022.

# Native format and friendlier forms
Plain SQL*Plus/SQLcl scripts: DDL in `hr_create.sql`, single-row `INSERT INTO <table> VALUES (...)` statements inside PL/SQL `BEGIN ... END; /` blocks in `hr_populate.sql` (dates as `TO_DATE('17-06-2013', 'dd-MM-yyyy')`), procedures/triggers in `hr_code.sql`. **No Oracle product is needed to read them**; the only Oracle-isms are `TO_DATE`, `Prompt`/`SET`/`REM` directives, `ORGANIZATION INDEX`, `CREATE SEQUENCE`, `COMMENT ON`, and the PL/SQL wrappers.

# Shape
| table | rows | notes |
|---|---|---|
| regions | 5 | `region_id NUMBER` (unconstrained, integer values), `region_name VARCHAR2(25)` |
| countries | 25 | `country_id CHAR(2)` PK (IOT), `country_name VARCHAR2(60)`, `region_id NUMBER` FK |
| locations | 23 | `location_id NUMBER(4)`, street/postal/city/state, `country_id CHAR(2)` FK |
| departments | 27 | `department_id NUMBER(4)`, `manager_id NUMBER(6)` FK employees, `location_id` FK |
| jobs | 19 | `job_id VARCHAR2(10)` PK, `min_salary`/`max_salary NUMBER(6)` |
| employees | 107 | `employee_id NUMBER(6)`, `email VARCHAR2(25)` UNIQUE, `hire_date DATE`, `salary NUMBER(8,2)` CHECK > 0, `commission_pct NUMBER(2,2)`, self-FK `manager_id` |
| job_history | 10 | PK (`employee_id`, `start_date DATE`), CHECK `end_date > start_date` |

Row counts are both the verification table in `hr_install.sql` and the count of INSERT statements in `hr_populate.sql` (REGIONS is **5**, not 4, in v23.3). Total 216 rows; loaded InnoDB size well under 1 MB (**inferred**). Encoding: pure ASCII (no byte ≥ 0x80 in any HR script); phone numbers `1.515.555.0100`, e-mails are bare upper-case logins (`SKING`). Dates have no time component.

# Conversion path
Python script parser → MySQL DDL + `INSERT` (path (a) in [the decision](/decisions/oracle-conversion-path.md)); the Oracle container is not required. The grammar is regular: `INSERT INTO <t> VALUES ( v, v, ... );` with numeric, `'string'` (`''` escapes), `NULL`, and `TO_DATE('d-m-y','dd-MM-yyyy')` tokens.

# Type-mapping hazards
* `NUMBER` without precision (regions.region_id, countries.region_id) → `INT` (all values are small integers; the converter asserts integrality and magnitude). Rule for the Oracle group: unconstrained NUMBER → `INT`/`BIGINT` when every value is integral, else `DECIMAL(38,10)`; never `DOUBLE` (Oracle NUMBER is exact, [data types source](/sources/oracle-docs-sql-language-reference-23-data-types.md)).
* `NUMBER(4)` → `SMALLINT`, `NUMBER(6)` → `INT` (surrogate keys), `NUMBER(8,2)` salary → `DECIMAL(8,2)`, `NUMBER(2,2)` commission_pct → `DECIMAL(2,2)` (values 0.10–0.40).
* `CHAR(2)` country_id → `CHAR(2)`; `VARCHAR2(n)` → `VARCHAR(n)` utf8mb4 (`n` is bytes in Oracle, characters in MySQL; data is ASCII so lengths cannot overflow).
* `DATE` → `DATE` for hire_date/start_date/end_date because no value carries a time (verified from the populate script); document that Oracle DATE is a datetime type so `DATETIME` is the faithful alternative if a downstream wants Oracle-identical semantics (`DATE` was chosen for query friendliness; the CHECK `end_date > start_date` behaves identically).
* Sequences: `employees_seq` (start 207, step 1) → `employees.employee_id ... AUTO_INCREMENT` with `ALTER TABLE employees AUTO_INCREMENT = 207`; `departments_seq` (start 280, step 10, max 9990) and `locations_seq` (start 3300, step 100, max 9900) cannot be expressed with AUTO_INCREMENT (increment is a global variable) → set `AUTO_INCREMENT = 280` / `3300` and document the lost step/maxvalue; no sequence-emulation table (over-engineering for a teaching schema).
* `ORGANIZATION INDEX` on countries → ordinary InnoDB table (InnoDB clusters on the PK anyway).
* Identifiers: lower-case as in the scripts; MySQL reserved words: none clash (`regions`, `jobs`, ... are fine).

# Programmable objects
| object | action | reason |
|---|---|---|
| view `emp_details_view` | port | plain 6-table join; drop `WITH READ ONLY` (MySQL join views are non-updatable anyway) |
| procedure `secure_dml` | port | `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='You may only make changes during normal office hours'` when `DATE_FORMAT(NOW(),'%H:%i') NOT BETWEEN '08:00' AND '18:00' OR DAYOFWEEK(NOW()) IN (1,7)` |
| trigger `secure_employees` | **not created** (documented) | upstream creates it and immediately `ALTER TRIGGER ... DISABLE`s it; **Inferred:** MySQL has no disabled-trigger state (no `ALTER TRIGGER ... DISABLE` exists; confirmed at S-05), and an active copy would block all writes outside office hours |
| procedure `add_job_history` | port | simple INSERT wrapper |
| trigger `update_job_history` | port | `AFTER UPDATE ON employees FOR EACH ROW IF NOT (OLD.job_id <=> NEW.job_id) OR NOT (OLD.department_id <=> NEW.department_id) THEN CALL add_job_history(OLD.employee_id, OLD.hire_date, CURDATE(), OLD.job_id, OLD.department_id)` — MySQL lacks `UPDATE OF column`, so the column test is explicit; note the PK (employee_id, start_date) collision if hire_date already exists in job_history, exactly as in Oracle |
| CHECK constraints `emp_salary_min`, `jhist_date_interval` | port | MySQL enforces CHECK constraints since 8.0.16 ([verified](/sources/mysql-refman-8-0-create-table-check-constraints.md); see [9.x notes](/tools/mysql-9x-behaviour-notes.md)) |
| `COMMENT ON TABLE/COLUMN` | port | as `COMMENT` clauses in DDL |
| sequences | replace | see hazards |

# Indexing
Recreate the 11 secondary indexes and the unique index on `email`; FKs as declared (`dept_mgr_fk` ↔ `emp_dept_fk` are mutually referencing: create employees and departments first, add both FKs afterwards with `SET foreign_key_checks=0` during load, as `hr_populate.sql` itself disables `dept_mgr_fk`).

# Tests and expected values
**S-05 result (2026-09-02): green.** All 7 counts match, including `regions` = 5 (this record's correction to the older documentation's 4). 10 foreign keys with 0 orphans. Probes confirmed exactly as recorded: employee 100 is `Steven King`, `AD_PRES`, salary 24000, hired 2013-06-17, department 90; and `commission_pct IS NOT NULL` is **35**, the figure this record had only inferred.
Four PL/SQL objects (`secure_dml`, `add_job_history`, `update_job_history`, `secure_employees`) are reported unported rather than guessed at: their bodies use `DECLARE`/`EXCEPTION`/`RAISE_APPLICATION_ERROR`, which is a semantic rewrite. 35 column comments are dropped because MySQL can only set one by restating the whole column definition; the 7 table comments are kept.

* Row counts as in the Shape table (from `hr_install.sql`'s verification block).
* Spot checks: `SELECT COUNT(*) FROM employees WHERE commission_pct IS NOT NULL` = 35 (**inferred**, compute from script); `employee_id 100` is `Steven King`, `AD_PRES`, salary 24000, hire_date 2013-06-17, department 90 (verified from the populate script).
* Checksums: executor computes `CHECKSUM TABLE` and an order-independent per-table sha256 over `SELECT * ORDER BY pk` at build time and stores them in `build/baseline.json`.

# Tier assignment
**core** — 216 rows, < 1 MB loaded (size evidence: scripts total 79 KB; [tier model](/decisions/tier-model.md)).

# License and attribution
MIT, `LICENSE.txt` at v23.3 — [MIT record](/licenses/mit.md). Attribution: "Oracle Database Sample Schemas — Copyright (c) 2023 Oracle and/or its affiliates. MIT License." Not UPL (verified).

# Open questions
* None blocking. The converter should assert that every `NUMBER` value in regions/countries is integral before choosing `INT` (build-time check, no research needed).
