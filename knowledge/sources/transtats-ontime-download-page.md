---
type: Source
title: TranStats "Reporting Carrier On-Time Performance" download page
description: The BTS field-selection download form; source of the full field list, the prezipped-file option and the lookup-table links.
resource: https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr
tags:
- bts
- ontime
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
- resource: https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr
  title: TranStats - Download - Reporting Carrier On-Time Performance (1987-present)
  accessed: "2026-09-02"
  version: page snapshot 2026-09-02; latest available data June 2026
stale_after: "2027-03-01"
---

# What was read
The TranStats download form for the "Reporting Carrier On-Time Performance (1987-present)" table, read 2026-09-02.

# Relevant excerpt
* **Latest available data: June 2026.**
* The form offers a **"Prezipped File"** checkbox (a `displayHelp(...,'DownloadZip')` control). The page does not print the resulting URL; that pattern was established separately - see [the prezip archive inspection](/sources/bts-prezip-archive-inspection.md).
* Field groups as printed on the form: time period (`Year`, `Quarter`, `Month`, `DayofMonth`, `DayOfWeek`, `FlightDate`); airline (`Reporting_Airline`, `DOT_ID_Reporting_Airline`, `IATA_CODE_Reporting_Airline`, `Tail_Number`, `Flight_Number_Reporting_Airline`); origin (`OriginAirportID`, `OriginAirportSeqID`, `OriginCityMarketID`, `Origin`, `OriginCityName`, `OriginState`, `OriginStateFips`, `OriginStateName`, `OriginWac`); destination (the nine matching `Dest*` fields); departure performance (`CRSDepTime`, `DepTime`, `DepDelay`, `DepDelayMinutes`, `DepDel15`, `DepartureDelayGroups`, `DepTimeBlk`, `TaxiOut`, `WheelsOff`); arrival performance (`WheelsOn`, `TaxiIn`, `CRSArrTime`, `ArrTime`, `ArrDelay`, `ArrDelayMinutes`, `ArrDel15`, `ArrivalDelayGroups`, `ArrTimeBlk`); cancellations and diversions (`Cancelled`, `CancellationCode`, `Diverted`); flight summaries (`CRSElapsedTime`, `ActualElapsedTime`, `AirTime`, `Flights`, `Distance`, `DistanceGroup`); **cause of delay (from 6/2003)**: `CarrierDelay`, `WeatherDelay`, `NASDelay`, `SecurityDelay`, `LateAircraftDelay`; **gate return information (from 10/2008)**: `FirstDepTime`, `TotalAddGTime`, `LongestAddGTime`; **diverted airport information (from 10/2008)**: `DivAirportLandings`, `DivReachedDest`, `DivActualElapsedTime`, `DivArrDelay`, `DivDistance` and the `Div1..Div5` blocks.
* Coded fields link to lookup tables through `Download_Lookup.asp` with obfuscated parameters (e.g. `Y11x72=Y_haVdhR_PNeeVRef`, `Y11x72=Y_NVeYVaR_VQ`).
* **No terms-of-use or data-policy text appears on this page.**

The "from 6/2003" and "from 10/2008" annotations are the reason those columns are entirely empty in older months.

# What it was used to decide
Column inventory and the "columns exist but are null before their start date" hazard in [BTS On-Time Performance](/datasets/bts-ontime.md).
