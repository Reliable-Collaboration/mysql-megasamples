---
type: Decision
title: "How the SQLite port is shaped: one file per database, written by the stdlib driver, shipped in a data image"
description: "Each database becomes <name>.sqlite with MySQL-like declared types, inline constraints, secondary indexes, a rollback journal and an application id; the files ship as release assets and in an Alpine image carrying the sqlite3 shell."
resource: /decisions/sqlite-file-conventions.md
tags:
- decision
- sqlite
- port
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:52:50Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:52:50Z"
sources:
- resource: /decisions/engine-hub.md
  title: the port design every engine follows
  accessed: "2026-09-09"
- resource: /tools/mysql-shell-dump-format.md
  title: what the port reads
  accessed: "2026-09-09"
---

# Question
SQLite has no server, no accounts, no decimal type and cannot add a constraint after a table exists.
What does a port of the corpus look like, and how is it shipped?

# Options considered
1. **One `<database>.sqlite` file per dataset, written by Python's stdlib `sqlite3` from the model and
   the MySQL Shell dump; a data image (`alpine` plus the `sqlite3` shell) carrying the files under
   `/data`; the same files as release assets** (chosen).
2. One file holding every database as attached schemas -- rejected: a 660 MB file nobody wants whole,
   and DoltLite opens one database per file.
3. A server-side driver for writing (a SQLite container) -- rejected: the stdlib driver on the build
   machine writes a portable file in seconds and needs nothing installed.

# Evidence
* Built and verified on 2026-09-09 for all 21 core datasets (`make build ENGINE=sqlite`): counts, canonical
  digests, foreign-key orphans and index parity all pass against the same `tests/` files as MySQL.
* SQLite 3.46.1 wrote the files (Python 3.14.4's stdlib driver on the build machine); the image's
  shell is SQLite 3.49.2 (2025-05-07), the version Alpine 3.22 packages (`sqlite3 --version` in the image).
* The 21 files total 868 MB; the largest are `employees` (233 MB), `adventureworks` (121 MB) and
  `wikipedia_simple` (116 MB) -- measured with `du` on 2026-09-09 after `VACUUM`.

# Outcome
* **Types.** MySQL-like declared names (`VARCHAR(45)`, `DECIMAL(10,2)`, `DATETIME`, `TINYINT`,
  `BLOB`, `TEXT`) chosen for the affinity SQLite derives from them; integers and decimals become
  numbers by affinity, dates and times stay ISO-8601 text as the dump wrote them (UTC). A single
  auto-increment integer key becomes `INTEGER PRIMARY KEY`, the rowid alias. No boolean is inferred.
* **Constraints inline.** Primary keys, foreign keys (with their ON UPDATE / ON DELETE actions) and
  CHECKs are declared in `CREATE TABLE`; secondary indexes are created after the data, named
  `<table>_<index>`. A CHECK that uses `regexp_like` is dropped with its name recorded, since SQLite
  has no such function; enum columns keep their membership CHECK; stored generated columns are
  carried as `GENERATED ALWAYS AS ... STORED`.
* **Loading.** `journal_mode=OFF`, `synchronous=OFF` and `foreign_keys=OFF` while inserting, then
  `journal_mode=DELETE` and `VACUUM`, so the shipped file is compact and uses the rollback journal
  that any reader accepts. Foreign keys are verified afterwards by the orphan check; enforcement at
  run time is the reader's `PRAGMA foreign_keys=ON`, as it is for every SQLite file.
* **Digest.** Decimals are re-rendered at the declared scale and date-times padded to six fractional
  digits before hashing, so the canonical text equals MySQL's; geometry is WKB with the SRID prefix
  removed, as on every port.
* **Provenance.** `PRAGMA application_id` is `0x4D534D50` ("MSMP"); `megasamples.sqlite` holds the
  registry with the same columns as the other engines plus `engine` and `not_ported`.
* **Shipping.** `sql-megasamples-sqlite:dev` is `alpine:3.22` (digest-pinned) with the `sqlite`
  package and the files under `/data`; its default command sleeps so the container holds the files
  for `docker exec` and for the consoles through a named volume. The files are also staged as a
  release asset set.

# Status
accepted
