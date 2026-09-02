---
type: Source
title: Microsoft Learn - ODBC Driver for SQL Server on Linux/macOS programming guidelines (character set support)
description: The ODBC driver (which bcp and ODBC sqlcmd use) encodes narrow-character data in the process locale's encoding and defaults to UTF-8 (including in the "C" locale); SQLWCHAR is UTF-16LE.
resource: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/programming-guidelines
tags: [odbc, encoding, bcp, docs]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/programming-guidelines
    title: Programming guidelines - ODBC Driver for SQL Server | Microsoft Learn
    accessed: "2026-09-02"
    version: ms.date 2022-02-17, updated_at 2026-08-24, git commit b327fa345801101e505260268af60a60ca2ab4bb
---

# What was read
The full page; the "Character Set Support" section is the relevant part.

# Relevant excerpt
> For ODBC Driver 13 and 13.1, SQLCHAR data must be UTF-8. No other encodings are supported.
> For ODBC Driver 17, SQLCHAR data in one of the following character sets/encodings is supported: UTF-8, CP437, CP850, ... ISO-8859-15
> Upon connection, the driver detects the current locale of the process it's loaded in. If it uses one of the encodings above, the driver uses that encoding for SQLCHAR (narrow-character) data; otherwise, it defaults to UTF-8. Since all processes start in the "C" locale by default (and cause the driver to default to UTF-8) ...
> SQLWCHAR data must be UTF-16LE (Little Endian).
> ... data loss is possible --- characters in the source encoding not representable in the target encoding will convert to a question mark ('?'). ... ensure that the client encoding can represent all the characters of the source data (this representation is always possible with UTF-8.)

# What it was used to decide
[sqlcmd/bcp tool record](/tools/sqlcmd-bcp.md): on Linux, `bcp -c` under `LANG=C`/`C.UTF-8`/`en_US.UTF-8` produces UTF-8 output without needing `-C 65001` (which is Windows-only). Still marked for a one-line verification in the [open question](/questions/mssql-bcp-linux-export-encoding-and-escaping.md) because bcp's own page is silent.
