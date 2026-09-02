---
type: Source
title: MySQL 9.7 Reference Manual — The JSON Data Type
description: JSON columns validate on insert, store a binary form with sorted keys where the last duplicate key wins, are size-limited by max_allowed_packet and are indexable only through generated columns.
resource: https://dev.mysql.com/doc/refman/9.7/en/json.html
tags: [mysql, json, type-mapping]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/json.html
    title: The JSON Data Type
    accessed: 2026-09-02
---

# What was read
The manual page, 2026-09-02.

# Relevant excerpt
* "Automatic validation of JSON documents stored in JSON columns. Invalid documents produce an error." (`ERROR 3140 (22032): Invalid JSON text`).
* Storage: "converted to an internal binary format that permits quick read access to document elements"; keys of objects are sorted; for duplicate keys the last value wins (`JSON_OBJECT('key1', 1, 'key2', 'abc', 'key1', 'def')` → `{"key1": "def", "key2": "abc"}`).
* "The size of any JSON document stored in a `JSON` column is limited to the value of the `max_allowed_packet` system variable."
* "JSON columns, like columns of other binary types, are not indexed directly; instead, you can create an index on a generated column that extracts a scalar value from the JSON column."

# What it was used to decide
[CO dataset record](/datasets/oracle-co.md): `products.product_details` (Oracle `BLOB CHECK (... IS JSON)`) → MySQL `JSON`; key order in output will differ from Oracle's textual storage (cosmetic); a JSON-normalised checksum is needed for the test baseline ([question](/questions/oracle-co-json-and-timestamp-fidelity.md)).
