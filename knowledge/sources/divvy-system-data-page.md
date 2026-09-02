---
type: Source
title: Divvy System Data page
description: The official landing page for Divvy trip data - contents, download location, processing rules and the licence link.
resource: https://divvybikes.com/system-data
tags: [divvy, download]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://divvybikes.com/system-data
    title: Divvy System Data
    accessed: "2026-09-02"
---

# What was read
The Divvy System Data page, read 2026-09-02.

# Relevant excerpt
> "Each trip is anonymized and includes: Trip start day and time, Trip end day and time, Trip start station, Trip end station, Rider type (Member, Single Ride, and Day Pass)"

> the dataset has been processed to exclude "trips that are taken by staff as they service and inspect the system; and any trips that were below 60 seconds in length (potentially false starts or users trying to re-dock a bike to ensure it was secure)."

* Download location: **`https://divvy-tripdata.s3.amazonaws.com/index.html`**
* Licence link text: **"Divvy Data License Agreement"** -> `https://www.divvybikes.com/data-license-agreement`
* Live station data: `https://gbfs.divvybikes.com/gbfs/2.3/gbfs.json`
* The page does not state the file format or the column names; those were read from the archives themselves.

Note the page's "Rider type (Member, Single Ride, and Day Pass)" description does **not** match the two-valued `member_casual` column actually present in the files.

# What it was used to decide
Source artifact and licence pointer for [Divvy](/datasets/divvy.md).
