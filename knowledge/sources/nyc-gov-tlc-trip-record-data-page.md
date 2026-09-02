---
type: Source
title: NYC TLC Trip Record Data page
description: The TLC's canonical download and metadata page for yellow, green, FHV and HVFHV trip records; source of the Parquet URL pattern, publication cadence and disclaimer.
resource: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
tags: [nyc-tlc, download, parquet]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
    title: TLC Trip Record Data
    accessed: 2026-09-02
    version: page snapshot 2026-09-02; latest month linked = May 2026
stale_after: 2026-12-01
---

# What was read
The full HTML of the TLC Trip Record Data page, fetched with `curl` on 2026-09-02 (142,294 bytes). Every monthly download link on the page points at the CloudFront origin `https://d37ci6vzurychx.cloudfront.net/trip-data/<type>_tripdata_YYYY-MM.parquet`; the metadata links point at `https://www.nyc.gov/assets/tlc/downloads/pdf/...` and `https://d37ci6vzurychx.cloudfront.net/misc/...`.

# Relevant excerpt
> "Yellow and green taxi trip records include fields capturing pickup and drop-off dates/times, pickup and drop-off locations, trip distances, itemized fares, rate types, payment types, and driver-reported passenger counts. The data used in the attached datasets were collected and provided to the NYC Taxi and Limousine Commission (TLC) by technology providers authorized under the Taxicab & Livery Passenger Enhancement Programs (TPEP/LPEP). **The trip data was not created by the TLC, and TLC makes no representations as to the accuracy of these data.**"

> "For 2025 data onwards, a cbd_congestion_fee column has been added to the Yellow, Green, and High Volume FHV datasets to reflect new congestion pricing charges."

> "Trip data is published monthly on this website, typically with a two-month delay to allow time for full vendor submissions. Due to the size of the datasets, the trip record files have been stored in the PARQUET format. ... **Please be advised that there may be minor changes in the near future to standardize the parquet schema across all years and datasets.** If you would like to view the data on NYC Open Data, and export the data in various other formats, you may view the collection"

Metadata links present on the page: Trip Record User Guide, Yellow Trips Data Dictionary, Green Trips Data Dictionary, High Volume FHV Trips Data Dictionary, Working With PARQUET Format, Taxi Zone Lookup Table (CSV), Taxi Zone Shapefile, and five borough taxi zone maps (JPG). The FHV dictionary PDF is also present in the page's link list (`data_dictionary_trip_records_fhv.pdf`) although it is not given a visible label in the metadata block.

The page carries **no licence statement and no terms-of-use link of its own**; the only rights-adjacent text is the accuracy disclaimer quoted above.

Latest months linked: 2026 group ends at **May 2026** for Yellow, Green and High Volume FHV. A `curl -sI` for `yellow_tripdata_2026-06.parquet` returned **HTTP 403** (object absent), confirming May 2026 is the newest published month on 2026-09-02.

# What it was used to decide
[NYC TLC trip records](/datasets/nyc-tlc.md) source artifact, URL pattern, cadence, schema-drift warning and tier; [NYC Open Data terms](/licenses/nyc-open-data-terms.md).
