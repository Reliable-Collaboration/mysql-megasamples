---
type: Source
title: test_db employees.sql (schema and loader driver)
description: DDL for the six tables, two views, the `source` commands that pull in the dump files, and a `flush binary logs` statement.
resource: https://raw.githubusercontent.com/datacharmer/test_db/master/employees.sql
tags: [employees, ddl]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/datacharmer/test_db/master/employees.sql
    title: employees.sql
    accessed: "2026-09-02"
    version: master @ e324b56
  - resource: https://raw.githubusercontent.com/datacharmer/test_db/master/employees_partitioned.sql
    title: employees_partitioned.sql (grep only)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/datacharmer/test_db/master/load_departments.dump
    title: load_departments.dump (full) and load_employees.dump (head + non-ASCII scan)
    accessed: "2026-09-02"
---

# What was read
employees.sql in full; employees_partitioned.sql grepped for `source`/`PARTITION`; load_departments.dump in full; load_employees.dump streamed through a non-ASCII grep.

# Relevant excerpt
* Header comment: "Copyright (C) 2007,2008, MySQL AB", "Original data created by Fusheng Wang and Carlo Zaniolo http://www.cs.aau.dk/TimeCenter/software.htm", "Current schema by Giuseppe Maxia", "Data conversion from XML to relational by Patrick Crews", CC BY-SA 3.0 notice, fabricated-data disclaimer.
* `DROP DATABASE IF EXISTS employees; CREATE DATABASE IF NOT EXISTS employees; USE employees;` then `/*!50503 set default_storage_engine = InnoDB */;`.
* Tables: employees(emp_no INT PK, birth_date DATE, first_name VARCHAR(14), last_name VARCHAR(16), gender ENUM('M','F'), hire_date DATE); departments(dept_no CHAR(4) PK, dept_name VARCHAR(40) UNIQUE); dept_manager(emp_no, dept_no, from_date, to_date; PK(emp_no,dept_no); FKs ON DELETE CASCADE); dept_emp(same shape); titles(emp_no, title VARCHAR(50), from_date, to_date NULLable; PK(emp_no,title,from_date)); salaries(emp_no, salary INT, from_date, to_date; PK(emp_no,from_date)). No explicit character set anywhere.
* Views: `dept_emp_latest_date` and `current_dept_emp` (CREATE OR REPLACE VIEW).
* `flush /*!50503 binary */ logs;` then `source load_departments.dump ;` ... `source load_salaries3.dump ;` `source show_elapsed.sql ;` - these are mysql-client commands with paths relative to the client's working directory. A `#`-style comment line is used ("# shows only the current department").
* Dumps are plain multi-row `INSERT INTO \`employees\` VALUES (10001,'1953-09-02','Georgi','Facello','M','1986-06-26'), ...`; load_employees.dump contains 0 non-ASCII lines; departments are d001 Marketing ... d009 Customer Service.
* employees_partitioned.sql sources the same eight dump files.

# What it was used to decide
Hazards and loader design in [Employees](/datasets/employees.md) / [decision](/decisions/employees-conversion-path.md).
