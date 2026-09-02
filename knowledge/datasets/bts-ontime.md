---
type: Dataset
title: BTS Airline On-Time Performance
description: One month of the US DOT Reporting Carrier On-Time Performance table (~536k flights, 109 columns) plus the airport and carrier lookup tables; public domain.
resource: https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr
tags: [tier-extended, csv, public-domain, aviation]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr
    title: TranStats download page
    accessed: 2026-09-02
    version: latest available data June 2026
  - resource: https://www.transtats.bts.gov/TableInfo.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr&V0s1_b0yB=D
    title: TranStats table profile (109 fields, 234,378,386 records)
    accessed: 2026-09-02
  - resource: /sources/bts-prezip-archive-inspection.md
    title: PREZIP archive inspection (URL pattern, header, encodings)
    accessed: 2026-09-02
  - resource: /sources/transtats-download-lookup-tables.md
    title: Lookup-table endpoints
    accessed: 2026-09-02
stale_after: 2027-03-01
---

# Identity
"Reporting Carrier On-Time Performance (1987-present)" from the BTS TranStats On-Time database: one row per scheduled domestic flight segment operated by a reporting carrier. Database name: **`bts_ontime`**.

# Source artifact
* **Bulk URL pattern (verified working with plain `curl`, no browser session, no cookies, no form POST):**
  `https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_<YYYY>_<M>.zip`
  The month is **not** zero-padded and the parentheses of the table name must be **removed from the URL** (`..._(1987_present)_..." returns 404`). The CSV *inside* the zip does keep the parentheses in its member name. This settles the frequently reported "TranStats blocks non-browser requests" problem: the interactive `DL_SelectFields.aspx` form does need a session, the `PREZIP` path does not.
* **Recommended pin - January 2025:** `Content-Length: 27,108,664`, `Last-Modified: Thu, 08 May 2025 14:59:27 GMT`. Members: `On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2025_1.csv` (**243,177,378 bytes uncompressed**, deflate) and `readme.html` (12,152 bytes, the record layout).
  Recent months for comparison: 2026-05 = 31,716,693 B; 2026-06 = 31,606,062 B (latest, published 2026-08-12).
* **Lookup tables** (verified 200 + `Content-Disposition`): `https://www.transtats.bts.gov/Download_Lookup.asp?Y11x72=<ROT13 of table name>` - `Y_NVecbeg` -> `L_AIRPORT.csv` (319,686 B), `Y_NVeYVaR_VQ` -> `L_AIRLINE_ID.csv` (66,730 B), `Y_haVdhR_PNeeVRef` -> `L_UNIQUE_CARRIERS.csv` (54,217 B).
* **Auth / click-through:** none for either path.
* **Checksums:** BTS publishes none. Record `sha256` at fetch time.

# Native format and friendlier forms
The prezipped CSV *is* the friendly form - no database product to stand up, no API key. The alternative (the `DL_SelectFields.aspx` form) requires a session and returns the same CSV with a user-chosen column subset; not worth the fragility.

# Shape
* **`ontime`** - **109 named columns**, confirmed both by the TranStats table profile ("Fields: 109") and by the actual header. Column names and order are quoted in [the archive inspection](/sources/bts-prezip-archive-inspection.md): the time-period block, airline block, the nine `Origin*` and nine `Dest*` columns, departure/arrival performance, cancellation/diversion, flight summary, the five delay-cause columns (populated from 6/2003), the three gate-return columns (from 10/2008), and five `Div1..Div5` blocks of seven columns each (from 10/2008).
* **Rows:** ~**536,000** for 2025-01 - **Inferred** from 243,177,378 bytes / 453.3 bytes per row measured over a 10,181-row sample. BTS publishes no per-month count. The whole table is 234,378,386 records across 1987-2026 (table profile).
* **Lookups:** `L_AIRPORT` (code -> description), `L_AIRLINE_ID` (DOT id -> carrier), `L_UNIQUE_CARRIERS` (unique carrier code -> name).
* **Encoding:** ASCII. No byte above 0x7F in ~10,000 sampled rows. `L_AIRPORT` descriptions contain foreign city names; **Inferred:** they are ASCII-transliterated, but the executor should re-check after loading the lookup, and `utf8mb4` covers either case.

# Conversion path
[DuckDB reader -> typed CSV -> `util.importTable`](/decisions/large-tabular-conversion-path.md), with the lookups written directly through the DuckDB MySQL extension.

**Downloader design.** Take a list of `(year, month)` pairs; build the URL with the non-padded month; `curl --fail --location --retry 5 --retry-all-errors --retry-delay 5 --connect-timeout 20 -C -`; **add `--ipv4`** - TranStats has a long history of stalling on IPv6-first resolvers, and forcing IPv4 is the cheapest mitigation (**Inferred**, but harmless). Verify the ZIP central directory before extracting, extract only the `.csv` member, and record the `sha256` of the zip plus the uncompressed member size.

