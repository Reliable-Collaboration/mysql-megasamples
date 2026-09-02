---
type: Source
title: "MySQL 9.7 Reference Manual: Aggregate Functions"
description: Definitions of BIT_XOR, SUM, COUNT(DISTINCT), GROUP_CONCAT and their NULL handling; the basis for the per-table checksum design.
resource: https://dev.mysql.com/doc/refman/9.7/en/aggregate-functions.html
tags: [mysql, docs, testing]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:19:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:19:13Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/aggregate-functions.html
    title: "MySQL 9.7 Reference Manual: Aggregate Functions"
    accessed: "2026-09-02"
---
# What was read
* https://dev.mysql.com/doc/refman/9.7/en/aggregate-functions.html, “MySQL 9.7 Reference Manual: Aggregate Functions”, accessed 2026-09-02

# Relevant excerpt
* BIT_XOR: "Returns the bitwise XOR of all bits in expr." "Numeric evaluation occurs otherwise, with argument value conversion to unsigned 64-bit integers as necessary." "Binary-string evaluation produces a binary string of the same length as the argument values ... If the argument size exceeds 511 bytes, an ER_INVALID_BITWISE_AGGREGATE_OPERANDS_SIZE error occurs." "NULL values do not affect the result unless all values are NULL." Empty set → neutral value (all bits 0).
* SUM: "return a DECIMAL value for exact-value arguments (integer or DECIMAL), and a DOUBLE value for approximate-value arguments (FLOAT or DOUBLE)"; returns NULL for no rows.
* COUNT(DISTINCT): "Returns a count of the number of rows with different non-NULL expr values."
* GROUP_CONCAT: "The result is truncated to the maximum length that is given by the group_concat_max_len system variable, which has a default value of 1024" — therefore GROUP_CONCAT is unsuitable for whole-table hashes.
* "Unless otherwise stated, aggregate functions ignore NULL values."

# What it was used to decide
[Per-table checksum method](/decisions/test-checksum-method.md): use BIT_XOR and SUM over a per-row 64-bit digest rather than GROUP_CONCAT.
