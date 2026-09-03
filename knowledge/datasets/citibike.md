---
type: Dataset
title: Citi Bike (NYC) trip data
description: Lyft-operated Citi Bike trip records from the public S3 bucket; the licence forbids redistributing the data as a stand-alone dataset, so it is extended tier and user-fetched only.
resource: https://citibikenyc.com/system-data
tags:
- tier-user-fetched
- csv
- bikeshare
- redistribution-blocked
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://citibikenyc.com/system-data
  title: Citi Bike System Data
  accessed: "2026-09-02"
- resource: https://citibikenyc.com/data-sharing-policy
  title: Citi Bike Data Sharing Policy
  accessed: "2026-09-02"
- resource: /sources/citibike-s3-tripdata-listing.md
  title: S3 bucket listing and archive inspection
  accessed: "2026-09-02"
  version: 174 keys on 2026-09-02; newest 202607
stale_after: "2026-12-01"
---

# Identity
Citi Bike system trip data for New York City and Jersey City/Hoboken, published by Lyft Bikes and Scooters, LLC ("Bikeshare"). One row per trip, staff and sub-60-second trips already removed upstream. Database name: **`citibike`**.

# Source artifact
* **Bucket:** `https://s3.amazonaws.com/tripdata/` - anonymous `ListBucket` works and returned **174 keys**, `IsTruncated=false`. The human index is `https://s3.amazonaws.com/tripdata/index.html`.
* **Three naming families:**
  * `YYYY-citibike-tripdata.zip` - yearly, 2013-2023 (2023 = 1,602,415,356 B).
  * `YYYYMM-citibike-tripdata.zip` - monthly, `202401` to `202607` (202607 = 974,302,094 B; 2025 months run 353 MB to 1.03 GB).
  * `JC-YYYYMM-citibike-tripdata.csv.zip` - Jersey City, 2015-09 to 2026-07, 0.1-4.3 MB.
* **Naming is inconsistent and a downloader must not template blindly:** `JC-201708 citibike-tripdata.csv.zip` (space), `JC-202207-citbike-tripdata.csv.zip` (typo), and `JC-202510` / `JC-202601` / `JC-202604` drop the `.csv` infix. List the bucket and match, do not construct.
* **Archive structure traps:** monthly NYC zips contain **multiple STORED (uncompressed) CSV parts** - `202602-citibike-tripdata.zip` (237,639,864 B) holds `_1.csv` (194,851,286 B) and `_2.csv` (42,788,284 B), so the zip saves nothing. Yearly zips are **zips of zips**: `2023-citibike-tripdata.zip` expands to 12 inner monthly zips totalling **6.87 GB** before those are themselves expanded. All archives carry `__MACOSX/._*` members to skip.
* **Auth / click-through:** none technically; the licence attaches on access.
* **Checksums:** none published. Record `sha256` and the S3 `LastModified` at fetch.

# Native format and friendlier forms
Already zipped CSV; nothing friendlier exists. Live station metadata is separate, as GBFS JSON (`https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json`, 1,358,268 B on 2026-09-02) - the only current station dimension, since the trip files carry denormalised station names.

# Shape
**Current schema (Feb 2021 onward), 13 columns, verified from `JC-202602-citibike-tripdata.csv` (5,606,126 B, ~25,900 rows):**
`"ride_id","rideable_type","started_at","ended_at","start_station_name","start_station_id","end_station_name","end_station_id","start_lat","start_lng","end_lat","end_lng","member_casual"`
Sample: `"365C1119177B8358","electric_bike","2026-02-11 14:43:52.970","2026-02-11 14:46:59.722","South Waterfront Walkway - Sinatra Dr & 1 St","HB103","4 St & River St","HB611",40.73698221818716,-74.02778059244156,40.7408139,-74.0274062,"member"`

**Legacy schema, 15 columns, verified from `JC-201509-citibike-tripdata.csv` (1,063,347 B):**
`Trip Duration,Start Time,Stop Time,Start Station ID,Start Station Name,Start Station Latitude,Start Station Longitude,End Station ID,End Station Name,End Station Latitude,End Station Longitude,Bike ID,User Type,Birth Year,Gender`
Sample: `61,2015-09-21 14:53:16,...,24722,Subscriber,1975,1`

**Header spelling varies by era and series.** The 2015 JC file uses Title Case with spaces; other vintages use the run-together lower-case spelling (`tripduration,starttime,stoptime,start station id,...`). A loader must normalise headers case- and whitespace-insensitively rather than matching literals.

**Encoding:** no byte above 0x7F in the first 5,000 lines of either file. Station names are ASCII with `&`, `-` and digits. `utf8mb4` regardless.

