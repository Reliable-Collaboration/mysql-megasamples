---
type: Source
title: TLC Yellow Taxi Trip Records data dictionary (PDF)
description: Field-by-field definitions for the yellow taxi Parquet files, including the 2025 cbd_congestion_fee column and the code lists for VendorID, RatecodeID and payment_type.
resource: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
tags: [nyc-tlc, data-dictionary]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
    title: Data Dictionary - Yellow Taxi Trip Records
    accessed: "2026-09-02"
    version: document date "March 18, 2025"; 148,556 bytes; Last-Modified Tue, 21 Jul 2026 16:38:17 GMT
---

# What was read
The one-page PDF, downloaded with `curl` (148,556 bytes, `Content-Type: application/pdf`) and text-extracted locally. Document date printed on the page: **March 18, 2025**.

# Relevant excerpt
Field list in document order, with the definitions verbatim (abbreviated):

* `VendorID` - "A code indicating the TPEP provider that provided the record." 1 = Creative Mobile Technologies, LLC; 2 = Curb Mobility, LLC; 6 = Myle Technologies Inc; 7 = Helix.
* `tpep_pickup_datetime` / `tpep_dropoff_datetime` - "The date and time when the meter was engaged / disengaged."
* `passenger_count` - "The number of passengers in the vehicle." (driver-entered)
* `trip_distance` - "The elapsed trip distance in miles reported by the taximeter."
* `RatecodeID` - 1 = Standard rate, 2 = JFK, 3 = Newark, 4 = Nassau or Westchester, 5 = Negotiated fare, 6 = Group ride, **99 = Null/unknown**.
* `store_and_fwd_flag` - Y = store and forward trip, N = not a store and forward trip.
* `PULocationID` / `DOLocationID` - "TLC Taxi Zone in which the taximeter was engaged / disengaged."
* `payment_type` - **0 = Flex Fare trip**, 1 = Credit card, 2 = Cash, 3 = No charge, 4 = Dispute, 5 = Unknown, 6 = Voided trip.
* `fare_amount`, `extra`, `mta_tax`, `tip_amount` ("This field is automatically populated for credit card tips. Cash tips are not included."), `tolls_amount`, `improvement_surcharge` ("began being levied in 2015"), `total_amount` ("Does not include cash tips."), `congestion_surcharge`.
* `airport_fee` - "For pick up only at LaGuardia and John F. Kennedy Airports."
* `cbd_congestion_fee` - "Per-trip charge for MTA's Congestion Relief Zone starting Jan. 5, 2025."

Note the dictionary spells the airport column **`airport_fee`** (lower case) while the 2025+ Parquet files name it **`Airport_fee`** - see [the footer inspection](/sources/nyc-tlc-parquet-footer-inspection.md).

# What it was used to decide
Column semantics, enumerations and the lookup-table joins in [NYC TLC trip records](/datasets/nyc-tlc.md).
