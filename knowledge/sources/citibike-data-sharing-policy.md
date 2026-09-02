---
type: Source
title: Citi Bike / NYCBS Data Sharing Policy (full text)
description: Lyft Bikes and Scooters' licence for Citi Bike system data, including the clause that forbids redistributing the data as a stand-alone dataset.
resource: https://citibikenyc.com/data-sharing-policy
tags: [license, citibike, blocker]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://citibikenyc.com/data-sharing-policy
    title: Citi Bike Data Sharing Policy
    accessed: 2026-09-02
    version: page footer "(c) Lyft, Inc. 2026"
---

# What was read
The whole policy, fetched with `curl` from `https://www.citibikenyc.com/data-sharing-policy` (redirects to `https://citibikenyc.com/data-sharing-policy`) on 2026-09-02 and text-extracted locally. Note `https://ride.citibikenyc.com/data-sharing-policy` - the URL printed in many third-party write-ups - returned **HTTP 503** on this date.

# Relevant excerpt (verbatim)

> "Lyft Bikes and Scooters, LLC ("Bikeshare") operates New York City's Citi Bike bicycle sharing service. Bikeshare is committed to supporting bicycling as an alternative transportation option. As part of that commitment, Bikeshare makes certain Citi Bike system data ("Data") available to the public, subject to the terms and conditions of this License Agreement ("Agreement"). By accessing or using any of the Data, you agree to all of the terms and conditions of this Agreement."

> "**License.** Bikeshare hereby grants to you a non-exclusive, royalty-free, limited, perpetual license to access, reproduce, analyze, copy, modify, distribute in your product or service and use the Data for any lawful purpose ("License")."

> "**Prohibited Conduct.** The License does not authorize you to do, and you will not do or assist others in doing, any of the following:
> (a) Use the Data in any unlawful manner or for any unlawful purpose;
> **(b) Host, stream, publish, distribute, sublicense, or sell the Data as a stand-alone dataset; provided, however, you may include the Data as source material, as applicable, in analyses, reports, or studies published or distributed for non-commercial purposes;**
> (c) Access the Data by means other than the interface Bikeshare provides or authorizes for that purpose;
> (d) Circumvent any access restrictions relating to the Data;
> (e) Use data mining or other extraction methods in connection with Bikeshare's website or the Data;
> (f) Attempt to correlate the Data with names, addresses, or other information of customers or subscribers of Bikeshare; and
> (g) State or imply that you are affiliated, approved, endorsed, or sponsored by Bikeshare.
> (h) Use or authorize others to use, without the written permission of the applicable owners, the trademarks or trade names of Lyft Bikes and Scooters, LLC, or Citigroup, Inc., (sponsor of the Citi Bike service). These marks include, but are not limited to CITI BIKE, and the CITI BIKE logo."

> "**No Warranty.** THE DATA IS PROVIDED "AS IS," AS AVAILABLE (AT BIKESHARE'S SOLE DISCRETION) AND AT YOUR SOLE RISK. TO THE MAXIMUM EXTENT PROVIDED BY LAW BIKESHARE DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. ..."

> "**Limitation of Liability and Covenant Not to Sue.** ... your maximum recovery is limited to $100 in the aggregate ..."

> "**Ownership and Provision of Data.** Bikeshare owns all right, title, and interest in the Data. Bikeshare may modify or cease providing any or all of the Data at any time, without notice, in its sole discretion."

> "**Termination of Agreement.** Bikeshare may terminate this Agreement at any time and for any reason in its sole discretion. Termination will be effective upon Bikeshare's transmission of written notice to you at the email address you provided to Bikeshare in connection with this or by Bikeshare's announcement on its website (currently www.citibikenyc.com/system-data) that it is revoking all licenses. Sections 2 - 6 and 9-10 will survive termination."

> "**Contact.** Questions relating to this Agreement, including requests for permission to use trademarks and trade names, should be sent to bike-data@lyft.com."

> "**Applicable Law and Forum.** This Agreement is governed by the laws of the State of New York ... Any dispute arising under or relating to this Agreement will be brought only in a court of competent jurisdiction sitting in New York City, New York."

# What it was used to decide
[Citi Bike data use policy](/licenses/citibike-data-use-policy.md) and the **redistribution blocker** recorded in [Citi Bike](/datasets/citibike.md) and [the open question](/questions/citibike-divvy-redistribution.md). Clause (b) is the operative one: a Docker image whose whole purpose is to ship a loadable copy of the trip table is "publishing/distributing the Data as a stand-alone dataset", and the carve-out it offers is limited to "analyses, reports, or studies ... for non-commercial purposes".
