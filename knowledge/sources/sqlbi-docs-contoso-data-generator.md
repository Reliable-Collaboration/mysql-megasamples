---
type: Source
title: docs.sqlbi.com - Contoso Data Generator documentation (index, details, config-json, formats, sqlscripts)
description: SQLBI's documentation site for the generator - generated entities, config parameter definitions, output-format options, SQL Server import scripts; no seed or row-count tables.
resource: https://docs.sqlbi.com/contoso-data-generator/
tags:
- contoso
- documentation
- sqlbi
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://docs.sqlbi.com/contoso-data-generator/
  title: Contoso Data Generator (index)
  accessed: "2026-09-02"
- resource: https://docs.sqlbi.com/contoso-data-generator/details
  title: Details
  accessed: "2026-09-02"
- resource: https://docs.sqlbi.com/contoso-data-generator/config-json
  title: Configuration file (config.json)
  accessed: "2026-09-02"
- resource: https://docs.sqlbi.com/contoso-data-generator/formats
  title: Output formats and related parameters
  accessed: "2026-09-02"
- resource: https://docs.sqlbi.com/contoso-data-generator/sqlscripts
  title: SQL Scripts
  accessed: "2026-09-02"
---

# What was read
The five pages, accessed 2026-09-02 (the `/configuration/` and `/ready-to-use-data/` URLs guessed earlier return 404).

# Relevant excerpt
* Index: generates "demo data" for the Contoso model with entities customer, date, product, store, sales, orders, orderrows, currencyexchange; links to the -Data repository for ready-to-use sets.
* Details: two stages - static data download to a cache ("fake customers, exchange rates, postal codes") producing `_customersall.csv`, then generation of "Customers, Stores, Dates, CurrencyExchanges, Sales, Orders & OrderRows (optional)".
* config-json: "OrdersCount (int) Total number of orders to be generated."; "StartDT (datetime) Date of the first order."; "YearsCount (int) Total number of years generated. Orders are distributed over years."; "CutDateBefore & CutDateAfter (datetime optional parameters) Allow creating data starting from a day different from January 1st and ending on a date different from December 31st."; "CustomerPercentage: Percentage of customers to be used. Range: 0.001 - 1.000"; "OutputFormat: CSV, PARQUET, DELTATABLE"; "SalesOrders: SALES / ORDERS / BOTH"; "CustomerFakeGenerator (int) Number of full random customers. Only used during tests to speed up." No seed parameter documented.
* formats: CSV single or multi-file (`CsvMaxOrdersPerFile` -1 = single file) with optional gz; Parquet row-group size (default 500000 orders); Delta orders-per-file. CSV dialect (delimiter, header, date format) is not documented.
* sqlscripts: `Sql_ImportData.cmd` recreates tables and BULK INSERTs CSVs from `scripts/sql/inputcsv` via SQLCMD (default `(LocalDb)\MSSQLLocalDB`, database ContosoDGV2Test); options sales / orders / both; SQLBI internal scripts name databases "Contoso V2 [row count]" where "row count approximates included orders".

# What it was used to decide
Parameter semantics and the CSV-dialect open question in [Contoso](/datasets/contoso.md).
