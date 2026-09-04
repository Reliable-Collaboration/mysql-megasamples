---
type: Dataset
title: NYC TLC trip records
description: New York City yellow and green taxi trip records in Parquet, plus the 265-row taxi zone lookup; one month per colour, with the yellow month in the extended tier.
resource: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
tags:
- tier-core
- tier-extended
- parquet
- public-data
- nyc
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
  title: TLC Trip Record Data
  accessed: "2026-09-02"
  version: snapshot 2026-09-02; newest month published = 2026-05
- resource: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
  title: Yellow Taxi data dictionary
  accessed: "2026-09-02"
  version: dated March 18, 2025
- resource: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf
  title: Green (LPEP) data dictionary
  accessed: "2026-09-02"
  version: dated March 18, 2025
- resource: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_hvfhs.pdf
  title: High Volume FHV data dictionary
  accessed: "2026-09-02"
- resource: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
  title: Taxi Zone Lookup Table
  accessed: "2026-09-02"
  version: Last-Modified 2024-02-22; MD5 c6064b7c144c716450641f769659d178
- resource: /sources/nyc-tlc-parquet-footer-inspection.md
  title: Parquet footer inspection (row counts, types, drift)
  accessed: "2026-09-02"
stale_after: "2026-12-01"
---

# Identity
NYC Taxi & Limousine Commission trip records: one row per completed trip by a TLC-licensed vehicle. Four families - yellow (medallion), green (street-hail livery), FHV and High-Volume FHV. This project uses **yellow and green** plus the **taxi zone** dimension. Database name: **`nyc_taxi`**.

# Source artifact
* **URL pattern:** `https://d37ci6vzurychx.cloudfront.net/trip-data/<yellow|green|fhv|fhvhv>_tripdata_YYYY-MM.parquet` (CloudFront; every link on the TLC page resolves here). Lookup: `https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv`; shapefile `.../misc/taxi_zones.zip`.
* **Format:** Apache Parquet (snappy-era `parquet-cpp-arrow` writer). The lookup is CSV.
* **Auth / click-through:** none. Plain anonymous HTTPS GET; `curl` works.
* **Recommended pin - January 2025** (a complete month, the first month containing `cbd_congestion_fee`, and untouched upstream since 2025-04-23):

| Artifact | Content-Length | Last-Modified | ETag | Rows |
|---|---:|---|---|---:|
| `green_tripdata_2025-01.parquet` | 1,178,451 | (2025) | `110776612e1b020e9c4a0e41f16da597` (single-part = **MD5**) | **48,326** |
| `yellow_tripdata_2025-01.parquet` | 59,158,238 | Wed, 23 Apr 2025 16:31:58 GMT | `3f99a46...-12` (multipart, **not** an MD5) | **3,475,226** |
| `taxi_zone_lookup.csv` | 12,331 | Thu, 22 Feb 2024 21:33:00 GMT | `c6064b7c144c716450641f769659d178` (**MD5**) | 265 |

  Alternative newest month 2026-05: yellow 69,699,174 B / 4,090,836 rows; green 1,102,947 B / 44,921 rows. `yellow_tripdata_2026-06.parquet` returns **403** (not yet published) - the page's stated cadence is "published monthly ... typically with a two-month delay".
* **Checksums:** TLC publishes **none**. For single-part S3 objects the CloudFront `ETag` is the MD5 and can be used as a weak upstream check; for multipart objects (the yellow file) it cannot. The executor records `sha256` at first fetch into `megasamples.datasets`.
* **Volatility:** TLC re-uploads historical files (`yellow_tripdata_2025-01` carries a 2025-04-23 Last-Modified) and the page warns "there may be minor changes in the near future to standardize the parquet schema across all years and datasets". Pin the sha256 and re-verify on rebuild.

