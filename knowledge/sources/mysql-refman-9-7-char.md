---
type: Source
title: MySQL 9.7 Reference Manual — The CHAR and VARCHAR Types
description: CHAR is right-padded on storage and trailing spaces are stripped on retrieval; VARCHAR keeps trailing spaces; PAD SPACE vs NO PAD collations.
resource: https://dev.mysql.com/doc/refman/9.7/en/char.html
tags: [mysql, char, varchar, type-mapping]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/char.html
    title: The CHAR and VARCHAR Types
    accessed: 2026-09-02
---

# What was read
The manual page, 2026-09-02.

# Relevant excerpt
> When `CHAR` values are stored, they are right-padded with spaces to the specified length. ... When `CHAR` values are retrieved, trailing spaces are removed unless the `PAD_CHAR_TO_FULL_LENGTH` SQL mode is enabled.
>
> `VARCHAR` values are not padded when they are stored. Trailing spaces are retained when values are stored and retrieved, in conformance with standard SQL.
>
> `NO PAD` collations treat trailing spaces as significant in comparisons ... `PAD SPACE` collations treat trailing spaces as insignificant ... MySQL collations have a pad attribute of `PAD SPACE`, other than Unicode collations based on UCA 9.0.0 and higher, which have a pad attribute of `NO PAD`.

# What it was used to decide
Oracle `CHAR(n)` (blank-padded) maps to MySQL `CHAR(n)`, but a MySQL `CHAR(7)` returns `'2019-02'` without padding while Oracle returns the value padded to 7 — irrelevant for `CHAR(2)`/`CHAR(1)` codes that are always full length (HR/SH country and gender codes, SH `calendar_quarter_desc CHAR(7)` values are 7 characters). The default utf8mb4_0900_ai_ci collation is NO PAD, so trailing-space comparisons differ from Oracle only if data carried trailing spaces (none observed).
