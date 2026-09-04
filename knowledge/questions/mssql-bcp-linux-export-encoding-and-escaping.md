---
type: Open Question
title: bcp on Linux - confirm UTF-8 output with -c, the NULL/empty-string sentinel, safe multi-character terminators, and the 2022 container's bcp flag set
description: Documentation establishes that -C is Windows-only, the ODBC driver defaults narrow data to UTF-8, and bcp never quotes; the concrete command line for exporting WWI NVARCHAR(MAX)/JSON/geography columns losslessly has not been executed.
resource: /questions/mssql-bcp-linux-export-encoding-and-escaping.md
tags:
- open-question
- bcp
- encoding
- wideworldimporters
status: deprecated
trust: verified
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://learn.microsoft.com/en-us/sql/tools/bcp-utility
  title: bcp reference (-C Windows-only; -Y/-u need bcp 18)
  accessed: "2026-09-02"
- resource: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/programming-guidelines
  title: ODBC driver character set support (UTF-8 default)
  accessed: "2026-09-02"
- resource: https://learn.microsoft.com/en-us/sql/relational-databases/import-export/specify-field-and-row-terminators-sql-server
  title: terminator rules (no quoting)
  accessed: "2026-09-02"
---

# Question
1. Does `LC_ALL=C.UTF-8 /opt/mssql-tools18/bin/bcp ... -c` inside `mcr.microsoft.com/mssql/server:2022-<CU>` emit UTF-8 for `nvarchar` data containing e.g. `Côte d'Ivoire` and CJK product names, with no `?` substitutions?
2. Which bcp version ships in the 2022 container (`bcp -v`), and does it accept `-u`/`-Yo` (bcp 18) or only the ODBC 17 style (encryption optional by default)?
3. Do `-t '|~|' -r '|~~|\n'` (or hex `-t 0x1F -r 0x1E0A`) survive every WWI text value (comments, JSON, delivery instructions) and load cleanly with `LOAD DATA ... FIELDS TERMINATED BY ... ESCAPED BY '' LINES TERMINATED BY ...`?
4. Does `ISNULL(col, '\N')` in `queryout` plus MySQL's `\N` convention restore NULL vs empty string correctly, given bcp writes NULL as empty and empty as NULL in `-c` mode?

# Cheapest experiment
One container run: restore `WideWorldImportersDW-Standard.bak` (54 MB, smaller than OLTP), export `Dimension.City` (has geography + accents) and `Dimension.[Stock Item]` with the proposed flags, `file`/`iconv -f UTF-8` the output, load into a scratch MySQL 9.7, and compare `COUNT(*)`, `COUNT(col IS NULL)` and a `SHA2(GROUP_CONCAT(...))` digest against the same digest computed in SQL Server (`HASHBYTES`). Also try the alternative of `sqlcmd -Q "SELECT ... FOR JSON PATH" -y0 -h -1` for the worst-case table to compare simplicity.

# Resolves
Export command in [sqlcmd/bcp tool record](/tools/sqlcmd-bcp.md) and the [WWI conversion decision](/decisions/mssql-wideworldimporters-conversion-path.md).

# Answer (2026-09-03, task X-02)
All four parts, measured against SQL Server 2022 CU26 over both WWI databases (77 tables, 5.6 M rows).
Recorded in full in the [sqlcmd/bcp record](/tools/sqlcmd-bcp.md).

1. **UTF-8: yes.** `LC_ALL=C.UTF-8 bcp ... -c` emitted `Côte d'Ivoire`, `São Tomé and Principe` and
   `Türkiye` intact, with no `?` substitution anywhere. Checked across every column, not by sampling:
   the export records a per-column count of rows containing any character outside printable ASCII, and
   the converter re-derives it from the parsed file.
2. **bcp 18.6.0002.1**, and it accepts `-u`.
3. **`-t 0x1f -r 0x1e0a` survived every value.** Verified rather than assumed — each row is checked to
   split into exactly its column count.
4. **A sentinel is not enough; the value needs the tag.** `ISNULL(col, <sentinel>)` fails on this
   data: four `Purchasing.Suppliers` rows hold a single NUL character as their value, so a
   lone-NUL-means-NULL convention read four real values as NULL. `ISNULL(NCHAR(1) + <render>, NCHAR(0))`
   works for any value at all. The mistake was caught by the per-column non-null counts, before
   anything was loaded.

One thing the question did not anticipate: `sqlcmd -y 0` is mutually exclusive with both `-h` and
`-W`, so every data-returning query goes through `bcp` instead.
