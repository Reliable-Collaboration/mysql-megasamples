---
type: Dataset
title: Divvy (Chicago) trip data
description: City-of-Chicago-owned, Lyft-operated Divvy trip records from a public S3 bucket; the licence forbids redistributing the data as a stand-alone dataset, so it is extended tier and user-fetched only.
resource: https://divvybikes.com/system-data
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
- resource: https://divvybikes.com/system-data
  title: Divvy System Data
  accessed: "2026-09-02"
- resource: https://divvybikes.com/data-license-agreement
  title: Divvy Data License Agreement
  accessed: "2026-09-02"
- resource: /sources/divvy-s3-tripdata-listing.md
  title: S3 bucket listing and archive inspection
  accessed: "2026-09-02"
  version: 95 keys on 2026-09-02; newest 202607
stale_after: "2026-12-01"
---

# Identity
Divvy bikeshare trip records for Chicago - data owned by the City of Chicago, published by Lyft Bikes and Scooters, LLC. One row per trip, staff and sub-60-second trips already removed upstream. Database name: **`divvy`**.

# Source artifact
* **Bucket:** `https://divvy-tripdata.s3.amazonaws.com/` - anonymous `ListBucket` works and returned **95 keys**, `IsTruncated=false`. Human index at `.../index.html`.
* **Two naming families, with the break at 2020-Q1 / 2020-04:**
  * Legacy quarterly/annual: `Divvy_Stations_Trips_2013.zip`, `Divvy_Stations_Trips_2014_Q1Q2.zip`, `Divvy_Trips_2015-Q1Q2.zip` (**hyphen**, unlike every sibling), `Divvy_Trips_2016_Q1Q2.zip` ... `Divvy_Trips_2019_Q1..Q4.zip`, `Divvy_Trips_2020_Q1.zip`.
  * Monthly `YYYYMM-divvy-tripdata.zip` from **`202004`** to **`202607`** (32,910,286 B, the largest).
* **Representative sizes:** `202004-divvy-tripdata.zip` 3,323,572 B -> 14,254,024 B CSV; `202607-divvy-tripdata.zip` 32,910,286 B -> **173,089,330 B** CSV; `Divvy_Trips_2019_Q1.zip` 9,565,886 B -> 50,528,553 B CSV. Unlike Citi Bike's, these members **are** deflated.
* **Auth / click-through:** none technically; the licence attaches on access.
* **Checksums:** none published. Record `sha256` and `LastModified` at fetch.
* Archives carry `__MACOSX/._*` junk members to skip.

# Native format and friendlier forms
Already zipped CSV. Station metadata is separate GBFS JSON (`https://gbfs.lyft.com/gbfs/2.3/chi/en/station_information.json`, 1,120,652 B on 2026-09-02).

# Shape
**Current schema, 13 columns - identical column names to Citi Bike's modern layout.** Verified in two eras:

*Unquoted era* (`202004-divvy-tripdata.csv`, 14,254,024 B, ~84,800 rows inferred):
`ride_id,rideable_type,started_at,ended_at,start_station_name,start_station_id,end_station_name,end_station_id,start_lat,start_lng,end_lat,end_lng,member_casual`
`A847FADBBC638E45,docked_bike,2020-04-26 17:45:14,2020-04-26 18:12:03,Eckhart Park,86,...,member`

*Quoted era* (`202607-divvy-tripdata.csv`, 173,089,330 B, ~1,357,000 rows inferred): same names, fully quoted, **millisecond timestamps**, and **empty station name/id for dockless e-bike trips** with coordinates rounded to two decimals:
`"21025F24DBEF6519","electric_bike","2026-07-12 22:05:11.820","2026-07-12 22:05:39.379",,,,,41.83,-87.67,41.83,-87.67,"casual"`

**Legacy schema, 12 columns** (`Divvy_Trips_2019_Q1.csv`, 50,528,553 B, ~364,000 rows inferred):
`trip_id,start_time,end_time,bikeid,tripduration,from_station_id,from_station_name,to_station_id,to_station_name,usertype,gender,birthyear`
`21742443,2019-01-01 00:04:37,2019-01-01 00:11:07,2167,390.0,199,Wabash Ave & Grand Ave,84,Milwaukee Ave & Grand Ave,Subscriber,Female,1990`

