---
type: Source
title: sql-bi/Contoso-Data-Generator-V2 README
description: Overview of the V2 generator - output formats (Parquet, Delta, CSV, CSV multi-file, gz, SQL Server bulk-insert script), required inputs (config.json, data.xlsx, output and cache folders), static files downloaded from a SQLBI repository.
resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/README.md
tags: [contoso, generator, readme]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/README.md
    title: README.md (1,704 bytes)
    accessed: 2026-09-02
    version: main (pushed 2025-07-02); latest release 2.0.1 (2025-01-17)
  - resource: https://api.github.com/repos/sql-bi/Contoso-Data-Generator-V2
    title: repository metadata (MIT) and releases/latest
    accessed: 2026-09-02
---

# What was read
README.md in full and the API metadata, accessed 2026-09-02.

# Relevant excerpt
> DataGenerator is a tool for generating sample data, ready to be imported into PowerBI or Fabric OneLake for analysis. This is the V2 version, evolution of the older one. ... Supported output formats: Parquet; Delta Table (files); CSV; CSV multi file; CSV multi file - gz compressed; Sql Server, via bulk insert script of the generated CSV files ... `databasegenerator.exe configfile datafile outputfolder cachefolder [param:AAAAA=nnnn]` ... the tool needs some files containing static data: fake customers, exchange rates, postal codes, etc. The files are cached after been downloaded over the Internet from a specific SQLBI repository.

Release 2.0.1 (2025-01-17) assets: DatabaseGenerator.linuxx64.zip 31,850,089 B; osx-arm64 30,155,549; osx-x64 31,799,652; winx64 33,374,129. Repository license MIT.

# What it was used to decide
[Contoso generator tool record](/tools/contoso-data-generator-v2.md).
