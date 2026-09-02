---
type: Dataset
title: Chicago crimes 2001 to present
description: The City of Chicago's 8.6 M-row reported-crime extract plus the 434-row IUCR code lookup; a single year (2024, 259,267 rows) is proposed for the core tier.
resource: https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2
tags: [tier-core, tier-extended, csv, socrata, chicago]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://data.cityofchicago.org/api/views/ijzp-q8t2.json
    title: Socrata view metadata for ijzp-q8t2
    accessed: "2026-09-02"
    version: truth last modified Wed, 02 Sep 2026 11:37:15 GMT; 8,627,693 rows
  - resource: /sources/chicago-crimes-socrata-metadata.md
    title: Portal metadata and SODA measurements
    accessed: "2026-09-02"
  - resource: /sources/chicago-iucr-codes-dataset.md
    title: IUCR code lookup (c7ck-438e)
    accessed: "2026-09-02"
  - resource: https://www.chicago.gov/city/en/narr/foia/data_disclaimer.html
    title: City of Chicago Data Terms of Use
    accessed: "2026-09-02"
stale_after: "2026-12-01"
---

# Identity
"Crimes - 2001 to Present" (`ijzp-q8t2`) on the City of Chicago Data Portal: one row per reported incident (one row per victim for homicides), extracted from the Chicago Police Department's CLEAR system, block-level redacted, excluding the most recent seven days. Database name: **`chicago_crimes`**.

# Source artifact
* **Bulk CSV export:** `https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD` - returns `200`, `Content-Type: text/csv; charset=utf-8`, `Content-disposition: attachment; filename=Crimes_-_2001_to_Present.csv` and **`Content-Length: 0`** (chunked; the size is never advertised). Verified working on 2026-09-02, so the endpoint survived the Socrata -> Tyler "Data & Insights" rebranding; no deprecation notice was found.
* **SODA 2.1 API:** `https://data.cityofchicago.org/resource/ijzp-q8t2.csv` (or `.json`) with `$limit` / `$offset` / `$where` / `$order` / `$select`. A `$limit=50000` request returned `200`. **Always pass `$order=id`** - the export and the default API order are not stable, and `$offset` paging without an explicit order can duplicate and skip rows.
* **Row count on 2026-09-02:** `$select=count(*)` -> **8,627,693**. Grows daily; the portal reports data through "minus the most recent seven days".
* **Size:** no upstream figure. Measured 191.4 bytes/row over the first 15,672 exported rows -> **~1.65 GB** uncompressed for the full export (**inferred**).
* **Lookup:** IUCR codes `https://data.cityofchicago.org/api/views/c7ck-438e/rows.csv?accessType=DOWNLOAD` - **434 rows**.
* **Auth / click-through:** none. An app token is optional for SODA and only raises throttling limits.
* **Checksums:** none published. Record `sha256` plus the row count and `X-SODA2-Truth-Last-Modified` at fetch time - the underlying data changes daily, so a checksum only pins *your* snapshot.

# Native format and friendlier forms
Already CSV. The API form is friendlier for a bounded subset: one `$where=year=2024` request stream is 259,267 rows instead of 8.6 million.

# Shape
**`crimes`** - 22 export columns:
`ID`, `Case Number`, `Date`, `Block`, `IUCR`, `Primary Type`, `Description`, `Location Description`, `Arrest`, `Domestic`, `Beat`, `District`, `Ward`, `Community Area`, `FBI Code`, `X Coordinate`, `Y Coordinate`, `Year`, `Updated On`, `Latitude`, `Longitude`, `Location`.

Null counts across all 8,627,693 rows (portal column statistics): `Ward` 614,812; `Community Area` 613,723; `X`/`Y`/`Latitude`/`Longitude` 98,693 each; `Location Description` 16,587; `District` 47; all others 0.

**`iucr`** - 434 rows: `iucr`, `primary_description`, `secondary_description`, `index_code`, `active`.

**Encoding:** `charset=utf-8` in the header, but **no byte above 0x7F appeared in 15,672 sampled export rows**: `Block`, `Description`, `Primary Type` and `Location Description` are upper-case ASCII in practice. `Description` values do contain `/` and `-` (`MANUFACTURE / DELIVER - CRACK`). `utf8mb4` is still the right column charset.

# Conversion path
[DuckDB reader -> typed CSV -> `util.importTable`](/decisions/large-tabular-conversion-path.md). For the **core** subset, the simpler path is a single SODA request with `$where=year=2024&$order=id&$limit=...` written straight to CSV; the IUCR lookup goes in through the DuckDB MySQL extension.

Target DDL: `ID` -> `INT UNSIGNED PRIMARY KEY`; `Case Number` -> `VARCHAR(16)`; `Date`/`Updated On` -> `DATETIME`; `Block` -> `VARCHAR(64)`; `IUCR` -> `CHAR(4)`; `Primary Type`/`Description`/`Location Description` -> `VARCHAR`; `Arrest`/`Domestic` -> `TINYINT(1)`; `Beat` -> `CHAR(4)`; `District` -> `CHAR(3)`; `Ward` -> `TINYINT UNSIGNED NULL`; `Community Area` -> `TINYINT UNSIGNED NULL`; `FBI Code` -> `VARCHAR(3)`; `X`/`Y Coordinate` -> `INT NULL`; `Latitude`/`Longitude` -> `DECIMAL(11,8)`/`DECIMAL(12,8)` NULL; `Location` **dropped** (pure duplication of lat/lon).

