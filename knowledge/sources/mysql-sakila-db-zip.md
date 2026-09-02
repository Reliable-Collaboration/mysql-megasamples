---
type: Source
title: sakila-db.zip as downloaded 2026-09-02 (inspection of the artifact)
description: Sizes, checksums, file list, DDL features and per-table INSERT row counts measured on the Sakila 1.5 archive fetched from downloads.mysql.com.
resource: https://downloads.mysql.com/docs/sakila-db.zip
tags: [sakila, artifact, checksum, measurement]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://downloads.mysql.com/docs/sakila-db.zip
    title: sakila-db.zip
    accessed: "2026-09-02"
    version: "Version 1.5 (file headers); HTTP Last-Modified Mon, 31 Aug 2026 22:05:33 GMT"
  - resource: https://downloads.mysql.com/docs/sakila-db.tar.gz
    title: sakila-db.tar.gz (HEAD only)
    accessed: "2026-09-02"
---

# What was read
`curl -sIL` on both archives, then the zip was fetched to the scratchpad, extracted with python `zipfile` and grepped. Commands: `md5sum`, `sha256sum`, `file`, `grep -nE`, and a small python tuple counter over `INSERT INTO ... VALUES` statements (string-aware).

# Relevant excerpt (measurements)
* Zip: Content-Length 729,654 bytes; md5 `a80df38456f8d4f36903771b67a1129a`; sha256 `e27ed871082e76e9d32021c2df07f97ebf7696ace132f5995218557dd87d7046`. Tar.gz: 732,423 bytes (Last-Modified 2026-08-31 22:05:32 GMT). No checksum is published upstream.
* Contents (zip entries dated 2026-09-01 00:05): `sakila-db/sakila-schema.sql` 24,269 B, ASCII, LF (md5 `fcf59afd9117470f6cd45f948a3e9dcb`, sha256 `b32170e1e2ad5828749b61a5ec896155bcd143104b076e5ee8a3a3b013f44915`); `sakila-db/sakila-data.sql` 3,351,749 B, UTF-8 without BOM, LF (md5 `799d84daf7137bc341770c3070013668`, sha256 `8c228c678cec6ea9e5145ea868f48be87982252e806a547dcddb67758cadf174`); `sakila-db/sakila.mwb` 40,093 B (md5 `50f2f00de3a66d65eb7462adcadf24ca`).
* Headers: "Sakila Sample Database Schema -- Version 1.5 -- Copyright (c) 2006, 2026, Oracle and/or its affiliates." followed by the three BSD conditions and the disclaimer; same header in the data file.
* Schema features: `SET NAMES utf8mb4;`, `SET_SQL_MODE='TRADITIONAL'`, `DROP SCHEMA IF EXISTS sakila; CREATE SCHEMA sakila; USE sakila;`; every table `ENGINE=InnoDB DEFAULT CHARSET=utf8mb4`; address: `/*!50705 location GEOMETRY */ /*!80003 SRID 0 */ /*!50705 NOT NULL,*/` and `/*!50705 SPATIAL KEY idx_location (location),*/`; film: `release_year YEAR`, `rating ENUM('G','PG','PG-13','R','NC-17') DEFAULT 'G'`, `special_features SET('Trailers','Commentaries','Deleted Scenes','Behind the Scenes')`; film_text: `FULLTEXT KEY idx_title_description (title,description)` after `/*!50610 SET @@default_storage_engine = 'InnoDB'*/`; staff.password `VARCHAR(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin`; views use `_utf8mb4' '` literals; `CREATE DEFINER=CURRENT_USER SQL SECURITY INVOKER VIEW actor_info`; `rewards_report` is `NOT DETERMINISTIC READS SQL DATA SQL SECURITY DEFINER`; triggers ins_film/upd_film/del_film are in the schema file, triggers customer_create_date, payment_date, rental_date are in the data file (lines 2213, 30355, 46413).
* Data file: multi-row INSERTs wrapped in `SET AUTOCOMMIT=0; ... COMMIT;`; address rows carry `/*!50705 0x0000000001010000...,*/` WKB POINT literals (many are 0-coordinate points).
* Row counts (tuples per table): actor 200, address 603, category 16, city 600, country 109, customer 599, film 1000, film_actor 5462, film_category 1000, inventory 4581, language 6, payment 16044, rental 16044, staff 2, store 2; total 46,268.
* Non-ASCII: 161 lines in the data file, all in `address` (94 lines), `city` (66) and `country` (1); e.g. `1566 Inegöl Manor`, `1531 Salé Drive`, `262 A Coruña (La Coruña) Parkway`, `Córdoba`, `São Paulo`. film, actor and language rows are pure ASCII (English, Italian, Japanese, Mandarin, French, German).

# What it was used to decide
[Sakila dataset record](/datasets/sakila.md) sections Source artifact, Shape, Tests; [Sakila checksum-drift question](/questions/sakila-download-checksum-drift.md).
