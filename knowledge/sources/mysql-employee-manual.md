---
type: Source
title: MySQL "Employees Sample Database" manual (dev.mysql.com)
description: Oracle-hosted guide for the employees database; installation and validation chapters; its printed dept_emp checksums are older than the repository's.
resource: https://dev.mysql.com/doc/employee/en/
tags:
- employees
- manual
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/employee/en/employees-installation.html
  title: 3 Installation
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/employee/en/employees-validation.html
  title: 4 Validating the Employee Data
  accessed: "2026-09-02"
---

# What was read
Chapters 3 and 4 of the manual, accessed 2026-09-02.

# Relevant excerpt
* Installation: download from https://github.com/datacharmer/test_db, `unzip test_db-master.zip; cd test_db-master/; mysql -t < employees.sql`; storage engine chosen by editing employees.sql. No file sizes; no mention of the sakila directory.
* Validation: `time mysql -t < test_employees_sha.sql` / `test_employees_md5.sql`; expected rows employees 300024, departments 9, dept_manager 24, dept_emp 331603, titles 443308, salaries 2844047. The page prints dept_emp SHA `f16f6ce609d032d6b1b34748421e9195c5083da8` and MD5 `c2c4fc7f0506e50959a6c67ad55cac31`, whereas the repository's test files carry `d95ab9fe07df0865f592574b3b33b9c741d9fd1b` / `ccf6fe516f990bdaa49713fc478701b7` (the 1.0.7 bug fixes changed dept_emp/dept_manager). No note about MySQL 9.6 hash-function removal.

# What it was used to decide
Treat the repository test files as authoritative, not this page ([Employees](/datasets/employees.md)).
