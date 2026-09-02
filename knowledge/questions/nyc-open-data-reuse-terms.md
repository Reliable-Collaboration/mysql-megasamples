---
type: Open Question
title: Does NYC Open Data actually permit unrestricted redistribution of TLC trip data?
description: The Open Data FAQ says there are no restrictions; the NYC.gov Terms of Use it incorporates reserve all rights. The tension is unresolved on the City's own pages.
resource: /questions/nyc-open-data-reuse-terms.md
tags: [license, nyc-open-data]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://opendata.cityofnewyork.us/faq/
    title: NYC Open Data FAQ
    accessed: 2026-09-02
  - resource: https://www.nyc.gov/home/terms-of-use.page
    title: NYC.gov Terms of Use
    accessed: 2026-09-02
---

# The question
The NYC Open Data FAQ states: "Open Data belongs to all New Yorkers. **There are no restrictions on the use of Open Data.**"

The portal's Terms of Use section instead says: "By accessing datasets and feeds available through NYC Open Data, the user agrees to all of the Terms of Use of NYC.gov", and NYC.gov's Terms of Use say its materials "are the property of the City of New York. **All rights are reserved.**"

No page found in this session states a licence (CC0, PDDL, ODbL, ...) for NYC Open Data datasets, and the TLC trip-record page itself carries no licence statement at all - only an accuracy disclaimer. The Socrata metadata for the TLC's mirrored yearly datasets on `data.cityofnewyork.us` (e.g. `t29m-gskq`, `4b4i-vvec`) has `license: null` and only `attribution: Taxi and Limousine Commission (TLC)`.

The project proceeds on the FAQ reading (unrestricted), which is also how every public mirror of this data behaves, and ships attribution voluntarily.

# Cheapest experiment that resolves it
Email `opendata@cityofnewyork.us` (the portal's published contact) asking whether TLC trip records may be redistributed in modified form in a public repository, and whether the City asserts copyright in the datasets. One email, no build cost.

Cheaper still and worth doing first: check whether the NYC Open Data **Technical Standards Manual** or the Open Data Law (Local Law 11 of 2012, NYC Admin. Code Sec. 23-502) states a licence - neither was opened in this session.

# Risk if unresolved
Low. The data contains no personal information, the City actively promotes reuse, and the fallback (download at load time, as for the bikeshare datasets) is already implemented in the loader.
