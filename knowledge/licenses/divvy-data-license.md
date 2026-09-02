---
type: License
title: Divvy Data License Agreement
description: Lyft Bikes and Scooters' licence for City-of-Chicago-owned Divvy data; grant and restrictions are word-for-word the Citi Bike policy, including the stand-alone-dataset prohibition.
resource: https://divvybikes.com/data-license-agreement
tags: [license, divvy, redistribution-blocked]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://divvybikes.com/data-license-agreement
    title: Divvy Data License Agreement (full text)
    accessed: "2026-09-02"
  - resource: https://divvybikes.com/system-data
    title: Divvy System Data (links to the agreement)
    accessed: "2026-09-02"
---

# Where the text lives
`https://divvybikes.com/data-license-agreement` (the System Data page links to `https://www.divvybikes.com/data-license-agreement`, which redirects there). **The document states no effective or revision date.** Full text quoted in [the source record](/sources/divvy-data-license-agreement.md). Ship as `LICENSES/DIVVY-DATA-LICENSE-AGREEMENT.txt`.

# Terms (verbatim, read 2026-09-02)
**Parties.** "Lyft Bikes and Scooters, LLC ('Bikeshare') operates the City of Chicago's ('City') Divvy bicycle sharing service. ... the City permits Bikeshare to make certain Divvy system data owned by the City ('Data') available to the public".

**Grant.** "Bikeshare hereby grants to you a non-exclusive, royalty-free, limited, perpetual license to access, reproduce, analyze, copy, modify, distribute in your product or service and use the Data for any lawful purpose."

**Prohibited Conduct** (unnumbered list; the same seven items as Citi Bike plus the trademark clause):
* "Host, stream, publish, distribute, sublicense, or sell the Data as a stand-alone dataset; provided, however, you may include the Data as source material, as applicable, in analyses, reports, or studies published or distributed for non-commercial purposes;"
* access only through the interface Bikeshare provides or authorizes; no circumvention; no data mining "in connection with Bikeshare's website or the Data";
* "Attempt to correlate the Data with names, addresses, or other information of customers or Members of Bikeshare;"
* "State or imply that you are affiliated, approved, endorsed, or sponsored by Bikeshare;"
* no use of "the trademarks or trade names of Lyft Bikes and Scooters, LLC, the City of Chicago or any sponsor of the Divvy service. These marks include, but are not limited to DIVVY, and the DIVVY logo, which are owned by the City of Chicago."

**Other.** "AS IS", no warranty; liability capped at $100; "**The City of Chicago owns all right, title, and interest in the Data**"; termination at Bikeshare's sole discretion; **Illinois** governing law with a **New York City** forum; `bike-data@lyft.com`.

**What the agreement does NOT say** (checked, because it is often mis-stated): there is no general "non-commercial use only" restriction on use, and no "may not compete with Divvy/Lyft" clause. The non-commercial limit attaches only to the redistribution carve-out.

# Obligations
Identical in substance to [Citi Bike](/licenses/citibike-data-use-policy.md): no attribution required, no share-alike, no re-identification, no DIVVY/Lyft/City-of-Chicago marks, no implied endorsement, and **redistribution of the corpus as a stand-alone dataset is prohibited**. Note that although the City of Chicago owns the data, the permissive [Chicago data portal terms](/licenses/chicago-data-portal-terms.md) do **not** apply - Divvy data is published under this agreement instead.

**Consequence:** extended tier only, downloaded from `https://divvy-tripdata.s3.amazonaws.com/` by the user at build/load time. Never baked into a published image or release asset.

# Attribution
> Bike trip data downloaded by the user at build time from the Divvy system-data bucket (https://divvybikes.com/system-data), owned by the City of Chicago and licensed under the Divvy Data License Agreement (https://divvybikes.com/data-license-agreement). This project is not affiliated with, endorsed or sponsored by Lyft Bikes and Scooters, LLC or the City of Chicago.

# Applied to
* [Divvy](/datasets/divvy.md).
* See also [the open question](/questions/citibike-divvy-redistribution.md).
