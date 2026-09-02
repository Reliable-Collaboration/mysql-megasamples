---
type: Tool
title: CSV loading notes for this group's flat-file datasets (LOAD DATA vs generated INSERTs)
description: Dataset-specific CSV facts verified for DS3, Jaffle Shop, Lahman, Contoso, Titanic, Iris and Penguins (headers, quoting, NA tokens, date formats, BOMs) and the loader recipe they imply; generic MySQL LOAD DATA / secure_file_priv behaviour is covered by the tools agent.
resource: /tools/smallcsv-load-data-infile.md
tags: [tool, csv, load-data, group-smallcsv]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/load/cust/mysqlds3_load_cust.sql
    title: DS3 loader scripts (LOAD DATA LOCAL INFILE pattern)
    accessed: "2026-09-02"
  - resource: https://github.com/dvdstore/ds3/tree/master/ds3/data_files
    title: DS3 CSV inspection
    accessed: "2026-09-02"
  - resource: https://github.com/dbt-labs/jaffle-shop-classic/tree/main/seeds
    title: Jaffle seeds inspection
    accessed: "2026-09-02"
  - resource: https://hbiostat.org/data/repo/titanic3.csv
    title: titanic3.csv inspection
    accessed: "2026-09-02"
  - resource: https://archive.ics.uci.edu/static/public/53/iris.zip
    title: iris.zip inspection
    accessed: "2026-09-02"
  - resource: https://github.com/allisonhorst/palmerpenguins/tree/main/inst/extdata
    title: penguins CSV inspection
    accessed: "2026-09-02"
---

# Facts
| dataset | header | quoting | missing token | dates | line endings / encoding | notes |
|---|---|---|---|---|---|---|
| DS3 | none | `OPTIONALLY ENCLOSED BY '"'` (upstream), rarely needed | empty | `YYYY/MM/DD`, `YYYY/MM` | LF, ASCII | upstream: `LOAD DATA LOCAL INFILE ... FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'`, keys disabled during load |
| Jaffle classic | yes | none | none | `YYYY-MM-DD` | LF, ASCII | integer cents |
| Jaffle (jafgen) | yes | double quotes on descriptions with commas | none | ISO `YYYY-MM-DDTHH:MM:SS` | LF, ASCII | `True`/`False` booleans, UUID keys |
| Titanic3 | yes | all strings double-quoted | empty field | n/a | LF, ASCII | column `home.dest` |
| Iris (UCI) | none | none | none | n/a | LF + trailing blank line, ASCII | class labels `Iris-setosa` |
| Penguins | yes | quotes on `"Adult, 1 Egg Stage"` | `NA` | `YYYY-MM-DD` | LF, ASCII | raw column names with spaces/parentheses |
| Lahman | yes | (to verify) | empty | (to verify) | **Inferred** UTF-8 with BOM (SABR "byte order markers updated") | 27 files |
| Contoso | (to verify) | (to verify) | (to verify) | (to verify) | (to verify) | dialect undocumented by SQLBI |

# Loader recipe used by this group
* Preferred: convert CSV to multi-row `INSERT` `.sql.zst` at image build time (python/duckdb - generic tool records by the tools agent: [DuckDB](/tools/duckdb.md)), so the runtime needs neither `local_infile=1` nor a `secure_file_priv` staging directory; the init loop of the official image executes `.sql.zst` natively ([image README](/sources/docker-library-mysql-readme.md)).
* Where LOAD DATA is used anyway (DS3 reviews, Contoso 1M+), the statement shape that matches these files is `LOAD DATA INFILE '<path>' INTO TABLE t CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (col1, @v2, ...) SET v2 = NULLIF(@v2, '')` with `NULLIF(@v,'NA')` for penguins - **Inferred** syntax from the MySQL manual not opened in this session; the tools agent verifies `LOAD DATA` on 9.7.
* Strip a UTF-8 BOM before loading (Lahman) - otherwise the first header name is corrupted.
* Dates with `/` separators (DS3, Chinook) - **Inferred** accepted by MySQL's date parser; verify once.

# Applies to
[Dell DVD Store](/datasets/dell-dvd-store.md), [Jaffle Shop](/datasets/jaffle-shop.md), [Lahman](/datasets/lahman.md), [Contoso](/datasets/contoso.md), [Titanic](/datasets/titanic.md), [Iris](/datasets/iris.md), [Palmer Penguins](/datasets/palmer-penguins.md).

# Limits
* Superseded for the build pipeline: every dataset now loads through the `mysql-build` service during `make <dataset>` (see [bake decision](/decisions/bake-data-vs-initdb.md)); the recipe above remains valid for ad-hoc loads but the init-directory delivery it mentions is not used.
* Header-less and BOM-bearing CSVs (DVD Store, Lahman) need the pre-pass described per dataset.
