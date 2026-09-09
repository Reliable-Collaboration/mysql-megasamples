---
type: Decision
title: Row-count, sample, and aggregate-checksum test method
description: A single canonical row-digest definition computed identically in Python on the source side and in SQL on the MySQL side, aggregated order-independently with BIT_XOR and SUM, plus per-column aggregates and deterministic samples.
resource: /decisions/test-checksum-method.md
tags:
- decision
- testing
- checksum
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:40:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:40:00Z"
sources:
- resource: /sources/mysql-refman-9-7-aggregate-functions.md
  accessed: "2026-09-02"
- resource: /sources/mysql-refman-9-7-encryption-functions.md
  accessed: "2026-09-02"
- resource: /sources/mysql-refman-9-7-mathematical-functions.md
  accessed: "2026-09-02"
- resource: /sources/mysql-refman-9-7-checksum-table.md
  accessed: "2026-09-02"
- resource: /sources/mysql-refman-9-7-information-schema-tables.md
  accessed: "2026-09-02"
- resource: /sources/percona-pt-table-checksum-docs.md
  accessed: "2026-09-02"
---

# Question
How do we prove, for every table, that what landed in MySQL equals what the source contained, without relying on engine-specific checksums?

# Options considered
1. `CHECKSUM TABLE` — rejected for cross-system comparison: depends on row format and engine ([doc](/sources/mysql-refman-9-7-checksum-table.md)); kept as a same-version build fingerprint.
2. `GROUP_CONCAT` of all rows then `SHA2` — rejected: truncated at `group_concat_max_len` (default 1024) ([doc](/sources/mysql-refman-9-7-aggregate-functions.md)).
3. **Per-row canonical digest aggregated with `BIT_XOR` and `SUM`** (chosen): order-independent, streamable, and computable outside MySQL because the canonical form is defined in plain text.

# Evidence
* [Aggregate functions](/sources/mysql-refman-9-7-aggregate-functions.md): BIT_XOR numeric evaluation, SUM return types, GROUP_CONCAT truncation.
* [Encryption functions](/sources/mysql-refman-9-7-encryption-functions.md): SHA2 returns a hex string.
* [Mathematical functions](/sources/mysql-refman-9-7-mathematical-functions.md): CONV returns a string with 64-bit precision; ROUND on DOUBLE is C-library dependent.
* [CHECKSUM TABLE](/sources/mysql-refman-9-7-checksum-table.md), [TABLES](/sources/mysql-refman-9-7-information-schema-tables.md).

# Canonical row form (`megasamples/canon.py` and the generated SQL must agree byte-for-byte)
Columns in DDL order, joined by the unit separator U+001F, with each value rendered as below. **The separator must be written as `CHAR(31)` (or `0x1F`) in SQL and `\x1f` in Python — never as `'\x1f'` in a MySQL string literal**: MySQL drops the backslash before an unrecognised escape, so `'a\x1fb'` is the six characters `ax1fb` (`HEX()` = `6178316662`), silently producing a digest that can never match the Python baseline. Verified 2026-09-02 on `mysql:9.7.2`: `SHA2(CONCAT('a',CHAR(31),'b'),256)` and Python `hashlib.sha256(b"a\x1fb")` both give `17315457580335015581` after the CONV/CAST reduction.

| Source type class | Canonical text | MySQL expression |
|---|---|---|
| NULL | `CHAR(0)` (U+0000). **Not** `\N`: MySQL strips the backslash before an unrecognised escape, so `'\N'` in a SQL literal is the single character `N` and collides with a real `N` value — the same trap as the separator. Python uses `"\x00"` | `COALESCE(<expr>, '\\N')` wrapping each expression below |
| integer, BIT, BOOLEAN | decimal digits, `-` sign | `CAST(col AS CHAR)` |
| DECIMAL(p,s) / money / NUMBER(p,s) | fixed `s` decimals, no thousands separators | `CAST(col AS CHAR)` (MySQL prints declared scale) |
| FLOAT/DOUBLE/unconstrained NUMBER | **excluded from the row digest**; compared per column through `COUNT`, `MIN`, `MAX`, `SUM` with 1e-9 relative tolerance, and in the deterministic samples with Python `math.isclose(rel_tol=1e-9)`; `ROUND` on DOUBLE is C-library dependent ([doc](/sources/mysql-refman-9-7-mathematical-functions.md)), so no in-database rounding is used | not part of `row_text` |
| DATE | `YYYY-MM-DD` | `CAST(col AS CHAR)` |
| DATETIME / TIMESTAMP | `YYYY-MM-DD HH:MM:SS.ffffff` always 6 fractional digits, UTC for offset-bearing sources | `DATE_FORMAT(col, '%Y-%m-%d %H:%i:%s.%f')` |
| TIME | `HH:MM:SS.ffffff` | `DATE_FORMAT(col, '%H:%i:%s.%f')` |
| CHAR/VARCHAR/TEXT | the string as-is; trailing whitespace preserved on both sides unless the dataset record says the source type pads (SQL Server `char`, Oracle `CHAR`) in which case both sides `RTRIM` | `col` (or `RTRIM(col)`) |
| BINARY/BLOB/geometry WKB/uniqueidentifier | lowercase hex | `LOWER(HEX(col))`; geometry: `LOWER(HEX(ST_AsBinary(col)))` |
| JSON/XML | XML: verbatim source text stored in a TEXT column and digested as a string. JSON: **excluded from the row digest**; `verify.py` fetches the column and compares `json.loads` objects on both sides (dict order-insensitive), because MySQL re-serialises JSON with its own key order and spacing ([json](/sources/mysql-refman-9-7-json.md)) | XML: `col`; JSON: not part of `row_text` |

