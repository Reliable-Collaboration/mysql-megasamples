---
type: Source
title: Oracle Database 23 SQL Language Reference — Data Types
description: Authoritative statements on NUMBER precision/scale, DATE contents, VARCHAR2 limits, TIMESTAMP WITH LOCAL TIME ZONE normalisation and CHAR padding used for the Oracle-to-MySQL type mapping.
resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/Data-Types.html
tags: [oracle, data-types, type-mapping]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/Data-Types.html
    title: Data Types (SQL Language Reference 23)
    accessed: "2026-09-02"
---

# What was read
The Data Types chapter, 2026-09-02.

# Relevant excerpt
* NUMBER: "The precision `p` can range from 1 to 38." "The scale `s` can range from -84 to 127." "Specify a floating-point number using the following form: `NUMBER`. The absence of precision and scale designators specifies the maximum range and precision for an Oracle number." "Oracle guarantees the portability of numbers with precision of up to 20 base-100 digits, which is equivalent to 39 or 40 decimal digits depending on the position of the decimal point."
* DATE: "For each `DATE` value, Oracle stores the following information: year, month, day, hour, minute, and second." "This data type contains the datetime fields `YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`, and `SECOND`. It does not have fractional seconds or a time zone."
* VARCHAR2 maximum: "32767 bytes if `MAX_STRING_SIZE` `=` `EXTENDED`; 4000 bytes if `MAX_STRING_SIZE` `=` `STANDARD`".
* TIMESTAMP WITH LOCAL TIME ZONE: "Data is normalized to the database time zone when it is stored in the database. When the data is retrieved, users see the data in the session time zone."
* CHAR: "If you insert a value that is shorter than the column length, then Oracle blank-pads the value to column length."

# What it was used to decide
The type-mapping tables in [HR](/datasets/oracle-hr.md), [CO](/datasets/oracle-co.md), [SH](/datasets/oracle-sh.md), [OE](/datasets/oracle-oe-pm-ix.md): unconstrained NUMBER has no fixed precision, so the mapping must be data-driven; Oracle DATE is a DATETIME-class type; TSLTZ values must be exported in an explicit zone.
