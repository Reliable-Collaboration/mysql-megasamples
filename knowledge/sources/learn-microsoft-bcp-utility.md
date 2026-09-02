---
type: Source
title: Microsoft Learn - bcp utility (reference)
description: Full option reference; establishes that -c uses tab/newline terminators with no quoting, that -C (code page, incl. 65001) and -N/-x/-V/-o/-i are Windows-only, that -w emits UTF-16 (nchar) with tab/\n terminators, and that Linux bcp uses tab and \n by default.
resource: https://learn.microsoft.com/en-us/sql/tools/bcp-utility
tags: [bcp, docs]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/tools/bcp-utility
    title: Bulk Copy with bcp Utility - SQL Server | Microsoft Learn (canonical tools/bcp/bcp-utility)
    accessed: "2026-09-02"
    version: ms.date 2026-08-11, updated_at 2026-08-24, git commit 3788e363569c9a5af042c9b4f688384852d2d144
---

# What was read
The full page (view=sql-server-ver17).

# Relevant excerpt
> ### Considerations for bcp on Linux and macOS - The field terminator is a tab (`\t`). - The line terminator is a newline (`\n`). - For SQL Server to SQL Server transfers, use native format (`-n`). Use character format (`-c`) only when the data crosses into a non-SQL Server system or when the data file shouldn't contain extended characters.
> `-c` Performs the operation using a character data type. ... It uses **char** as the storage type, without prefixes, and uses `\t` (tab character) as the field separator and `\r\n` (newline character) as the row terminator. `-c` isn't compatible with `-w`.
> `-C { ACP | OEM | RAW | code_page }` **Applies to**: Windows only. Not supported on Linux and macOS. ... Versions before SQL Server 2016 (13.x) don't support code page 65001 (UTF-8 encoding).
> `-w` Performs the bulk copy operation by using Unicode characters. ... It uses **nchar** as the storage type, no prefixes, `\t` (tab character) as the field separator, and `\n` (newline character) as the row terminator.
> `-t field_term` Specifies the field terminator. The default is `\t` (tab character). ... `-r row_term` Specifies the row terminator. The default is `\n` (newline character).
> `-k` Specifies that empty columns keep a null value ... `-E` Specifies that the operation uses identity values in the imported data file
> When the **`bcp`** utility extracts data, it represents an empty string as a null, and a null string as an empty string.
> `-Y[s|m|o]` **Applies to**: bcp version 18 and later ... `-Ym` (for `Mandatory`) is the default. `-u` ... Trust server certificate.
> `-G`, `-D`, `-K`, `-l`, `-H`, `-J`, `-T`, `-q`, `queryout` ... (option table also lists `-N`, `-x`, `-V`, `-i`, `-o`, `-h` as Windows-only).

The page says nothing about quoting or escaping field values - bcp has no quoting mode; see the terminators page for the consequence.

# What it was used to decide
[sqlcmd/bcp tool record](/tools/sqlcmd-bcp.md); [bcp export encoding/escaping open question](/questions/mssql-bcp-linux-export-encoding-and-escaping.md).
