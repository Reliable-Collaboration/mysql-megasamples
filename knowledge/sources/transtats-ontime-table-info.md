---
type: Source
title: TranStats table profile - Reporting Carrier On-Time Performance
description: The table-info page giving the field count (109), the total record count and the definition of an on-time arrival.
resource: https://www.transtats.bts.gov/TableInfo.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr&V0s1_b0yB=D
tags:
- bts
- ontime
- metadata
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://www.transtats.bts.gov/TableInfo.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr&V0s1_b0yB=D
  title: TranStats - Table Information
  accessed: "2026-09-02"
  version: snapshot 2026-09-02
stale_after: "2027-03-01"
---

# What was read
The TranStats table profile page for the On-Time Reporting Carrier table, read 2026-09-02.

# Relevant excerpt
> "Reporting carriers are required to (or voluntarily) report on-time data for flights they operate: on-time arrival and departure data for non-stop domestic flights by month and year, by carrier and by origin and destination airport."

* **Total records: 234,378,386** (whole table, 1987 through 2026).
* **Fields: 109.** Frequency: monthly. Coverage 1987-2026. Latest available data: **June 2026**.
* Source agency: U.S. Department of Transportation, Bureau of Transportation Statistics.
* A flight is on time when "it arrives less than 15 minutes after its published arrival time"; arrival delay is "the difference of the actual arrival time minus the scheduled arrival time"; departure delay is "the difference between the scheduled departure time and the actual departure time from the origin airport gate."

The 109-field count matches the 109 named columns observed in the actual prezipped CSV.

# What it was used to decide
Column count, table semantics and the whole-table row count in [BTS On-Time Performance](/datasets/bts-ontime.md).
