---
type: Source
title: test_db test_employees_sha.sql (SHA-1 integrity test, MySQL 8.0-9.5 only)
description: Same expected counts and SHA-1 checksums as the md5 file's crc_sha column, computed with sha(); unusable on 9.6+ without classic_hashing.
resource: https://raw.githubusercontent.com/datacharmer/test_db/master/test_employees_sha.sql
tags:
- employees
- checksum
- sha1
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
- resource: https://raw.githubusercontent.com/datacharmer/test_db/master/test_employees_sha.sql
  title: test_employees_sha.sql
  accessed: "2026-09-02"
  version: master @ e324b56
---

# What was read
The whole file (4,715 bytes), accessed 2026-09-02.

# Relevant excerpt
Identical `expected_values` rows to the md5 file; computes `@crc := sha(CONCAT_WS('#',@crc, ...))` per table and compares `crc_sha`.

# What it was used to decide
Not used for tests on 9.7; documented for completeness in [Employees](/datasets/employees.md).