Row digest: `d = CAST(CONV(SUBSTRING(SHA2(row_text, 256), 1, 16), 16, 10) AS UNSIGNED)` — `CONV` returns a *string*, so the `CAST` is what makes the aggregates evaluate it as an unsigned 64-bit integer ([SHA2](/sources/mysql-refman-9-7-encryption-functions.md), [CONV 64-bit](/sources/mysql-refman-9-7-mathematical-functions.md)). Python: `int(hashlib.sha256(row_text.encode('utf-8')).hexdigest()[:16], 16)`.

Table fingerprint: `(COUNT(*), COALESCE(BIT_XOR(d), 0), COALESCE(SUM(d), 0) MOD 18446744073709551616)` — the `COALESCE` matters because `SUM` returns NULL over zero rows ([doc](/sources/mysql-refman-9-7-aggregate-functions.md)) while the Python side reduces an empty table to 0 (Northwind ships two empty tables); BIT_XOR alone cancels duplicated rows and SUM alone is blind to nothing but duplicates, so both are recorded. `SUM` over the UNSIGNED digest returns DECIMAL ([doc](/sources/mysql-refman-9-7-aggregate-functions.md)) and cannot overflow; without the CAST, SUM over CONV's string would return DOUBLE and lose precision above 2^53, which is why the first code review rejected the earlier wording. Python keeps an int and reduces mod 2^64.

# Companion checks per column (cheap, catch truncation/coercion)
`COUNT(col)`, `COUNT(DISTINCT col)`, `MIN`, `MAX`, and for text `SUM(CHAR_LENGTH(col))` and `SUM(LENGTH(col))` (byte length exposes charset mistakes: a Latin-1-loaded `é` is 1 byte, a proper utf8mb4 `é` is 2). Numeric columns add `SUM(col)`.

# Deterministic samples
First 20 and last 20 rows by primary key plus every row whose `CRC32(pk_text) % 997 = 0` capped at 50; compared column by column against the source values written to `build/baseline.json`. Tables without a natural key use the surrogate key assigned by the loader, so the sample is reproducible only when load order is deterministic (all converters sort by the source file order).

# Baseline production
**Exception for native-SQL sources** (Sakila, Chinook, Employees, whose upstream artifact is itself MySQL SQL): no converter streams typed rows, so the baseline is the upstream-published counts and checksums (Employees ships SHA-256 checks; Sakila and Chinook document counts) plus the digests of the first verified load, pinned in `tests/` and re-compared on every rebuild. This is the only case where MySQL participates in producing the baseline, and PLAN.md §3 names each dataset it applies to.

The converter itself writes `build/baseline.json` as it streams rows (count, xor, sum, per-column aggregates, sampled rows) so the baseline is computed from the exact typed values that were emitted, before any MySQL involvement. For datasets converted by a native product export (SQL Server, Oracle) the baseline query runs inside that product with the same canonical rules expressed in T-SQL/PL-SQL, generated from the same column map.

# Outcome
Adopted as the S3–S4 test contract for every dataset (see PLAN.md §4), with the exception for native-SQL datasets stated under Baseline production.

# Row counts
Always `SELECT COUNT(*)`; `information_schema.TABLES.TABLE_ROWS` is an estimate that "may vary ... by as much as 40% to 50%" ([doc](/sources/mysql-refman-9-7-information-schema-tables.md)).

# Verified on the target server (2026-09-02, `mysql:9.7.2`)
* `SUM(CONV(...))` without the cast returns `1.8446744073709552e19` for two digests near 2^63 while `SUM(CAST(CONV(...) AS UNSIGNED))` returns `18446744073709551620`, exactly the Python value — the defect the first code review found, and the cast that fixes it.
* Over an empty table `SUM(...)` is `NULL` and `COALESCE(SUM(...), 0)` is `0` — the third review's finding, confirmed; Northwind ships two empty tables, so the `COALESCE` is load-bearing.
* `SHA2()` is available (the image is an SSL build); `MD5()` and `SHA1()` are **not** (`FUNCTION probe.MD5 does not exist`), confirming they moved into the optional `classic_hashing` component in 9.6.

# Status
accepted
