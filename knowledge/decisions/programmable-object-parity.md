---
type: Decision
title: Views, routines, triggers, full-text and spatial indexes are ported to every engine, and each exception is recorded with its reason
description: The PostgreSQL and SQLite ports carry the MySQL corpus's views, stored routines (PostgreSQL), triggers, ON UPDATE columns, FULLTEXT indexes and REGEXP checks through deterministic translators, verified by executing them against outputs pinned from MySQL; what an engine cannot carry is dropped by name with the reason, and the seven kinds of exception are listed here.
resource: /decisions/programmable-object-parity.md
tags:
- decision
- engines
- postgresql
- sqlite
- views
- routines
- triggers
- verification
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-09T22:40:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-10T00:20:00Z"
sources:
- resource: /decisions/engine-hub.md
  title: MySQL is the hub; PostgreSQL and SQLite are ports of the verified MySQL corpus
  accessed: "2026-09-09"
- resource: /decisions/test-checksum-method.md
  title: the canonical row digest, computable on every engine
  accessed: "2026-09-09"
- resource: /datasets/adventureworks-oltp.md
  title: which AdventureWorks routines the T-SQL conversion carries, and which it refuses
  accessed: "2026-09-09"
- resource: /datasets/northwind.md
  title: Northwind's procedures as converted from T-SQL
  accessed: "2026-09-09"
---

# Question
The MySQL corpus carries 69 views, 42 stored routines (19 functions, 23 procedures), 11 triggers,
16 `ON UPDATE CURRENT_TIMESTAMP` columns, 8 FULLTEXT indexes, 1 SPATIAL index and 5 `REGEXP` check
constraints (measured on the build server, 21 core databases, 2026-09-09). The three engines are
meant to show the same databases, so which of these objects reach PostgreSQL and SQLite, how are
they translated without anyone writing them by hand, how is a translation proven right, and what
exactly cannot be carried?

# Options considered
1. **Translate by rule, verify by execution, record every exception by name** (chosen). One
   translator per object kind over a closed census of constructs; anything outside the census
   drops the object with its reason; the port is verified by running the ported objects and
   comparing with outputs pinned from MySQL.
2. Leave views, routines and triggers MySQL-only, as the first three-engine release did — rejected:
   the point of offering the same sample databases on three engines is that a tutorial written for
   one runs on the others, and Sakila's or Northwind's stored procedures are part of the tutorial.
3. Hand-write the PL/pgSQL and SQLite equivalents — rejected: not reproducible, not reviewable as a
   diff against the MySQL source, and silently drifts when a converter changes the hub.

# Evidence
* Deterministic translation with existing tooling. Statements and expressions go through sqlglot
  (30.18.0) and a fixed list of rewrite rules (`megasamples/port/sqltranslate.py`); procedural
  bodies through a scanner over the census of constructs the 42 routines use
  (`megasamples/port/routines.py`); the result-set columns of a procedure are measured once with
  psql's `\gdesc` and recorded in `datasets/<name>/ports/result_sets.yaml`. `megasamples ports-check`
  re-renders everything from the build server and fails on a byte of difference from what is
  committed: on 2026-09-09 all 21 datasets were reproducible.
