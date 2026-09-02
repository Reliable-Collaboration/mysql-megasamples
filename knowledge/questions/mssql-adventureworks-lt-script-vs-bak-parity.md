---
type: Open Question
title: Does the 2012 AdventureWorksLT script zip produce the same data as the LT2016-LT2022 .bak files (and how does LT2025 differ)?
description: The only SQL-Server-free form of AdventureWorksLT is the 2012 release zip; the README says 2012-2022 AdventureWorks builds differ only in name/compatibility level, and 2025 adjusted dates, but this was stated for the OLTP database, not explicitly for LT.
resource: /questions/mssql-adventureworks-lt-script-vs-bak-parity.md
tags: [open-question, adventureworks-lt]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/README.md
    title: adventure-works README (release history statements)
    accessed: "2026-09-02"
  - resource: https://github.com/microsoft/sql-server-samples/releases/download/adventureworks2012/adventure-works-2012-oltp-lt-script.zip
    title: LT 2012 script zip
    accessed: "2026-09-02"
---

# Question
Are the 12 tables / 3,277 rows in `adventure-works-2012-oltp-lt-script.zip` identical (modulo dates) to `AdventureWorksLT2022.bak` (8,511,488 B) and `AdventureWorksLT2025.bak` (1,765,376 B)? The LT2025 .bak is 5x smaller than LT2022, which may reflect compression/compat level rather than content.

# Cheapest experiment
Restore `AdventureWorksLT2022.bak` and `AdventureWorksLT2025.bak` once in the [SQL Server container](/tools/mssql-server-container.md) (amd64), run `SELECT COUNT(*)`, `CHECKSUM_AGG(BINARY_CHECKSUM(*))` and `MIN/MAX(OrderDate)` per table, and compare with the CSV-derived MySQL load. If LT2025 differs only in dates, ship the 2012 data and document; if content differs, switch LT to the .bak/bcp path (it is tiny).

# Resolves
[AdventureWorks LT](/datasets/adventureworks-lt.md) source-version statement and the [conversion decision](/decisions/mssql-adventureworks-conversion-path.md).
