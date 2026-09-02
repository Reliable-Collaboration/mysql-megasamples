---
type: Source
title: Microsoft Learn - Specify field and row terminators (SQL Server)
description: Authoritative statement that a terminator character occurring inside data is interpreted as a terminator (no quoting/escaping), the supported terminator forms (up to 10 printable chars, \t \n \r \0, 0x hex), and the CRLF-vs-LF behaviour of \n.
resource: https://learn.microsoft.com/en-us/sql/relational-databases/import-export/specify-field-and-row-terminators-sql-server
tags: [bcp, bulk-insert, docs]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/relational-databases/import-export/specify-field-and-row-terminators-sql-server
    title: Specify Field and Row Terminators (SQL Server) - SQL Server | Microsoft Learn
    accessed: 2026-09-02
    version: ms.date 2025-03-30, updated_at 2026-08-24, git commit 58c9ba7063458281263c05cba4e0e8dc7da7358a
---

# What was read
The full page.

# Relevant excerpt
> If a terminator character occurs within the data, the character is interpreted as a terminator, not as data, and the data after that character is interpreted as belonging to the next field or record. Therefore, choose your terminators carefully to make sure that they never appear in your data.
> String of up to 10 printable characters, including some or all of the terminators listed earlier (`**\t**`, `end`, `!!!!!!!!!!`, `\t-\n`, and so on)
> When you specify `\n` as a row terminator for bulk export, or implicitly use the default row terminator, bcp outputs a carriage return-line feed combination (CRLF) as the row terminator. If you want to output a line feed character only (LF) ... use hexadecimal notation to specify the LF row terminator. For example: `bcp -r '0x0A'`
> `FIELDTERMINATOR = '<field_terminator>'` ... The default is `\t` (tab character). `ROWTERMINATOR = '<row_terminator>'` ... The default is `\n` (newline character).

This explains the AdventureWorks install script's use of `'+|'` / `'&|\n'` for tables whose text contains tabs or newlines and `'0x0a'` for LF files, and confirms bcp offers no quoting - the executor must pick terminators that cannot occur in the data.

# What it was used to decide
[sqlcmd/bcp tool record](/tools/sqlcmd-bcp.md); [AdventureWorks OLTP](/datasets/adventureworks-oltp.md); [bcp export open question](/questions/mssql-bcp-linux-export-encoding-and-escaping.md).
