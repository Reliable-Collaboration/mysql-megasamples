---
type: Source
title: "mysql/mysql-workbench: plugins/migration sources (wbcopytables) and License.txt at 8.0.47"
description: "wbcopytables is a C++ command-line helper shipped inside Workbench (ODBC or Python-DB-API source, MySQL target, --table-file, --thread-count); the GUI writes copy_migrated_tables.sh/.cmd scripts that call it; Workbench 8.0.47 Community is GPLv2 with Oracle's linking permission."
resource: https://github.com/mysql/mysql-workbench/tree/8.0.47/plugins/migration
tags: [workbench, migration, source, license]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://github.com/mysql/mysql-workbench/tree/8.0.47/plugins/migration
    title: "mysql/mysql-workbench: plugins/migration sources (wbcopytables) and License.txt at 8.0.47"
    accessed: 2026-09-02
    version: "tag 8.0.47; repo last push 2026-04-23"
---

# What was read
https://github.com/mysql/mysql-workbench/tree/8.0.47/plugins/migration, accessed 2026-09-02; version: tag 8.0.47; repo last push 2026-04-23.

# Relevant excerpt
* `plugins/migration/`: `backend/ copytable/ dbcopy/ doc/ frontend/ migration_grt.py unit-tests/ wbcopytables.in`. `wbcopytables.in` is a shell wrapper: sets `LD_LIBRARY_PATH` to the Workbench lib dir and `MWB_BINARIES_DIR`, then `exec`s `$MWB_BINARIES_DIR/wbcopytables-bin "$@"`.
* `copytable/main.cpp` usage text: `copytable --*-source=<source db> --target=<target db> <options>` with `--odbc-source=<odbc connstring>`, `--pythondbapi-source=<python connstring>`, `--source-password`, `--source-ssh-*`, `--target=<mysql connstring>`, `--target-password`, `--truncate-target`, `--table-file=<filename>`, `--log-file`, `--log-level`, `--thread-count=<count>`, `--source-charset`.
* `frontend/migration_data_transfer.py` writes `copy_migrated_tables.sh`/`.cmd` and `bulk_copy_tables.sh`/`.cmd` to the Desktop; the batch template says `REM Set the location for wbcopytables.exe in this variable` and the wizard warns "You should edit this file to add the source and target server passwords before running it."
* `License.txt` (8.0.47): "This release of MySQL Workbench 8.0.47 Community is brought to you by the MySQL team at Oracle. This software is released under version 2 of the GNU General Public License (GPLv2), as set forth below, with the following additional permissions:" (linking permission for separately licensed software such as OpenSSL); "Last updated: March 2026".

# What it was used to decide
[Workbench Migration Wizard record](/tools/mysql-workbench-migration-wizard.md): the data copier is scriptable in principle but only exists inside a full Workbench install (GUI toolkit dependencies), and schema conversion still requires the wizard.