# Type-mapping hazards
1. **Trailing comma on every line.** The header ends `..."Div5TailNum",` so a naive split gives 110 fields with an unnamed empty one; pandas would create `Unnamed: 110`. Declare 109 columns and let the parser discard the trailing empty field, or add a throwaway column and drop it.
2. **Clock columns are quoted zero-padded strings, not numbers.** `CRSDepTime` = `"0659"`, `"0053"`. Read as an integer, `"0053"` silently becomes 53. Keep them `CHAR(4)` and expose `TIME` through a generated column, because -
3. **`"2400"` occurs** (observed once in a ~10,000-row sample of `DepTime`). It is not a valid `TIME`-of-day for `STR_TO_DATE('%H%i')`-style parsing in the way a naive mapping expects; midnight-end is encoded as 2400 rather than 0000. Any `TIME` conversion must special-case it.
4. **`FlightDate` is `2025-01-01`, not `yyyymmdd`** - the BTS readme documents `(yyyymmdd)` and the data disagrees. Trust the data.
5. **Integral quantities are written as decimals**: `Cancelled` = `0.00`, `Diverted` = `0.00`, `DepDel15` = `0.00`, `Flights` = `1.00`, `Distance` = `2475.00`. Cast to `TINYINT`/`SMALLINT` explicitly; do not let inference make them DOUBLE.
6. **Two null spellings on one row:** `CancellationCode` is `""` (empty *quoted* string) when absent while numeric nulls are bare empty fields. A `NULLSTR` of `''` would turn the quoted empty string into NULL too - decide deliberately.
7. **Leading-zero strings**: `OriginStateFips` = `"36"`, `"06"`; `Flight_Number_Reporting_Airline` = `"1"`. Keep as `CHAR`/`VARCHAR`.
8. **Embedded commas inside quotes**: `"New York, NY"`. A real CSV parser is mandatory.
9. **Columns that are entirely NULL in older months** - the five delay causes before 6/2003 and the gate-return/diversion blocks before 10/2008. Irrelevant for a 2025 month but fatal for a multi-year load with inferred types.
10. **`Reporting_Airline` can be `PA(1)`, `PA(2)`** - parentheses inside a carrier code (documented in the readme).
11. The 25 `Div2..Div5` columns are **empty in essentially every row**; they cost 25 columns of DDL for near-zero data. Keep them for fidelity but do not index them.

# Programmable objects
None upstream. This project adds a view `v_ontime_delay` (flight, carrier name via `L_UNIQUE_CARRIERS`, origin/dest descriptions via `L_AIRPORT`, `ArrDelayMinutes`), `SQL SECURITY INVOKER`. No procedures/triggers.

# Indexing
* **No natural primary key.** The intuitive candidate `(FlightDate, Reporting_Airline, Flight_Number_Reporting_Airline, Origin, Dest, CRSDepTime)` is **not reliably unique** - a flight number can be re-used on the same route and date after a schedule change, and the table historically contains exact duplicate rows. **Marked inferred: this was not tested against the data in this session.** Use a surrogate `flight_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY` and, if desired, add a *non-unique* index on the tuple. The cheapest confirmation is a `GROUP BY ... HAVING COUNT(*) > 1` after load.
* `KEY (FlightDate)` - every temporal query.
* `KEY (Origin)`, `KEY (Dest)` - FK-like into `L_AIRPORT.Code`.
* `KEY (Reporting_Airline)` - FK-like into `L_UNIQUE_CARRIERS.Code`.
* `KEY (ArrDelayMinutes)` only if the teaching queries rank delays; otherwise skip.
* Real `FOREIGN KEY`s are **not** recommended: `Origin`/`Dest` reference airport codes that have been re-used over time (which is why BTS provides `OriginAirportSeqID`), so referential integrity against a current lookup is not guaranteed.

# Tests and expected values
* `SELECT COUNT(*) FROM ontime` -> **~536,000** for 2025-01 (**inferred**; the executor replaces this with the exact count at first load and logs a **Verification**).
* `SELECT COUNT(*) FROM l_airport` / `l_airline_id` / `l_unique_carriers` -> recorded at first load (files are 319,686 / 66,730 / 54,217 bytes).
* Column count check: `SELECT COUNT(*) FROM information_schema.columns WHERE table_name='ontime'` -> **109**.
* Sanity: `SELECT COUNT(*) FROM ontime WHERE DepTime='2400'` -> non-zero, proving hazard 3 is preserved rather than silently mangled.

# Tier assignment
**Extended.** 27 MB zipped / **243 MB of CSV** for one month, 109 columns wide. **Inferred:** 250-400 MB as an InnoDB table before indexes - well over the 50 MB core budget and over the ~200 MB "medium core" allowance too, especially since a 109-column table is mostly empty `Div*` columns. Fetched by `make load-bts_ontime`. The three lookup tables (441 KB total) could ship in core as a standalone curiosity but are meaningless without the fact table, so they travel with it.

# License and attribution
[US Government public domain](/licenses/us-government-public-domain.md) - 17 U.S.C. Sec. 105(a). No attribution required, no share-alike, no re-identification concern (the data has no personal information; `Tail_Number` identifies aircraft, not people). Do not ship the BTS/DOT seal and do not imply endorsement.

# Open questions
* The BTS and DOT web-policy pages returned **403** to every request in this session, so the agency's own reuse wording was never read; the public-domain conclusion rests on the statute and USA.gov. Re-check `https://www.bts.gov/web-policies` from a browser before publication.
* Exact row count for the pinned month (resolved by the first load).
* Whether the six-column tuple is unique in practice (one `GROUP BY` after load).
* Whether `L_AIRPORT` descriptions contain non-ASCII bytes (one `grep` on the downloaded lookup).
