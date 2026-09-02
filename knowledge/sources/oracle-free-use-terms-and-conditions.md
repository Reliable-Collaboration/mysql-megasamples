---
type: Source
title: Oracle Free Use Terms and Conditions (license governing Oracle Database Free)
description: The license text under which Oracle Database Free (and its container image) is distributed; grants internal use and unmodified redistribution, no resource limits stated in the text itself.
resource: https://www.oracle.com/downloads/licenses/oracle-free-license.html
tags: [oracle, license, oracle-database-free]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.oracle.com/downloads/licenses/oracle-free-license.html
    title: Oracle Free Use Terms and Conditions
    accessed: "2026-09-02"
    version: "Last updated: 9 June 2021"
---

# What was read
The full license page (fetched with curl; WebFetch was refused with HTTP 403), 2026-09-02.

# Relevant excerpt
> Your use of this Program is governed by the Free Use Terms and Conditions set forth below, unless you have received this Program (alone or as part of another Oracle product) under an Oracle license agreement ...
>
> **License Rights and Restrictions** Oracle grants to You, as a recipient of this Program, a nonexclusive, nontransferable, limited license to, subject to the conditions stated herein, (a) internally use the unmodified Programs for the purposes of developing, testing, prototyping and demonstrating your applications, and running the Programs for your own internal business operations; and (b) redistribute unmodified Programs and Programs Documentation, under the terms of this License, provided that You do not charge Your end users any additional fees for the use of the Programs. ...
>
> Your license is contingent on Your compliance with the following conditions: - You include a copy of this license with any distribution by You of the Programs; - You do not remove markings or notices of either Oracle's or a licensor's proprietary rights from the Programs or Program Documentation; - You comply with all U.S. and applicable export control and economic sanctions laws ...; - You do not cause or permit reverse engineering, disassembly or decompilation of the Programs (except as allowed by law) ...
>
> THE PROGRAMS ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. ... Last updated: 9 June 2021

The text itself contains **no** CPU/RAM/data-size limits; those are product limits documented in the FAQ ([Oracle Database Free FAQ and get-started pages](/sources/oracle-database-free-faq-and-get-started.md)).

# What it was used to decide
[Oracle Database Free container tool record](/tools/oracle-database-free-container.md): using the image in a build stage is "internal use ... for developing, testing"; we do not redistribute the image, so the copy-of-license condition does not arise for the mysql-megasamples image.
