---
type: Dataset
title: Sakila
description: Oracle's DVD-rental sample database for MySQL (Version 1.5), 16 tables / 7 views / 3 procedures / 3 functions / 6 triggers, 46,268 rows, BSD-licensed SQL scripts.
resource: https://dev.mysql.com/doc/sakila/en/
tags:
- tier-core
- mysql-native
- sakila
- spatial
- fulltext
- bsd-3-clause
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/sakila/en/
  title: Sakila Sample Database manual
  accessed: "2026-09-02"
  version: revision 84779 (2026-08-04)
- resource: https://dev.mysql.com/doc/sakila/en/sakila-license.html
  title: License for the Sakila Sample Database
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/sakila/en/sakila-news.html
  title: Sakila Change History
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/index-other.html
  title: Example Databases download table
  accessed: "2026-09-02"
- resource: https://downloads.mysql.com/docs/sakila-db.zip
  title: sakila-db.zip (Version 1.5)
  accessed: "2026-09-02"
  version: Last-Modified 2026-08-31; md5 a80df38456f8d4f36903771b67a1129a
---

# Identity
Sakila, Oracle's official MySQL sample database modelling a DVD rental chain (two stores). Version 1.5 per the file headers and the change history. Development began in 2005; first release March 2006; film and actor names borrowed from the Dell DVD Store sample ([manual](/sources/mysql-sakila-manual.md)).

# Source artifact
* URL: https://downloads.mysql.com/docs/sakila-db.zip (729,654 bytes; md5 `a80df38456f8d4f36903771b67a1129a`; sha256 `e27ed871082e76e9d32021c2df07f97ebf7696ace132f5995218557dd87d7046`) or https://downloads.mysql.com/docs/sakila-db.tar.gz (732,423 bytes). Advertised as 712 Kb / 715 Kb on the [download table](/sources/mysql-index-other-example-databases.md). No login or click-through; no upstream checksum.
* **Verified 2026-09-02**: the download matches the pinned sha256 exactly, and the inner files match their recorded sizes and md5s (`sakila-schema.sql` 24,269 B / `fcf59afd…`, `sakila-data.sql` 3,351,749 B / `799d84da…`, `sakila.mwb` 40,093 B), version string 1.5, LF endings, 161 non-ASCII lines, 16 tables / 6 view statements / 6 triggers / 3 procedures / 3 functions.
* Snapshot: HTTP Last-Modified 2026-08-31; inner file headers "Version 1.5", "Copyright (c) 2006, 2026, Oracle and/or its affiliates".
* Contents ([inspection](/sources/mysql-sakila-db-zip.md)): `sakila-schema.sql` 24,269 B (md5 `fcf59afd9117470f6cd45f948a3e9dcb`), `sakila-data.sql` 3,351,749 B (md5 `799d84daf7137bc341770c3070013668`), `sakila.mwb` 40,093 B (Workbench model - not open-licensed, do not ship).

# Native format and friendlier forms
Native MySQL SQL scripts (schema + multi-row INSERT data); nothing friendlier is needed. The datacharmer/test_db repository carries a derived copy (`sakila/sakila-mv-schema.sql`, `sakila-mv-data.sql`) but the Oracle download is authoritative and is used instead ([test_db sakila README](/sources/github-datacharmer-test-db-sakila-readme.md)).

# Shape
| table | rows | table | rows |
|---|---|---|---|
| actor | 200 | inventory | 4,581 |
| address | 603 | language | 6 |
| category | 16 | payment | 16,044 |
| city | 600 | rental | 16,044 |
| country | 109 | staff | 2 |
| customer | 599 | store | 2 |
| film | 1,000 | film_actor | 5,462 |
| film_category | 1,000 | film_text | (filled by triggers = 1,000) |

Total 46,268 inserted rows (counted from the data file). Note payment is 16,044, not the historical 16,049: Version 1.3 "Removed five rows in the payment table that had a null rental_id value" ([change history](/sources/mysql-sakila-change-history.md)). **Inferred:** film_text ends with 1,000 rows because `ins_film` copies every film row.
* Encoding: `sakila-data.sql` is UTF-8 without BOM, LF; `SET NAMES utf8mb4` at the top of both files. 161 lines contain non-ASCII, all in `address` (94), `city` (66), `country` (1) - e.g. `Inegöl`, `Salé`, `A Coruña (La Coruña)`, `Córdoba`, `São Paulo`. Films, actors, categories and language names are ASCII. Good encoding canary: `SELECT city FROM city WHERE city_id=...` values with accents must round-trip.
* Size: 3.4 MB of SQL. **Inferred:** loaded InnoDB footprint under 10 MB.

