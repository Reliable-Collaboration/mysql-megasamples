---
type: Source
title: Citi Bike S3 tripdata bucket listing and archive inspection
description: The full S3 index of the tripdata bucket with sizes, plus the CSV headers of one old-schema and one new-schema archive read over range requests.
resource: https://s3.amazonaws.com/tripdata/
tags: [citibike, download, measurement]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://s3.amazonaws.com/tripdata/
    title: S3 ListBucket XML for the tripdata bucket
    accessed: 2026-09-02
    version: 174 keys, IsTruncated=false
  - resource: https://s3.amazonaws.com/tripdata/JC-202602-citibike-tripdata.csv.zip
    title: JC-202602 archive (central directory + first CSV block)
    accessed: 2026-09-02
stale_after: 2026-12-01
---

# What was read
The bucket's anonymous `ListBucket` XML (174 keys, `IsTruncated=false`), then ZIP central directories and the first compressed block of two archives, over HTTP `Range` requests. Accessed 2026-09-02.

# Relevant excerpt

**File-name patterns present in the bucket:**
* `YYYY-citibike-tripdata.zip` - **yearly** archives for 2013 through 2023 (2013: 329,797,836 B; 2018: 1,337,685,504 B; 2023: 1,602,415,356 B).
* `YYYYMM-citibike-tripdata.zip` - **monthly** archives from `202401` onward, up to `202607` (974,302,094 B). 2025 monthly archives range 353 MB (Jan) to 1.03 GB (Sep).
* `JC-YYYYMM-citibike-tripdata.csv.zip` - the small **Jersey City / Hoboken** series, 2015-09 to 2026-07, typically 0.1-4.3 MB. Naming is inconsistent: `JC-201708 citibike-tripdata.csv.zip` (space, not hyphen), `JC-202207-citbike-tripdata.csv.zip` (typo "citbike"), and `JC-202510`, `JC-202601`, `JC-202604` drop the `.csv` infix (`JC-202601-citibike-tripdata.zip`). **A downloader must not assume one template.**

**Archive structure:**
* `202602-citibike-tripdata.zip` (237,639,864 B) contains **two** CSV members, `202602-citibike-tripdata_1.csv` (194,851,286 B) and `_2.csv` (42,788,284 B), both **STORED, not deflated** (compressed size equals uncompressed size) - the zip provides no compression at all. Total 237,639,570 B for one month.
* `2023-citibike-tripdata.zip` (1,602,415,356 B) is a **zip of zips**: 12 inner monthly `.zip` members plus a `.DS_Store`, expanding to **6.87 GB** of inner archives before those are themselves expanded. Two levels of extraction are required.
* Archives carry macOS `__MACOSX/._*` junk members that must be skipped.

**New schema** (`JC-202602-citibike-tripdata.csv`, 5,606,126 B uncompressed, ~25,900 rows inferred) - header verbatim, fully quoted:
`"ride_id","rideable_type","started_at","ended_at","start_station_name","start_station_id","end_station_name","end_station_id","start_lat","start_lng","end_lat","end_lng","member_casual"`
Sample row: `"365C1119177B8358","electric_bike","2026-02-11 14:43:52.970","2026-02-11 14:46:59.722","South Waterfront Walkway - Sinatra Dr & 1 St","HB103","4 St & River St","HB611",40.73698221818716,-74.02778059244156,40.7408139,-74.0274062,"member"`
Timestamps carry **millisecond fractions**; `ride_id` is a 16-character uppercase hex-like token; station IDs are **strings** (`HB103`), not integers; latitudes are quoted-free floats with up to 14 decimals.

**Old schema** (`JC-201509-citibike-tripdata.csv`, 1,063,347 B) - header verbatim, **unquoted, with spaces in the names**:
`Trip Duration,Start Time,Stop Time,Start Station ID,Start Station Name,Start Station Latitude,Start Station Longitude,End Station ID,End Station Name,End Station Latitude,End Station Longitude,Bike ID,User Type,Birth Year,Gender`
Sample row: `61,2015-09-21 14:53:16,2015-09-21 14:54:17,3185,City Hall,40.7177325,-74.043845,3185,City Hall,40.7177325,-74.043845,24722,Subscriber,1975,1`
15 columns, seconds-resolution timestamps, integer station IDs, `Subscriber`/`Customer` instead of `member`/`casual`, and `Birth Year` may be empty. **Note:** this spelling differs from the lower-case run-together spelling (`tripduration,starttime,...`) used in other vintages of the archive - header spelling varies by era and by NYC-vs-JC series, so a loader must map headers case- and space-insensitively.

No non-ASCII bytes were found in the first 5,000 lines of either file.

The GBFS `station_information.json` feed (`https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json`, 1,358,268 B on 2026-09-02) is the only current station dimension; the trip files themselves carry denormalised station names.

# What it was used to decide
Source artifact sizes, the two-schema history, archive-structure hazards and the tier argument in [Citi Bike](/datasets/citibike.md).