# Native format and friendlier forms
Parquet needs a Parquet reader; there is no SQL script and no CSV upstream. The friendlier form is DuckDB's `read_parquet`, which needs no Hadoop/Spark stack. The same data is mirrored per-year on NYC Open Data (`data.cityofnewyork.us`, e.g. `4b4i-vvec` = 2023 Yellow) where CSV export is available, but those views are stale (2023 datasets last updated 2024-07) and slower to export; the CloudFront Parquet is authoritative.

# Shape
**`yellow_trips`** - 20 columns, all nullable (from the 2025-01 footer):
`VendorID` INT32, `tpep_pickup_datetime` / `tpep_dropoff_datetime` INT64 TIMESTAMP_MICROS (`isAdjustedToUTC=false`), `passenger_count` INT64, `trip_distance` DOUBLE, `RatecodeID` INT64, `store_and_fwd_flag` UTF8, `PULocationID` INT32, `DOLocationID` INT32, `payment_type` INT64, `fare_amount`, `extra`, `mta_tax`, `tip_amount`, `tolls_amount`, `improvement_surcharge`, `total_amount`, `congestion_surcharge`, **`Airport_fee`**, **`cbd_congestion_fee`** DOUBLE.

**`green_trips`** - 21 columns in a **different order**, with `lpep_*` datetime names, plus `ehail_fee` and `trip_type`, and **no** `Airport_fee`.

**`taxi_zone`** - `LocationID` 1..265, `Borough`, `Zone`, `service_zone`; 265 rows; sentinels 264 "Unknown"/"N/A" and 265 "N/A"/"Outside of NYC".

**Encoding:** Parquet strings are UTF-8 by definition; the only string columns in yellow/green are `store_and_fwd_flag` (`Y`/`N`). `taxi_zone_lookup.csv` is **pure ASCII** (`file` reports "CSV ASCII text"; no byte > 0x7F). No encoding traps. `utf8mb4` throughout is safe and costs nothing.

**Value semantics worth knowing:** `RatecodeID` 99 = null/unknown; `payment_type` 0 = Flex Fare trip; `VendorID` 1/2/6/7 (green has no 7); tips are credit-card only; `total_amount` excludes cash tips.

# Conversion path
[DuckDB reader -> typed CSV -> `util.importTable`](/decisions/large-tabular-conversion-path.md). `taxi_zone` (265 rows) goes straight in through the DuckDB MySQL extension.

Target DDL sketch: `VendorID` -> `TINYINT UNSIGNED NULL`, datetimes -> `DATETIME(6) NULL` (**no timezone conversion** - the source is local wall-clock), `passenger_count` -> `TINYINT UNSIGNED NULL`, `RatecodeID`/`payment_type` -> `TINYINT UNSIGNED NULL`, `store_and_fwd_flag` -> `CHAR(1) NULL`, `PULocationID`/`DOLocationID` -> `SMALLINT UNSIGNED NULL`, `trip_distance` -> `DECIMAL(8,2)`, every money column -> `DECIMAL(10,2)`. Add a surrogate `trip_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY`.

# Built and measured (2026-09-03, core subset)
`green_tripdata_2025-01.parquet` loads **48,326** rows — the count the record predicted — alongside the full **265**-row zone lookup, in 0.7 s at **11.1 MB** in InnoDB. Three checks were run rather than assumed:

