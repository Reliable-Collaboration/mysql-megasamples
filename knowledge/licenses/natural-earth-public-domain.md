---
type: License
title: Natural Earth public domain terms
description: Natural Earth vector/raster map data is public domain with no attribution requirement; relevant because WideWorldImporters embeds country/state borders and city locations derived from Natural Earth (and data.gov).
resource: https://www.naturalearthdata.com/about/terms-of-use/
tags: [license, public-domain, geodata]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://www.naturalearthdata.com/about/terms-of-use/
    title: Natural Earth » Terms of Use
    accessed: 2026-09-02
  - resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-what-is
    title: WWI "Terms of use" section naming data.gov and Natural Earth as the public data sources
    accessed: 2026-09-02
---

# Where the verbatim text lives
`https://www.naturalearthdata.com/about/terms-of-use/` ([source record](/sources/naturalearthdata-terms-of-use.md)).

# Key terms (verbatim)
> All versions of Natural Earth raster + vector map data found on this website are in the public domain.
> No permission is needed to use Natural Earth. Crediting the authors is unnecessary.
> The authors provide Natural Earth as a public service and are not responsible for any problems relating to accuracy, content, design, and how it is used.

# Obligations
None (public domain; commercial use and modification allowed). Courtesy credit "Made with Natural Earth" is optional. data.gov content is US federal public data (no separate terms page was read for it - the WWI Learn page is the only citation; treat as public domain but do not quote terms).

# Applied to
* [WideWorldImporters](/datasets/wideworldimporters.md) (`Application.Countries.Border`, `Application.StateProvinces.Border`, `Application.Cities.Location`/population) and [WideWorldImportersDW](/datasets/wideworldimporters-dw.md) (`Dimension.City`).