**Encoding:** no byte above 0x7F in the first 5,000 lines of any of the three files. Station names are ASCII and include a `(*)` marker in the legacy era (`Dearborn St & Van Buren St (*)`).

# Conversion path
[DuckDB reader -> typed CSV -> `util.importTable`](/decisions/large-tabular-conversion-path.md), reading zip members directly. Same target DDL as [Citi Bike](/datasets/citibike.md) - one shared loader handles both, which is the main reason to keep them as a pair.

# Type-mapping hazards
1. **Two incompatible schemas** (12-column legacy vs 13-column modern), with the break exactly at `Divvy_Trips_2020_Q1` -> `202004`. `gender` and `birthyear` disappear; `tripduration` disappears and must be computed.
2. **`tripduration` is a float in the legacy files** (`390.0`) despite being whole seconds.
3. **Quoting changed** mid-life (unquoted in 2020-04, fully quoted by 2026-07) and **timestamp precision changed** (seconds -> milliseconds). `DATETIME(3)` covers both.
4. **Empty station name and id on dockless trips**, with **coordinates rounded to 2 decimals** on exactly those rows - a real analytic caveat, not just a null. Station columns must be nullable and coordinate precision must not be assumed uniform.
5. **Station ids changed type**: small integers in 2020-04, strings in the Citi Bike sibling and in later Divvy files. Use `VARCHAR(16)` for both eras.
6. **Legacy station names carry a `(*)` suffix** for temporarily relocated stations.
7. **Duplicate `ride_id`s are reported by third-party analyses of some months**, though the analyses that were searched for actually found none in the months they examined. **This is unverified either way in this session** - the safe design is a surrogate PK plus a post-load `GROUP BY ride_id HAVING COUNT(*)>1` assertion recorded in the manifest, rather than declaring `PRIMARY KEY (ride_id)` on faith.
8. `rideable_type` values changed over time (`docked_bike` in 2020, `electric_bike`/`classic_bike` later) - use `VARCHAR`, not a fixed `ENUM`, unless the enum is derived from the loaded month.

# Programmable objects
None upstream; same view treatment as Citi Bike.

# Indexing
Surrogate `BIGINT UNSIGNED AUTO_INCREMENT` PK plus `KEY (ride_id)`; `KEY (started_at)`; `KEY (start_station_id)`, `KEY (end_station_id)`. No `FOREIGN KEY` to a station table (dockless rows have no station, and historical ids are retired).

# Tests and expected values
No upstream row counts exist. **Inferred** from measured average row length against the uncompressed member size: `202004` ~84,800 rows; `Divvy_Trips_2019_Q1` ~364,000 rows; `202607` ~1,357,000 rows. The executor replaces these with exact `COUNT(*)` values plus `MIN`/`MAX(started_at)` and `CHECKSUM TABLE` at first load, and asserts the `ride_id` duplicate check from hazard 7.

# Tier assignment
**Extended, and never baked into a published artifact** - see the licence note. On size alone `202004-divvy-tripdata` (3.3 MB zipped, 14 MB CSV, ~85k rows; **inferred** 15-25 MB loaded) would be an ideal *core* dataset - small, modern schema, joins to nothing, perfect for teaching. The licence, not the size, is what pushes it out.

# License and attribution
[Divvy data license](/licenses/divvy-data-license.md). Word-for-word the same prohibition as Citi Bike: "Host, stream, publish, distribute, sublicense, or sell the Data as a stand-alone dataset; provided, however, you may include the Data as source material ... in analyses, reports, or studies published or distributed for non-commercial purposes". The City of Chicago owns the data, but the permissive [Chicago portal terms](/licenses/chicago-data-portal-terms.md) do **not** apply here - this agreement governs instead, which is a trap for anyone assuming "Chicago data = Chicago terms". Also: no DIVVY / Lyft / City-of-Chicago marks, no implied endorsement, no re-identification. There is **no** general non-commercial restriction and **no** anti-competition clause, contrary to common summaries.

**Design consequence:** identical to Citi Bike - ship the loader and the licence text, let `make load-divvy` fetch from the S3 bucket.

# Open questions
* [May a converted copy be redistributed at all?](/questions/citibike-divvy-redistribution.md) - one email to `bike-data@lyft.com` covers both bikeshare datasets.
* Whether duplicate `ride_id`s exist in the chosen month (one `GROUP BY` after load).
* Exact row counts (resolved at first load).
