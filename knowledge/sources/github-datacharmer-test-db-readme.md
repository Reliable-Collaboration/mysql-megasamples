---
type: Source
title: datacharmer/test_db README (master, 2026-04-10)
description: README of the MySQL Employees sample database repository - origin, license, install and test instructions, MD5/SHA removal note for MySQL 9.6+.
resource: https://raw.githubusercontent.com/datacharmer/test_db/master/README.md
tags: [employees, test_db, readme]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/datacharmer/test_db/master/README.md
    title: README.md
    accessed: 2026-09-02
    version: master @ e324b56 (2026-04-10)
---

# What was read
README.md at master (9,531 bytes), accessed 2026-09-02.

# Relevant excerpt
* "The original data was created by Fusheng Wang and Carlo Zaniolo at Siemens Corporate Research. The data is in XML format. http://timecenter.cs.aau.dk/software.htm" ... "Giuseppe Maxia made the relational schema and Patrick Crews exported the data in relational format." "The database contains about 300,000 employee records with 2.8 million salary entries. The export data is 167 MB".
* "To the best of my knowledge, this data is fabricated and it does not correspond to real people. Any similarity to existing people is purely coincidental."
* "Starting with MySQL 9.6, the `MD5()` and `SHA()` functions have been removed from the server. The integrity test files `test_employees_md5.sql` and `test_employees_sha.sql` will not work on 9.6+. Use `test_employees_sha2.sql` instead, which uses `SHA2(..., 256)` and is compatible with all versions".
* Tested versions in CI (dbdeployer, weekly): MySQL 5.6, 5.7, 8.0, 8.4, 9.0, 9.2, 9.5, 9.6; Percona 8.0, 8.4; MariaDB 10.11, 11.4, 12.1; "The SHA-256 checksums are identical between MySQL and PostgreSQL".
* Install: `mysql < employees.sql` (or `employees_partitioned.sql`); test: `mysql -t < test_employees_sha2.sql`. Expected records: employees 300024, departments 9, dept_manager 24, dept_emp 331603, titles 443308, salaries 2844047 (with MD5 CRCs in the README example output).
* "## LICENSE This work is licensed under the Creative Commons Attribution-Share Alike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA."

# What it was used to decide
[Employees dataset](/datasets/employees.md); [CC BY-SA 3.0 record](/licenses/cc-by-sa-3-0.md); [classic_hashing tool note](/tools/mysql-classic-hashing-component.md).