# Conversion path
[DuckDB reader -> typed CSV -> `util.importTable`](/decisions/large-tabular-conversion-path.md), reading the zip members directly. Target DDL: `ride_id` -> `CHAR(16)`, `rideable_type` -> `ENUM`/`VARCHAR(16)`, `started_at`/`ended_at` -> `DATETIME(3)` (millisecond fractions are present), station names -> `VARCHAR(96)`, station ids -> `VARCHAR(16)` (**not** integers - modern ids are `HB103`), lat/lng -> `DECIMAL(17,14)` or `DOUBLE`, `member_casual` -> `ENUM('member','casual')`. A generated `trip_duration_s` column reproduces the legacy `tripduration`.

# Type-mapping hazards
1. **Two incompatible schemas.** The Feb-2021 break changes column count (15 -> 13), names, semantics and even the *kind* of station id. Never union eras without an explicit mapping; `gender` and `birth year` simply do not exist after the break (a deliberate privacy change).
2. **Station ids are strings.** `HB103`, `HB611`. A legacy-era integer column type would break on modern data.
3. **Fractional-second timestamps.** `2026-02-11 14:43:52.970` - `DATETIME` without `(3)` truncates silently.
4. **Quoting changed.** Older files are unquoted, newer ones fully quoted; station names contain `&` and `-` but no commas in the samples seen - still, use a real CSV parser.
5. **Empty station name/id for dockless e-bike trips** (seen in the sibling Divvy data; **Inferred:** the same applies here, since both are Lyft pipelines). Station columns must be nullable.
6. **Zips are STORED, so disk needs are the uncompressed size**, and yearly zips need two extraction passes.
7. **`ride_id` uniqueness:** documented as a per-ride identifier and unique within the sampled file; **Inferred** across a whole month - assert it after load rather than declaring `UNIQUE` blindly.

# Programmable objects
None upstream. This project would add a `v_trip_duration` view; no procedures or triggers.

# Indexing
* `PRIMARY KEY (ride_id)` if the post-load uniqueness assertion passes; otherwise a surrogate `BIGINT UNSIGNED AUTO_INCREMENT` with a non-unique index on `ride_id`.
* `KEY (started_at)`; `KEY (start_station_id)`, `KEY (end_station_id)` (FK-like into a GBFS-derived `station` table, though the trip files are self-describing); `KEY (member_casual)` is too low-cardinality to bother.
* No `FOREIGN KEY` to stations: historical station ids are retired and will not all exist in the current GBFS feed.

# Tests and expected values
No row count can be quoted from upstream - Citi Bike publishes none, and this project did not download a full month. The executor records `COUNT(*)`, `MIN(started_at)`, `MAX(started_at)` and `CHECKSUM TABLE` at first load and logs a **Verification**. As a smoke expectation, **Inferred** from the sampled row sizes: `JC-202602` holds roughly 25,900 rows; `202602-citibike-tripdata` (237.6 MB of CSV) holds on the order of 1.1 million.

# Tier assignment
**Extended, and never baked into a published artifact** - see the licence note below. Even ignoring the licence, one NYC month is 237 MB of CSV (roughly 300-400 MB loaded, **inferred**) and a year is multiple GB. If the dataset is wanted at all, the **Jersey City monthly file is the practical choice**: `JC-202602-citibike-tripdata.csv.zip` is 958,731 B on the wire and ~5.6 MB of CSV, which would fit core comfortably **if the licence permitted shipping it**. It does not, so it is fetched at load time like the rest.

# License and attribution
[Citi Bike data use policy](/licenses/citibike-data-use-policy.md). **This is the blocking finding of this dataset group.** The policy grants a perpetual licence to "access, reproduce, analyze, copy, modify, distribute in your product or service and use the Data", then prohibits: "Host, stream, publish, distribute, sublicense, or sell the Data as a stand-alone dataset; provided, however, you may include the Data as source material ... in analyses, reports, or studies published or distributed for non-commercial purposes". A sample-database image is a stand-alone dataset, not an analysis, report or study. Also: no re-identification, no CITI BIKE / Citigroup / Lyft marks, no implied endorsement, and access only "by means ... Bikeshare provides or authorizes" (so fetch from the S3 bucket, never a mirror).

**Design consequence:** ship the loader, the DDL, the expected checks and the licence text; the user's own `make load-citibike` performs the download, which is how the user accepts the licence directly.

# Open questions
* [May a converted copy be redistributed at all?](/questions/citibike-divvy-redistribution.md) - resolvable by one email to `bike-data@lyft.com`, the address both licences nominate.
* Exact row counts and `ride_id` uniqueness per month (resolved at first load).
* Whether NYC monthly files, like Divvy's, blank the station columns for dockless trips (one `head` of an extracted member).
