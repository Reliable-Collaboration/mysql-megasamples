---
type: Source
title: TPC Benchmark DS Standard Specification Version 2.10.0 (as shipped in tpcds-kit)
description: The TPC-DS spec version that tpcds-kit and DuckDB's dsdgen implement; read for the 24-table row counts at 1 GB, scale factors and the minor query modification list.
resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/specification/TPC-DS_v2.10.0.pdf
tags: [tpc-ds, specification]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/specification/TPC-DS_v2.10.0.pdf
    title: TPC BENCHMARK DS Standard Specification Version 2.10.0, September 2018
    accessed: "2026-09-02"
    version: 2.10.0, 3.4 MB PDF (text extracted locally)
---

# What was read
Only the v2.10.0 PDF was read. The current v4.0.0 PDF (https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-DS_v4.0.0.pdf, 2.9 MB) was downloaded but its subset fonts defeated local text extraction, so it is deliberately absent from `sources` and nothing in this bundle cites it.
Version 2.10.0 (September 2018): Clauses 3.1–3.3, 4.2.3, Table 3-2. The current v4.0.0 PDF could not be text-extracted locally; its content is **not** cited anywhere in this bundle (see [open question](/questions/tpcds-dsdgen-version-output-identity.md)).

# Relevant excerpt (verbatim)
* 3.1.2: "The set of scale factors defined for TPC-DS is: 1TB, 3TB, 10TB, 30TB, 100TB"; Table 3-1 maps them to SF 1000, 3000, 10000, 30000, 100000. 3.1.4: "No other scale factors may be used for a TPC-DS result." 3.2.2 comment: "The 1GB entries are used solely for the qualification database (see Clause 3.3.1) and are included here for ease of reference."
* Table 3-2 Database Row Counts, 1GB column ("Number of rows are within 1/100th Percent of these numbers"): call_center 6; catalog_page 11,718; catalog_returns 144,067; catalog_sales 1,441,548; customer 100,000; customer_address 50,000; customer_demographics 1,920,800; date_dim 73,049; household_demographics 7,200; income_band 20; inventory 11,745,000; item 18,000; promotion(s) 300; reason 35; ship_mode 20; store 12; store_returns 287,514; store_sales 2,880,404; time_dim 86,400; warehouse 5; web_page 60; web_returns 71,763; web_sales 719,384; web_site 30. (Avg row sizes are also given, e.g. store_sales 164 B, catalog_sales 226 B, web_sales 226 B, inventory 16 B.)
* 4.2.3.4 minor query modifications include: a) table names; "3. WITH() clause ... can be replaced with semantically equivalent derived tables or views"; b) outer/inner join syntax; c) "4. Rollup operator - an operator of the form "rollup (x,y)" may be substituted with the following operator: "x,y with rollup""; e) aliases, "GROUP BY <ordinal>"; f) "1. Date expressions - ... vendor-specific syntax may be used ... e.g. "DATE(<date>) + 3 MONTHS""; "4. Substring Scalar Functions ... "SUBSTRING(S_ZIP, 1, 5)""; "5. Standard Deviation Function ... (stddev_samp), vendor specific syntax may be used (e.g. stdev, stddev)"; "6. Explicit Casting"; "8. Date casting"; "9. Casting syntax". 4.2.3.3: "The use of minor modifications shall be disclosed and justified".

# What it was used to decide
[TPC-DS dataset](/datasets/tpc-ds.md) shape, MySQL query porting rules and tests.
