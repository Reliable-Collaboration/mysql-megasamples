---
type: Decision
title: MySQL is the hub; PostgreSQL and SQLite are ports of the verified MySQL corpus
description: Every converter emits MySQL SQL and the MySQL build server is where a dataset is loaded and verified; other engines are built from that corpus (schema from information_schema, data from the MySQL Shell dump) and verified against the same pinned expectations.
resource: /decisions/engine-hub.md
tags:
- decision
- engines
- postgresql
- sqlite
- architecture
status: stable
trust: inferred
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:52:50Z"
sources:
- resource: /decisions/test-checksum-method.md
  title: the canonical row digest is defined as text and computable outside MySQL
  accessed: "2026-09-09"
- resource: /decisions/indexing-strategy.md
  title: the index set every dataset carries, and how it is verified
  accessed: "2026-09-09"
- resource: /tools/pgloader.md
  title: pgloader record (rejected for MySQL as a target; its state as a MySQL-to-PostgreSQL loader)
  accessed: "2026-09-09"
---

# Question
When the same datasets are offered on PostgreSQL and SQLite as well as MySQL, what is the source
each engine is built from, and how is a port proven correct?

# Options considered
1. **Port the verified MySQL corpus** (chosen). Schema is read from the build server's
   `information_schema`, data from the MySQL Shell dump's TSV chunks; one type-mapping table
   serves every target engine; each port is verified against the same `datasets/<name>/tests/`
   files as MySQL, including the canonical content digest.
2. Retarget the converters to emit each engine's dialect — rejected: all 27 converters and the
   shared translators (`tsql.py`, `plsql.py`, `csvtable.py`, …) emit MySQL SQL, so this is 27
   converters times two dialects, and the native-MySQL datasets (Sakila, Employees) would still need
   a MySQL-to-X path.
3. An engine-neutral TSV contract emitted by every converter, loaded into each engine — rejected as
   a rewrite of the same 27 converters for no gain over option 1, since the MySQL Shell dump already
   is that TSV contract, produced once from a verified load.
4. pgloader for the PostgreSQL side — not used: its last release is v3.6.9 (2022, SBCL) with the v4
   rewrite unreleased, it cannot serve SQLite, and it would be a second type-mapping policy outside
   the project's control. Whether its MySQL driver can authenticate against MySQL 9.7, which no
   longer ships `mysql_native_password`, was not tested and is moot.

# Evidence
* [Checksum method](/decisions/test-checksum-method.md): the per-row digest is defined as plain
  text (columns joined by U+001F, NULL as U+0000, fixed date and binary renderings) precisely so it
  can be computed outside MySQL. A port whose per-table `(count, xor, sum)` equals MySQL's holds
  the same bytes in every non-float column.
* [Indexing strategy](/decisions/indexing-strategy.md): `tests/indexes.yaml` lists every index by
  columns, uniqueness and type, so index parity is checkable per engine with a documented list of
  what a target cannot carry.
* Inventory of what the ports must translate, measured on the built image on 2026-09-09
  (21 databases, 248 base tables; recorded in PLAN.md section 3.1): 124 unsigned columns, 85
  auto_increment, 117 generated (109 default expressions, 8 stored), 604 btree indexes, 221 foreign
  keys, 123 check constraints, 17 tables without a primary key, 7 binary-collation tables, 8 FULLTEXT
  and 1 SPATIAL index, 69 views, 26 routines, 11 triggers.
* [pgloader](/tools/pgloader.md): release state and scope.

# Outcome
Option 1. `megasamples.yaml` may name a dataset for any engine; the build always loads it into the
MySQL build server first, and every other engine is produced from that verified corpus. Tables,
data, primary and unique keys, btree indexes, foreign keys, check constraints and stored generated
columns are ported, and so are views, stored routines (PostgreSQL), triggers, `ON UPDATE` columns
and FULLTEXT indexes — [programmable-object parity](/decisions/programmable-object-parity.md) has
the translators, the verification by execution and the seven kinds of exception, which the
catalogue lists per database. Enum and set become text with a CHECK constraint on every target;
no boolean is inferred from `tinyint(1)` except for a function's return type; the
`<schema>_<table>` flattening is kept so every engine carries an identical table set.

Rules fixed while porting the 21 core datasets on 2026-09-09, each the outcome of a verification
failure and now covered by a unit test:
* An identity column keeps an integer type PostgreSQL accepts: a `bigint unsigned auto_increment`
  key becomes `bigint`, where a plain `bigint unsigned` becomes `numeric(20,0)`.
* Index and constraint names longer than 63 bytes are shortened with a hash suffix by one function
  the emitter and the verification adapters share, so PostgreSQL never truncates them silently.
* Stored generated columns are not in the dump; the ports load the other columns and each engine
  computes them from the translated expression, and the digest check proves the values agree.
* Geometry is standard WKB with longitude first: the canonical digest on the MySQL side renders
  `ST_AsBinary(col, 'axis-order=long-lat')`, because MySQL's default order for a geographic SRS
  (4326) is latitude first and hashes different bytes from the same point
  ([checksum method](/decisions/test-checksum-method.md)).
* Multi-line table comments and defaults are read from the client in escaped batch mode, so a
  value holding a newline cannot break a row of `information_schema` output.

# Status
accepted
