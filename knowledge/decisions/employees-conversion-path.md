---
type: Decision
title: Employees conversion path - concatenate schema and dumps into plain SQL, verify with SHA-256
description: Replace the mysql-client `source` directives with a single generated SQL stream; drop `flush binary logs`; run test_employees_sha2.sql as the acceptance test.
resource: /decisions/employees-conversion-path.md
tags: [employees, decision, mysql-native]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/datacharmer/test_db/master/employees.sql
    title: employees.sql
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/datacharmer/test_db/master/test_employees_sha2.sql
    title: test_employees_sha2.sql
    accessed: "2026-09-02"
---

# Question
How to load datacharmer/test_db (v1.0.7 + master fixes) inside the image build without the interactive mysql client's `source` semantics.

# Options considered
1. Run `mysql < employees.sql` from inside the checked-out directory (works only when the client's CWD is the checked-out directory; brittle inside `make`).
2. Generate one file: header of employees.sql (DDL + views) + the eight `load_*.dump` files in the same order + optional objects.sql, with `source` and `flush binary logs` lines removed; stream it into the build server during `make employees`.
3. `employees_partitioned.sql` variant (partitioned salaries/titles/dept_emp) - no advantage for a sample image.

# Evidence
* `source load_departments.dump ;` etc. are client commands with relative paths; `flush /*!50503 binary */ logs;` needs RELOAD and is pointless during a build load ([employees.sql](/sources/github-datacharmer-test-db-employees-sql.md)).
* Dumps are plain multi-row INSERTs, ASCII, 172 MB total; release tarball 35.6 MB ([API](/sources/github-datacharmer-test-db-api.md)).
* Acceptance test with published SHA-256 chained checksums exists and works on 9.6+ ([sha2 test](/sources/github-datacharmer-test-db-test-sha2.md)); MD5/SHA1 variants do not ([classic_hashing](/tools/mysql-classic-hashing-component.md)).

# Outcome
Option 2. Pin the commit (`e324b56` or a later tag if datacharmer releases one) and record md5s of the eight dumps at build time. Load `objects.sql` after the data (functions call across tables). Run `test_employees_sha2.sql` (it creates/drops helper tables `expected_values`, `found_values`, `tchecksum` inside the `employees` database - run it before the image is snapshotted or accept the transient tables).

# Status
accepted
