---
type: Source
title: "MySQL 9.7 Reference Manual: The DATE, DATETIME, and TIMESTAMP Types"
description: "DATETIME 1000-01-01 to 9999-12-31, TIMESTAMP 1970-01-01 00:00:01 to 2038-01-19 03:14:07 UTC (unchanged in 9.7), 6 fractional digits, TIMESTAMP time-zone conversion."
resource: https://dev.mysql.com/doc/refman/9.7/en/datetime.html
tags: [mysql, docs, temporal]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/datetime.html
    title: "MySQL 9.7 Reference Manual: The DATE, DATETIME, and TIMESTAMP Types"
    accessed: "2026-09-02"
    version: "MySQL 9.7 manual, section 13.2.2"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/datetime.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 13.2.2.

# Relevant excerpt
* DATETIME: `'1000-01-01 00:00:00'` to `'9999-12-31 23:59:59'` (with fractions `... 23:59:59.499999`); TIMESTAMP: `'1970-01-01 00:00:01'` UTC to `'2038-01-19 03:14:07'` UTC (no extended range is documented for 9.7); DATE: `'1000-01-01'` to `'9999-12-31'`.
* Fractional seconds up to microseconds (6 digits).
* TIMESTAMP: "MySQL converts values from the current time zone to UTC for storage, and back from UTC to the current time zone for retrieval"; DATETIME is not converted.
* Invalid values become the zero value `'0000-00-00 00:00:00'` depending on SQL mode; two-digit years 00-69 → 2000-2069, 70-99 → 1970-1999.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): SQL Server `9999-12-31 23:59:59.9999999` temporal end dates round to the DATETIME maximum, not beyond (converters clamp to `9999-12-31 23:59:59.999999`); Oracle dates before year 1000 and SQL Server `datetime2` year 0001 are outside DATETIME and are recorded per dataset; TIMESTAMP is avoided for source values after 2038.
