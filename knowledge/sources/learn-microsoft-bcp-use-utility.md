---
type: Source
title: Microsoft Learn - How to use the bcp utility (examples and best practices)
description: Character-mode best practices (terminator collisions, use long unique terminators), computed-column behaviour on import/export, queryout examples, and the note that the row terminator is always appended.
resource: https://learn.microsoft.com/en-us/sql/tools/bcp/bcp-use-utility
tags: [bcp, docs]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/tools/bcp/bcp-use-utility
    title: How to Use the bcp Utility - SQL Server | Microsoft Learn
    accessed: 2026-09-02
    version: ms.date 2026-06-25, updated_at 2026-08-24, git commit 3788e363569c9a5af042c9b4f688384852d2d144
---

# What was read
The full page.

# Relevant excerpt
> (Administrator/User) When possible, use native format (`-n`) to avoid the separator issue. ... Export data from SQL Server using the `-c` or `-w` option if you plan to export the data to a non-SQL Server database.
> (Administrator) Verify data when using `bcp out`. ... verify that the data is properly exported and the terminator values aren't used as part of some data value. Consider overriding the default terminators (using `-t` and `-r` options) with random hexadecimal values to avoid conflicts between terminator values and data values.
> (User) Use a long and unique terminator (any sequence of bytes or characters) to minimize the possibility of a conflict with the actual string value.
> Values in the data file being imported for computed or **timestamp** columns are ignored ... Computed and **timestamp** columns are bulk copied from SQL Server to a data file as usual.
> `bcp "SELECT FullName, PreferredName FROM WideWorldImporters.Application.People ORDER BY FullName" queryout D:\bcp\People.txt -t, -c -T`
> The row terminator is always added, even to the last record. The field terminator, however, isn't added to the last field.
> `bcp MyTable in "D:\data.csv" -T -c -C 65001 -t , ...` (code page example; -C is Windows-only per the reference page)

# What it was used to decide
[sqlcmd/bcp tool record](/tools/sqlcmd-bcp.md); [bcp export open question](/questions/mssql-bcp-linux-export-encoding-and-escaping.md).