# Type-mapping hazards
1. **Date format `MM/DD/YYYY hh:mm:ss AM`** in the CSV export (`07/29/2022 03:39:00 AM`) - needs `STR_TO_DATE(x,'%m/%d/%Y %h:%i:%s %p')`, and note `%h` (12-hour) with `%p`, not `%H`. The **SODA API returns ISO-8601 instead** (`2001-01-01T10:40:00.000`), so the two ingest paths need different parsers. Both are naive local times with no timezone.
2. **Leading-zero identifiers**: `Beat` = `0733`, `District` = `007`, `IUCR` = `0110`, `FBI Code` = `01A`. All must be strings; `FBI Code` is not even numeric.
3. **Booleans arrive as the literals `true`/`false`** in the export - `LOAD DATA` into a `TINYINT(1)` silently stores 0 for both unless converted.
4. **`Location` contains embedded newlines in the SODA CSV output** (the value spans three lines) though not in the `rows.csv` export. Dropping the column sidesteps this; if kept, the parser must handle multi-line quoted fields.
5. **`Case Number` is NOT unique** - 8,627,693 rows but only **8,627,064 distinct** values (verified). `ID` is unique and is the documented "Unique identifier for the record". Do not make `Case Number` a key.
6. **Empty coordinates** on 98,693 rows; `Location` is empty on the same rows.
7. **The export is not ordered by `ID`** and its order is not stable between requests.
8. **`Ward` and `Community Area` are typed differently by the portal** (`ward` number, `community_area` text) despite both being small integers; `community_area` may be an empty string rather than null in some vintages.
9. The eight `:@computed_region_*` columns exist in the view but not in `rows.csv` - do not build DDL from the view metadata.

# Programmable objects
None upstream. This project adds a view `v_crime_iucr` joining `crimes` to `iucr` (showing that `Primary Type`/`Description` are denormalised copies of the lookup - a good normalisation lesson), `SQL SECURITY INVOKER`. No procedures/triggers. The three referenced boundary datasets (Community Areas `cauq-8yn6`, Police Beats `aerh-rz74`, Police Districts `fthy-xz3r`) are **shapefile/KML only, with no tabular columns**, so no geography tables are created.

# Indexing
* `PRIMARY KEY (ID)` - the only true natural key.
* `KEY (Date)` - every temporal query.
* `KEY (IUCR)` - FK-like into `iucr.iucr`; a real `FOREIGN KEY` is plausible but **Inferred:** historical rows may carry retired IUCR codes absent from the current 434-row lookup, so verify with a left-join count before declaring it.
* `KEY (Primary Type)` (~35 distinct values, still useful for the classic `GROUP BY` demo), `KEY (Arrest)` skipped as too low-cardinality.
* `KEY (Beat)`, `KEY (District)`, `KEY (Community Area)` for the geography drill-downs.
* No unique index on `Case Number` (proven non-unique).

# Tests and expected values
* Core subset: `SELECT COUNT(*) FROM crimes` -> **259,267** for `Year = 2024` (verified count on 2026-09-02; it can still change because CPD amends old records, so the executor records the count and the fetch date together).
* `SELECT COUNT(*) FROM iucr` -> **434**.
* `SELECT COUNT(*) FROM crimes WHERE Latitude IS NULL` -> non-zero (proves hazard 6 survived the load).
* `SELECT COUNT(DISTINCT ID) = COUNT(*)` -> true.
* Full extract (extended): 8,627,693 rows as of 2026-09-02 - a moving target, so the test asserts a floor rather than equality.

# Tier assignment
* **Core: calendar year 2024, 259,267 rows** (2023 = 263,449 and 2025 = 237,695 are equally usable). **Inferred:** ~50 MB uncompressed CSV and roughly **60-90 MB** as an InnoDB table with six secondary indexes - at or slightly over the strict 50 MB line but inside the "medium core" allowance in [the tier model](/decisions/tier-model.md), and it is the single most recognisable public dataset in the whole image. If the budget bites, drop to a half-year. The 434-row `iucr` table ships with it unconditionally.
* **Extended: the full 2001-present extract.** ~1.65 GB of CSV, 8.6 M rows; `make load-chicago_crimes` streams the export.

# License and attribution
[Chicago data portal terms](/licenses/chicago-data-portal-terms.md). Redistribution is permitted; the **mandatory disclaimer** paragraph must be reproduced verbatim in the README and image documentation, together with the CPD's own accuracy disclaimer and the prohibition on deriving specific addresses. The user also accepts an indemnity, and the City may demand that distribution stop.

# Open questions
* Whether every `IUCR` value in the loaded subset exists in the 434-row lookup (one left join).
* Whether the 2024 subset stays at 259,267 rows between builds - CPD revises history, so the test should assert a tolerance rather than an exact equality. Cheapest check: re-run the `$select=count(*)&$where=year=2024` query at build time and compare with the manifest.
