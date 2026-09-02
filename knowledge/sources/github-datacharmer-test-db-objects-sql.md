---
type: Source
title: test_db objects.sql (optional functions, procedures, views)
description: Four functions, two procedures and two views layered on the employees schema; not loaded by employees.sql.
resource: https://raw.githubusercontent.com/datacharmer/test_db/master/objects.sql
tags: [employees, routines, views]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/datacharmer/test_db/master/objects.sql
    title: objects.sql
    accessed: "2026-09-02"
    version: master @ e324b56
---

# What was read
The whole file (4,568 bytes), accessed 2026-09-02.

# Relevant excerpt
* Functions: `emp_dept_id(int) RETURNS char(4) reads sql data`, `emp_dept_name(int) RETURNS varchar(40)`, `emp_name(int) RETURNS varchar(32)`, `current_manager(char(4)) RETURNS varchar(32)`, `employees_usage() RETURNS TEXT DETERMINISTIC` (help text).
* Views: `v_full_employees` (uses emp_dept_name per row) and `v_full_departments` (uses current_manager).
* Procedures: `show_departments() modifies sql data` (creates and drops TEMPORARY tables department_max_date / department_people, references bug#320513), `employees_help()`.
* Functions set a user variable (`set @max_date=max_date;`) as a side effect; all use `delimiter //`.

# What it was used to decide
Programmable-object inventory in [Employees](/datasets/employees.md) - ported optionally, after the data load.
