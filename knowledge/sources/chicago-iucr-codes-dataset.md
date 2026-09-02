---
type: Source
title: Chicago IUCR code lookup dataset (c7ck-438e)
description: The 434-row IUCR dimension table that the crimes dataset's IUCR column references.
resource: https://data.cityofchicago.org/Public-Safety/Chicago-Police-Department-Illinois-Uniform-Crime-R/c7ck-438e
tags:
- chicago
- lookup
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://data.cityofchicago.org/api/views/c7ck-438e.json
  title: Socrata view metadata for c7ck-438e
  accessed: "2026-09-02"
- resource: https://data.cityofchicago.org/resource/c7ck-438e.csv
  title: SODA endpoint for the IUCR codes
  accessed: "2026-09-02"
---

# What was read
The Socrata view metadata and the first rows of the SODA CSV for `c7ck-438e`, plus a `count(*)`, on 2026-09-02.

# Relevant excerpt
> "Illinois Uniform Crime Reporting (IUCR) codes are four digit codes that law enforcement agencies use to classify criminal incidents when taking individual reports. These codes are also used to aggregate types of cases for statistical purposes. In Illinois, the Illinois State Police establish IUCR codes, but the agencies can add codes to suit their individual needs."

* `count(*)` = **434 rows**. Attribution: `Chicago Police Department`. License: `See Terms of Use`.
* Columns: `iucr` text, `primary_description` text, `secondary_description` text, `index_code` text, `active` checkbox.
* First rows: `"0110","HOMICIDE","FIRST DEGREE MURDER","I","true"` / `"0130","HOMICIDE","SECOND DEGREE MURDER","I","true"` / `"0141","HOMICIDE","INVOLUNTARY MANSLAUGHTER","N","true"`.
* `iucr` carries leading zeros and must be a string; it joins to the crimes table's `IUCR` column, whose per-row `Primary Type`/`Description` are denormalised copies of `primary_description`/`secondary_description`.

Bulk CSV export URL for the same dataset: `https://data.cityofchicago.org/api/views/c7ck-438e/rows.csv?accessType=DOWNLOAD`.

The other referenced lookups are **geospatial**, not tabular: `cauq-8yn6` (Boundaries - Community Areas - Map), `aerh-rz74` (Boundaries - Police Beats (current)), `fthy-xz3r` (Boundaries - Police Districts (current)), `sp34-6z76` (Wards). Their view metadata returns **no tabular columns** ("special GIS software, such as ESRI ArcGIS (shapefile) or Google Earth (KML or KMZ), is required").

# What it was used to decide
The `iucr` dimension table and the decision to skip the boundary datasets in [Chicago crimes](/datasets/chicago-crimes.md).
