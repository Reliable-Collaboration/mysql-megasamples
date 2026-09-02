---
type: Decision
title: Row-count, sample, and aggregate-checksum test method
description: A single canonical row-digest definition computed identically in Python on the source side and in SQL on the MySQL side, aggregated order-independently with BIT_XOR and SUM, plus per-column aggregates and deterministic samples.
resource: /decisions/test-checksum-method.md
tags: [decision, testing, checksum]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:40:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:40:00Z" }
sources:
  - resource: /sources/mysql-refman-9-7-aggregate-functions.md
    accessed: 2026-09-02
  - resource: /sources/mysql-refman-9-7-encryption-functions.md
    accessed: 2026-09-02
  - resource: /sources/mysql-refman-9-7-mathematical-functions.md
    accessed: 2026-09-02
  - resource: /sources/mysql-refman-9-7-checksum-table.md
    accessed: 2026-09-02
  - resource: /sources/mysql-refman-9-7-information-schema-tables.md
    accessed: 2026-09-02
  - resource: /sources/percona-pt-table-checksum-docs.md
    accessed: 2026-09-02
---

# Question
How do we prove, for every table, that what landed in MySQL equals what the source contained, without relying on engine-specific checksums?

# Options considered
1. `CHECKSUM TABLE` — rejected for cross-system comparison: depends on row format and engine ([doc](/sources/mysql-refman-9-7-checksum-table.md)); kept as a same-version build fingerprint.
2. `GROUP_CONCAT` of all rows then `SHA2` — rejected: truncated at `group_concat_max_len` (default 1024) ([doc](/sources/mysql-refman-9-7-aggregate-functions.md)).
3. **Per-row canonical digest aggregated with `BIT_XOR` and `SUM`** (chosen): order-independent, streamable, and computable outside MySQL because the canonical form is defined in plain text.

# Canonical row form (`scripts/canon.py` and the generated SQL must agree byte-for-byte)
Columns in DDL order, joined by `\x1f` (unit separator), with each value rendered as:

| Source type class | Canonical text | MySQL expression |
|---|---|---|
| NULL | `\N` | `COALESCE(<expr>, '\\N')` wrapping each expression below |
| integer, BIT, BOOLEAN | decimal digits, `-` sign | `CAST(col AS CHAR)` |
| DECIMAL(p,s) / money / NUMBER(p,s) | fixed `s` decimals, no thousands separators | `CAST(col AS CHAR)` (MySQL prints declared scale) |
| FLOAT/DOUBLE/unconstrained NUMBER | `repr` with 15 significant digits: Python `format(x, '.15g')` | `FORMAT` is locale-bound, so use `CAST(CAST(col AS DECIMAL(65,15)) AS CHAR)` **only** for datasets where the plan declares 15-decimal comparability; otherwise the float column is excluded from the digest and compared through `SUM`/`MIN`/`MAX` with tolerance 1e-9 relative |
| DATE | `YYYY-MM-DD` | `CAST(col AS CHAR)` |
| DATETIME / TIMESTAMP | `YYYY-MM-DD HH:MM:SS.ffffff` always 6 fractional digits, UTC for offset-bearing sources | `DATE_FORMAT(col, '%Y-%m-%d %H:%i:%s.%f')` |
| TIME | `HH:MM:SS.ffffff` | `DATE_FORMAT(col, '%H:%i:%s.%f')` |
| CHAR/VARCHAR/TEXT | the string as-is; trailing whitespace preserved on both sides unless the dataset record says the source type pads (SQL Server `char`, Oracle `CHAR`) in which case both sides `RTRIM` | `col` (or `RTRIM(col)`) |
| BINARY/BLOB/geometry WKB/uniqueidentifier | lowercase hex | `LOWER(HEX(col))`; geometry: `LOWER(HEX(ST_AsBinary(col)))` |
| JSON/XML | the exact source text (no reformatting) stored in a TEXT column; JSON columns compare `JSON_UNQUOTE(JSON_EXTRACT(...))`? **No** — JSON columns are stored as `JSON` and compared via `SHA2(CAST(col AS CHAR),256)` after normalising the source with `json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)`; MySQL's JSON output ordering is engine-defined, so the digest uses the Python-normalised text stored in a shadow `_canon` step only in the test harness, not in the table |

Row digest: `d = CONV(SUBSTRING(SHA2(row_text, 256), 1, 16), 16, 10)` → unsigned 64-bit ([SHA2](/sources/mysql-refman-9-7-encryption-functions.md), [CONV 64-bit](/sources/mysql-refman-9-7-mathematical-functions.md)). Python: `int(hashlib.sha256(row_text.encode('utf-8')).hexdigest()[:16], 16)`.

Table fingerprint: `(COUNT(*), BIT_XOR(d), SUM(d) MOD 18446744073709551616)`; BIT_XOR alone cancels duplicated rows, SUM alone is order-sensitive to nothing but catches duplicates, so both are recorded. `SUM` returns DECIMAL for integer arguments ([doc](/sources/mysql-refman-9-7-aggregate-functions.md)) so it does not overflow; the Python side keeps a Python int and reduces mod 2^64.

# Companion checks per column (cheap, catch truncation/coercion)
`COUNT(col)`, `COUNT(DISTINCT col)`, `MIN`, `MAX`, and for text `SUM(CHAR_LENGTH(col))` and `SUM(LENGTH(col))` (byte length exposes charset mistakes: a Latin-1-loaded `é` is 1 byte, a proper utf8mb4 `é` is 2). Numeric columns add `SUM(col)`.

# Deterministic samples
First 20 and last 20 rows by primary key plus every row whose `CRC32(pk_text) % 997 = 0` capped at 50; compared column by column against the source values written to `build/baseline.json`. Tables without a natural key use the surrogate key assigned by the loader, so the sample is reproducible only when load order is deterministic (all converters sort by the source file order).

# Baseline production
The converter itself writes `build/baseline.json` as it streams rows (count, xor, sum, per-column aggregates, sampled rows) so the baseline is computed from the exact typed values that were emitted, before any MySQL involvement. For datasets converted by a native product export (SQL Server, Oracle) the baseline query runs inside that product with the same canonical rules expressed in T-SQL/PL-SQL, generated from the same column map.

# Row counts
Always `SELECT COUNT(*)`; `information_schema.TABLES.TABLE_ROWS` is an estimate that "may vary ... by as much as 40% to 50%" ([doc](/sources/mysql-refman-9-7-information-schema-tables.md)).

# Status
accepted
