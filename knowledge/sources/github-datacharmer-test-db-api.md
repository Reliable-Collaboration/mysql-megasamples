---
type: Source
title: datacharmer/test_db repository metadata (GitHub API)
description: Release v1.0.7 asset, file sizes of the SQL dumps, sakila subdirectory, latest commit, as returned by the GitHub REST API.
resource: https://api.github.com/repos/datacharmer/test_db
tags: [employees, test_db, github-api, sizes]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://api.github.com/repos/datacharmer/test_db
    title: repos/datacharmer/test_db, /releases/latest, /contents, /contents/sakila, /commits/master
    accessed: 2026-09-02
---

# What was read
`gh api` calls on 2026-09-02 (read-only).

# Relevant excerpt
* Repository: default branch master, GitHub license detection `null` (license is stated in README only), size 75,213 KB, last push 2026-04-10; master commit `e324b56193ca506ab7cc1ab143a9153d8c4535d7` ("Fix dbdeployer path").
* Only release: tag `v1.0.7` ("test_db 1.0.7", published 2020-10-31, commit e5f310a) with one asset `test_db-1.0.7.tar.gz` 35,607,473 bytes at https://github.com/datacharmer/test_db/releases/download/v1.0.7/test_db-1.0.7.tar.gz. Note the Changelog dates 1.0.7 to 2015-08-30; master has moved on (sha2 test, CI) without a new tag.
* Root files (bytes): employees.sql 4,193; employees_partitioned.sql 6,276; employees_partitioned_5.1.sql 7,948; objects.sql 4,568; load_departments.dump 250; load_dept_emp.dump 14,159,880; load_dept_manager.dump 1,090; load_employees.dump 17,722,832; load_salaries1.dump 39,806,034; load_salaries2.dump 39,805,981; load_salaries3.dump 39,080,916; load_titles.dump 21,708,736; test_employees_md5.sql 4,711; test_employees_sha.sql 4,715; test_employees_sha2.sql 3,668; show_elapsed.sql 272; sql_test.sh; test_versions.sh; Changelog 964; directories images/, postgresql/, sakila/, .github/. Sum of the eight dump files = 172,285,719 bytes.
* `sakila/`: README.md 333 B, sakila-mv-data.sql 3,398,269 B, sakila-mv-schema.sql 23,471 B.

# What it was used to decide
Sizes and version pin in [Employees dataset](/datasets/employees.md); the Sakila copy is noted but not used ([Sakila dataset](/datasets/sakila.md)).
