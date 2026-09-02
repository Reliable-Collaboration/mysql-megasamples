---
type: Source
title: BTS PREZIP archive inspection (URL pattern, members, header, sample rows)
description: Direct HTTP inspection of the prezipped On-Time monthly archives - the URL pattern works without a browser session, and the enclosed CSV's exact header and value encodings were read.
resource: https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2025_1.zip
tags: [bts, ontime, download, measurement]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2025_1.zip
    title: Prezipped On-Time monthly archive, 2025-01 (headers, central directory, readme.html, first ~380 KB of the CSV member)
    accessed: 2026-09-02
    version: Content-Length 27108664; Last-Modified Thu, 08 May 2025 14:59:27 GMT
stale_after: 2027-03-01
---

# What was read
`curl -sI` on three prezip URLs, then HTTP `Range` reads of the ZIP central directory, of the whole embedded `readme.html`, and of the first ~380 KB of the CSV member (inflated locally). Accessed 2026-09-02. No full dataset was downloaded.

# Relevant excerpt

**The URL pattern works with a plain `curl` - no cookies, no form post, no browser session:**
`https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_<YYYY>_<M>.zip`
with the month **not** zero-padded and the parentheses of the table name **removed** from the URL.

| URL month | HTTP | Content-Length | Last-Modified |
|---|---|---:|---|
| `..._2025_1.zip` | 200 | 27,108,664 | Thu, 08 May 2025 14:59:27 GMT |
| `..._2026_5.zip` | 200 | 31,716,693 | Tue, 30 Jun 2026 18:02:30 GMT |
| `..._2026_6.zip` | 200 | 31,606,062 | Wed, 12 Aug 2026 12:15:44 GMT |
| `..._(1987_present)_2025_1.zip` (parens kept) | **404** | - | - |

**Archive members (2025-01):**
* `On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2025_1.csv` - deflate, compressed 27,105,978, **uncompressed 243,177,378 bytes**. Note the member name *does* contain parentheses even though the URL must not.
* `readme.html` - deflate, uncompressed 12,152 bytes.

**readme.html** contains the record layout in file order and states: "The data contained in the compressed file has been extracted from the Reporting Carrier On-Time Performance (1987-present) data table of the 'On-Time' database from the TranStats data library. The time period is indicated in the name of the compressed file; for example, XXX_XXXXX_2001_1 contains data of the first month of the year 2001." It documents `FlightDate` as "Flight Date (yyyymmdd)" and all six clock columns as "(local time: hhmm)". It also notes: "DivActualElapsedTime ... The ActualElapsedTime column remains NULL for all diverted flights" and "DivArrDelay ... The ArrDelay column remains NULL for all diverted flights."

**CSV header (verbatim, 2025-01)** - 109 quoted names, then a **trailing comma**, so a naive split yields 110 fields with an unnamed empty last one:
`"Year","Quarter","Month","DayofMonth","DayOfWeek","FlightDate","Reporting_Airline","DOT_ID_Reporting_Airline","IATA_CODE_Reporting_Airline","Tail_Number","Flight_Number_Reporting_Airline","OriginAirportID","OriginAirportSeqID","OriginCityMarketID","Origin","OriginCityName","OriginState","OriginStateFips","OriginStateName","OriginWac","DestAirportID","DestAirportSeqID","DestCityMarketID","Dest","DestCityName","DestState","DestStateFips","DestStateName","DestWac","CRSDepTime","DepTime","DepDelay","DepDelayMinutes","DepDel15","DepartureDelayGroups","DepTimeBlk","TaxiOut","WheelsOff","WheelsOn","TaxiIn","CRSArrTime","ArrTime","ArrDelay","ArrDelayMinutes","ArrDel15","ArrivalDelayGroups","ArrTimeBlk","Cancelled","CancellationCode","Diverted","CRSElapsedTime","ActualElapsedTime","AirTime","Flights","Distance","DistanceGroup","CarrierDelay","WeatherDelay","NASDelay","SecurityDelay","LateAircraftDelay","FirstDepTime","TotalAddGTime","LongestAddGTime","DivAirportLandings","DivReachedDest","DivActualElapsedTime","DivArrDelay","DivDistance","Div1Airport","Div1AirportID","Div1AirportSeqID","Div1WheelsOn","Div1TotalGTime","Div1LongestGTime","Div1WheelsOff","Div1TailNum",` ... repeating the seven-column `Div2..Div5` blocks ... `"Div5TailNum",`

**First data row (verbatim):**
`2025,1,1,1,3,2025-01-01,"AA",19805,"AA","N104NN","1",12478,1247805,31703,"JFK","New York, NY","NY","36","New York",22,12892,1289208,32575,"LAX","Los Angeles, CA","CA","06","California",91,"0659","0656",-3.00,0.00,0.00,-1,"0600-0659",23.00,"0719","1004",9.00,"1020","1013",-7.00,0.00,0.00,-1,"1000-1059",0.00,"",0.00,381.00,377.00,345.00,1.00,2475.00,10,,,,,,"",,,0,,,,,"",,,"",,,"","","",,,...`

**Encoding facts observed in the data (all load-bearing):**
1. `FlightDate` is emitted as **`2025-01-01`**, not the `yyyymmdd` the readme claims.
2. Clock columns are **quoted, zero-padded four-character strings**: `"0659"`, `"0053"`, `"0055"`. Read as integers they silently become 659 and 53. `DepTime` value **`"2400"`** occurs in the sample (1 occurrence in ~10,000 rows) and is not a valid `TIME`.
3. Integral quantities are written as decimals: `Cancelled` = `0.00`, `Diverted` = `0.00`, `DepDel15` = `0.00`, `Distance` = `2475.00`, `Flights` = `1.00`, `DepartureDelayGroups` = `-1`.
4. `OriginStateFips` / `DestStateFips` are **quoted strings with leading zeros** (`"36"`, `"06"`); `Flight_Number_Reporting_Airline` is also quoted (`"1"`).
5. `CancellationCode` is `""` (empty quoted string) when absent, while numeric nulls are bare empty fields - two distinct null spellings on the same row.
6. Every data line ends with a trailing comma, matching the header.
7. `OriginCityName` contains an embedded comma inside quotes (`"New York, NY"`) - a naive comma split is wrong.
8. No byte above 0x7F was found in ~10,000 sampled rows: the file is ASCII.

**Row count estimate:** the sample of 10,181 rows averaged **453.3 bytes/row**, giving **~536,000 rows** for 2025-01 (243,177,378 / 453.3). **Inferred**, not published; the executor should record the exact `COUNT(*)` after load.

# What it was used to decide
Source artifact, downloader design, type-mapping hazards and the row-count baseline method in [BTS On-Time Performance](/datasets/bts-ontime.md).
