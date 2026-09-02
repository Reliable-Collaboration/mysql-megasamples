---
type: Source
title: TLC Taxi Zone Lookup Table (CSV)
description: The 265-row zone dimension table that PULocationID/DOLocationID reference; downloaded and counted.
resource: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
tags: [nyc-tlc, lookup]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
    title: taxi_zone_lookup.csv
    accessed: 2026-09-02
    version: Content-Length 12331; Last-Modified Thu, 22 Feb 2024 21:33:00 GMT; ETag c6064b7c144c716450641f769659d178
---

# What was read
The whole 12,331-byte CSV, downloaded with `curl` on 2026-09-02 and inspected with `wc`, `head`, `tail`, `cut` and a non-ASCII grep. Because the object was uploaded in a single part, its **ETag is the MD5**: `c6064b7c144c716450641f769659d178`.

# Relevant excerpt
Header: `"LocationID","Borough","Zone","service_zone"`

* 266 lines = header + **265 data rows**; `LocationID` runs 1..265 with no gaps.
* First rows: `1,"EWR","Newark Airport","EWR"` / `2,"Queens","Jamaica Bay","Boro Zone"` / `3,"Bronx","Allerton/Pelham Gardens","Boro Zone"`.
* Last rows: `263,"Manhattan","Yorkville West","Yellow Zone"` / `264,"Unknown","N/A","N/A"` / `265,"N/A","Outside of NYC","N/A"`.
* Distinct `Borough` values: Bronx, Brooklyn, EWR, Manhattan, N/A, Queens, Staten Island, Unknown.
* `file` reports **"CSV ASCII text"**; a `grep` for bytes above 0x7F found none. Note that `Zone` values contain `/` and `(` `)` but no non-ASCII characters.
* The sentinel rows 264 ("Unknown") and 265 ("Outside of NYC") mean a strict FK from trip rows to zones does hold for in-range IDs; trip files also contain `PULocationID` values of 264/265.

The companion shapefile `https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip` returned `Content-Length: 1022574`, `Last-Modified: Thu, 19 Feb 2026 17:12:14 GMT`.

# What it was used to decide
The `taxi_zone` dimension table, its exact row count baseline (265) and the FK design in [NYC TLC trip records](/datasets/nyc-tlc.md).
