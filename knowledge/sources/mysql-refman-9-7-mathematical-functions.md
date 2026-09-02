---
type: Source
title: "MySQL 9.7 Reference Manual: Mathematical Functions"
description: CONV, CRC32 and ROUND semantics used by the checksum and sample-comparison design.
resource: https://dev.mysql.com/doc/refman/9.7/en/mathematical-functions.html
tags: [mysql, docs, testing]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:21:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:21:00Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/mathematical-functions.html
    title: "MySQL 9.7 Reference Manual: Mathematical Functions"
    accessed: 2026-09-02
---

# Relevant excerpt
* CONV: "Returns a string representation of the number N, converted from base from_base to base to_base. Returns NULL if any argument is NULL ... If from_base is a negative number, N is regarded as a signed number. Otherwise, N is treated as unsigned. CONV() works with 64-bit precision."
* CRC32: "Computes a cyclic redundancy check value and returns a 32-bit unsigned value. The result is NULL if the argument is NULL."
* ROUND on exact values: "round half away from zero"; on approximate values "the result depends on the C library. On many systems, this means that ROUND() uses the round to nearest even rule" — example `ROUND(2.5)=3`, `ROUND(25E-1)=2`.

# What it was used to decide
[Per-table checksum method](/decisions/test-checksum-method.md): `CONV(SUBSTRING(SHA2(x,256),1,16),16,10)` yields an unsigned 64-bit integer; floats are never rounded inside MySQL for comparison — they are formatted with 15 significant digits on both sides instead, because ROUND on DOUBLE is C-library dependent.