# Conversion path
Run the two upstream files unchanged through the mysql client against the `mysql-build` service during `make sakila`, schema then data; the loaded database is dumped with `util.dumpSchemas` and baked into the image like every other core dataset (no init-directory files) ([decision](/decisions/sakila-conversion-path.md)). No conversion tool.

# Type-mapping hazards
* `address.location GEOMETRY SRID 0 NOT NULL` with `SPATIAL KEY idx_location`, inserted as WKB hex literals inside `/*!50705 ... */` comments; many points are (0,0). A 9.7 server executes all version-gated comments (50705, 50610, 80003).
* `film.rating ENUM(...)`, `film.special_features SET(...)`, `film.release_year YEAR`, `DECIMAL(4,2)/(5,2)` money columns, `TIMESTAMP ... DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` on every table.
* `film_text` has an InnoDB `FULLTEXT KEY idx_title_description (title,description)`; the script sets `@@default_storage_engine='InnoDB'` first.
* The scripts set `SQL_MODE='TRADITIONAL'`, `UNIQUE_CHECKS=0`, `FOREIGN_KEY_CHECKS=0` and restore them; they run `DROP SCHEMA IF EXISTS sakila` - do not pre-create the database.
* `staff.password VARCHAR(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin` (binary collation) - collation-sensitive comparisons in tests.

# Programmable objects
All ported unchanged (native MySQL):
* Views (7): actor_info (declared `DEFINER=CURRENT_USER SQL SECURITY INVOKER`), customer_list, film_list, nicer_but_slower_film_list, sales_by_film_category, sales_by_store, staff_list.
* Procedures (3): rewards_report (`SQL SECURITY DEFINER`, creates a temporary table), film_in_stock, film_not_in_stock (OUT parameter).
* Functions (3): get_customer_balance (DETERMINISTIC READS SQL DATA), inventory_held_by_customer, inventory_in_stock (RETURNS BOOLEAN).
* Triggers (6): ins_film, upd_film, del_film (schema file, maintain film_text); customer_create_date, payment_date, rental_date (created inside the data file after the bulk load).
* Definer: objects without an explicit DEFINER get the loading user (`root@localhost` in the build server); `routines.sql` then re-creates the read-only views and routines with `SQL SECURITY INVOKER` per the [account model](/decisions/database-naming-convention.md).

# Indexing
Upstream indexes are kept: primary keys, `idx_*` secondary keys, foreign keys with `ON DELETE RESTRICT ON UPDATE CASCADE`, the spatial index and the fulltext index.

# Tests and expected values
* Row counts as in Shape; `SELECT COUNT(*) FROM film_text` = 1000 (inferred), `information_schema.TRIGGERS` = 6, `ROUTINES` = 6, `VIEWS` = 7, `TABLES` (BASE TABLE) = 16.
* Spatial: `SELECT ST_SRID(location) FROM address LIMIT 1` = 0; `SHOW INDEX FROM address` includes `idx_location` type SPATIAL.
* Fulltext: `SELECT COUNT(*) FROM film_text WHERE MATCH(title,description) AGAINST('dinosaur')` > 0 (inferred; ACADEMY DINOSAUR exists).
* Encoding: `SELECT address FROM address WHERE address_id=8` = `1566 Inegöl Manor`.
* Checksums: none published; the executor records `CHECKSUM TABLE` output after the first verified load. Do not use `MD5()` in tests on 9.6+ ([classic_hashing note](/tools/mysql-classic-hashing-component.md)).

# Tier assignment
core - 3.4 MB of SQL, the canonical MySQL sample; evidence: [zip inspection](/sources/mysql-sakila-db-zip.md).

# License and attribution
[BSD 3-Clause (Sakila)](/licenses/bsd-3-clause-sakila.md): keep the Oracle copyright/notice/disclaimer; only the two .sql files are covered - the manual and `sakila.mwb` are not open-licensed and must not be redistributed.

# Database name
`sakila` (fixed by the upstream script).

# Open questions
* [Checksum drift of the download](/questions/sakila-download-checksum-drift.md).
* Whether `sakila.mwb` may be referenced (link only) in the docs - treat as not redistributable until Oracle says otherwise.
