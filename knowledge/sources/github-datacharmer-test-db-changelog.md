---
type: Source
title: test_db Changelog
description: Version history 1.0.0 (2008-01-03) to 1.0.7 (2015-08-30) of the employees sample database.
resource: https://raw.githubusercontent.com/datacharmer/test_db/master/Changelog
tags:
- employees
- changelog
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://raw.githubusercontent.com/datacharmer/test_db/master/Changelog
  title: Changelog
  accessed: "2026-09-02"
  version: master @ e324b56
---

# What was read
The whole file (964 bytes), accessed 2026-09-02.

# Relevant excerpt
"1.0.7 2015-08-30 - Moved to GitHub - Fixed bug#393423 Duplicate key in dept_manager - Fixed bug#393429 Column order in employees.dept_manager is incorrect - Adapted partitioned structure to MySQL 5.5+ syntax"; 1.0.5 2008-08-02 "added some database objects (views, stored procedures and functions)"; 1.0.3 2008-07-19 "adapted for testing on MD5 or SHA1 (two separated test files)"; 1.0.2 2008-03-15 "replaced LOAD DATA with SQL dumps"; 1.0.0 2008-01-03 "Based on a work by Fusheng Wang and Carlo Zaniolo - modified by Giuseppe Maxia and Patrick Crews".

# What it was used to decide
Version identity (1.0.7) and the explanation for the dept_emp checksum differing from the older dev.mysql.com page, in [Employees](/datasets/employees.md).
