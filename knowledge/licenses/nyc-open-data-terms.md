---
type: License
title: NYC Open Data Terms of Use
description: The terms governing NYC Open Data (and therefore TLC trip records) - the FAQ says there are no use restrictions, while the incorporated NYC.gov terms reserve the City's rights; no attribution or share-alike is required.
resource: https://opendata.cityofnewyork.us/overview/#termsofuse
tags:
- license
- nyc-open-data
- permissive
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://opendata.cityofnewyork.us/overview/
  title: NYC Open Data - Terms of Use section
  accessed: "2026-09-02"
- resource: https://opendata.cityofnewyork.us/faq/
  title: NYC Open Data FAQ
  accessed: "2026-09-02"
- resource: https://www.nyc.gov/home/terms-of-use.page
  title: NYC.gov Terms of Use
  accessed: "2026-09-02"
- resource: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
  title: TLC Trip Record Data (accuracy disclaimer)
  accessed: "2026-09-02"
---

# Where the text lives
There is **no single licence document**. Three pages together form the terms, and all three were read on 2026-09-02:

1. `https://opendata.cityofnewyork.us/overview/` (the `#termsofuse` section) - [source record](/sources/nyc-open-data-overview-terms.md)
2. `https://opendata.cityofnewyork.us/faq/` - [source record](/sources/nyc-open-data-faq.md)
3. `https://www.nyc.gov/home/terms-of-use.page`, incorporated by reference - [source record](/sources/nyc-gov-terms-of-use.md)

This is **not** an SPDX-identifiable licence. Ship the three URLs plus the quoted text in `LICENSES/NYC-OPEN-DATA-TERMS.txt`; there is no upstream file to copy.

# Terms (excerpts read 2026-09-02)

**Permission.** The FAQ states plainly: "Open Data belongs to all New Yorkers. **There are no restrictions on the use of Open Data.**" That is the City's clearest grant and the basis on which the whole open-data ecosystem redistributes these files.

**Incorporation.** The portal's Terms of Use section says: "By accessing datasets and feeds available through NYC Open Data, the user agrees to all of the Terms of Use of NYC.gov as well as the Privacy Policy for NYC.gov."

**Reservation.** Those NYC.gov terms say material on NYC.gov is "the property of the City of New York. All rights are reserved" and grant no reuse licence. **The two statements are in tension** - see [the open question](/questions/nyc-open-data-reuse-terms.md). The reservation is written about NYC.gov *site* content (design, text, graphics, software); the FAQ is written about the *datasets*, so the better reading is that the datasets carry no restrictions. This project proceeds on that reading and records the risk.

**Warranty.** "The City does not warranty the completeness, accuracy, content, or fitness for any particular purpose or use of any public data set made available on NYC Open Data"; "Submitting City Agencies are the authoritative source"; "Data may be updated, corrected, or refreshed at any time."

**Dataset-specific disclaimer** (TLC page): "The trip data was not created by the TLC, and TLC makes no representations as to the accuracy of these data."

# Obligations
* **Attribution:** none is legally required. This project credits anyway.
* **Share-alike:** none.
* **Trademarks:** the City's marks (including the City seal) are not licensed; do not use them.
* **Personal data:** trip records are already de-identified to taxi-zone granularity (no coordinates since 2016); no additional obligation is stated.

# Attribution
> Trip record data: NYC Taxi & Limousine Commission, published via NYC Open Data (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). The trip data was not created by the TLC, and TLC makes no representations as to the accuracy of these data. Terms of use: https://opendata.cityofnewyork.us/overview/#termsofuse

# Applied to
* [NYC TLC trip records](/datasets/nyc-tlc.md) - yellow and green taxi Parquet files and the taxi zone lookup table.
