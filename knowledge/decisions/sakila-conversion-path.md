---
type: Decision
title: Sakila conversion path - load the upstream scripts unmodified
description: Sakila is MySQL-native; run sakila-schema.sql then sakila-data.sql through the mysql client with no transformation; pin inner-file checksums.
resource: /decisions/sakila-conversion-path.md
tags: [sakila, decision, mysql-native]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://downloads.mysql.com/docs/sakila-db.zip
    title: sakila-db.zip inspection
    accessed: "2026-09-02"
  - resource: https://dev.mysql.com/doc/sakila/en/sakila-installation.html
    title: Sakila installation chapter
    accessed: "2026-09-02"
---

# Question
How to get Sakila 1.5 into the `mysql:9.7` image.

# Options considered
1. Run the two upstream .sql files as-is (`mysql < sakila-schema.sql; mysql < sakila-data.sql`) - the documented install path.
2. Re-dump with `mysqldump`/MySQL Shell after loading, to normalise into the project's own script layout.
3. Vendor the files into the repository versus downloading at build time.

# Evidence
* Files are MySQL-native, `utf8mb4`, InnoDB, LF line endings, and use version-gated comments (`/*!50705 ...*/`, `/*!80003 SRID 0 */`, `/*!50610 ...*/`) which a 9.7 server executes ([zip inspection](/sources/mysql-sakila-db-zip.md)).
* The schema file itself issues `DROP SCHEMA IF EXISTS sakila; CREATE SCHEMA sakila; USE sakila;` so the database name is fixed by upstream and needs no wrapper.
* The data file sets `AUTOCOMMIT=0` and commits per table; it creates three triggers after loading - order (schema first, then data) matters.
* License permits redistribution with notice ([license record](/licenses/bsd-3-clause-sakila.md)).

# Outcome
Option 1, executed against the build server during `make sakila` (`mysql < sakila-schema.sql; mysql < sakila-data.sql`), followed by `util.dumpSchemas` so the result is baked with the other core datasets; nothing is placed in `/docker-entrypoint-initdb.d` ([bake decision](/decisions/bake-data-vs-initdb.md)). Verify inner-file md5s, not the zip md5 ([open question](/questions/sakila-download-checksum-drift.md)). Do not ship `sakila.mwb`. Post-load assertions: 16 tables, 7 views, 3 procedures, 3 functions, 6 triggers, row counts per [dataset record](/datasets/sakila.md).

# Status
accepted
