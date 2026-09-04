---
type: Open Question
title: WideWorldImporters and WideWorldImportersDW - published row counts and loaded sizes do not exist; measure at export
description: No Microsoft page read publishes WWI row counts; the dataset records' values were inferred and had to be replaced by counts taken in SQL Server during the export step. Answered on 2026-09-03 - all 19 OLTP figures were exact, 4 of the DW's 14 were not.
resource: /questions/mssql-wideworldimporters-row-counts.md
tags:
- open-question
- wideworldimporters
- row-counts
status: deprecated
trust: verified
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-oltp-database-catalog
  title: WWI OLTP catalog (no counts)
  accessed: "2026-09-02"
- resource: https://learn.microsoft.com/en-us/sql/samples/wide-world-importers-dw-database-catalog
  title: WWI DW catalog (no counts)
  accessed: "2026-09-02"
---

# Question
What are the per-table row counts, the `_Archive` history sizes, the total data size (`sp_spaceused`) and the date range (`MIN/MAX(OrderDate)`, `MAX(RecordedWhen)`) in `WideWorldImporters-Standard.bak` and `WideWorldImportersDW-Standard.bak` (v1.0, 2016-06-08)? Is the Standard data identical to the Full data (same generation run)?

# Cheapest experiment
In the export job ([decision](/decisions/mssql-wideworldimporters-conversion-path.md)), after `RESTORE DATABASE`, run `SELECT s.name, t.name, SUM(p.rows) FROM sys.tables t JOIN sys.schemas s ON ... JOIN sys.partitions p ON p.object_id=t.object_id AND p.index_id IN (0,1) GROUP BY ...` and `EXEC sp_spaceused` and store the output next to the export artifact; optionally restore the Full .bak in the same session and diff the count table. One container run (~5 minutes).

# Resolves
`# Tests and expected values` and `# Tier assignment` in [WideWorldImporters](/datasets/wideworldimporters.md) and [WideWorldImportersDW](/datasets/wideworldimporters-dw.md).

# Answer (2026-09-03, task X-02)
Measured after restoring both Standard backups. **WideWorldImporters: 48 tables, 4,713,833 rows**,
633.7 MB loaded in MySQL. **WideWorldImportersDW: 29 tables in the backup, 16 kept, 923,643 rows**,
249.9 MB loaded. Per-table counts are in
`datasets/wideworldimporters*/tests/expected_counts.yaml`, generated from `sys.partitions` inside the
restored backup, so the checked-in expectation is the source's own count rather than a figure read
back from MySQL.

Date range: `2013-01-01` to `2016-05-31` in both. The largest table by far is
`ColdRoomTemperatures_Archive` at 3,654,736 rows; its current table holds 4.

Scoring the records' from-memory figures: **every one of the OLTP's nineteen was exact**; four of the
DW's fourteen were wrong, all because slowly-changing dimensions carry versioned rows and an "Unknown"
member (`Fact.Transaction` 99,585 not 91,109; `Dimension.Supplier` 28 not 13; `Payment Method` 6 not 4;
`Transaction Type` 15 not 8). Details in [WideWorldImporters](/datasets/wideworldimporters.md) and
[WideWorldImportersDW](/datasets/wideworldimporters-dw.md).

Standard versus Full was not compared: only the Standard backups were restored, so "is the Standard
data identical to the Full data" remains unanswered and is not worth a second 1.3 GB pull.
