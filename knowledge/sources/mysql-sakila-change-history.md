---
type: Source
title: Sakila Change History (manual chapter 11)
description: Version-by-version change list for Sakila 0.2 through 1.5; establishes utf8mb4, SRID 0, InnoDB FULLTEXT, and the removal of five payment rows.
resource: https://dev.mysql.com/doc/sakila/en/sakila-news.html
tags:
- sakila
- changelog
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/sakila/en/sakila-news.html
  title: 11 Sakila Change History
  accessed: "2026-09-02"
  version: manual revision 84779; latest entry Version 1.5
---

# What was read
The full change history page, accessed 2026-09-02 (note: the URL is `sakila-news.html`; `sakila-changes.html` returns 404).

# Relevant excerpt
* Version 1.5: "Fixed MySQL Bug #112552: Accented characters were missing from the address fields."
* Version 1.4: film_text.film_id made unsigned; film_list / nicer_but_slower_film_list now return films without actors.
* Version 1.3: accented characters restored in city and country (from the world database); "Removed five rows in the payment table that had a null rental_id value."
* Version 1.2: "Database objects now use utf8mb4 rather than utf8"; film.title redeclared VARCHAR(128); "sakila-schema.sql and sakila-data.sql include a SET NAMES utf8mb4 statement"; data file converted to LF line endings; "The location column was changed to include an SRID 0 attribute for MySQL 8.0.3 and higher"; staff.password redeclared `VARCHAR(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin`; rewards_report parameter no longer `DECIMAL UNSIGNED`; FOUND_ROWS() replaced by COUNT(*) in film_in_stock / film_not_in_stock; film_text uses MyISAM only before 5.6.10.
* Version 1.1: all MyISAM references removed; film_text FULLTEXT on InnoDB.
* Version 1.0: spatial schema merged into one file using version-specific comments; spatial data inserted as of 5.7.5.

# What it was used to decide
Row-count expectation payment = 16044 (not the historical 16049) and the encoding/spatial hazards in [the Sakila dataset record](/datasets/sakila.md).