* **The DOUBLE -> DECIMAL(10,2) narrowing is lossless here.** DuckDB's sums over the Parquet and MySQL's sums over the loaded table agree exactly: total_amount 1,093,822.36, fare_amount 810,062.91, trip_distance 1,040,575.25.
* **No trip carries a zone id outside the lookup** (hazard 8's precondition), so the two foreign keys onto `taxi_zone` are declared rather than left as bare indexes.
* **The dirty rows are real and are kept.** 3,447 of 48,326 trips (7.1%) are suspect by at least one measure, and the pickup timestamps run from 2024-12-25 to 2025-02-05 — 38 distinct dates in a 31-day month, which is the "pickup dates outside the file's month" hazard, measured. A `v_suspect_trips` view names them instead of deleting them.

Timestamps are `DATETIME(6)`, never `TIMESTAMP`, because the Parquet says `isAdjustedToUTC=false`. Views: `v_trip_zone`, `v_green_daily`, `v_suspect_trips`, all `SQL SECURITY INVOKER`.

## Yellow, the extended tier (2026-09-03, task X-03)
`yellow_tripdata_2025-01.parquet` is 59,158,238 bytes — the size this record predicted, to the byte —
and holds **3,475,226** rows, the count it predicted. `make nyc-taxi-yellow` appends them to a loaded
`nyc_taxi` in 22 s, taking the database from 11.1 MB to **610.9 MB**. Converting 3.5 M rows of Parquet
to TSV takes 1.4 s; DuckDB is not the slow part of anything.

The schema is exactly as recorded: 20 columns, `tpep_*` datetimes, **`Airport_fee` with a capital A**
(hazard 2 — normalised to `airport_fee`), no `ehail_fee` or `trip_type`, and a column order that does
not match green's (hazard 7), which is why every projection is by name.

Measured rather than assumed:
* **The DECIMAL(10,2) narrowing is lossless.** No money value in the file needs a third decimal — the
  converter now checks that and refuses to run otherwise — and MySQL's sums match DuckDB's over the
  source exactly: total_amount **89,005,026.80**, fare_amount **59,363,125.08**, trip_distance
  **20,347,886.73**.
* **All 3.5 M trips carry zone ids inside 1..265**, so both foreign keys onto `taxi_zone` are declared.
  261 of the 265 zones appear as a pickup zone.
* **`cbd_congestion_fee` is populated on every row**, which confirms 2025-01 as the first month
  carrying it; `airport_fee` is NULL on exactly 540,149 rows — the same 540,149 that are
  `payment_type` 0 (Flex Fare).
* **Dirty rows are real and kept**: 173,644 suspect trips (5.0%), 24,656 with no passengers, 63,596
  with a non-positive total, 162 longer than 100 miles, and pickups from 2024-12-31 20:47 to
  2025-02-01 00:00 — 33 distinct dates in a 31-day month. `v_suspect_yellow_trips` names them.
* Manhattan is 89% of pickups (3,089,275), then Queens 294,986 and Brooklyn 66,070.

Both colours share one database and one `taxi_zone`; green stays core (11.1 MB baked into the image)
and yellow is `append: true`, fetched and loaded only on request.

# Type-mapping hazards
1. **Cross-year schema drift** (the big one). `VendorID`/`PULocationID`/`DOLocationID` are INT64 in 2015-2022 files and INT32 in 2025+; `passenger_count`/`RatecodeID` are INT64 (2015-16), DOUBLE (2019-2022), INT64 again (2025+). Any multi-year read needs `union_by_name := true` and explicit casts.
2. **`airport_fee` vs `Airport_fee`.** Lower case in every pre-2025 file, capital A in 2025+. The **data dictionary spells it lower case**, so the dictionary and the data disagree. MySQL identifiers on Linux are case-sensitive for tables but not columns - normalise to `airport_fee` on the way in.
3. **All-null typed columns.** In `yellow_tripdata_2015-01` and `2016-07`, `congestion_surcharge` and `airport_fee` are physical INT32 with logical type **UNKNOWN (Null)**; in `2019-01`, `airport_fee` still is. A naive `CAST` to DECIMAL works, but schema inference across a mixed set will fail without `union_by_name`.
4. **Timestamps are local wall-clock** (`isAdjustedToUTC=false`). Storing them as `TIMESTAMP` would apply a session timezone conversion; use `DATETIME(6)`. DST-ambiguous instants exist in November files.
5. **Dirty values.** The archive is well known for out-of-range rows - `passenger_count = 0`, zero/negative `total_amount`, `trip_distance` in the thousands, and pickup dates outside the file's month. **Inferred** (not measured here): keep them, since the TLC disclaimer says the data was not created by the TLC and makes no accuracy representations; do not silently clean, and add a documented "dirty data" exercise view instead.
6. **`Airport_fee` and `cbd_congestion_fee` are absent from pre-2025 files** - a fixed DDL must allow NULL for them.
7. Column **order** differs between yellow and green; never load by position across colours.

# Programmable objects
None upstream - the source is flat files. This project adds: a view `v_trip_zone` joining `yellow_trips` to `taxi_zone` on both `PULocationID` and `DOLocationID` (a natural two-join teaching example), and a `v_yellow_daily` aggregate. Both `SQL SECURITY INVOKER` per the naming/accounts decision. No procedures, triggers, computed columns or temporal tables.

# Indexing
* Surrogate `trip_id` PK (there is **no natural key**: two identical trips by the same vendor in the same second are indistinguishable, and no trip identifier is published).
* `KEY (tpep_pickup_datetime)` - the range predicate every example query uses.
* `KEY (PULocationID)`, `KEY (DOLocationID)` - FK-like columns into `taxi_zone` (a real `FOREIGN KEY` is defensible here since the lookup is complete for 1..265; **Inferred:** verify no trip row carries a zone ID outside that range before enabling it, and expect `0` values in some months).
* `KEY (payment_type)` is low-cardinality; skip.
* `taxi_zone`: `PRIMARY KEY (LocationID)`, `KEY (Borough)`.

# Tests and expected values
* `SELECT COUNT(*) FROM taxi_zone` -> **265** (published-file-derived, exact).
* `SELECT COUNT(*) FROM green_trips` -> **48,326** for 2025-01 (from the Parquet footer `num_rows`).
* `SELECT COUNT(*) FROM yellow_trips` -> **3,475,226** for 2025-01 (footer `num_rows`).
* `SELECT MAX(locationid) FROM taxi_zone` -> 265; `SELECT COUNT(DISTINCT borough) FROM taxi_zone` -> 8.
* Executor records `CHECKSUM TABLE` for each after first load; no upstream checksum exists to compare against.

# Tier assignment
* **Core: green taxi 2025-01 + taxi zones.** 1.18 MB of Parquet, 48,326 rows, 21 narrow columns. **Inferred:** roughly 8-12 MB as an InnoDB table with two secondary indexes - comfortably inside the 50 MB core budget from [the tier model](/decisions/tier-model.md), and it exercises Parquet reading, `DATETIME(6)`, `DECIMAL` money and a dimension join at negligible cost.
* **Extended: yellow taxi 2025-01.** 59 MB Parquet / 3.48 M rows. **Inferred:** roughly 500-700 MB loaded with indexes - far past the core budget, so it is fetched by `make load-nyc_taxi`.
* **Excluded: HVFHV and FHV.** `fhvhv_tripdata_2026-05.parquet` alone is 537,576,484 bytes / 22,125,744 rows; documented here for completeness only.

# License and attribution
[NYC Open Data terms](/licenses/nyc-open-data-terms.md). No attribution is legally required and there is no share-alike; the project ships the attribution string anyway, including the TLC's own disclaimer: "The trip data was not created by the TLC, and TLC makes no representations as to the accuracy of these data." The reuse position rests on the Open Data FAQ ("There are no restrictions on the use of Open Data") - see [the open question](/questions/nyc-open-data-reuse-terms.md).

# Open questions
* [Does NYC Open Data actually permit unrestricted redistribution?](/questions/nyc-open-data-reuse-terms.md)
* [When exactly did TLC switch to Parquet?](/questions/tlc-parquet-switch-date.md) - and, relatedly, the pre-2016 lat/lon columns. The 2015-01 Parquet already carries `PULocationID`/`DOLocationID` and **no coordinate columns**, so the historical rewrite normalised old data to the modern layout; the original CSV-era coordinate columns are not obtainable from TLC today. Anyone needing them must use a third-party mirror, which is out of scope.
* Whether every `PULocationID` in the chosen month falls in 1..265 (decides whether a real FK can be declared) - cheapest test is one `SELECT` after load.
