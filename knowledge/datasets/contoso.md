---
type: Dataset
title: Contoso (SQLBI Contoso Data Generator V2)
description: SQLBI's synthetic Contoso retail star schema V2 - customer, product, store, date, currencyexchange, sales, orders, orderrows - published as ready-to-use CSV sets of 10K to 100M orders under MIT; csv-100k (9.8 MB 7z) for core.
resource: https://github.com/sql-bi/Contoso-Data-Generator-V2-Data
tags:
- tier-core
- tier-extended
- csv
- contoso
- mit
- generator
- star-schema
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:48:59Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://api.github.com/repos/sql-bi/Contoso-Data-Generator-V2-Data/releases
  title: ready-to-use-data release assets
  accessed: "2026-09-02"
  version: release ready-to-use-data (2025-09-21)
- resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/README.md
  title: generator README (2.0.1)
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/build_data/build_single.cmd
  title: build parameters and config.json
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/scripts/sql/CreateTablesCommon.sql
  title: SQL Server DDL
  accessed: "2026-09-02"
- resource: https://docs.sqlbi.com/contoso-data-generator/
  title: SQLBI docs
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2-Data/main/LICENSE
  title: MIT LICENSE (data)
  accessed: "2026-09-02"
---

# Identity
Contoso Data Generator V2 (SQLBI, Marco Russo/Alberto Ferrari's company) - a modern re-creation of Microsoft's "Contoso" retail demo as a generated star schema for Power BI/Fabric demos. This is NOT the Microsoft ContosoRetailDW SQL Server backup ([decision](/decisions/contoso-conversion-path.md)).

# Source artifact
* Data: https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/download/ready-to-use-data/csv-100k.7z - 9,786,343 bytes (release `ready-to-use-data`, 2025-09-21). Siblings: csv-10k.7z 5,409,141; csv-1m.7z 48,894,397; csv-10m.7z 512,408,852; csv-100m.7z 9 volumes about 4.46 GB; parquet/delta/pbix/bak variants ([releases](/sources/github-sql-bi-contoso-v2-data-releases.md)). No auth; no published checksums (record sha256 at first download). 7-zip format.
* Generator: Contoso-Data-Generator-V2 release 2.0.1, .NET 8 ([tool](/tools/contoso-data-generator-v2.md)); build parameters for each size are in `scripts/build_data/build_single.cmd` (100k = OrdersCount 100000, CustomerPercentage 0.05, StartDT 2015-01-01, YearsCount 10, CutDateBefore 2014-05-18, CutDateAfter 2024-04-20) ([build scripts](/sources/github-sql-bi-contoso-v2-config-and-build-scripts.md)).

# Native format and friendlier forms
Native = CSV (also Parquet/Delta) produced by the generator; SQLBI's SQL Server scripts BULK INSERT the CSVs. CSV is the friendliest form; **CSV dialect (delimiter, header, quoting, date format) is not documented** ([docs](/sources/sqlbi-docs-contoso-data-generator.md)) - inspect the archive.

# Shape
Eight tables (from the SQL Server DDL, [source](/sources/github-sql-bi-contoso-v2-sql-scripts.md)): customer (24 cols: name, address, geo, birthday, occupation, lat/long), date (17 cols), product (14 cols: code, name, manufacturer, brand, color, weight, cost, price, category/subcategory), store (11 cols), currencyexchange (date, from, to, rate), sales (13 cols, PK OrderKey+LineNumber), orders (6 cols), orderrows (7 cols). Currencies AUD, CAD, EUR, GBP, USD; countries AU, CA, DE, FR, IT, NL, GB/UK, US.
**Built and measured 2026-09-03** (100k set): 8 tables, **753,467 rows**, **103.3 MB** in InnoDB (the record inferred 60–120 MB, so no need to drop either fact table), loading in 4.8 s, 7 foreign keys with 0 orphans. Counts: currencyexchange 100,450; customer 104,990; date 4,018; orderrows 223,974; **orders 93,470**; product 2,517; sales 223,974; store 74.

Two inferences are corrected. **orders is 93,470, not 100,000** — `OrdersCount` is what the generator is asked for, but the build then cuts orders outside its date window (`CutDateBefore` 2014-05-18, `CutDateAfter` 2024-04-20), so the shipped set is smaller. And sales/orderrows are **223,974**, a ratio of 2.40 rather than the inferred 2.43. `sales` and `orderrows` hold the same 223,974 rows and join one-to-one on (orderkey, linenumber).

**The 1 M set (2026-09-03, task X-03)**: `csv-1m.7z` is 48,894,397 bytes — the size this record
predicted — and gives **5,890,897 rows in 767.3 MB**, loading in 28.6 s. What scales and what does
not is worth stating, because it is not what "1 M orders" suggests: at this size **only the fact
tables grow**. `customer` is 104,990, `product` 2,517, `store` 74 and `date` 4,018 at *both* the
100 k and 1 M sizes, spanning the same 2016-01-01 to 2026-12-31, and even the 6,142 non-ASCII
customers are the same 6,142. `sales` and `orderrows` go from 223,974 to **2,349,091** (10.5×) and
`orders` from 93,470 to **980,666** — again short of the round number, cut by the same date window.
Revenue scales with them: `SUM(quantity * netprice)` is 2,298,959,220.81 against the 100 k set's
218,814,472.24. (The customer pool does eventually grow: see the 10 M set below.)

The store sentinel is clearer at this size: `storecode` -1, country `--`, carries 973,210 of the
2,349,091 sales lines — the online store, 41% of the business.


**The 10 M set (2026-09-03, task X-03)**: `csv-10m.7z` is 512,408,852 bytes — again the size this
record predicted — and gives **59,114,388 rows in 7,766.9 MB**, loading in 222 s. Here the customer
pool finally moves: **1,679,846 customers** against 104,990 at both smaller sizes, and 97,703 of them
carry non-ASCII text. `product` (2,517), `store` (74), `date` (4,018) and `currencyexchange` (100,450)
are unchanged at every scale. `sales` and `orderrows` are 23,719,935; `orders` 9,887,613.
`SUM(quantity * netprice)` is 23,204,619,919.05. The online store (`storecode` -1) is 9,822,929 of
the sales lines, the same 41%.

One test had to change shape at this size. The core set proves `sales` and `orderrows` hold the same
rows with a 1:1 join; over 23.7 M rows that becomes a multi-minute nested loop of random primary-key
lookups. The scaled sets make the same claim with five single-table aggregates — counts plus the sums
of `orderkey`, `linenumber`, `quantity`, `netprice` and `productkey` — which agree exactly
(`5606843664697694,27666276,74586697,7377545409.97,28082132055` on both sides) and scan instead of
joining.

**CSV dialect (was undocumented, now measured)**: comma-delimited, one header row of column names in DDL order, no quoting needed, ISO `YYYY-MM-DD` dates, empty field = NULL, UTF-8 without BOM. The converter checks each header against the pinned SQL Server DDL before writing a row, because the load is positional.

**Encoding** confirmed non-ASCII as inferred: 6,142 of 104,990 customers carry non-ASCII text in their name or city — `Stuttgart Dürrlewang`, `Schönwalde`, `Mönchengladbach Großheide`.

**7-zip without 7-zip**: the archive is read with `py7zr`, a pure-Python reader added to the project's dependencies, so neither the build machine nor CI needs a system 7-zip.

* Row counts (100k set): orders = 100,000 by definition ("OrdersCount ... Total number of orders"); **Inferred:** sales/orderrows about 2.4 x orders (OrderRowsWeights [12,9,7,4,1,1,1] -> mean 2.43 lines) i.e. about 243,000; customers = 5% of the static customer pool (pool size unknown; measure); date = 10 years about 3,650 rows; currencyexchange = days x currency pairs. Executor records exact counts from the CSVs.
* Encoding: **Inferred** UTF-8 (customer names from multi-country fake-name files, e.g. DE/FR/IT with accents - expect non-ASCII in customer.GivenName/Surname/City; verify with a grep on the CSV). Loaded size for 100k: **Inferred** 60-120 MB InnoDB (sales + orderrows duplicate the fact data); consider loading only `sales` or only `orders`+`orderrows` in core to halve it.

# Conversion path
Download csv-100k.7z, `7z x`, load with server-side LOAD DATA (or build-time INSERT conversion) into MySQL DDL translated from SQLBI's SQL Server scripts ([decision](/decisions/contoso-conversion-path.md); CSV notes [tool note](/tools/smallcsv-load-data-infile.md)).

# Type-mapping hazards
* `money` -> DECIMAL(19,4); `float` -> DOUBLE (Exchange rates, lat/long, weight); `bit` WorkingDay -> BOOLEAN; `nchar(3)`/`nvarchar` -> utf8mb4 CHAR/VARCHAR; `bigint` OrderKey; `date` columns (OrderDate, DeliveryDate, Birthday, StartDT/EndDT nullable).
* Date table PK is `DateKey nvarchar(50)` (string) while `Date` is the natural key - keep both.
* Column names with spaces exist only in the dbo views; base tables are CamelCase (`CustomerKey`) - lower-cased to `customerkey` per the [naming convention](/decisions/database-naming-convention.md); tables `customer`, `date`, `product`, `store`, `currencyexchange`, `sales`, `orders`, `orderrows` (`date` is a MySQL keyword - backtick it or name the table `dates`; **Inferred**, check the reserved-word list).
* Possible large `ProductName nvarchar(500)`; `MiddleInitial nvarchar(150)`.
* CSV unknowns: header presence, quoting, decimal separator (SQLBI is Italian - verify the decimal point), date format.

# Programmable objects
None in the data; SQLBI's `dbo.*` views (renamed columns) are optional - port as MySQL views only if cheap. No FKs in the CSV; DDL adds FKs sales/orders -> customer, product, store.

# Indexing
From the SQL Server DDL: PKs, FK indexes on CustomerKey, ProductKey, StoreKey, OrderKey. Create after load.

# Tests and expected values
`SELECT COUNT(*) FROM orders` = 100000 (100k set); counts of other tables recorded at first load; `SELECT MIN(orderdate), MAX(orderdate) FROM sales` within 2015-01-01 .. 2024-04-20 (from CutDateAfter) - **Inferred**; `SELECT COUNT(DISTINCT currencycode) FROM sales` = 5; sha256 of the 7z pinned.

# Tier assignment
core: csv-100k (9.8 MB archive; inferred 60-120 MB loaded - if the budget is tight, ship csv-10k at 5.4 MB instead). extended: csv-1m (48.9 MB archive) and csv-10m (512 MB). Evidence: [release sizes](/sources/github-sql-bi-contoso-v2-data-releases.md).

# License and attribution
[MIT](/licenses/mit.md) - "Copyright (c) 2024 SQLBI" (data) and "Copyright (c) 2022 SQLBI" (generator); include the notices. Contoso is a Microsoft fictional brand name used by SQLBI; no Microsoft license applies to this generated data (**Inferred**).

# Database name
`contoso`.

# Open questions
* [Generator determinism](/questions/contoso-generator-determinism.md).
* CSV dialect and exact per-table row counts of csv-100k (resolve by downloading the 9.8 MB archive at execution time).
