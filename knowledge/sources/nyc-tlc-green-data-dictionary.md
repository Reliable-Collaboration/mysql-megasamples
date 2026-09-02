---
type: Source
title: TLC Green Taxi (LPEP) Trip Records data dictionary (PDF)
description: Field definitions for the green/SHL taxi Parquet files, which add ehail_fee and trip_type to the yellow layout.
resource: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf
tags:
- nyc-tlc
- data-dictionary
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf
  title: Data Dictionary - LPEP Trip Records
  accessed: "2026-09-02"
  version: document date "March 18, 2025"; 148,750 bytes; 2 pages
---

# What was read
The two-page PDF (148,750 bytes), downloaded with `curl` and text-extracted locally. Header: "Data Dictionary - LPEP Trip Records", dated **March 18, 2025**.

# Relevant excerpt
> "This data dictionary describes SHL trip data."

* `VendorID` - "A code indicating the LPEP provider that provided the record." 1 = Creative Mobile Technologies, LLC; 2 = Curb Mobility, LLC; **6 = Myle Technologies Inc** (the green list has no `7 = Helix`, unlike yellow).
* `lpep_pickup_datetime` / `lpep_dropoff_datetime` - the green analogues of the `tpep_*` columns; **the datetime column names differ from yellow**.
* `store_and_fwd_flag`, `RatecodeID` (1 = Standard rate, 2 = JFK, 3 = ...) as per yellow.

The extraction of page 2 was incomplete for the tail of the field table; the authoritative green column list used in this bundle is the Parquet footer read in [the footer inspection](/sources/nyc-tlc-parquet-footer-inspection.md), which adds `ehail_fee` and `trip_type` relative to yellow and omits `Airport_fee`.

# What it was used to decide
Green taxi column semantics and the yellow/green schema difference in [NYC TLC trip records](/datasets/nyc-tlc.md).
