---
type: Source
title: MySQL "Other MySQL Documentation" page - Example Databases table
description: Official download links and sizes for sakila, world, employee (GitHub), airportdb and menagerie example databases.
resource: https://dev.mysql.com/doc/index-other.html
tags:
- mysql
- downloads
- sakila
- employees
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/index-other.html
  title: Other MySQL Documentation - Example Databases
  accessed: "2026-09-02"
---

# What was read
The "Example Databases" table on dev.mysql.com, accessed 2026-09-02.

# Relevant excerpt
* sakila: TGZ https://downloads.mysql.com/docs/sakila-db.tar.gz (715 Kb), Zip https://downloads.mysql.com/docs/sakila-db.zip (712 Kb); HTML guide https://dev.mysql.com/doc/sakila/en/.
* employee data: "large dataset, includes data and test/verification suite", DB download https://github.com/datacharmer/test_db (GitHub); HTML guide https://dev.mysql.com/doc/employee/en/.
* world (90 Kb), airportdb (625.3 Mb), menagerie (1-3 Kb) also listed. No `world_x` entry and no checksums on the page.

# What it was used to decide
Download URLs in [Sakila](/datasets/sakila.md) and [Employees](/datasets/employees.md); the observed Content-Length (729,654 bytes) matches the advertised 712 Kb.
