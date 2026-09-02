---
type: Open Question
title: May a converted copy of Citi Bike / Divvy trip data be redistributed in a public image?
description: Both Lyft bikeshare licences forbid publishing or distributing the data "as a stand-alone dataset"; this decides whether these two datasets can ship at all or must be user-fetched.
resource: /questions/citibike-divvy-redistribution.md
tags: [license, blocker, citibike, divvy]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://citibikenyc.com/data-sharing-policy
    title: Citi Bike Data Sharing Policy
    accessed: 2026-09-02
  - resource: https://divvybikes.com/data-license-agreement
    title: Divvy Data License Agreement
    accessed: 2026-09-02
---

# The question
Both licences grant a "perpetual license to access, reproduce, analyze, copy, modify, **distribute in your product or service** and use the Data for any lawful purpose", and both then forbid:

> "Host, stream, publish, distribute, sublicense, or sell the Data as a stand-alone dataset; provided, however, you may include the Data as source material, as applicable, in analyses, reports, or studies published or distributed for non-commercial purposes"

Does a public Docker image containing a MySQL database of the trips count as "distributing the Data as a stand-alone dataset" (prohibited), or as "distribute in your product or service" (granted)?

**The conservative reading, adopted by this plan:** it is prohibited. The image's entire value proposition for this dataset is the dataset itself, which is what "stand-alone dataset" means; nothing in the image analyses or reports on the trips. The carve-out is limited to "analyses, reports, or studies ... for non-commercial purposes" and does not cover a redistributable database.

Consequences already baked into the plan: [Citi Bike](/datasets/citibike.md) and [Divvy](/datasets/divvy.md) are **extended tier only**, fetched by the user from the upstream S3 buckets at load time, never baked into a published image or a GitHub release asset, and never mirrored.

# Cheapest experiment that resolves it
Email **`bike-data@lyft.com`** - the contact address named in both agreements - describing exactly the artifact (a public Docker image / GitHub repo containing one month of trips converted to MySQL tables, for teaching SQL, no Citi Bike/Divvy branding, upstream attribution and a link to the licence) and asking for written permission or a written confirmation that this falls under "distribute in your product or service". Cost: one email; both licences invite exactly this ("requests for permission ... should be sent to bike-data@lyft.com").

Until an answer arrives, ship nothing and keep the download-at-load-time design, which is licence-safe under either reading because the user fetches from Lyft's own interface and thereby accepts the agreement directly.

# If the answer is no
The fallback that needs no permission: ship the **loader script plus the expected schema, row counts and checksums**, and let `make load-citibike` / `make load-divvy` do the fetch. This is already the design, so a "no" costs nothing.