* Verification by execution, against MySQL. Three stages were added to `megasamples verify`:
  views (row count and canonical digest of every view, 69 pinned), routines (52 hand-chosen calls
  across 7 datasets, their printed output pinned from MySQL and normalised line by line by
  `megasamples/probe.py`), triggers (16 DML scenarios across 3 datasets inside rolled-back
  transactions, the probe query's output pinned from MySQL). On 2026-09-09 every core dataset
  passed every stage its engine supports on PostgreSQL 18.6 and on SQLite 3.46/3.49.
* Rules the verification forced, each now a unit test (`tests/test_port.py`, `tests/test_routines.py`,
  `tests/test_probe.py`):
  - unquoted identifiers in a hand-written body are resolved to the schema's spelling, because
    PostgreSQL folds them to lower case and Northwind's tables are lower-case while its views are not;
  - MySQL evaluates a FLOAT operand in double precision and PostgreSQL in single, so a FLOAT column
    inside arithmetic is cast to double precision; and PostgreSQL converts a double to numeric
    through a 15-digit rendering (7.764749999999999 → 7.7648 at four places, MySQL 7.7647), so such
    a `CAST(... AS DECIMAL)` goes through the shortest-exact text form;
  - MySQL has no boolean, so a comparison in a select list becomes an integer on PostgreSQL, while
    the condition of an IF or a trigger WHEN stays boolean;
  - a compact date literal (`'19970101'`) compared with a date-time column is written in ISO form,
    and on SQLite, where a DATETIME is text, a date-only literal gets midnight appended;
  - `CONVERT(binary_col USING utf8mb4)` becomes `convert_from(col, 'UTF8')`, since `bytea::text`
    renders hex;
  - `JSON_TABLE ... NESTED PATH` keeps the parent row when the array is empty, so SQLite's
    `json_each` is a LEFT JOIN;
  - `TO_DAYS(a) - TO_DAYS(b)` is a date difference (sqlglot expands `TO_DAYS` from year 0000, which
    PostgreSQL rejects);
  - a SQLite trigger cannot modify the row being inserted, so a NOT NULL column a BEFORE INSERT
    trigger sets to `NOW()` carries `DEFAULT CURRENT_TIMESTAMP` and the trigger updates it after;
  - printed outputs are compared after normalising what clients render differently: booleans,
    CHAR padding, an AVG's scale (MySQL four places, PostgreSQL sixteen; both to four), fractional
    seconds, row order.
* Hub defects the parity work exposed, all fixed in the T-SQL converter and reconverted: a view's
  `+` string concatenation (Northwind's `Invoices` gave 0 for `Salesperson`); `DATENAME(yy, d)`
  left as-is (Northwind's `sales_by_year` failed on MySQL itself); a line comment between a CTE's
  column list and `AS` hid the recursion from the `WITH RECURSIVE` rewrite (AdventureWorks'
  `uspgetbillofmaterials` failed on MySQL itself with "table bom_cte doesn't exist").

# Outcome
Option 1. What each engine carries, from the committed `datasets/*/ports/not_ported.yaml`:

| object | corpus | PostgreSQL | SQLite |
|---|---:|---:|---:|
| views | 69 | 67 | 61 |
| stored routines | 42 | 42 | 0 |
| triggers | 11 | 11 | 10 |
| `ON UPDATE CURRENT_TIMESTAMP` columns | 16 | 16 (BEFORE UPDATE trigger) | 16 (AFTER UPDATE trigger) |
| FULLTEXT indexes | 8 | 8 (GIN over `to_tsvector('simple', …)`) | 8 (FTS5 external-content table + 3 sync triggers) |
| `REGEXP` check constraints | 5 | 5 (`regexp_like`) | 5 (`GLOB`, anchored character classes) |
| SPATIAL indexes | 1 | 0 | 0 |

The exceptions, each a technical limitation of the engine and recorded by name in the port record:
1. **Cross-database views and foreign keys** (both engines; 2 views and 3 foreign keys of
   `oracle_oe` into `oracle_hr`): a PostgreSQL database and a SQLite file cannot reference another
   database. A `FOREIGN DATA WRAPPER` or an `ATTACH` would make the dependency an operational
   requirement of the image rather than a property of the database.
2. **Stored routines on SQLite** (42): SQLite has no stored routines; the 2 `employees` views that
   call functions are therefore not portable either.
3. **XML functions on SQLite** (3 views): `EXTRACTVALUE` has no counterpart; PostgreSQL carries them
   through `xpath()`.
4. **`GROUP_CONCAT(DISTINCT x SEPARATOR s ORDER BY y)` on SQLite** (1 view, `sakila.actor_info`):
   SQLite's `group_concat` cannot combine DISTINCT with a separator or an ORDER BY.
5. **A BEFORE INSERT trigger assigning the primary key on SQLite** (1 trigger,
   `oracle_oe.insert_ord_line`): a SQLite trigger cannot modify NEW, and the row must carry its
   key before the AFTER trigger could run.
6. **AUTO_INCREMENT on a column that is not the whole primary key on SQLite** (4 columns in
   `adventureworks` and `adventureworks_lt`): SQLite auto-assigns only a single-column INTEGER
   PRIMARY KEY; inserts must supply the value.
7. **The SPATIAL index** (`sakila.address.idx_location`, both engines): core PostgreSQL has no
   geometry type to index the WKB the port stores; PostGIS would carry it, at the cost of moving
   the image off the official `postgres` base to `postgis/postgis:18-3.6` (which exists as of
   2026-08-31) and of a GPL-2 extension in the runtime image, for one demonstration index on a
   603-row table. SQLite has no geometry type or functions, and an R*Tree cannot be maintained
   from a BLOB column. **Decided by the maintainer on 2026-09-10: the limitation is kept** on both
   engines; the geometry column itself is ported as standard WKB, so the points are there and a
   reader with its own geometry library can use them.

Two comparisons are deliberately weaker than a digest, and say so in the verification output: a
view with a `GROUP_CONCAT` that has no ORDER BY is held to its row count (MySQL leaves the order
unspecified, and the two Sakila film lists differ between engines), and on SQLite, which computes
decimal arithmetic in binary floating point, a view's computed decimal columns are left out of the
digest and every other column is still compared exactly (`x_exact`, `s_exact` in `tests/views.yaml`;
9 Northwind views and 3 others).

Two PostgreSQL translations change a procedure's shape and are recorded in `ports/notes.yaml`: a
procedure that returns rows becomes a function `RETURNS TABLE(...)`, and if it also had OUT
parameters those are omitted (in this corpus each such OUT is the row count of the result set,
which the verification checks by that equivalence); `START TRANSACTION`/`COMMIT`/`ROLLBACK` inside
a body are dropped, since a PL/pgSQL procedure runs in the caller's transaction; a bare
`SELECT 'message'` becomes `RAISE NOTICE`; `SET @var` becomes `set_config('megasamples.var', …)`.
AdventureWorks' three update procedures keep their handler's call to `usplogerror()`, which the
T-SQL conversion refuses on every engine ([record](/datasets/adventureworks-oltp.md)); the call
fails identically on MySQL and PostgreSQL and the routine test pins that failure.

# Status
accepted
