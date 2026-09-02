---
type: Source
title: TranStats Download_Lookup.asp lookup-table endpoints
description: The obfuscated-parameter endpoints that serve the L_AIRLINE_ID, L_AIRPORT and L_UNIQUE_CARRIERS dimension CSVs; verified by HEAD.
resource: https://www.transtats.bts.gov/Download_Lookup.asp?Y11x72=Y_haVdhR_PNeeVRef
tags: [bts, lookup, download]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.transtats.bts.gov/Download_Lookup.asp?Y11x72=Y_haVdhR_PNeeVRef
    title: Download_Lookup.asp - L_UNIQUE_CARRIERS.csv
    accessed: "2026-09-02"
---

# What was read
`curl -sI` against three `Download_Lookup.asp` endpoints on 2026-09-02. Each returned `HTTP/1.1 200 OK` with `Content-Type: application/octet-stream` and a `Content-Disposition` naming the CSV, so the endpoints are directly fetchable without a browser session.

# Relevant excerpt

| Query parameter | `Content-Disposition` filename | Content-Length |
|---|---|---:|
| `Y11x72=Y_haVdhR_PNeeVRef` | `L_UNIQUE_CARRIERS.csv` | 54,217 |
| `Y11x72=Y_NVeYVaR_VQ` | `L_AIRLINE_ID.csv` | 66,730 |
| `Y11x72=Y_NVecbeg` | `L_AIRPORT.csv` | 319,686 |

The parameter values are ROT13 of the table name (`Y_NVecbeg` -> `L_AIRPORT`), which is how further lookups (`L_AIRPORT_ID`, `L_CITY_MARKET_ID`, `L_STATE_FIPS`, `L_CANCELLATION`, `L_WEEKDAYS`, `L_MONTHS`, `L_DISTANCE_GROUP_250`, `L_DIVERSIONS`, ...) can be derived. **Inferred:** the ROT13 relationship is evident from these three samples but was not verified against a BTS statement.

# What it was used to decide
The dimension tables and foreign-key targets (`Origin`/`Dest` -> `L_AIRPORT`, `Reporting_Airline` -> `L_UNIQUE_CARRIERS`, `DOT_ID_Reporting_Airline` -> `L_AIRLINE_ID`) in [BTS On-Time Performance](/datasets/bts-ontime.md).
