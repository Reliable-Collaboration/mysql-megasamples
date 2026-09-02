---
type: Source
title: TLC "Working With PARQUET Format" (PDF)
description: The TLC's own note explaining that it moved raw trip data from CSV to Parquet; the note gives no switch date.
resource: https://www.nyc.gov/assets/tlc/downloads/pdf/working_parquet_format.pdf
tags:
- nyc-tlc
- parquet
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://www.nyc.gov/assets/tlc/downloads/pdf/working_parquet_format.pdf
  title: Working With Parquet Format
  accessed: "2026-09-02"
  version: 81,043 bytes, 1 page
---

# What was read
The one-page PDF (81,043 bytes), downloaded with `curl` and text-extracted locally.

# Relevant excerpt
> "TLC is switching to the Parquet file type for storing raw trip data on our website. Parquet is the industry standard for working with big data. Using Parquet format results in reduced file sizes and increased speeds. However, we have been using the CSV format for a while and the Parquet format might be new to some users."

The remainder of the page is worked examples of opening Parquet files.

# What it was used to decide
Confirms the CSV-to-Parquet migration is TLC-documented. **It does not state a date.** The widely repeated "May 2022" date could not be verified from any TLC page in this session - see [the open question](/questions/tlc-parquet-switch-date.md) and the corroborating (but indirect) `created_by` evidence in [the footer inspection](/sources/nyc-tlc-parquet-footer-inspection.md).
