---
type: Source
title: Contoso V2 scripts/build_data (config.json, build_single.cmd, build_all.cmd)
description: The exact parameters SQLBI used to build the ready-to-use sizes - OrdersCount 10k..100M, CustomerPercentage, StartDT 2015-01-01, YearsCount 10, cut dates - and the full config.json defaults.
resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/build_data/build_single.cmd
tags: [contoso, generator, config]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/build_data/config.json
    title: config.json
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/build_data/build_single.cmd
    title: build_single.cmd
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/build_data/build_all.cmd
    title: build_all.cmd
    accessed: 2026-09-02
---

# What was read
The three files in full, accessed 2026-09-02.

# Relevant excerpt
* config.json defaults: `OrdersCount 100000`, `StartDT 2014-01-01`, `YearsCount 10`, `CutDateBefore 2000-05-18`, `CutDateAfter 2050-11-12`, `CustomerFakeGenerator -100000`, `CustomerPercentage 0.15`, `OutputFormat "CSV"`, `SalesOrders "BOTH"`, `DeltaTableOrdersPerFile 100000`, `-CsvMaxOrdersPerFile 100000`, `-CsvGzCompression 1` (dash-prefixed = disabled), plus DaysWeight (weekday factors, spikes), `OrderRowsWeights [12,9,7,4,1,1,1]`, `OrderQuantityWeights`, `DiscountWeights`, `OnlinePerCent`, `DeliveryDateLambdaWeights`, `CountryCurrency {AU:AUD, CA:CAD, FR/DE/IT/NL:EUR, GB:GBP, US:USD}`, AnnualSpikes, OneTimeSpikes (incl. 2020-02-28..2021-06-15 factor 0.3), CustomerActivity weights. No seed parameter.
* build_single.cmd: `csv-10k` = OrdersCount 10000, CustomerPercentage 0.05, StartDT 2015-01-01, YearsCount 10, CutDateBefore 2021-05-18, CutDateAfter 2024-04-20; `csv-100k` = 100000 / 0.05 / 2015-01-01 / 10 / 2014-05-18 / 2024-04-20; `csv-1m` = 1000000 / 0.05; `csv-10m` = 10000000 / 0.80; `csv-100m` = 100000000 / 1.00 (same dates). Invocation: `DatabaseGenerator.exe config.json data.xlsx out\%1 cache param:OutputFormat=... param:OrdersCount=... param:CustomerPercentage=... param:StartDT=... param:YearsCount=... param:CutDateBefore=... param:CutDateAfter=...`.
* build_all.cmd zips each output with 7za (`-v500m` volumes for 100m).

# What it was used to decide
Row-count semantics (OrdersCount = orders) and reproduction recipe in [Contoso](/datasets/contoso.md) / [tool](/tools/contoso-data-generator-v2.md).
