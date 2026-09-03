---
type: Source
title: Divvy S3 tripdata bucket listing and archive inspection
description: The full S3 index of divvy-tripdata with sizes, plus the CSV headers of the old quarterly and new monthly schemas read over range requests.
resource: https://divvy-tripdata.s3.amazonaws.com/
tags:
- divvy
- download
- measurement
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://divvy-tripdata.s3.amazonaws.com/
  title: S3 ListBucket XML for divvy-tripdata
  accessed: "2026-09-02"
  version: 95 keys, IsTruncated=false
- resource: https://divvy-tripdata.s3.amazonaws.com/202004-divvy-tripdata.zip
  title: 202004 archive (central directory + first CSV block)
  accessed: "2026-09-02"
stale_after: "2026-12-01"
---

# What was read
The bucket's anonymous `ListBucket` XML (95 keys, `IsTruncated=false`), then ZIP central directories and first compressed blocks of three archives over HTTP `Range` requests. Accessed 2026-09-02.

# Relevant excerpt

**File-name patterns present:**
* `YYYYMM-divvy-tripdata.zip` - monthly, **`202004` through `202607`**, 1.9 MB to 32.9 MB. `202607-divvy-tripdata.zip` = 32,910,286 B (largest).
* Legacy quarterly/annual: `Divvy_Stations_Trips_2013.zip`, `Divvy_Stations_Trips_2014_Q1Q2.zip`, `Divvy_Stations_Trips_2014_Q3Q4.zip`, `Divvy_Trips_2015-Q1Q2.zip` (**hyphen**, not underscore), `Divvy_Trips_2015_Q3Q4.zip`, `Divvy_Trips_2016_Q1Q2.zip`, `Divvy_Trips_2016_Q3Q4.zip`, `Divvy_Trips_2017_Q1Q2.zip`, `Divvy_Trips_2017_Q3Q4.zip`, `Divvy_Trips_2018_Q1..Q4.zip`, `Divvy_Trips_2019_Q1..Q4.zip`, `Divvy_Trips_2020_Q1.zip`. Plus `index.html` (a GPL'd S3 bucket-listing page by Francesco Pasqualini).
* The naming break is exactly at **2020-Q1 -> 202004**: `Divvy_Trips_2020_Q1.zip` is the last legacy file and `202004-divvy-tripdata.zip` the first monthly one.

**New schema, unquoted era** - `202004-divvy-tripdata.csv` (14,254,024 B uncompressed; ~84,800 rows inferred):
`ride_id,rideable_type,started_at,ended_at,start_station_name,start_station_id,end_station_name,end_station_id,start_lat,start_lng,end_lat,end_lng,member_casual`
Sample: `A847FADBBC638E45,docked_bike,2020-04-26 17:45:14,2020-04-26 18:12:03,Eckhart Park,86,Lincoln Ave & Diversey Pkwy,152,41.8964,-87.661,41.9322,-87.6586,member`
Second-resolution timestamps; **integer** station IDs; `docked_bike` rideable type.

**New schema, quoted era** - `202607-divvy-tripdata.csv` (173,089,330 B uncompressed; ~1,357,000 rows inferred): same 13 column names but **fully quoted**, millisecond timestamps, and **empty station name/id** for dockless e-bike trips:
`"21025F24DBEF6519","electric_bike","2026-07-12 22:05:11.820","2026-07-12 22:05:39.379",,,,,41.83,-87.67,41.83,-87.67,"casual"`
Coordinates in these rows are **rounded to 2 decimals** (privacy fuzzing for dockless trips) whereas docked rows carry 4+.

**Old schema** - `Divvy_Trips_2019_Q1.csv` (50,528,553 B uncompressed; ~364,000 rows inferred), 12 unquoted columns:
`trip_id,start_time,end_time,bikeid,tripduration,from_station_id,from_station_name,to_station_id,to_station_name,usertype,gender,birthyear`
Sample: `21742443,2019-01-01 00:04:37,2019-01-01 00:11:07,2167,390.0,199,Wabash Ave & Grand Ave,84,Milwaukee Ave & Grand Ave,Subscriber,Male,1989`
Note `tripduration` is a **float** (`390.0`), there are **no coordinate columns**, `usertype` is `Subscriber`/`Customer`, `gender` is `Male`/`Female`/empty, and station names contain a `(*)` marker (`Dearborn St & Van Buren St (*)`).

Every archive also contains `__MACOSX/._*` junk members to be skipped. No non-ASCII bytes were found in the first 5,000 lines of any of the three files. The Divvy monthly files **are** deflated (unlike Citi Bike's stored members): 32.9 MB compressed to 173 MB uncompressed for 202607.

The GBFS `station_information.json` (`https://gbfs.lyft.com/gbfs/2.3/chi/en/station_information.json`, 1,120,652 B on 2026-09-02) is the current station dimension.

# What it was used to decide
Source artifact sizes, the schema break, row-count estimates and the tier argument in [Divvy](/datasets/divvy.md).
