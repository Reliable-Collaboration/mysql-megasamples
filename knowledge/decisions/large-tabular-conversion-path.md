---
type: Decision
title: Conversion path for the large public tabular datasets
description: DuckDB reads Parquet/CSV and emits typed MySQL-ready CSV; MySQL Shell util.importTable (LOAD DATA) writes it. One pipeline for TLC, BTS, Chicago, Citi Bike and Divvy.
resource: /decisions/large-tabular-conversion-path.md
tags: [decision, etl, duckdb, tabular]
status: stable
trust: inferred
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: /tools/duckdb.md
    title: DuckDB
    accessed: "2026-09-02"
  - resource: /sources/nyc-tlc-parquet-footer-inspection.md
    title: Observed Parquet schemas and drift
    accessed: "2026-09-02"
  - resource: /sources/bts-prezip-archive-inspection.md
    title: BTS CSV quirks
    accessed: "2026-09-02"
---

# Question
How do five very different flat-file sources - Parquet (TLC), zipped 243 MB CSV with a trailing comma (BTS), a 1.65 GB streamed Socrata export (Chicago), and two eras of zipped bikeshare CSV (Citi Bike, Divvy) - become MySQL tables with one maintainable script?

# Options considered
1. **DuckDB as reader/reshaper -> typed CSV -> MySQL Shell `util.importTable` (`LOAD DATA`)** (chosen). One tool reads all four container formats (`read_parquet`, `read_csv`, zipped CSV), does the casting and column renaming in SQL, and writes a canonical CSV that the fastest MySQL bulk path consumes.
2. **DuckDB writing directly into MySQL via the `mysql` extension.** Rejected as the default: the docs never state how rows are transmitted or how fast it is ([open question](/questions/duckdb-mysql-write-throughput.md)), and a 3.5 M-row month is the wrong place to find out. **Kept** for the small dimension tables (265 taxi zones, 434 IUCR codes, ~19k `L_AIRPORT` rows) where one statement beats a file round-trip.
3. **Python + pyarrow/pandas -> `LOAD DATA`.** Rejected: adds a Python data stack to the loader image and requires hand-written handling of the TLC type drift that `union_by_name` solves declaratively. Neither library is installed on the build machine, and nothing about them was verified here.
4. **Direct `LOAD DATA` on the upstream files.** Rejected: cannot read Parquet at all; for the CSVs it cannot fix the BTS trailing comma, the `"0659"` HHMM strings, the Chicago `MM/DD/YYYY hh:mm:ss AM` dates, or the Citi Bike/Divvy header-spelling changes without per-column `SET` expressions that would have to be rewritten per era anyway.

# Evidence
* The TLC archive is Parquet only and its physical types change across years (`passenger_count` INT64 -> DOUBLE -> INT64; `airport_fee` -> `Airport_fee`; INT64 -> INT32 IDs) - see [the footer inspection](/sources/nyc-tlc-parquet-footer-inspection.md). `read_parquet([...], union_by_name := true)` plus explicit `CAST`s is the smallest correct answer.
* The BTS CSV has a trailing comma on every line, quoted zero-padded clock strings, `"New York, NY"` embedded commas and two spellings of null - see [the archive inspection](/sources/bts-prezip-archive-inspection.md). A real CSV parser is mandatory.
* Chicago's export is chunked with `Content-Length: 0`, so it must be streamed and cannot be size-checked in advance; the SODA API is the alternative for a bounded subset.
* Citi Bike monthly zips are **STORED, not deflated**, and the yearly ones are zips of zips; Divvy zips are deflated. The extractor must handle both and skip `__MACOSX/._*`.

# Outcome
Per dataset, the loader does:
1. **Fetch** the upstream artifact into `./downloads/`, record `sha256`, `Content-Length` and `Last-Modified` in `downloads/<id>.meta.json`, which `scripts/registry.py` folds into the `megasamples.datasets` table at image build or extended load (no upstream checksums exist for any of these five - see each dataset record).
2. **Normalise with DuckDB**: one `.sql` per dataset that selects from `read_parquet` / `read_csv` with an explicit column list and target types, renames columns to lower snake_case, and `COPY ... TO 'staging/<table>.csv' (FORMAT CSV, HEADER false, NULLSTR '\N')`.
3. **Load** with `mysqlsh util.importTable` into a pre-created table whose DDL lives in the repo (never rely on inferred DDL).
4. **Verify** `COUNT(*)`, the canonical digests of the [checksum method](/decisions/test-checksum-method.md) and the `CHECKSUM TABLE` fingerprint against the values recorded in the dataset record and `build/baseline.json`.

Dimension tables (taxi zones, IUCR codes, `L_AIRPORT`/`L_AIRLINE_ID`/`L_UNIQUE_CARRIERS`) skip steps 2-3 and are written straight through the DuckDB MySQL extension.

# Status
accepted (the DuckDB-vs-`LOAD DATA` throughput assumption is inferred; resolving [the write-throughput question](/questions/duckdb-mysql-write-throughput.md) may collapse steps 2-3 into one)
