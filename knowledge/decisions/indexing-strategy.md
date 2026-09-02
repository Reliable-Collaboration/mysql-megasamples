---
type: Decision
title: Indexing strategy and order of operations
description: Carry upstream keys and indexes faithfully; derive indexes for index-less sources from key candidates, join columns, and range columns; load first, index second, constrain last; verify with information_schema and EXPLAIN.
resource: /decisions/indexing-strategy.md
tags: [decision, indexing, innodb]
status: stable
trust: inferred
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:40:00Z" }
sources:
  - resource: /sources/mysql-refman-9-7-explain-output.md
    accessed: 2026-09-02
  - resource: /sources/mysql-refman-9-7-information-schema-statistics.md
    accessed: 2026-09-02
  - resource: /tools/load-data-infile.md
    title: bulk-load recommendations (tools agent)
    accessed: 2026-09-02
  - resource: /tools/mysql-9x-behaviour-notes.md
    title: partitioning and FULLTEXT limits (tools agent)
    accessed: 2026-09-02
---

# Question
What indexes does each converted database get, in what order are they created, and how is that verified?

# Rules
1. **Faithful carry-over** for sources with declared keys: primary keys, unique constraints, foreign keys, and plain secondary indexes are recreated with the same column order and names (lower-cased). Unsupported forms map as follows and each instance is listed in the dataset record: filtered indexes → plain index on the same columns (+ comment naming the dropped predicate); included columns → appended as trailing key columns only if the total key stays under 3072 bytes, else dropped; bitmap indexes (Oracle) → B-tree; columnstore (SQL Server) → none (documented); partitioned indexes → plain; clustered index on a non-PK column → the PK remains the InnoDB cluster, the clustered column gets a secondary index; XML/spatial/full-text indexes → FULLTEXT or SPATIAL where MySQL supports the column type.
2. **Derived design** for index-less sources (CSV, Parquet, XML, generators): the dataset record lists, per table, (a) the natural key or the justification for a surrogate `id BIGINT AUTO_INCREMENT`, (b) foreign-key-like columns (each gets a single-column index and, where the referenced lookup table is shipped, an actual FK), (c) date/time columns used for range scans (index; composite `(date, fk)` when the canonical queries filter on both), (d) high-cardinality filter columns, (e) composite indexes justified by the dataset's canonical queries, with the expected cardinality of each leading column recorded from the baseline `COUNT(DISTINCT)`.
3. **Clustered key choice**: prefer a monotonically increasing integer PK (upstream identity or surrogate assigned in source order) so bulk loads append at the end of the clustered index; for natural composite keys (Lahman `batting`, TPC-H `lineitem`), load the data pre-sorted by the PK so page splits are avoided. Wide tables (BTS 110 columns, Stack Exchange posts) get the minimum set of secondary indexes because every secondary index carries the PK.
4. **FULLTEXT** (InnoDB) on Stack Exchange `posts.body` and `posts.title`, Enron `messages.body`/`subject`, Wikipedia `text.old_text`, WideWorldImporters `stockitems.searchdetails`, AdventureWorks `productreview.comments`; created after load (InnoDB builds FULLTEXT faster in one pass). Stopword and `innodb_ft_min_token_size` behaviour is documented in the smoke tests.
5. **SPATIAL** on geometry columns (Sakila `address.location`, AdventureWorks `address.spatiallocation`, WWI `cities.location`) — requires `NOT NULL` and an SRID on the column; NULL-bearing sources get a `POINT SRID 4326` column with NULLs kept and **no** spatial index (documented) or a filtered copy table if a canonical query needs it.
6. **Partitioning**: not used by default; MySQL disallows foreign keys on partitioned tables (see [9.x notes](/tools/mysql-9x-behaviour-notes.md)). Offered as an opt-in `indexes-partitioned.sql` only for the extended-tier fact tables (NYC taxi by month, TPC-DS `store_sales` by `ss_sold_date_sk` range) where a demo of partition pruning is itself valuable.

# Order of operations (every dataset)
1. `schema.sql`: tables with primary keys only (the clustered index must exist before load; a PK added later rebuilds the table).
2. Load with `SET unique_checks=0, foreign_key_checks=0, sql_log_bin=0` and `LOAD DATA` / `util.importTable` / `util.loadDump(deferTableIndexes:"all")` ([load-data record](/tools/load-data-infile.md)).
3. `indexes.sql`: secondary, FULLTEXT, SPATIAL indexes (one `ALTER TABLE ... ADD INDEX ..., ADD INDEX ...` per table so InnoDB builds them in a single pass).
4. Orphan check: for every planned FK, `SELECT COUNT(*) FROM child LEFT JOIN parent ... WHERE parent.pk IS NULL` must be 0 unless the dataset record documents an expected orphan count (Sakila: 0; upstream-known orphans such as some BTS `Tail_Number` values are handled by not declaring that FK).
5. `constraints.sql`: foreign keys and CHECK constraints; then `ANALYZE TABLE` for every table.
6. `tests/`: counts, digests, indexes, EXPLAIN, smoke queries.
Load-time measurement: `make bench-index-order DATASET=employees` loads once with indexes pre-created and once with the order above and records both times in the dataset record (task E-02).

# Verification
* `tests/indexes.yaml` lists every expected index as `table, name, unique, type, columns[]`; `scripts/verify.py indexes` compares it with `INFORMATION_SCHEMA.STATISTICS` grouped by index ([doc](/sources/mysql-refman-9-7-information-schema-statistics.md)); missing or extra indexes fail the build.
* `tests/explain.yaml` lists each smoke query with the tables that must not show `access_type: "ALL"` in `EXPLAIN FORMAT=JSON` ([doc](/sources/mysql-refman-9-7-explain-output.md)); tiny lookup tables (< 100 rows) are exempt because the optimizer legitimately scans them.

# Status
accepted
