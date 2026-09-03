---
type: Dataset
title: Employees (datacharmer/test_db)
description: The MySQL "Employees Sample Database" - 300,024 fabricated employees with 2.8 M salary rows; MySQL-native SQL dumps with a published SHA-256 integrity suite; CC BY-SA 3.0.
resource: https://github.com/datacharmer/test_db
tags:
- tier-core-medium
- mysql-native
- employees
- cc-by-sa-3-0
- checksums
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:48:59Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://raw.githubusercontent.com/datacharmer/test_db/master/README.md
  title: test_db README
  accessed: "2026-09-02"
  version: master @ e324b56 (2026-04-10)
- resource: https://api.github.com/repos/datacharmer/test_db
  title: GitHub API - release v1.0.7, file sizes
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/datacharmer/test_db/master/employees.sql
  title: employees.sql
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/datacharmer/test_db/master/objects.sql
  title: objects.sql
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/datacharmer/test_db/master/test_employees_sha2.sql
  title: test_employees_sha2.sql
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/datacharmer/test_db/master/Changelog
  title: Changelog
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/employee/en/employees-validation.html
  title: MySQL Employees manual - validation
  accessed: "2026-09-02"
---

# Identity
"Employees Sample Database", maintained by Giuseppe Maxia (datacharmer) on GitHub and documented by Oracle at https://dev.mysql.com/doc/employee/en/. Six tables of temporal HR data: employees, departments, dept_manager, dept_emp, titles, salaries. Version 1.0.7 (Changelog 2015-08-30; GitHub tag 2020-10-31) plus untagged master fixes (SHA-256 test, CI) ([README](/sources/github-datacharmer-test-db-readme.md), [Changelog](/sources/github-datacharmer-test-db-changelog.md)).

# Source artifact
* Repository https://github.com/datacharmer/test_db, master commit `e324b56193ca506ab7cc1ab143a9153d8c4535d7` (2026-04-10). Release tarball https://github.com/datacharmer/test_db/releases/download/v1.0.7/test_db-1.0.7.tar.gz (35,607,473 bytes) is older than master and lacks `test_employees_sha2.sql` - pin the commit, not the tag ([API](/sources/github-datacharmer-test-db-api.md)).
* Files: employees.sql 4,193 B; objects.sql 4,568 B; load_departments.dump 250 B; load_employees.dump 17,722,832 B; load_dept_emp.dump 14,159,880 B; load_dept_manager.dump 1,090 B; load_titles.dump 21,708,736 B; load_salaries1/2/3.dump 39,806,034 / 39,805,981 / 39,080,916 B - dumps total 172,285,719 B (README: "167 MB"). No auth. No upstream file checksums; per-table SHA-256 data checksums are published (below).
* Also in the repo: `postgresql/` port, `sakila/` derived copy (not used), `employees_partitioned.sql`.

# Native format and friendlier forms
Native: MySQL SQL - `employees.sql` (DDL + views) that `source`s eight `.dump` files of multi-row INSERTs. Friendlier form is not needed; the only obstacle is the client-side `source` directive ([employees.sql](/sources/github-datacharmer-test-db-employees-sql.md)).

# Shape
| table | rows (published) | table | rows |
|---|---|---|---|
| employees | 300,024 | dept_emp | 331,603 |
| departments | 9 | titles | 443,308 |
| dept_manager | 24 | salaries | 2,844,047 |

Total 3,919,015 rows. Encoding: no charset declared in the DDL (server default utf8mb4 applies); `load_employees.dump` contains no non-ASCII bytes; names are Latin transliterations ("Kyoichi Maliniak", "Duangkaew Piveteau"). **Inferred:** the other dumps (dates, ints, titles like "Senior Engineer") are ASCII too. Loaded size: **Inferred** 150-250 MB InnoDB including secondary indexes (the dumps are 172 MB of text).

# Conversion path
Concatenate DDL + dumps (+ objects.sql) into one SQL stream, drop `source`/`flush binary logs`, load through the mysql client against the build server during `make employees`, verify with `test_employees_sha2.sql` ([decision](/decisions/employees-conversion-path.md)).

# Type-mapping hazards
* `flush /*!50503 binary */ logs;` in employees.sql - remove (needs RELOAD, and binary logging may be off).
* `source file ;` lines resolve relative to the mysql client CWD - remove by inlining.
* `#`-style comment line in employees.sql - valid for the mysql client and server; keep or convert to `--`.
* `gender ENUM('M','F')`, `CHAR(4)` dept_no keys, `to_date` sentinel `9999-01-01` for current rows (**Inferred** from the temporal design; verify with `SELECT MAX(to_date) FROM salaries`).
* `employees_partitioned.sql` (RANGE partitioning) not used.
* Test scripts create helper tables inside the `employees` database; they and `show_departments()` use TEMPORARY tables.

