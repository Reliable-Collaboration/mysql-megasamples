---
type: Source
title: "MySQL Workbench Manual: 10.2 Migration Overview"
description: "The wizard's steps; non-MySQL triggers, views, procedures and functions are copied but commented out; generic ODBC support."
resource: https://dev.mysql.com/doc/workbench/en/wb-migration-overview.html
tags: [workbench, migration]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://dev.mysql.com/doc/workbench/en/wb-migration-overview.html
    title: "MySQL Workbench Manual: 10.2 Migration Overview"
    accessed: "2026-09-02"
    version: "MySQL Workbench 8.0 manual"
---

# What was read
https://dev.mysql.com/doc/workbench/en/wb-migration-overview.html, accessed 2026-09-02; version: MySQL Workbench 8.0 manual.

# Relevant excerpt
* Steps: connect to the source RDBMS; reverse engineer into an internal representation; automatically migrate objects (schemas, tables, columns with data types and defaults mapped, indexes, primary keys); "Triggers are copied, and commented out if the source is not MySQL"; foreign keys converted; "View objects are copied, and commented out if the source is not MySQL"; "Stored Procedure and Function objects are copied, and commented out if the source is not MySQL"; review/edit; create objects on the target; copy data.
* "other unsupported database products can also be migrated by using its Generic database support, as long as you have an ODBC driver for it."

# What it was used to decide
[Workbench Migration Wizard record](/tools/mysql-workbench-migration-wizard.md): even if it were scriptable, it does not port programmable objects.
