---
type: Source
title: sql-bi/Contoso-Data-Generator-V2-Data README and release assets
description: The ready-to-use data repository (MIT) - release "ready-to-use-data" (2025-09-21) with csv/parquet/delta/pbix/bak archives for 10k, 100k, 1M, 10M, 100M orders; older "ready-to-use-data-2024" and "static-files" releases.
resource: https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/tag/ready-to-use-data
tags: [contoso, data, releases, sizes]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2-Data/main/README.md
    title: README.md (239 bytes)
    accessed: 2026-09-02
  - resource: https://api.github.com/repos/sql-bi/Contoso-Data-Generator-V2-Data/releases
    title: releases with assets (paginated)
    accessed: 2026-09-02
---

# What was read
README and the full releases/assets listing via `gh api --paginate`, accessed 2026-09-02.

# Relevant excerpt
* README: "Here you can find ready to use sets of data, created with CDGV2 ... Ready to use data - download here (releases/tag/ready-to-use-data)".
* Release `ready-to-use-data` (2025-09-21) CSV assets (bytes): csv-10k.7z 5,409,141; csv-100k.7z 9,786,343; csv-1m.7z 48,894,397; csv-10m.7z 512,408,852; csv-100m.7z parts .001-.009 (8 x 524,288,000 + 265,039,589 = about 4.46 GB). Parquet: parquet-100k 9,930,769; parquet-1m 66,012,150; parquet-10m 679,235,825; parquet-100m 12 parts. Delta: delta-100k 9,992,552; delta-1m 66,403,641; delta-10m 679,249,108. SQL Server backups bak-ContosoV2-10k.7z 6,866,480 ... bak-ContosoV2-100M.7z 13 parts. pbix/pbit files. URL pattern https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/download/ready-to-use-data/csv-100k.7z.
* Release `ready-to-use-data-2024` (2024-06-15) holds the previous generation (csv-100k.7z 8,914,259 etc.). Release `static-files` (2024-04-13) holds the generator inputs: Cust.{AU,CA,DE,FR,IT,NL,UK,US}.NN.csv.gz (21 files, ~22-23 MB each), ECB_eurofxref-hist.csv, Exch_{AUD,CAD,EUR,GBP,USD}.csv, UKPostcodes.csv.
* Repository license MIT ("Copyright (c) 2024 SQLBI").

# What it was used to decide
Artifact choice and sizes in [Contoso](/datasets/contoso.md).
