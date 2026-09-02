---
type: License
title: City of Chicago Data Terms of Use
description: Chicago permits reuse of portal data but requires a verbatim disclaimer wherever a derivative application is published, plus an indemnity.
resource: https://www.chicago.gov/city/en/narr/foia/data_disclaimer.html
tags: [license, chicago, attribution-required]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.chicago.gov/city/en/narr/foia/data_disclaimer.html
    title: "City of Chicago :: Data Terms of Use"
    accessed: 2026-09-02
  - resource: https://data.cityofchicago.org/api/views/ijzp-q8t2.json
    title: Crimes dataset metadata (license = "See Terms of Use")
    accessed: 2026-09-02
---

# Where the verbatim text lives
`https://www.chicago.gov/city/en/narr/foia/data_disclaimer.html` - the full text is quoted in [the source record](/sources/chicago-data-terms-of-use.md). The Socrata metadata for each dataset declares `license: {"name": "See Terms of Use"}`, i.e. these terms and nothing else. Ship as `LICENSES/CHICAGO-DATA-TERMS-OF-USE.txt`.

# Terms (excerpts read 2026-09-02)
* The City "voluntarily provides the data on this website as a service to the public", "makes this data available on an 'as is' basis" and "explicitly disclaims any representations and warranties".
* Redistribution is permitted by implication: the terms regulate "any software application, or other secondary or derivative application using data supplied at this website" rather than forbidding it.
* **Mandatory disclaimer.** Any such application must "Include the following disclaimer at the site where the software application, or other secondary or derivative application can be accessed or downloaded":
  > "This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago. The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site. The data provided at this site is subject to change at any time. It is understood that the data provided at this site is being used at one's own risk."
* Must also "Comply with any additional Terms of Use set forth by the City agency or department providing data" - for the crimes dataset, the CPD disclaimer embedded in the dataset description, including "attempts to derive specific addresses are strictly prohibited".
* The City may "require a user of this data to terminate any and all display, distribution or other use" for any reason.
* The user indemnifies and holds the City harmless for any claim arising from use, "including any secondary or derivative use".
* Intellectual property is reserved but not asserted here: "If the City claims or seeks to protect any intellectual property rights ... then this website will so indicate on the webpage". The crimes dataset page carries no such indication.

# Obligations
* **Attribution / disclaimer:** the boxed paragraph above must appear verbatim in the repository README and on the image's documentation page. This is the strongest obligation in the whole bundle for this dataset.
* **Extra dataset terms:** reproduce the CPD accuracy disclaimer alongside it.
* **Share-alike:** none.
* **Personal data:** the data is already block-level redacted; do not attempt to re-derive addresses.
* **Risk:** the City may revoke; the image must be able to drop the dataset.

# Attribution string to ship
> Crime data: City of Chicago Data Portal, "Crimes - 2001 to Present" (ijzp-q8t2), Chicago Police Department. Terms of use: https://www.chicago.gov/city/en/narr/foia/data_disclaimer.html
>
> This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago. The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site. The data provided at this site is subject to change at any time. It is understood that the data provided at this site is being used at one's own risk.

# Applied to
* [Chicago crimes](/datasets/chicago-crimes.md) - the crimes extract and the IUCR code lookup.
* Note: **Divvy data is City-of-Chicago-owned but is not licensed under these terms**; it carries its own [Divvy Data License Agreement](/licenses/divvy-data-license.md).
