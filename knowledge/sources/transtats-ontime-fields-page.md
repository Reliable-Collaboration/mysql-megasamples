---
type: Source
title: TranStats field descriptions for the On-Time table
description: "The per-field description page; establishes that all six clock columns are \"local time: hhmm\" and all delay columns are minutes."
resource: https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FGJ
tags: [bts, ontime, data-dictionary]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FGJ
    title: TranStats - Field Descriptions
    accessed: "2026-09-02"
---

# What was read
The TranStats field-description page for the On-Time table, read 2026-09-02.

# Relevant excerpt
* Clock columns, all "**(local time: hhmm)**": `CRSDepTime`, `DepTime`, `WheelsOff`, `WheelsOn`, `CRSArrTime`, `ArrTime`, plus the `Div*WheelsOn` / `Div*WheelsOff` columns. `FirstDepTime` is "First Gate Departure Time at Origin Airport" in the same encoding.
* `FlightDate` is documented as "**(yyyymmdd)**" (the prezipped CSV actually emits `yyyy-mm-dd` - see [the archive inspection](/sources/bts-prezip-archive-inspection.md)).
* Delay columns in minutes: `DepDelay` (negative when early), `DepDelayMinutes` ("Early departures set to 0"), `ArrDelay`, `ArrDelayMinutes` ("Early arrivals set to 0"), `CarrierDelay`, `WeatherDelay`, `NASDelay`, `SecurityDelay`, `LateAircraftDelay`, `TaxiOut`, `TaxiIn`, `CRSElapsedTime`, `ActualElapsedTime`, `AirTime`, `DivActualElapsedTime`.
* Indicator columns "(1=Yes)": `DepDel15`, `ArrDel15`, `Cancelled`, `Diverted`, `DivReachedDest`.
* Grouping columns: `DepartureDelayGroups` / `ArrivalDelayGroups` "15 minute intervals from <-15 to >180"; `DepTimeBlk` / `ArrTimeBlk` "Hourly Intervals"; `DistanceGroup` "250 Miles" intervals.
* `Reporting_Airline`: "Unique Carrier Code. When the same code has been used by multiple carriers, a numeric suffix is used for earlier users, for example, PA, PA(1), PA(2). Use this field for analysis across a range of years."

# What it was used to decide
The HHMM decoding hazard and the delay-column typing in [BTS On-Time Performance](/datasets/bts-ontime.md).
