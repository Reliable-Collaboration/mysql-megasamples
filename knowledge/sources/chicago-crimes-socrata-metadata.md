---
type: Source
title: Chicago "Crimes - 2001 to Present" - portal metadata and SODA measurements
description: The dataset's Socrata metadata, live row count, per-column null counts, export header and date format, read directly from the portal API.
resource: https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2
tags: [chicago, socrata, measurement]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://data.cityofchicago.org/api/views/ijzp-q8t2.json
    title: Socrata view metadata for ijzp-q8t2
    accessed: "2026-09-02"
    version: rowsUpdatedAt 1788349026 = 2026-09-02; X-SODA2-Truth-Last-Modified Wed, 02 Sep 2026 11:37:15 GMT
  - resource: https://data.cityofchicago.org/resource/ijzp-q8t2.json
    title: SODA 2.1 endpoint (count, group-by-year, distinct case_number)
    accessed: "2026-09-02"
  - resource: https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD
    title: CSV export (headers and first ~3 MB)
    accessed: "2026-09-02"
stale_after: "2026-12-01"
---

# What was read
The dataset landing page is a JavaScript app, so the metadata was read from the Socrata view API and the SODA 2.1 endpoint, and the CSV export's first 3,000,000 bytes were streamed with `curl`. All on 2026-09-02. (WebFetch on the HTML landing page returned only the portal chrome.)

# Relevant excerpt

**Description (verbatim, abridged):**
> "This dataset reflects reported incidents of crime (with the exception of murders where data exists for each victim) that occurred in the City of Chicago from 2001 to present, **minus the most recent seven days**. Data is extracted from the Chicago Police Department's CLEAR (Citizen Law Enforcement Analysis and Reporting) system. In order to protect the privacy of crime victims, addresses are shown at the block level only and specific locations are not identified. ... Disclaimer: These crimes may be based upon preliminary information supplied to the Police Department by the reporting parties that have not been verified. ... the Chicago Police Department does not guarantee (either expressed or implied) the accuracy, completeness, timeliness, or correct sequencing of the information and the information should not be used for comparison purposes over time. ... All data visualizations on maps should be considered approximate and attempts to derive specific addresses are strictly prohibited."

**Metadata:** `attribution: Chicago Police Department`; `attributionLink: https://www.chicagopolice.org/data-statistics/`; **`license: {"name": "See Terms of Use"}`** - i.e. the portal declares no SPDX-style licence, only the City terms.

**Live counts on 2026-09-02:** `SELECT count(*)` = **8,627,693**. `count(distinct case_number)` = **8,627,064**, so `Case Number` is **not** unique (629 fewer distinct values); example repeated values: `G023235`, `G083440`, `G137655`, `G183906`, `G219399`, each with 2 rows. `id` is documented as "Unique identifier for the record." and its cached cardinality equals the row count.

**Rows per year (recent):** 2026 149,408 (partial); 2025 237,695; **2024 259,267**; 2023 263,449; 2022 240,156; 2021 209,747; 2020 212,793; 2019 261,742; 2018 269,189; 2017 269,323; 2016 269,999; 2015 264,909.

**Null counts (from cached column stats, out of 8,627,693):** `ward` 614,812; `community_area` 613,723; `x_coordinate` / `y_coordinate` / `latitude` / `longitude` 98,693 each; `location_description` 16,587; `district` 47; everything else 0.

**SODA field names and types** (from the `X-SODA2-Fields` / `X-SODA2-Types` response headers): `id` number, `case_number` text, `date` floating_timestamp, `block` text, `iucr` text, `primary_type` text, `description` text, `location_description` text, `arrest` boolean, `domestic` boolean, `beat` text, `district` text, `ward` number, `community_area` text, `fbi_code` text, `x_coordinate` number, `y_coordinate` number, `year` number, `updated_on` floating_timestamp, `latitude` number, `longitude` number, `location` location.

**CSV export header (verbatim, 22 columns):**
`ID,Case Number,Date,Block,IUCR,Primary Type,Description,Location Description,Arrest,Domestic,Beat,District,Ward,Community Area,FBI Code,X Coordinate,Y Coordinate,Year,Updated On,Latitude,Longitude,Location`

**Export encoding facts:**
* `Content-Type: text/csv; charset=utf-8`, `Content-disposition: attachment; filename=Crimes_-_2001_to_Present.csv`, **`Content-Length: 0`** (chunked stream - the size is not advertised).
* Dates in the export are **`MM/DD/YYYY hh:mm:ss AM`** (e.g. `07/29/2022 03:39:00 AM`, `04/18/2024 03:40:59 PM`); the SODA API instead returns ISO-8601 floating timestamps (`2001-01-01T10:40:00.000`).
* `Arrest` / `Domestic` are the literals `true` / `false`.
* `Beat` and `District` carry **leading zeros** (`0733`, `007`) and `IUCR` / `FBI Code` too (`0110`, `01A`) - all must be strings.
* `Location` is `(41.76261474, -87.652840463)`, i.e. a parenthesised pair duplicating Latitude/Longitude; it is empty whenever the coordinates are null.
* In the **SODA CSV** output (not the export) the `location` column contains **embedded newlines**; the export form does not.
* **No byte above 0x7F** in the 15,672 sampled export rows: the export is ASCII in practice.
* Sampled average row length **191.4 bytes**, giving an estimated full export of **~1.65 GB** for 8,627,693 rows (**inferred**).
* Export rows are **not** ordered by `ID`.

The view also carries eight `:@computed_region_*` columns (spatial joins added by the portal); they are absent from the `rows.csv` export.

# What it was used to decide
Row-count baseline, primary key, column typing, date parsing and tier for [Chicago crimes](/datasets/chicago-crimes.md).
