---
type: Source
title: SQL*Plus User's Guide — Continuing a Long Command on Additional Lines
description: A hyphen at the end of a line is a continuation character; SQL*Plus joins the lines and removes the hyphen before the statement is parsed as SQL.
resource: https://docs.oracle.com/database/121/SQPUG/ch_four.htm
tags:
- oracle
- sqlplus
- oe
- parsing
status: stable
trust: verified
generated:
  by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
sources:
- resource: https://docs.oracle.com/database/121/SQPUG/ch_four.htm
  title: SQL*Plus Basics — "Continuing a Long SQL*Plus Command on Additional Lines"
  accessed: "2026-09-03"
---

# What was read
The "SQL*Plus Basics" chapter, section "Continuing a Long SQL*Plus Command on Additional Lines", 2026-09-03.

# Relevant excerpt
* "You can continue a long SQL*Plus command by typing a hyphen at the end of the line and pressing Return. If you wish, you can type a space before typing the hyphen."
* "Since SQL*Plus identifies the hyphen as a continuation character, entering a hyphen within a SQL statement is ignored by SQL*Plus. **SQL*Plus does not identify the statement as a SQL statement until after the input processing has joined the lines together and removed the hyphen.**"

# What it was used to decide
How `datasets/oracle_oe/oeparse.py` reassembles the Order Entry scripts before parsing them.

The Oracle Order Entry data files are written entirely in this style — 76,831 continuations across the
scripts — including inside string literals, so the join decides what 11,140 rows of text say. The page
establishes that the hyphen is consumed and the lines are joined, but does not state whether a space
takes its place. That was settled empirically instead; see
[the OE record](/datasets/oracle-oe-pm-ix.md) and
[the independent export](/sources/oe-independent-export-sql-problems.md).
