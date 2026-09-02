---
type: Source
title: "MySQL 9.7 Reference Manual: Miscellaneous Functions (UUID, UUID_TO_BIN, BIN_TO_UUID, IS_UUID)"
description: "UUID_TO_BIN returns VARBINARY(16); the swap_flag reorders time-low/time-high for index locality; IS_UUID accepts dashed, undashed and braced forms."
resource: https://dev.mysql.com/doc/refman/9.7/en/miscellaneous-functions.html
tags: [mysql, docs, uuid]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/miscellaneous-functions.html
    title: "MySQL 9.7 Reference Manual: Miscellaneous Functions (UUID, UUID_TO_BIN, BIN_TO_UUID, IS_UUID)"
    accessed: 2026-09-02
    version: "MySQL 9.7 manual, section 14.25"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/miscellaneous-functions.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 14.25.

# Relevant excerpt
* `UUID()` returns a version-1 UUID as a utf8mb3 string `aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee`.
* `UUID_TO_BIN(string_uuid [, swap_flag])`: "The return binary UUID is a VARBINARY(16) value"; with swap_flag 1 "The time-low and time-high parts ... are swapped. This moves the more rapidly varying part to the right and can improve indexing efficiency if the result is stored in an indexed column." "Time-part swapping assumes the use of UUID version 1 values ... For UUID values produced by other means that do not follow version 1 format, time-part swapping provides no benefit."
* `BIN_TO_UUID(binary_uuid [, swap_flag])` is the inverse; mismatched flags corrupt the round trip.
* `IS_UUID()` accepts `aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee`, `aaaaaaaabbbbccccddddeeeeeeeeeeee` and `{aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee}`.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): SQL Server `uniqueidentifier` (version-4 style GUIDs) → `BINARY(16)` via `UUID_TO_BIN(@v)` without swap (swap gives no benefit for non-v1 values), with `BIN_TO_UUID(col)` in demo views; the checksum canonical form is lowercase hex of the 16 bytes.
