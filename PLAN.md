# Plan

What is being built next, and the design it follows. `ARCHITECTURE.md` describes what exists;
this file stops describing something once it does.

## 1. Goal

Make the same verified corpus available on **PostgreSQL** and **SQLite** beside MySQL, chosen per
engine from one configuration, so that any combination of engines, databases and consoles can be
built with `make run`. That corpus is then the input for comparing Dolt with its siblings
DoltgreSQL (PostgreSQL wire protocol) and DoltLite (a SQLite fork that reads stock SQLite files) in
`dolt-megasamples`; that comparison starts only when the two engines are built and verified here.

## 2. Status

| phase | what | state |
|---|---|---|
| 1 | one package, `engines/` and `consoles/` directories, `megasamples.yaml`, generated `compose.yaml`, the `make` shims | done |
| 2 | interactive configurator; once-only download monitor with IPv4 fallback | done |
| 3 | the port toolkit and the PostgreSQL engine, all 21 core datasets verified | next |
| 4 | the SQLite engine, all 21 core datasets verified | after 3 |
| 5 | catalogue, landing page, registry and release assets engine-aware; consoles configured per engine | after 4 |
| — | `dolt-megasamples`: DoltgreSQL and DoltLite beside Dolt | after 5 |

## 3. The ports: design

**Source of truth is the MySQL corpus** (`knowledge/decisions/engine-hub.md`). A port reads
schema from the build server's `information_schema` and data from the MySQL Shell dump (TSV
chunks), translates through one type-mapping table, loads, and is verified against the same
`datasets/<name>/tests/` files as MySQL: counts, the canonical digest (byte-equal on every non-float
column), foreign keys, the index set.

```
megasamples/port/
  model.py     information_schema -> an engine-neutral table model (columns, types, nullability,
               defaults, generated expressions, primary/unique/secondary indexes, foreign keys, checks)
  typemap.py   the ONE mapping table: MySQL type -> PostgreSQL type, SQLite type, canonical digest rule
  tsv.py       reader for the dump's TSV chunks (MySQL LOAD DATA escapes: \N, \t, \n, \\, \0), typed
megasamples/engines/postgres/   emit.py (DDL)  load.py (COPY through psycopg)  server, image, image_test, adapter
megasamples/engines/sqlite/     emit.py (DDL)  load.py (executemany)            files, image, image_test, adapter
datasets/<name>/postgres/  schema.sql indexes.sql constraints.sql   generated, committed: type decisions as reviewable diffs
datasets/<name>/sqlite/    schema.sql
```

`megasamples/verify.py` gains an adapter interface (connect, query, list indexes, digest SQL per
dialect) so the counts, digests, foreign-key and index stages run unchanged on every engine; the
explain and smoke stages stay MySQL-only. SQLite computes the digest with a Python aggregate
function, which the digest definition allows because it is defined as text
(`knowledge/decisions/test-checksum-method.md`).

### 3.1 What the ports must handle — measured on the built image, 2026-09-09, 21 databases, 248 tables

| what | count | rule |
|---|---:|---|
| columns by type | varchar 871 · int 508 · tinyint 227 · smallint 223 · decimal 188 · datetime 182 · char 124 · date 68 · text kinds 58 · bigint 29 · binary kinds 28 · timestamp 16 · double/float 14 · enum/set 8 · geometry/point 2 · json 1 · time 2 · year 1 | one row each in `typemap.py` |
| unsigned columns | 124 | next wider signed integer |
| auto_increment columns | 85 | PostgreSQL identity; SQLite `INTEGER PRIMARY KEY` where it is the single-column integer key |
| generated columns | 117 (109 default expressions, 8 stored computed) | both engines carry stored generated columns; defaults carried where the function exists |
| btree indexes including primary keys | 604 | ported; parity checked |
| foreign keys / check constraints | 221 / 123 | ported |
| tables without a primary key | 17 | fine in PostgreSQL; SQLite's implicit rowid |
| binary-collation tables | 7 (all `wikipedia_simple`) | bytea / BLOB |
| FULLTEXT / SPATIAL indexes | 8 / 1 | **not ported**; listed per database in the catalogue |
| views / routines / triggers | 69 / 26 / 11 | **not ported**; listed per database. Views are a later candidate through sqlglot, statement by statement, verified by execution (`megasamples/sources/tsqlbody.py` records why it is not used for procedural bodies) |

Mapping rules fixed in advance: enum and set become text with a CHECK constraint on both engines
(PostgreSQL enum types would be a second policy); `tinyint(1)` stays an integer, no boolean guessing;
datetime becomes `timestamp` without time zone in PostgreSQL and ISO-8601 text in SQLite; geometry
becomes WKB in bytea / BLOB (no PostGIS); the `<schema>_<table>` flattening is kept so every engine
carries the identical table set.

### 3.2 PostgreSQL packaging

One database per dataset, same names, tables in `public`; `demo` and `admin` accounts with the same
meaning as MySQL's; a `megasamples` database holding the registry. The cluster is initialised and
loaded in a builder stage and copied into the final image, as MySQL's is; the data directory must
sit outside the official image's `VOLUME` path, and the entrypoint's skip-initialisation branch is
verified from its source before the design is relied on. The major version is pinned after
checking what the official image publishes at the time. Image: `sql-megasamples-postgres:dev`.

### 3.3 SQLite packaging

One `<name>.sqlite` file per dataset plus `megasamples.sqlite` for the registry; `VACUUM`ed before
shipping; rollback journal, since WAL is not portable as a shipped file; foreign-key enforcement
documented as the per-connection pragma it is. Shipped both as release assets and as a small image
(`alpine` plus the `sqlite3` CLI) so `docker run` works like the other engines; a compose service
mounts the files for the consoles. DoltLite reads these files directly.

### 3.4 To verify before building on them

* The official PostgreSQL image's `PGDATA` and `VOLUME` layout for the pinned major, and that its
  entrypoint skips initialisation on a populated directory.
* That PostgreSQL's `COPY ... FORMAT text` escaping matches what the TSV reader emits (`\N`, `\t`,
  `\n`, `\\`, `\0`), including binary columns.
* The SQLite library version used to write the files, recorded in the registry.
* Which datasets contain zero dates or other MySQL-only values that PostgreSQL rejects.

## 4. Phase 5: engine-aware documents and consoles

* `CATALOGUE.md` and the landing page show each dataset per engine, with what is not ported.
* `megasamples/consoles.py` configures Adminer, DbGate and CloudBeaver for every engine present;
  pgAdmin or pgweb for PostgreSQL and a SQLite browser are evaluated and recorded before being added.
* `megasamples release` stages the SQLite files as an asset set with checksums.
* The image tests and the console test run per engine.

## 5. After this repository: the Dolt comparison

`dolt-megasamples` switches its input to the new image name, then adds DoltgreSQL (loaded from the
PostgreSQL corpus through `pg_dump` and `psql`) and DoltLite (opening the SQLite files directly)
beside Dolt, reusing its disk, time and memory measurements. Not before phases 3 and 4 are done.
