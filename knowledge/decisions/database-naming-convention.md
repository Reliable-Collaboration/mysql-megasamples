---
type: Decision
title: Database naming convention and account model
description: One MySQL database per dataset named in lower snake_case after the dataset, with a shared read-only demo user and a read-write admin user.
resource: /decisions/database-naming-convention.md
tags:
- decision
- naming
- accounts
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:17:31Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:17:31Z"
sources:
- resource: /sources/mysql-refman-9-7-stored-objects-security.md
  accessed: "2026-09-02"
- resource: /sources/mysql-refman-9-7-privileges-provided.md
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/identifier-case-sensitivity.html
  title: Identifier case sensitivity (cited via tools/mysql-9x-behaviour-notes.md)
  accessed: "2026-09-02"
---

# Question
How are databases, tables and users named so that 30 datasets coexist predictably?

# Options considered
1. **Lower snake_case database per dataset, tables keep upstream names but lower-cased with schema prefix where the source had schemas** (chosen).
2. Keep upstream casing (`SalesOrderHeader`) — rejected: Linux MySQL is case-sensitive for table names by default (`lower_case_table_names=0`), so mixed-case names make ad-hoc queries fragile and differ from macOS/Windows behaviour. Setting `lower_case_table_names=1` at init is possible but then the image differs from most users' servers; we prefer names that behave identically everywhere.
3. One database per source schema (`adventureworks_sales`, `adventureworks_person`) — rejected for the default because cross-schema foreign keys become cross-database, which MySQL allows but most tools display poorly; see [schema-to-database mapping](/decisions/schema-to-database-mapping.md).

# Evidence
* [Identifier case sensitivity](/sources/mysql-refman-9-7-identifier-case-sensitivity.md): `lower_case_table_names=0` on Linux makes table names case-sensitive.
* [Stored-object security](/sources/mysql-refman-9-7-stored-objects-security.md) and [privileges](/sources/mysql-refman-9-7-privileges-provided.md) for the account model.
* [Schema-to-database mapping](/decisions/schema-to-database-mapping.md) for multi-schema sources.

# Outcome
* Database names: `northwind`, `pubs`, `adventureworks`, `adventureworks_dw`, `adventureworks_lt`, `wideworldimporters`, `wideworldimporters_dw`, `contoso`, `oracle_hr`, `oracle_sh`, `oracle_co`, `oracle_oe`, `sakila`, `chinook`, `dvdstore`, `jaffle_shop` (plus `jaffle_shop_gen` for non-reproducible jafgen output), `tpch`, `tpcds`, `tpcc`, `ssb`, `nyc_taxi`, `enron`, `bts_ontime`, `chicago_crimes`, `smallsets` (titanic, iris, penguins as tables), `employees`, `stackexchange_<site>`, `wikipedia_simple`, `lahman`, `citibike`, `divvy`. Final per-dataset names are confirmed in each dataset record.
* **Reserved words.** Lower-casing does not make an identifier safe: MySQL reserves `RANK`, `GROUP`, `SYSTEM`, `ROWS`, `OVER`, `LEAD`, `LAG`, `CUBE`, `RECURSIVE` and the other window-function keywords added in 8.0.2. Any column or table whose name is a reserved word keeps the name and is written with backticks everywhere (`` `rank` ``, `` `group` ``); the converter emits backticked DDL for every identifier, and `name_map.yaml` marks the affected columns so the smoke tests quote them too. Known instances: Lahman `teams.rank` and `teamshalf.rank`, AdventureWorks `sales_salesterritory.group`. Columns starting with a digit (Lahman `2b`, `3b`) need the same treatment ([keywords](/sources/mysql-refman-9-7-keywords.md)).
* Table names: lower snake_case; multi-schema sources use `<schema>_<table>` (`sales_salesorderheader` → written as `sales_sales_order_header`? **No**: keep upstream words, only lower-case and prefix: `sales_salesorderheader`) so that upstream documentation still maps one-to-one. Column names keep upstream spelling lower-cased.
* Every database gets a `_meta` table? **No** — instead one shared database `megasamples` holds `datasets` (name, tier, knowledge record path, upstream version, `licenses` JSON array of license ids, `artifacts` JSON array of {id, sha256, size, source}, `row_counts` JSON, build id) so provenance is queryable from SQL; `scripts/registry.py` is its only writer.
* Accounts (created by `docker/init/00-users.sql` in the builder stage; at run time `entrypoint-wrapper.sh` applies `DEMO_PASSWORD`/`ADMIN_PASSWORD`/`MYSQL_ROOT_PASSWORD` overrides through a generated `--init-file`, see [bake decision](/decisions/bake-data-vs-initdb.md)):
  * `demo` (default password `demo`, override `DEMO_PASSWORD`): `GRANT SELECT, SHOW VIEW ON *.*`; `GRANT EXECUTE ON PROCEDURE/FUNCTION` individually for routines the dataset record marks read-only. Because routines run in DEFINER context by default and "the invoker's privileges are ignored" ([stored-object security](/sources/mysql-refman-9-7-stored-objects-security.md)), every routine and view that `demo` may use is created with `SQL SECURITY INVOKER`; routines that write keep DEFINER=`admin` and are not granted to `demo`. Image test S8 proves `demo` cannot write, including via `CALL`.
  * `admin` (default `admin`, override `ADMIN_PASSWORD`): `GRANT ALL PRIVILEGES ON *.* WITH GRANT OPTION` plus dynamic `ROLE_ADMIN, SET_ANY_DEFINER` ([privileges](/sources/mysql-refman-9-7-privileges-provided.md)); `root@'%'` is created in the builder stage with the default password `root` (the official entrypoint's `docker_setup_db`, which normally creates it from `MYSQL_ROOT_PASSWORD`, never runs on a baked data directory) and `MYSQL_ROOT_PASSWORD` overrides it at run time through the wrapper; `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_ONETIME_PASSWORD` and `MYSQL_RANDOM_ROOT_PASSWORD` are not supported and the README says so.
  * Authentication plugin `caching_sha2_password` only (9.x removed `mysql_native_password`, see [MySQL 9.x notes](/tools/mysql-9x-behaviour-notes.md)); client libraries older than 2018 cannot connect, which the README states.

# Status
accepted
