---
type: Source
title: HR schema scripts at v23.3 (hr_install.sql, hr_create.sql, hr_populate.sql, hr_code.sql, README.md)
description: DDL, data, programmable objects and the built-in row-count verification of the Human Resources schema, read from the v23.3 tag.
resource: https://github.com/oracle-samples/db-sample-schemas/tree/v23.3/human_resources
tags:
- oracle
- hr
- scripts
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/human_resources/hr_install.sql
  title: hr_install.sql (8,275 B)
  accessed: "2026-09-02"
  version: v23.3
- resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/human_resources/hr_create.sql
  title: hr_create.sql (17,112 B)
  accessed: "2026-09-02"
  version: v23.3
- resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/human_resources/hr_populate.sql
  title: hr_populate.sql (41,301 B)
  accessed: "2026-09-02"
  version: v23.3
- resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/human_resources/hr_code.sql
  title: hr_code.sql (3,849 B)
  accessed: "2026-09-02"
  version: v23.3
- resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/human_resources/README.md
  title: human_resources/README.md (2,642 B)
  accessed: "2026-09-02"
  version: v23.3
---

# What was read
All four HR scripts and the schema README at tag v23.3 (downloaded to the scratchpad and grepped; `file` reports every script as plain ASCII text; `grep -P '[^\x00-\x7F]'` finds no non-ASCII bytes).

# Relevant excerpt
* README: "Schema Version 21.1", "Release Date 03-FEB-2022", "Supported with Database Versions 19c and higher"; major changes: "All DATE data is updated", "Updated phone numbers in US for globalization", "Countries are updated: replaced `UK United Kingdom` with `GB United Kingdom of Great Britain and Northern Ireland`", "`country_name` column changed from `varchar2(40)` to `varchar2(60)`", "New install mechanism".
* hr_install.sql: prompts for password/tablespace/overwrite, `CREATE USER hr`, grants (`CREATE MATERIALIZED VIEW, PROCEDURE, SEQUENCE, SESSION, SYNONYM, TABLE, TRIGGER, TYPE, VIEW`), `ALTER SESSION SET NLS_LANGUAGE=American; NLS_TERRITORY=America`, then `@@hr_create.sql`, `@@hr_populate.sql`, `@@hr_code.sql`, and a verification block: `regions 5, countries 25, departments 27, locations 23, employees 107, jobs 19, job_history 10` ("provided" counts compared with `count(1)`).
* hr_create.sql DDL: `regions(region_id NUMBER NOT NULL PK, region_name VARCHAR2(25))`; `countries(country_id CHAR(2) PK, country_name VARCHAR2(60), region_id NUMBER FK) ORGANIZATION INDEX`; `locations(location_id NUMBER(4) PK, street_address VARCHAR2(40), postal_code VARCHAR2(12), city VARCHAR2(30) NOT NULL, state_province VARCHAR2(25), country_id CHAR(2) FK)`; `departments(department_id NUMBER(4) PK, department_name VARCHAR2(30) NOT NULL, manager_id NUMBER(6) FK employees, location_id NUMBER(4) FK)`; `jobs(job_id VARCHAR2(10) PK, job_title VARCHAR2(35) NOT NULL, min_salary NUMBER(6), max_salary NUMBER(6))`; `employees(employee_id NUMBER(6) PK, first_name VARCHAR2(20), last_name VARCHAR2(25) NOT NULL, email VARCHAR2(25) NOT NULL UNIQUE, phone_number VARCHAR2(20), hire_date DATE NOT NULL, job_id VARCHAR2(10) NOT NULL FK, salary NUMBER(8,2) CHECK (salary > 0), commission_pct NUMBER(2,2), manager_id NUMBER(6) FK employees, department_id NUMBER(4) FK)`; `job_history(employee_id NUMBER(6), start_date DATE, end_date DATE, job_id VARCHAR2(10), department_id NUMBER(4); PK (employee_id, start_date); CHECK (end_date > start_date))`. Sequences: `locations_seq START WITH 3300 INCREMENT BY 100 MAXVALUE 9900`, `departments_seq START WITH 280 INCREMENT BY 10 MAXVALUE 9990`, `employees_seq START WITH 207 INCREMENT BY 1`. View `emp_details_view` (6-table join, `WITH READ ONLY`). Eleven secondary indexes (emp_department_ix, emp_job_ix, emp_manager_ix, emp_name_ix, dept_location_ix, jhist_job_ix, jhist_employee_ix, jhist_department_ix, loc_city_ix, loc_state_province_ix, loc_country_ix). `COMMENT ON TABLE/COLUMN` for every table.
* hr_populate.sql: `SET VERIFY OFF; ALTER SESSION SET NLS_LANGUAGE=American;` then PL/SQL blocks of single-row `INSERT INTO <table> VALUES (...)`; counted INSERTs: regions 5, countries 25, locations 23, departments 27, jobs 19, employees 107, job_history 10. Dates use `TO_DATE('17-06-2013', 'dd-MM-yyyy')` (no time component anywhere). Phone numbers like `'1.515.555.0100'`. `ALTER TABLE departments DISABLE CONSTRAINT dept_mgr_fk` before loading departments and `ENABLE` after employees; `COMMIT`.
* hr_code.sql: `PROCEDURE secure_dml` (raises -20205 "You may only make changes during normal office hours" outside 08:00–18:00 or on SAT/SUN); `TRIGGER secure_employees BEFORE INSERT OR UPDATE OR DELETE ON employees` calling it, immediately followed by `ALTER TRIGGER secure_employees DISABLE`; `PROCEDURE add_job_history(p_emp_id, p_start_date, p_end_date, p_job_id, p_department_id)` inserting into job_history; `TRIGGER update_job_history AFTER UPDATE OF job_id, department_id ON employees FOR EACH ROW` calling `add_job_history(:old.employee_id, :old.hire_date, sysdate, :old.job_id, :old.department_id)`.

# What it was used to decide
[HR dataset record](/datasets/oracle-hr.md): shape, row counts, programmable objects, type mapping.
