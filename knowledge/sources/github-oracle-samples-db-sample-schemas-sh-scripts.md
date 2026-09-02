---
type: Source
title: SH schema scripts and CSV data files at v23.3 (sh_install.sql, sh_create.sql, sh_populate.sql, *.csv, README.md)
description: Partitioned DDL, SQLcl LOAD-based population from six CSV files, bitmap/Text indexes, materialized views, dimensions, and the verification row counts of the Sales History schema; plus byte-level samples of the CSV files.
resource: https://github.com/oracle-samples/db-sample-schemas/tree/v23.3/sales_history
tags: [oracle, sh, scripts, csv]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/sales_history/sh_install.sql
    title: sh_install.sql (8,412 B)
    accessed: "2026-09-02"
    version: v23.3
  - resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/sales_history/sh_create.sql
    title: sh_create.sql (25,051 B)
    accessed: "2026-09-02"
    version: v23.3
  - resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/sales_history/sh_populate.sql
    title: sh_populate.sql (41,072 B)
    accessed: "2026-09-02"
    version: v23.3
  - resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/sales_history/sales.csv
    title: sales.csv (74,426,366 B; only HTTP Range samples read)
    accessed: "2026-09-02"
    version: v23.3
  - resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/sales_history/customers.csv
    title: customers.csv (12,615,719 B; header + three 64 KB Range samples read)
    accessed: "2026-09-02"
    version: v23.3
  - resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/sales_history/promotions.csv
    title: promotions.csv (56,158 B; read fully)
    accessed: "2026-09-02"
    version: v23.3
  - resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/sales_history/README.md
    title: sales_history/README.md (2,433 B)
    accessed: "2026-09-02"
    version: v23.3
---

# What was read
The three SQL scripts fully; the CSV headers and small HTTP Range samples (first 1.5 KB of each file, a 64 KB slice from the middle of sales.csv, three 64 KB slices of customers.csv, the tails of times.csv and supplementary_demographics.csv); promotions.csv in full. `Content-Length` headers confirmed the GitHub API sizes. No dataset was downloaded whole except promotions.csv (56 KB).

# Relevant excerpt
* README: "Schema Version 21.1", "Release Date 06-DEC-2022", "19c and higher", **"Requires SQLcl command prompt!"**.
* sh_install.sql grants include `CREATE DIMENSION` and `CREATE MATERIALIZED VIEW`; verification block: `channels 5, costs 82112, countries 35, customers 55500, products 72, promotions 503, sales 918843, times 1826, supplementary_demographics 4500`.
* sh_create.sql: `countries` (9 cols, PK country_id NUMBER), `customers` (23 cols; cust_id NUMBER PK; cust_gender CHAR(1); cust_year_of_birth NUMBER(4); cust_credit_limit NUMBER; cust_eff_from/cust_eff_to DATE; FK country_id), `promotions` (11 cols; promo_id NUMBER(6) PK; promo_cost NUMBER(10,2); promo_begin_date/promo_end_date DATE), `products` (22 cols; prod_id NUMBER(6) PK; prod_desc VARCHAR2(4000); prod_list_price/prod_min_price NUMBER(8,2)), `times` (38 cols; time_id DATE PK; calendar_quarter_desc CHAR(7)), `channels` (6 cols), `sales(prod_id NUMBER(6), cust_id NUMBER, time_id DATE, channel_id NUMBER(1), promo_id NUMBER(6), quantity_sold NUMBER(3), amount_sold NUMBER(10,2))` with FKs to promotions, customers, products, channels, times and **`PARTITION BY RANGE (time_id)` in 15 partitions SALES_2018 … SALES_Q4_2022 (upper bound 2023-01-01)**; `costs(prod_id, time_id, promo_id, channel_id, unit_cost NUMBER(10,2), unit_price NUMBER(10,2))` with FKs and **20 `COMPRESS` range partitions COSTS_Q1_2019 … COSTS_Q4_2023**; `supplementary_demographics(cust_id NUMBER PK, education/occupation/household_size VARCHAR2(21), yrs_residence NUMBER, affinity_card, cricket, baseball, tennis, soccer, golf, unknown, misc NUMBER(10), comments VARCHAR2(4000))`. View `profits` (costs × sales join). Materialized views `cal_month_sales_mv` and `fweek_pscat_sales_mv` (`ENABLE QUERY REWRITE`, referencing `sh.sales` etc.). `COMMENT ON` for tables/columns (sales: "facts table, without a primary key").
* sh_populate.sql: disables all FKs/PKs `NOVALIDATE`; inserts `channels` (5), `countries` (35) and `products` (72) with literal INSERTs (products use `to_date('2019-01-01-00-00-00','YYYY-MM-DD-HH24-MI-SS')`); then **`SET LOAD BATCH_ROWS 10000 BATCHES_PER_COMMIT 1 DATE_FORMAT YYYY-MM-DD`** and `LOAD costs costs.csv`, `LOAD customers customers.csv`, `LOAD promotions promotions.csv`, `LOAD sales sales.csv`, `LOAD times times.csv`, `LOAD supplementary_demographics supplementary_demographics.csv` (SQLcl commands); re-enables constraints `NOVALIDATE`; creates `CREATE BITMAP INDEX ... LOCAL NOLOGGING` on sales (prod_id, cust_id, time_id, channel_id, promo_id) and costs (prod_id, time_id), bitmap indexes on products(prod_status), customers(cust_gender, cust_marital_status, cust_year_of_birth) and on the MV `fweek_pscat_sales_mv`, B-tree indexes products(prod_subcategory), products(prod_category), and **`CREATE INDEX sup_text_idx ON supplementary_demographics(comments) INDEXTYPE IS ctxsys.context PARAMETERS('nopopulate')`** (Oracle Text); `CREATE DIMENSION customers_dim, products_dim, times_dim, channels_dim, promotions_dim`; `dbms_stats.gather_schema_stats('SH')`.
* CSV format (observed): first line is a header of double-quoted column names in table-column order; comma delimiter; string values double-quoted, numbers and dates unquoted; dates `YYYY-MM-DD` with no time; NULL numeric/date as an empty field (`,,`); NULL string as `""` (customers.csv `CUST_MARITAL_STATUS`, `CUST_EFF_TO`); LF line endings, no CR. **sales.csv lines are right-padded with spaces to a fixed width of 80 characters** (808 of 810 sampled lines are exactly 80 chars; hexdump shows `1232.16` followed by 0x20 padding before `\n`); costs.csv, customers.csv, times.csv and promotions.csv are not padded. times.csv is not sorted (first data row 2019-05-31), last rows 2023-12-30/31. supplementary_demographics.csv `COMMENTS` are free-text customer remarks with embedded punctuation but no embedded newlines seen. No non-ASCII bytes in any sample or in promotions.csv/sh_populate.sql.
* Header of sales.csv: `"PROD_ID","CUST_ID","TIME_ID","CHANNEL_ID","PROMO_ID","QUANTITY_SOLD","AMOUNT_SOLD"`; customers.csv has 23 columns matching the DDL; times.csv 38 columns.

# What it was used to decide
[SH dataset record](/datasets/oracle-sh.md); [conversion path](/decisions/oracle-conversion-path.md) (no Oracle needed because the data is plain CSV); [row-count/checksum question](/questions/oracle-sh-csv-row-counts-and-padding.md).
