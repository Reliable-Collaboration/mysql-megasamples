---
type: Source
title: Citi Bike System Data page
description: The official landing page for Citi Bike trip data - field list, download location, processing rules and the link to the data use policy.
resource: https://citibikenyc.com/system-data
tags:
- citibike
- download
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
---

# What was read
The Citi Bike System Data page, read 2026-09-02.

# Relevant excerpt
Current trip-data fields as listed on the page: Ride ID; Rideable type; Started at / Ended at; Start and end station names and IDs; Start and end latitude/longitude; Member or casual ride.

The page also documents the **previous** field set: trip duration, start/stop times, station names and IDs, bike ID, user type, gender, and year of birth.

> "This data has been processed to remove trips that are taken by staff as they service and inspect the system, trips that are taken to/from any of our 'test' stations ... and any trips that were below 60 seconds in length"

* Download location: **`https://s3.amazonaws.com/tripdata/index.html`**
* Data use policy link text: **"NYCBS Data Use Policy"**, pointing at `https://www.citibikenyc.com/data-sharing-policy`.
* Real-time data is separately available as GBFS at `https://gbfs.citibikenyc.com/gbfs/2.3/gbfs.json`.

The 60-second and staff-trip filtering means the published trip counts are **not** raw system totals, and gender/birth-year columns disappear entirely in the newer schema (a privacy change).

# What it was used to decide
Source artifact, schema history and the licence pointer for [Citi Bike](/datasets/citibike.md).
