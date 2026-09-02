---
type: Source
title: TLC High Volume FHV Trip Records data dictionary (PDF)
description: Field definitions for the HVFHV (Uber/Lyft/Via/Juno) Parquet files, including the licence-number code list and the driver-pay columns.
resource: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_hvfhs.pdf
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
- resource: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_hvfhs.pdf
  title: Data Dictionary - High Volume FHV Trip Records
  accessed: "2026-09-02"
  version: document date "March 18, 2025"; 117,347 bytes
---

# What was read
The one-page PDF (117,347 bytes), downloaded with `curl` and text-extracted locally. Document date: **March 18, 2025**.

# Relevant excerpt
> "On August 14, 2018, Mayor de Blasio signed Local Law 149 of 2018, creating a new license category for TLC-licensed FHV businesses that currently dispatch or plan to dispatch more than 10,000 FHV trips in New York City per day under a single brand, trade, or operating name, referred to as High-Volume For-Hire Services (HVFHS). This law went into effect on Feb 1, 2019."

* `hvfhs_license_num` - "HV0002: Juno, HV0003: Uber, HV0004: Via, HV0005: Lyft" (as of September 2019).
* `dispatching_base_num`, `originating_base_num`, `request_datetime`, `on_scene_datetime` ("Accessible Vehicles-only"), `pickup_datetime`, `dropoff_datetime`, `PULocationID`, `DOLocationID`.
* `trip_miles`, `trip_time` ("Total time in seconds for passenger trip"), `base_passenger_fare`, `tolls`, `bcf` (Black Car Fund), `sales_tax`, `congestion_surcharge`, `airport_fee` ("$2.50 for both drop off and pick up at LaGuardia, Newark, and John F. Kennedy airports"), `tips`, `driver_pay`.
* Y/N flags: `shared_request_flag`, `shared_match_flag`, `access_a_ride_flag`, `wav_request_flag`, `wav_match_flag`.
* `cbd_congestion_fee` - "Per-trip charge for MTA's Congestion Relief Zone starting Jan. 5, 2025."

# What it was used to decide
The HVFHV variant description and the "why HVFHV is out of scope for the image" size argument in [NYC TLC trip records](/datasets/nyc-tlc.md).
