---
type: Source
title: Contoso V2 generator source (DatabaseGenerator.csproj, Config.cs, Engine.cs, Engine_Setup.cs, MyRnd.cs, Program.cs)
description: Confirms net8.0 target, the config schema, and that all random generators are seeded with constants (Random(0), per-day seed from the date) - no user-facing seed parameter.
resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/DatabaseGenerator/Engine.cs
tags: [contoso, generator, source, determinism, dotnet]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/DatabaseGenerator/DatabaseGenerator.csproj
    title: DatabaseGenerator.csproj
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/DatabaseGenerator/Config.cs
    title: Config.cs
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/DatabaseGenerator/Engine.cs
    title: Engine.cs (grep Random)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/DatabaseGenerator/Engine_Setup.cs
    title: Engine_Setup.cs (lines 170-185, grep)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/DatabaseGenerator/MyRnd.cs
    title: MyRnd.cs
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/DatabaseGenerator/Program.cs
    title: Program.cs (grep)
    accessed: "2026-09-02"
---

# What was read
The listed files (full or grepped), accessed 2026-09-02.

# Relevant excerpt
* csproj: `<TargetFramework>net8.0</TargetFramework>`; packages CsvHelper 31.0.3, ExcelDataReader.DataSet 3.6.0, MathNet.Numerics 5.0.0, Parquet.Net 4.23.5.
* Config.cs properties: OrdersCount, StartDT, YearsCount, CutDateBefore/After, CustomerPercentage, CustomerFakeGenerator ("// >0 : use fake customers"), OutputFormat ("CSV PARQUET DELTATABLE"), SalesOrders ("SALES ORDERS BOTH"), DeltaTableOrdersPerFile, ParquetOrdersRowGroupSize, CsvMaxOrdersPerFile, CsvGzCompression, DaysWeight, weight vectors, CountryCurrency, AnnualSpikes, OneTimeSpikes, CustomerActivity.
* Program.cs: usage `databasegenerator.exe configfile datafile outputfolder cachefolder [param:OrdersCount=nnnnnnn]`; any config property can be overridden with `param:Name=value`.
* Engine.cs line 86: `Random rng = new Random(0);` with the comment "Do not not use a static global rng: it's not supported in multithread"; line 290: `var localRNG = new Random(today.Year * 1000 + today.DayOfYear);` for per-day transaction counts. Engine_Setup.cs line 179: `var localRnd = new Random(0);` used to shuffle `customersall.csv` before taking `CustomerPercentage` of them.
* MyRnd.cs: weighted-index helpers over `Random`.

# What it was used to decide
Determinism assessment in [Contoso generator tool](/tools/contoso-data-generator-v2.md) and [question](/questions/contoso-generator-determinism.md).
