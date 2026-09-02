---
type: Source
title: Star Schema Benchmark, Revision 3 (O'Neil, O'Neil, Chen, June 5 2009)
description: The reference paper defining the SSB schema, cardinalities and 13 queries.
resource: https://www.cs.umb.edu/~poneil/StarSchemaB.PDF
tags: [ssb, paper]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.cs.umb.edu/~poneil/StarSchemaB.PDF
    title: Star Schema Benchmark Revision 3, June 5, 2009
    accessed: "2026-09-02"
    version: Revision 3, June 5 2009; 137 KB PDF (text extracted locally)
---

# What was read
Title, Sections 1–3.1 (schema figures, table layouts, query flights).

# Relevant excerpt (verbatim unless noted)
* Title page: "Star Schema Benchmark Revision 3, June 5, 2009 Pat O'Neil, Betty O'Neil, Xuedong Chen {poneil, eoneil, xuedchen}@cs.umb.edu UMass/Boston".
* "The SSB ... is based on the TPC-H benchmark [TPC-H], modified in a number of ways"; "We combine the TPC-H LINEITEM and ORDERS tables into one sales fact table that we name LINEORDER"; "We drop the PARTSUPP table"; NATION/REGION snowflakes are folded into CUSTOMER/SUPPLIER as C_NATION/C_REGION etc.
* Figure 1.2 cardinalities: LINEORDER SF*6,000,000; PART 200,000*[1+log2 SF]; CUSTOMER SF*30,000; SUPPLIER SF*2,000; DATE "7 Years of Days".
* 2.6 DATE layout "(7 years of days)": D_DATEKEY "unique id -- e.g. 19980327"; D_DATE fixed text 18 ("December 22, 1998"); D_DAYOFWEEK fixed text 8; D_MONTH fixed text 9; D_YEAR "unique value 1992-1998"; D_YEARMONTHNUM numeric (YYYYMM); D_YEARMONTH fixed text 7 ("Mar1998"); D_DAYNUMINWEEK 1-7; D_DAYNUMINMONTH 1-31; D_DAYNUMINYEAR 1-366; D_MONTHNUMINYEAR 1-12; D_WEEKNUMINYEAR 1-53; D_SELLINGSEASON text 12; four 1-bit flags; PK D_DATEKEY.
* 2.3 PART: "200,000*floor(1+log2SF)"; P_MFGR fixed text 6 (MFGR#1-5); P_CATEGORY 7 (CARD 25); P_BRAND1 9 (CARD 1000); P_COLOR variable 11 (CARD 94); P_TYPE 25; P_SIZE 1-50; P_CONTAINER 10.
* LINEORDER layout: LO_ORDERKEY "numeric (int up to SF 300) first 8 of each 32 keys populated"; LO_LINENUMBER 1-7; LO_CUSTKEY/LO_PARTKEY/LO_SUPPKEY FKs; LO_ORDERDATE FK to D_DATEKEY; LO_ORDERPRIORITY fixed 15; LO_SHIPPRIORITY fixed 1; LO_QUANTITY 1-50; LO_EXTENDEDPRICE ≤ 55,450; LO_ORDTOTALPRICE ≤ 388,000; LO_DISCOUNT 0-10; LO_REVENUE = (lo_extendedprice*(100-lo_discnt))/100; LO_SUPPLYCOST; LO_TAX 0-8; LO_COMMITDATE FK to D_DATEKEY; LO_SHIPMODE fixed 10; "Compound Primary Key: LO_ORDERKEY, LO_LINENUMBER". "Text is in 8-bit ASCII."
* Customers: "We change the number of customers to SF*30,000".
* 3.1 queries, four flights Q1.1–Q1.3, Q2.1–Q2.3, Q3.1–Q3.4, Q4.1–Q4.3; Q1.1: `select sum(lo_extendedprice*lo_discount) as revenue from lineorder, date where lo_orderdate = d_datekey and d_year = 1993 and lo_discount between 1 and 3 and lo_quantity < 25;` with expected selectivity "0.0194805*6,000,000 ≈ 116,883" rows at SF=1; Q1.2 (d_yearmonthnum = 199401, discount 4–6, quantity 26–35) ≈ 3896 rows.
* The paper does not name the generator "dbgen" (the word does not occur); it references the TPC-H spec page numbers for distributions.

# What it was used to decide
[SSB dataset](/datasets/ssb.md); [ssb-dbgen tool record](/tools/ssb-dbgen.md).
