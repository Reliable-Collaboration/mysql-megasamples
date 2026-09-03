---
type: Open Question
title: Do the SH CSV files reproduce the published row counts, and does LOAD DATA need the padding/NULL pre-pass?
description: 918,843 sales rows and the other counts are published inside sh_install.sql but the CSVs were not downloaded during research; sales.csv is space-padded to 80 columns and NULL strings appear as "".
resource: /questions/oracle-sh-csv-row-counts-and-padding.md
tags:
- question
- oracle
- sh
- csv
status: deprecated
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
sources:
- resource: /sources/github-oracle-samples-db-sample-schemas-sh-scripts.md
  title: SH scripts and CSV samples
  accessed: "2026-09-02"
---

# Question
1. Does `wc -l` (minus header) of each v23.3 CSV equal the verification counts in `sh_install.sql` (costs 82,112; customers 55,500; promotions 503 — already confirmed; sales 918,843; times 1,826; supplementary_demographics 4,500)?
2. Does MySQL 9.7 `LOAD DATA LOCAL INFILE` accept `1232.16` followed by trailing spaces into a `DECIMAL(10,2)` column without warnings/truncation, or must the converter strip the padding first?
3. Do the `""` values in `customers.csv` (`CUST_MARITAL_STATUS`, `CUST_EFF_TO`) need explicit `NULLIF(@v,'')` mapping to become NULL (Oracle semantics), and are there other nullable columns with `""`?
4. Measured InnoDB size of `oracle_sh` after indexing (tier confirmation: core-medium vs extended).
5. Does the full `customers.csv` contain any non-ASCII byte (`grep -cP '[^\x00-\x7F]'`)?
6. Confirm on `mysql:9.7` that an InnoDB table `PARTITION BY RANGE (TO_DAYS(time_id))` rejects `FOREIGN KEY` (the reason the SH record drops partitioning instead of FKs), e.g. `CREATE TABLE p (id INT, d DATE, FOREIGN KEY (id) REFERENCES t(id)) PARTITION BY RANGE (TO_DAYS(d)) (PARTITION p0 VALUES LESS THAN MAXVALUE)` → expected error 1506.

# Cheapest experiment
```
sha=e3325a83e56c516815844025418a96ecaf219751
for f in sales customers costs times promotions supplementary_demographics; do curl -sLO https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/$sha/sales_history/$f.csv; done
for f in *.csv; do echo "$f $(($(wc -l < $f) - 1)) rows, non-ascii lines: $(grep -cP '[^\x00-\x7F]' $f), padded lines: $(grep -c ' $' $f)"; done
```
then load `sales.csv` unmodified into a scratch table with `LOAD DATA LOCAL INFILE ... FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' IGNORE 1 LINES` and inspect `SHOW WARNINGS` and `SELECT amount_sold FROM sales LIMIT 3`; repeat with `SET amount_sold = TRIM(@amount)`; then `SELECT COUNT(*) FROM customers WHERE cust_marital_status = ''` after a naive load. Record `SELECT SUM(data_length+index_length) FROM information_schema.tables WHERE table_schema='oracle_sh'`.

# Answer
Answered 2026-09-03 by building the dataset; all six CSVs were downloaded and their sizes match the
research byte for byte.

1. **Yes, every count matches.** costs 82,112; customers 55,500; promotions 503; sales 918,843;
   times 1,826; supplementary_demographics 4,500 — each equal to the figure `sh_install.sql`
   publishes for itself. (Note `wc -l` is one short on five of the six files: only
   `supplementary_demographics.csv` ends with a newline.)
2. **No, the padding pre-pass is not required for this file** — but it is still done. MySQL 9.7 loads
   `1232.16` followed by trailing spaces into `DECIMAL(10,2)` and stores `1232.16` with **no
   warnings**. The converter strips trailing blanks from every field anyway, because the same padding
   in a character column would be kept silently; measured, that strip touches exactly 918,843 fields
   — one per `sales` row — and none in any other file.
3. **Yes, and it is broader than the two named columns.** Oracle's `''` is NULL, so the converter maps
   *every* empty field, quoted or not, to `\N` in the contract TSV. Loaded, `customers` has 17,506
   NULL `cust_marital_status` and **0** empty strings, which is the record's own NULL-semantics test.
   The same rule was needed for the `''` literals in `sh_populate.sql`, where they land in integer
   columns and MySQL rejects them outright.
4. **168.7 MB** in InnoDB, loading in 10.5 s — inside the 150–250 MB the record inferred, so
   **core (medium)** stands.
5. **No non-ASCII bytes at all**, in any of the six files (`grep -cP '[^\x00-\x7F]'` returns 0 for
   each), confirming the ASCII sampling done during research.
6. **Confirmed on mysql:9.7.2**: `CREATE TABLE p (id INT, d DATE, FOREIGN KEY (id) REFERENCES t(id))
   PARTITION BY RANGE (TO_DAYS(d)) ...` fails with `ERROR 1506 (HY000): Foreign keys are not yet
   supported in conjunction with partitioning`. Dropping the partitioning and keeping the foreign
   keys is therefore the only choice, not a preference.

# Resolves
[SH dataset record](/datasets/oracle-sh.md) tests and tier; the converter's pre-pass design.
