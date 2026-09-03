---
type: Source
title: test_db test_employees_sha2.sql (SHA-256 integrity test)
description: Expected row counts and chained SHA-256 checksums per table, plus the exact ORDER BY / CONCAT_WS recipe that produces them.
resource: https://raw.githubusercontent.com/datacharmer/test_db/master/test_employees_sha2.sql
tags:
- employees
- checksum
- sha256
- test
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://raw.githubusercontent.com/datacharmer/test_db/master/test_employees_sha2.sql
  title: test_employees_sha2.sql
  accessed: "2026-09-02"
  version: master @ e324b56
---

# What was read
The whole file (3,668 bytes), accessed 2026-09-02. Header: "Uses SHA2() which is available on all MySQL versions (8.0+). This test works on MySQL 9.6+ where md5() and sha() have been removed".

# Relevant excerpt
Expected values (`table_name, recs, crc_sha2`):
* employees 300024 `21f5d003842f24853e251d3d5116798bafe257ec3d1bb448b5365b68deaabbf4`
* departments 9 `377c5d727383a32633e2973f8e3411beffe29e2f4cc297c586fa6b24aa7df9ba`
* dept_manager 24 `3a4e69723deec413a7d8a4f5ce55013830303fa617b6380ed2b0fd2d48b1c768`
* dept_emp 331603 `34548ee9989dd4d5e065168b43249c8d3eb48bfbbfb3f2fc1cf01be6658f6a75`
* titles 443308 `a9e940ef9ba1029a8f0356fdbe495430bedc59eec5ceb4f71e0cc35ddcbf9980`
* salaries 2844047 `4e99e691a9ea98fefc0b4fec8ca4e758baeefba2967bd8d6474810a9a5f6e729`

Recipe (chained hash via a user variable): `SET @crc=''; INSERT INTO tchecksum SELECT @crc := SHA2(CONCAT_WS('#',@crc, emp_no,birth_date,first_name,last_name,gender,hire_date), 256) FROM employees ORDER BY emp_no;` and analogously departments (`dept_no,dept_name` ORDER BY dept_no), dept_manager and dept_emp (`dept_no,emp_no,from_date,to_date` ORDER BY dept_no,emp_no), titles (`emp_no,title,from_date,to_date` ORDER BY emp_no,title,from_date), salaries (`emp_no,salary,from_date,to_date` ORDER BY emp_no,from_date,to_date). Final output: `CRC OK/FAIL`, `count OK/FAIL`.

# What it was used to decide
The test suite for [Employees](/datasets/employees.md) (use this file, not the md5/sha variants, on MySQL 9.7).
