---
type: Source
title: Divvy Data License Agreement (full text)
description: Lyft Bikes and Scooters' licence for City-of-Chicago-owned Divvy data; near-identical to the Citi Bike policy, including the stand-alone-dataset prohibition.
resource: https://divvybikes.com/data-license-agreement
tags: [license, divvy, blocker]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://divvybikes.com/data-license-agreement
    title: Divvy Data License Agreement
    accessed: "2026-09-02"
    version: page footer "(c) Lyft, Inc. 2026"; no effective date stated in the agreement
---

# What was read
The whole agreement, fetched with `curl` on 2026-09-02 and text-extracted locally. **The document carries no effective or revision date.**

# Relevant excerpt (verbatim)

> "Lyft Bikes and Scooters, LLC ("Bikeshare") operates the City of Chicago's ("City") Divvy bicycle sharing service. Bikeshare and the City are committed to supporting bicycling as an alternative transportation option. As part of that commitment, **the City permits Bikeshare to make certain Divvy system data owned by the City ("Data") available to the public**, subject to the terms and conditions of this License Agreement ("Agreement"). By accessing or using any of the Data, you agree to all of the terms and conditions of this Agreement."

> "**License.** Bikeshare hereby grants to you a non-exclusive, royalty-free, limited, perpetual license to access, reproduce, analyze, copy, modify, distribute in your product or service and use the Data for any lawful purpose ("License")."

> "**Prohibited Conduct.** The License does not authorize you to do, and you will not do or assist others in doing, any of the following
> Use the Data in any unlawful manner or for any unlawful purpose;
> **Host, stream, publish, distribute, sublicense, or sell the Data as a stand-alone dataset; provided, however, you may include the Data as source material, as applicable, in analyses, reports, or studies published or distributed for non-commercial purposes;**
> Access the Data by means other than the interface Bikeshare provides or authorizes for that purpose;
> Circumvent any access restrictions relating to the Data;
> Use data mining or other extraction methods in connection with Bikeshare's website or the Data;
> Attempt to correlate the Data with names, addresses, or other information of customers or Members of Bikeshare; and
> State or imply that you are affiliated, approved, endorsed, or sponsored by Bikeshare.
> Use or authorize others to use, without the written permission of the applicable owners, the trademarks or trade names of Lyft Bikes and Scooters, LLC, the City of Chicago or any sponsor of the Divvy service. These marks include, but are not limited to DIVVY, and the DIVVY logo, which are owned by the City of Chicago."

> "**No Warranty.** THE DATA IS PROVIDED "AS IS," AS AVAILABLE (AT BIKESHARE'S SOLE DISCRETION) AND AT YOUR SOLE RISK. TO THE MAXIMUM EXTENT PROVIDED BY LAW BIKESHARE DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED ..."

> "**Limitation of Liability and Covenant Not to Sue.** ... your maximum recovery is limited to $100 in the aggregate ..."

> "**Ownership and Provision of Data.** **The City of Chicago owns all right, title, and interest in the Data.** Bikeshare may modify or cease providing any or all of the Data at any time, without notice, in its sole discretion."

> "**No Waiver.** Nothing in this Agreement is or implies a waiver of any rights Bikeshare or the City of Chicago has in the Data or in any copyrights, patents, or trademarks owned or licensed by Bikeshare, its parent, affiliates or sponsors. The DIVVY trademarks are owned by the City of Chicago."

> "**Termination of Agreement.** Bikeshare may terminate this Agreement at any time and for any reason in its sole discretion. ... (currently www.divvybikes.com/data ...). Sections 2-6 and 9-10 will survive termination."

> "**Contact.** ... bike-data@lyft.com."

> "**Applicable Law and Forum.** This Agreement is governed by the laws of the State of Illinois, without regard to conflicts of law principles. Any dispute arising under or relating to this Agreement will be brought only in a court of competent jurisdiction sitting in New York City, New York."

**Differences from the Citi Bike text:** the City of Chicago (not Bikeshare) owns the Data; the trademark clause adds the City of Chicago; governing law is Illinois while the forum is still New York City; the prohibited-conduct list is unnumbered. **The stand-alone-dataset prohibition is word-for-word identical.** There is no "non-commercial only" restriction on *use* and no "may not compete" clause - the non-commercial limit applies only to the carve-out permitting redistribution inside analyses/reports/studies.

# What it was used to decide
[Divvy data license](/licenses/divvy-data-license.md) and the **redistribution blocker** in [Divvy](/datasets/divvy.md) and [the open question](/questions/citibike-divvy-redistribution.md).
