---
type: Source
title: Microsoft Learn - Generate data in WideWorldImporters
description: Documents that the released databases contain data from 2013-01-01 to the generation date and how DataLoadSimulation.PopulateDataToCurrentDate and Application.Configuration_PopulateLargeSaleTable extend it (randomised, non-deterministic).
resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-generate-data
tags:
- wideworldimporters
- docs
- data-generation
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-generate-data
  title: Generate data in SQL samples WideWorldImporters - SQL Server | Microsoft Learn
  accessed: "2026-09-02"
  version: ms.date 2020-10-23, updated_at 2025-05-30, git commit 67ebe15c092655bcc23eeca30a2effef022a6ed6
---

# What was read
The full page.

# Relevant excerpt
> The released versions of the WideWorldImporters and WideWorldImportersDW databases have data from January 1, 2013, up to the day that the databases were generated.
> `EXECUTE DataLoadSimulation.PopulateDataToCurrentDate @AverageNumberOfCustomerOrdersPerDay = 60, @SaturdayPercentageOfNormalWorkDay = 50, @SundayPercentageOfNormalWorkDay = 0, @IsSilentMode = 1, @AreDatesPrinted = 1;`
> Because of a random factor in the data generation, there are some differences in the data that's generated between runs.
> `Application.Configuration_PopulateLargeSaleTable` ... `@EstimatedRowsFor2012` bigint (with a default of 12000000) ... The rows are inserted in the 2012 calendar year ... The procedure artificially limits the number of rows to 50,000 per day.

For the DW: `EXECUTE [Application].Configuration_ReseedETL` then run the *Daily ETL.ispac* SSIS package.

# What it was used to decide
[WideWorldImporters](/datasets/wideworldimporters.md) and [DW](/datasets/wideworldimporters-dw.md): the shipped .bak is the only reproducible dataset; regeneration is random and needs SQL Server + SSIS, so the conversion path is "restore the .bak once, export, and pin the exported artifact".
