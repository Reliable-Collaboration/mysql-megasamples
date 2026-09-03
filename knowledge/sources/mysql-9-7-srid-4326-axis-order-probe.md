---
type: Source
title: MySQL 9.7 SRID 4326 axis order and hierarchyid/geography decoding, measured
description: What mysql:9.7.2 does with POINT under SRID 4326, and the verification of pure-Python decoders for SQL Server's hierarchyid and geography binary formats.
resource: /sources/mysql-9-7-srid-4326-axis-order-probe.md
tags:
- mysql
- spatial
- mssql
- adventureworks
- verification
status: stable
trust: verified
generated:
  by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
sources:
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/b47eadc852/samples/databases/adventure-works/oltp-install-script/Employee.csv
  title: Employee.csv (290 rows with OrganizationNode and OrganizationLevel)
  accessed: "2026-09-03"
- resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/b47eadc852/samples/databases/adventure-works/oltp-install-script/Address.csv
  title: Address.csv (SpatialLocation as SQL Server geography binary)
  accessed: "2026-09-03"
---

# What was read
The two AdventureWorks CSVs that carry SQL Server's exotic binary types, and the responses of a
`mysql:9.7.2` server to spatial probes, 2026-09-03.

# Relevant excerpt
* `Employee.csv` row 2: `OrganizationNode` = `58`, `OrganizationLevel` = `1`. Row 3: `5AC0`, level 2.
* `Address.csv` row 1: `SpatialLocation` =
  `E6100000010CAE8BFC28BCE4474067A89189898A5EC0` (22 bytes).
* `SELECT ST_AsText(p), ST_Latitude(p), ST_Longitude(p) FROM (SELECT ST_SRID(POINT(-122.164645,
  47.786992), 4326) p) t` → `POINT(47.786992 -122.164645)`, `47.786992`, `-122.164645`.
* `ST_SRID(POINT(47.786992, -122.164645), 4326)` → `ERROR 3732 (22S03): ... contains a geometry with
  latitude -122.164645, which is out of range. It must be within [-90.000000, 90.000000]`.

# What it was used to decide
That both binary formats can be decoded in Python, with no SQL Server, to a standard the build can
check — which is what [risk 5](/decisions/mssql-adventureworks-conversion-path.md) asked for.

**geography.** The 22 bytes are SRID (`E6100000` little-endian = 4326), version `01`, flags `0C`, then
two little-endian doubles: **latitude first, then longitude**. Row 1 decodes to 47.786992,
-122.164645, which is Bothell, Washington, the address the row gives.

**MySQL's axis order for SRID 4326**, which two dataset records had flagged as unverified: `POINT(x, y)`
takes **longitude then latitude**, and the SRS's own lat-long axis order then governs the text form,
so `ST_AsText` prints latitude first and `ST_X` returns the latitude. Both `ST_SRID(POINT(long, lat),
4326)` and `ST_GeomFromText('POINT(lat long)', 4326)` produce the same correct point; passing latitude
first to `POINT()` is rejected outright once the value exceeds ±90, which is a useful guard rather
than a silent error.

**hierarchyid.** The binary is a concatenation of one variable-length code per level, zero-padded to a
byte boundary; every code ends in a 1 bit, which makes the padding unambiguous. The ranges were
derived from the data itself — one AdventureWorks manager has 22 consecutive children, which pins the
codes for values 1 to 22 — and agree with the two values Microsoft documents (`0x58` = `/1/`,
`0x5AC0` = `/1/1/`). `scripts/hierarchyid.py` implements both directions and **raises rather than
guesses** for any code outside the verified ranges.

Verified over all 290 employees: every decoded path has exactly the level the `OrganizationLevel`
column states, every path re-encodes to its original bytes, all 290 paths are distinct, and every
node's parent path is itself present. The deepest is `/3/1/21/10/`.
