---
type: Source
title: Microsoft Learn - Use Unicode character format to import or export data (bcp -w)
description: bcp -w writes UTF-16 with a 0xFFFE byte-order mark, tab/newline terminators; recommended when extended characters would be lost in -c.
resource: https://learn.microsoft.com/en-us/sql/relational-databases/import-export/use-unicode-character-format-to-import-or-export-data-sql-server
tags: [bcp, encoding, docs]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/relational-databases/import-export/use-unicode-character-format-to-import-or-export-data-sql-server
    title: Use Unicode Character Format to Import & Export Data - SQL Server | Microsoft Learn
    accessed: "2026-09-02"
    version: ms.date 2026-02-10, updated_at 2026-08-24, git commit 58c9ba7063458281263c05cba4e0e8dc7da7358a
---

# What was read
The full page.

# Relevant excerpt
> Unicode character format is recommended for bulk transfer of data between multiple instances of SQL Server by using a data file that contains extended/DBCS characters.
> Unicode character format data files follow the conventions for Unicode files. The first two bytes of the file are hexadecimal numbers, 0xFFFE. These bytes serve as byte-order marks (BOM)
> By default, the bcp utility separates the character-data fields with the tab character and terminates the records with the newline character.
> | `bcp` | `-w` | Uses the Unicode character format. | | `BULK INSERT` | `DATAFILETYPE ='widechar'` |

# What it was used to decide
[sqlcmd/bcp tool record](/tools/sqlcmd-bcp.md): `-w` output must be converted from UTF-16LE (BOM) to UTF-8 before `LOAD DATA`, or `-c` under a UTF-8 locale used instead.
