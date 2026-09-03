---
type: Open Question
title: WideWorldImporters and WideWorldImportersDW - published row counts and loaded sizes do not exist; measure at export
description: No Microsoft page read publishes WWI row counts; the values in the dataset records are from memory and must be replaced by counts taken in SQL Server during the export step.
resource: /questions/mssql-wideworldimporters-row-counts.md
tags:
- open-question
- wideworldimporters
- row-counts
status: draft
trust: open
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
