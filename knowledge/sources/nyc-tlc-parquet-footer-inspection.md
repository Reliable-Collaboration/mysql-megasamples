---
type: Source
title: TLC Parquet footer inspection (observed schemas and row counts)
description: Thrift footers of nine TLC Parquet files read directly over HTTP range requests, giving exact row counts, physical types and the year-to-year schema drift.
resource: /sources/nyc-tlc-parquet-footer-inspection.md
tags: [nyc-tlc, parquet, schema, measurement]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet
    title: yellow_tripdata_2025-01.parquet (footer only)
    accessed: "2026-09-02"
    version: Content-Length 59158238; Last-Modified Wed, 23 Apr 2025 16:31:58 GMT; ETag 3f99a46606c0c7e76a386f81167d8e15-12
  - resource: https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-01.parquet
    title: green_tripdata_2025-01.parquet (footer only)
    accessed: "2026-09-02"
    version: Content-Length 1178451; ETag 110776612e1b020e9c4a0e41f16da597 (single-part, = MD5)
---

# What was read
The last 64 KiB of each file was fetched with an HTTP `Range` request and the Parquet Thrift `FileMetaData` footer decoded locally (no bulk data was downloaded). Accessed 2026-09-02.

# Relevant excerpt

| File | Content-Length | `num_rows` | row groups | `created_by` |
|---|---:|---:|---:|---|
| `yellow_tripdata_2015-01.parquet` | 175,325,767 | 12,741,035 | 1 | parquet-cpp-arrow 7.0.0 |
| `yellow_tripdata_2016-07.parquet` | 144,621,113 | 10,294,080 | 1 | parquet-cpp-arrow 7.0.0 |
| `yellow_tripdata_2019-01.parquet` | 110,439,634 | 7,696,617 | 1 | parquet-cpp-arrow 7.0.0 |
| `yellow_tripdata_2022-04.parquet` | 55,222,692 | 3,599,920 | 1 | parquet-cpp-arrow 7.0.0 |
| `yellow_tripdata_2022-05.parquet` | 55,558,821 | 3,588,295 | 1 | parquet-cpp-arrow **8.0.0** |
| `yellow_tripdata_2025-01.parquet` | 59,158,238 | **3,475,226** | 4 | parquet-cpp-arrow 16.1.0 |
| `yellow_tripdata_2026-05.parquet` | 69,699,174 | 4,090,836 | 4 | parquet-cpp-arrow 16.1.0 |
| `green_tripdata_2025-01.parquet` | 1,178,451 | **48,326** | 1 | parquet-cpp-arrow 16.1.0 |
| `green_tripdata_2026-05.parquet` | 1,102,947 | 44,921 | 1 | parquet-cpp-arrow 16.1.0 |
| `fhvhv_tripdata_2026-05.parquet` | 537,576,484 | 22,125,744 | 22 | parquet-cpp-arrow 16.1.0 |

**Yellow, 2025-01 and 2026-05 (identical schemas), physical types:**
`VendorID` INT32; `tpep_pickup_datetime`, `tpep_dropoff_datetime` INT64 TIMESTAMP_MICROS (`isAdjustedToUTC=false`, i.e. local wall-clock); `passenger_count` INT64; `trip_distance` DOUBLE; `RatecodeID` INT64; `store_and_fwd_flag` BYTE_ARRAY/UTF8; `PULocationID` INT32; `DOLocationID` INT32; `payment_type` INT64; `fare_amount`, `extra`, `mta_tax`, `tip_amount`, `tolls_amount`, `improvement_surcharge`, `total_amount`, `congestion_surcharge`, **`Airport_fee`**, **`cbd_congestion_fee`** all DOUBLE. All columns OPTIONAL (nullable). 20 data columns.

**Green, 2025-01 and 2026-05:** `VendorID` INT32, `lpep_pickup_datetime`, `lpep_dropoff_datetime` INT64 TIMESTAMP_MICROS, `store_and_fwd_flag`, `RatecodeID` INT64, `PULocationID` INT32, `DOLocationID` INT32, `passenger_count` INT64, `trip_distance`, `fare_amount`, `extra`, `mta_tax`, `tip_amount`, `tolls_amount`, **`ehail_fee`**, `improvement_surcharge`, `total_amount`, `payment_type` INT64, **`trip_type`** INT64, `congestion_surcharge`, `cbd_congestion_fee`. 21 data columns; **column order differs from yellow** and there is no `Airport_fee`.

**HVFHV, 2026-05:** `hvfhs_license_num`, `dispatching_base_num`, `originating_base_num` (UTF8); `request_datetime`, `on_scene_datetime`, `pickup_datetime`, `dropoff_datetime` (TIMESTAMP_MICROS); `PULocationID`, `DOLocationID` INT32; `trip_miles` DOUBLE; `trip_time` INT64; `base_passenger_fare`, `tolls`, `bcf`, `sales_tax`, `congestion_surcharge`, `airport_fee` (lower case), `tips`, `driver_pay` DOUBLE; `shared_request_flag`, `shared_match_flag`, `access_a_ride_flag`, `wav_request_flag`, `wav_match_flag` UTF8; `cbd_congestion_fee` DOUBLE. 24 columns.

**Observed schema drift across yellow files (the load-bearing finding):**
1. `VendorID`, `PULocationID`, `DOLocationID`: **INT64 in 2015-2022 files, INT32 in 2025+ files.**
2. `passenger_count` and `RatecodeID`: **INT64 in 2015-2016, DOUBLE in 2019-2022, INT64 again in 2025+.**
3. The airport column is named **`airport_fee`** (lower case) in every pre-2025 file and **`Airport_fee`** (capital A) in the 2025 and 2026 files.
4. In `yellow_tripdata_2015-01` and `2016-07`, `congestion_surcharge` and `airport_fee` are physical INT32 carrying logical type **UNKNOWN (Null)** - the columns exist but are entirely null placeholders back-filled when the archive was rewritten. `yellow_tripdata_2019-01` has `congestion_surcharge` DOUBLE but `airport_fee` still INT32/Null.
5. `cbd_congestion_fee` exists only from 2025-01 onward.
6. `created_by` is 7.0.0 for every file through 2022-04 and 8.0.0 for 2022-05, then 16.1.0 for the recent files: the whole archive was rewritten with Arrow 7 at one point, and 2022-05 is the first month written by a newer build. This is **indirect** support for the widely cited "TLC switched to Parquet in May 2022" claim, which no TLC page in this session stated outright.
7. All timestamps are `isAdjustedToUTC=false` - they are New York local wall-clock times, so DST-ambiguous instants exist; do not tag them UTC.

`yellow_tripdata_2025-01.parquet` carries `Last-Modified: Wed, 23 Apr 2025 16:31:58 GMT` - three months after publication - so TLC **re-uploads** historical files. Pin a sha256 at fetch time.

# What it was used to decide
The whole `# Shape`, `# Type-mapping hazards` and `# Tier assignment` sections of [NYC TLC trip records](/datasets/nyc-tlc.md).
