---
type: Source
title: "MySQL Workbench Manual: 10.8.10 Data Transfer and Migration Setup"
description: "Three data-copy modes: online copy through a MySQL connection, a batch file for later, or a source-side dump script that loads with LOAD DATA on the target; 2 worker tasks by default."
resource: https://dev.mysql.com/doc/workbench/en/wb-migration-wizard-data-migration-setup.html
tags: [workbench, migration, data-copy]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://dev.mysql.com/doc/workbench/en/wb-migration-wizard-data-migration-setup.html
    title: "MySQL Workbench Manual: 10.8.10 Data Transfer and Migration Setup"
    accessed: "2026-09-02"
    version: "MySQL Workbench 8.0 manual"
---

# What was read
https://dev.mysql.com/doc/workbench/en/wb-migration-wizard-data-migration-setup.html, accessed 2026-09-02; version: MySQL Workbench 8.0 manual.

# Relevant excerpt
* "Online copy of table data to target RDBMS": "This (default) will copy the data to the target RDBMS."
* "Create a batch file to copy the data at another time": "The data may also be dumped to a file that can be executed at a later time, or be used as a backup. This script uses a MySQL connection to transfer the data."
* "Create a shell script to use native server dump and load abilities for fast migration": "this generates a script to be executed on the source host to then generate a Zip file containing all of the data and information needed to migrate the data locally on the target host. Copy and extract the generated Zip file on the target host and then execute the import script (on the target host) to import the data into MySQL using a LOAD DATA call. This faster method avoids the need to traffic all data through MySQL Workbench".
* "Worker tasks: The default value is 2. This is the number of tasks (database connections) used while copying the data."; "Truncate target tables before copying data"; debug output option. No helper program is named on the page.

# What it was used to decide
[Workbench Migration Wizard record](/tools/mysql-workbench-migration-wizard.md).
