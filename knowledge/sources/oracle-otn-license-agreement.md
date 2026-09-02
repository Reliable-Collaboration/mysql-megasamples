---
type: Source
title: Oracle Technology Network License Agreement (standard-license.html), linked from the SQLcl download page
description: The click-through developer license for OTN downloads such as SQLcl; internal development/testing use only, no production or data-processing use.
resource: https://www.oracle.com/downloads/licenses/standard-license.html
tags: [oracle, license, sqlcl]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.oracle.com/downloads/licenses/standard-license.html
    title: Oracle Technology Network License Agreement
    accessed: 2026-09-02
---

# What was read
The license page (curl), 2026-09-02. It is the only license link on the SQLcl download page.

# Relevant excerpt
> Oracle Technology Network License Agreement. Oracle is willing to authorize Your access to software associated with this License Agreement ("Agreement") only upon the condition that You accept that this Agreement governs Your use of the software. By selecting the "Accept License Agreement" button or box (or the equivalent) or installing or using the Programs You indicate Your acceptance ...
>
> License Rights and Restrictions. Oracle grants You a nonexclusive, nontransferable, limited license to internally use the Programs, subject to the restrictions stated in this Agreement, only for the purpose of developing, testing, prototyping, and demonstrating Your application and only as long as Your application has not been used for any data processing, business, commercial, or production purposes, and not for any other purpose.

# What it was used to decide
[SQLcl and python-oracledb tool record](/tools/sqlcl-and-python-oracledb.md): SQLcl may be used inside our build/verification stage (development/testing) but must not be redistributed in the published image; python-oracledb (Apache/UPL) is the preferred export tool because it carries no such restriction.
