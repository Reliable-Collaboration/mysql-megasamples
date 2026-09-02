---
type: Open Question
title: When exactly did the TLC switch trip records from CSV to Parquet?
description: The "May 2022" date repeated everywhere was not stated on any TLC page read in this session; only indirect evidence supports it.
resource: /questions/tlc-parquet-switch-date.md
tags: [nyc-tlc, provenance]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.nyc.gov/assets/tlc/downloads/pdf/working_parquet_format.pdf
    title: Working With Parquet Format (states the switch, gives no date)
    accessed: 2026-09-02
  - resource: /sources/nyc-tlc-parquet-footer-inspection.md
    title: created_by values across the archive
    accessed: 2026-09-02
---

# The question
The TLC's "Working With PARQUET Format" PDF says "TLC is switching to the Parquet file type for storing raw trip data on our website" but gives **no date**, and the trip-record page gives none either. The commonly cited date is May 2022 (with a simultaneous rewrite of the whole historical archive from CSV to Parquet), but no TLC-published statement of that was found in this session.

# Indirect evidence collected
Parquet footer `created_by` strings: every yellow file inspected from 2015-01 through **2022-04** was written by `parquet-cpp-arrow version 7.0.0`, **2022-05** by `version 8.0.0`, and the 2025/2026 files by `version 16.1.0`. That pattern is consistent with a one-off bulk conversion of everything up to 2022-04 followed by native Parquet publication from 2022-05 onward - i.e. it corroborates "May 2022" without proving it.

Why it matters: it is the boundary before which no CSV original is available from TLC, and it explains why pre-2016 files carry `PULocationID`/`DOLocationID` (assigned during the rewrite) rather than the original pickup/dropoff latitude and longitude columns that the CSV-era files had. **That coordinate-to-zone change is a separate fact and is also unverified from a TLC page** - the 2015-01 Parquet inspected here already has location IDs and no coordinate columns, which is itself evidence that the rewrite normalised old data to the modern layout.

# Cheapest experiment that resolves it
Fetch `https://web.archive.org/web/2022*/https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page` and read the April and June 2022 captures: the file extension on the download links changes from `.csv` to `.parquet` between them, dating the switch to the month. One or two WebFetch calls, no downloads.

# Impact if unresolved
Cosmetic. The dataset record simply states what the footers show and marks the May 2022 date **Inferred:**.
