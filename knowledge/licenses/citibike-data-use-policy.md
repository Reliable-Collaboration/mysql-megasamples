---
type: License
title: Citi Bike / NYCBS Data Sharing Policy
description: Lyft Bikes and Scooters' licence for Citi Bike trip data; it grants broad use but expressly forbids publishing or distributing the data as a stand-alone dataset, which blocks shipping it in this image.
resource: https://citibikenyc.com/data-sharing-policy
tags: [license, citibike, redistribution-blocked]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://citibikenyc.com/data-sharing-policy
    title: Citi Bike Data Sharing Policy (full text)
    accessed: 2026-09-02
  - resource: https://citibikenyc.com/system-data
    title: Citi Bike System Data (links to the policy as "NYCBS Data Use Policy")
    accessed: 2026-09-02
---

# Where the verbatim text lives
`https://citibikenyc.com/data-sharing-policy` (the System Data page links to it as the "NYCBS Data Use Policy" via `https://www.citibikenyc.com/data-sharing-policy`, which redirects there). The frequently cited `https://ride.citibikenyc.com/data-sharing-policy` returned **HTTP 503** on 2026-09-02. Full text quoted in [the source record](/sources/citibike-data-sharing-policy.md). Ship as `LICENSES/CITIBIKE-DATA-SHARING-POLICY.txt`.

# Terms (verbatim, read 2026-09-02)
**Grant.** "Bikeshare hereby grants to you a non-exclusive, royalty-free, limited, perpetual license to access, reproduce, analyze, copy, modify, distribute in your product or service and use the Data for any lawful purpose."

**Prohibited Conduct** (the operative restrictions):
* (b) "Host, stream, publish, distribute, sublicense, or sell the Data as a stand-alone dataset; provided, however, you may include the Data as source material, as applicable, in analyses, reports, or studies published or distributed for non-commercial purposes;"
* (c) "Access the Data by means other than the interface Bikeshare provides or authorizes for that purpose;"
* (d) circumvent access restrictions; (e) "Use data mining or other extraction methods in connection with Bikeshare's website or the Data;"
* (f) "Attempt to correlate the Data with names, addresses, or other information of customers or subscribers of Bikeshare;"
* (g) "State or imply that you are affiliated, approved, endorsed, or sponsored by Bikeshare;"
* (h) no use of the trademarks or trade names of Lyft Bikes and Scooters, LLC or Citigroup, Inc. - "These marks include, but are not limited to CITI BIKE, and the CITI BIKE logo."

**Other.** Data is "AS IS"; liability capped at $100; "Bikeshare owns all right, title, and interest in the Data"; Bikeshare "may terminate this Agreement at any time and for any reason in its sole discretion"; New York law and forum; questions to `bike-data@lyft.com`.

# Obligations and the blocking finding
* **Attribution:** not required, but clause (g)/(h) mean the image must not use the CITI BIKE name or logo as branding and must not suggest endorsement.
* **Share-alike:** none.
* **Re-identification:** forbidden.
* **Redistribution: BLOCKED for this project's default use.** An image whose purpose is to ship a loadable copy of the trip table is "hosting/publishing/distributing the Data as a stand-alone dataset". The proviso only rescues inclusion "as source material ... in analyses, reports, or studies published or distributed for non-commercial purposes" - a sample database is none of those. The words "distribute in your product or service" in the grant do **not** override clause (b); read together, they permit distributing data *inside* a product's own functionality, not republishing the corpus.
* **Consequence:** the dataset must be **extended tier, downloaded from the upstream S3 bucket at build/load time on the user's own machine** (which is the user accepting the licence directly), never baked into a published image or a release asset. Clause (c) ("means other than the interface Bikeshare provides") also argues for fetching from the documented S3 bucket rather than a mirror.

# Attribution string to ship (in documentation, not as branding)
> Bike trip data downloaded by the user at build time from the Citi Bike system-data S3 bucket (https://citibikenyc.com/system-data), subject to the Citi Bike Data Sharing Policy (https://citibikenyc.com/data-sharing-policy). This project is not affiliated with, endorsed or sponsored by Lyft Bikes and Scooters, LLC or Citigroup, Inc.

# Applied to
* [Citi Bike](/datasets/citibike.md).
* See also the near-identical [Divvy Data License Agreement](/licenses/divvy-data-license.md) and [the open question](/questions/citibike-divvy-redistribution.md).
