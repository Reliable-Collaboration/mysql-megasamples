---
type: Tool
title: SQLBI Contoso Data Generator V2 (2.0.1)
description: .NET 8 console tool (MIT) that generates the Contoso V2 star schema (customer, date, product, store, currencyexchange, sales, orders, orderrows) as CSV/Parquet/Delta for any OrdersCount; constant-seeded RNG; pre-built sizes published as 7z archives.
resource: https://github.com/sql-bi/Contoso-Data-Generator-V2
tags: [tool, generator, contoso, dotnet, mit]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/README.md
    title: README + release 2.0.1 assets
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/DatabaseGenerator/Engine.cs
    title: generator source (csproj, Config.cs, Engine*.cs)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/build_data/build_single.cmd
    title: build scripts and config.json
    accessed: "2026-09-02"
  - resource: https://docs.sqlbi.com/contoso-data-generator/
    title: SQLBI documentation
    accessed: "2026-09-02"
---

# Facts
* Release 2.0.1 (2025-01-17): self-contained zips for linux-x64 (31.85 MB), osx-arm64, osx-x64, win-x64; source targets `net8.0` ([README](/sources/github-sql-bi-contoso-v2-readme.md), [source](/sources/github-sql-bi-contoso-v2-generator-source.md)). MIT.
* Invocation: `DatabaseGenerator config.json data.xlsx <outdir> <cachedir> param:OrdersCount=N param:OutputFormat=CSV param:CustomerPercentage=0.05 param:StartDT=2015-01-01 param:YearsCount=10 param:CutDateBefore=2014-05-18 param:CutDateAfter=2024-04-20` - exactly how SQLBI built the published `csv-100k` set ([build scripts](/sources/github-sql-bi-contoso-v2-config-and-build-scripts.md)).
* Needs network on first run to fill the cache with the `static-files` release (21 customer files of ~22 MB gz, ECB rates, UK postcodes) ([data releases](/sources/github-sql-bi-contoso-v2-data-releases.md)).
* Determinism: RNGs are constructed as `new Random(0)` and `new Random(year*1000+dayOfYear)`; no seed parameter exists. **Inferred:** output is reproducible for identical config, data.xlsx, static files and tool version, unless multithreaded sections interleave - see [question](/questions/contoso-generator-determinism.md).
* Output entities: customer, date, product, store, currencyexchange, sales (flat) and/or orders + orderrows ([docs](/sources/sqlbi-docs-contoso-data-generator.md)). CSV dialect not documented - inspect the 7z.

# Use in this project
Not run in core (the published `csv-100k.7z` is used); optional extended-tier regeneration in a `mcr.microsoft.com/dotnet/runtime:8.0` stage (**Inferred** image choice) for custom OrdersCount. Requires `7z` (p7zip) to unpack SQLBI's archives either way.

# Limits
* Not seedable: every run produces different rows ([question](/questions/contoso-generator-determinism.md)); the plan ships SQLBI's published CSV releases instead of regenerating.
* Requires the .NET 8 SDK image at build time; never part of the final image.