# Programmable objects
* Ported: views `dept_emp_latest_date`, `current_dept_emp` (in employees.sql).
* Ported optionally (objects.sql, loaded after data): functions `emp_dept_id`, `emp_dept_name`, `emp_name`, `current_manager`, `employees_usage`; procedures `show_departments`, `employees_help`; views `v_full_employees`, `v_full_departments` ([objects.sql](/sources/github-datacharmer-test-db-objects-sql.md)). Functions declare `reads sql data`; with binary logging on, non-deterministic functions need `log_bin_trust_function_creators` or a `DETERMINISTIC` declaration (**Inferred**; the official image enables binlog by default in 8.x - verify on 9.7).
* No triggers.

# Indexing
Upstream: primary keys on every table, `UNIQUE KEY (dept_name)`, foreign keys with `ON DELETE CASCADE` (dept_manager, dept_emp, titles, salaries -> employees; -> departments). Keep as-is.

# Tests and expected values
Run [test_employees_sha2.sql](/sources/github-datacharmer-test-db-test-sha2.md); it must print `CRC OK` and `count OK`. Expected SHA-256 chained checksums: employees `21f5d003842f24853e251d3d5116798bafe257ec3d1bb448b5365b68deaabbf4`, departments `377c5d727383a32633e2973f8e3411beffe29e2f4cc297c586fa6b24aa7df9ba`, dept_manager `3a4e69723deec413a7d8a4f5ce55013830303fa617b6380ed2b0fd2d48b1c768`, dept_emp `34548ee9989dd4d5e065168b43249c8d3eb48bfbbfb3f2fc1cf01be6658f6a75`, titles `a9e940ef9ba1029a8f0356fdbe495430bedc59eec5ceb4f71e0cc35ddcbf9980`, salaries `4e99e691a9ea98fefc0b4fec8ca4e758baeefba2967bd8d6474810a9a5f6e729`. The MD5/SHA-1 variants ([md5](/sources/github-datacharmer-test-db-test-md5.md), [sha](/sources/github-datacharmer-test-db-test-sha.md)) cannot run on 9.7 without the classic_hashing component ([tool note](/tools/mysql-classic-hashing-component.md)); the dept_emp values printed on dev.mysql.com are stale ([manual](/sources/mysql-employee-manual.md)).

**M-01 result (2026-09-02): green, and independently verified.** All six published row counts match, and the upstream `test_employees_sha2.sql` reports `CRC OK` and `count OK` for every table — third-party confirmation that the conversion is byte-perfect, with the same SHA-256 values this record quotes (employees `21f5d003…`, salaries `4e99e691…`). 3,919,015 rows load in 15.2 s and occupy **146.8 MB** in InnoDB, against this record's inferred 150–250 MB. Full verification including per-table digests takes 10.7 s.
The upstream loader is driven by the mysql client's own `source` command and a `flush binary logs`; neither survives being piped, so the converter splices the dump files inline in upstream order and skips the non-data helper `show_elapsed.sql`.

# Tier assignment
core (medium) - the [tier model](/decisions/tier-model.md) explicitly names Employees among the "medium" core datasets (up to roughly 200 MB each); it is the canonical "large" MySQL sample with a built-in verification suite, 172 MB of SQL compressing to ~36 MB; loaded size (inferred 150-250 MB) must be measured to confirm it stays within that allowance. Evidence: [API sizes](/sources/github-datacharmer-test-db-api.md).

# License and attribution
[CC BY-SA 3.0](/licenses/cc-by-sa-3-0.md). Required notice (verbatim from the README/file headers): "This work is licensed under the Creative Commons Attribution-Share Alike 3.0 Unported License." Attribution: "Original data created by Fusheng Wang and Carlo Zaniolo" (Siemens Corporate Research, TimeCenter), "Current schema by Giuseppe Maxia", "Data conversion from XML to relational by Patrick Crews", "Copyright (C) 2007,2008, MySQL AB". Keep the disclaimer "To the best of our knowledge, this data is fabricated, and it does not correspond to real people." Share-alike: the converted database stays CC BY-SA 3.0.

# Database name
`employees` (fixed by upstream `CREATE DATABASE employees`).

# Open questions
* Whether to keep binary logging on in the image (affects function creation) - see the generic MySQL behaviour notes ([tools/mysql-9x-behaviour-notes.md](/tools/mysql-9x-behaviour-notes.md), owned by the tools agent).
* Exact loaded InnoDB size on 9.7 (measure `information_schema.TABLES` after first load) to settle core vs extended.
