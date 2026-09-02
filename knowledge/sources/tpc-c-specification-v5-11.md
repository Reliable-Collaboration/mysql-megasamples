---
type: Source
title: TPC Benchmark C Standard Specification Revision 5.11 (February 2010)
description: The current TPC-C spec (v5.11.0 on the TPC page); read for per-warehouse cardinalities, population rules, NURand constants and the trademark/copying notice.
resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/tpc-c_v5.11.0.pdf
tags: [tpc-c, specification]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/tpc-c_v5.11.0.pdf
    title: TPC BENCHMARK C Standard Specification Revision 5.11, February 2010
    accessed: "2026-09-02"
    version: Revision 5.11, 1.1 MB PDF (text extracted locally)
---

# What was read
Title page, revision history, Clauses 1.1, 1.3, 2.1.6, 4.2, 4.3.3, Appendix A.6.

# Relevant excerpt (verbatim)
* "TPC Benchmark, TPC-C, and tpmC are trademarks of the Transaction Processing Performance Council. Permission to copy without fee all or part of this material is granted provided that the TPC copyright notice, the title of the publication, and its date appear, and notice is given that copying is by permission of the Transaction Processing Performance Council. To copy otherwise requires specific permission."
* 1.1: "Each regional warehouse covers 10 districts. Each district serves 3,000 customers. All warehouses maintain stocks for the 100,000 items sold by the Company."
* Clause 4.2 table, "cardinality of the initial population per warehouse": WAREHOUSE 1 (89 B); DISTRICT 10 (95 B); CUSTOMER 30k (655 B); HISTORY 30k (46 B); ORDER 30k (24 B); NEW-ORDER 9k (8 B); ORDER-LINE 300k (54 B); STOCK 100k (306 B); ITEM 100k (82 B) with footnote 2 "Fixed cardinality: does not scale with number of warehouses" on ITEM and footnote 4 "One percent (1%) variation in row cardinality is allowed" on ORDER/NEW-ORDER/ORDER-LINE. "The increment (granularity) for scaling the database and the terminal population is one warehouse".
* 4.3.3.1 population: ITEM "100,000 rows ... I_IM_ID random within [1 .. 10,000] ... I_PRICE random within [1.00 .. 100.00] ... For 10% of the rows ... "ORIGINAL""; per warehouse "100,000 rows in the STOCK table", "10 rows in the DISTRICT table ... D_YTD = 30,000.00 D_NEXT_O_ID = 3,001"; per district "3,000 rows in the ORDER table ... O_C_ID selected sequentially from a random permutation of [1 .. 3,000] ... O_CARRIER_ID random within [1 .. 10] if O_ID < 2,101, null otherwise O_OL_CNT random within [5 .. 15]"; "A number of rows in the ORDER-LINE table equal to O_OL_CNT ... OL_DELIVERY_D = O_ENTRY_D if OL_O_ID < 2,101, null otherwise ... OL_AMOUNT = 0.00 if OL_O_ID < 2,101, random within [0.01 .. 9,999.99] otherwise"; "900 rows in the NEW-ORDER table corresponding to the last 900 rows in the ORDER table for that district (i.e., with NO_O_ID between 2,101 and 3,000)". W_YTD = 300,000.00; W_TAX/D_TAX random within [0.0000 .. 0.2000]; zip = 4 random digits + '11111'.
* 2.1.6 NURand(A, x, y) = (((random(0, A) | random(x, y)) + C) % (y - x + 1)) + x; A = 255 for C_LAST, 1023 for C_ID, 8191 for OL_I_ID; "C is a run-time constant randomly chosen within [0 .. A]"; 2.1.6.1 C-Load (used at population) vs C-Run must differ by C-Delta in [65..119] excluding 96 and 112.
* Appendix A.6 "Sample Load Program": `#define MAXITEMS 100000 #define CUST_PER_DIST 3000 #define DIST_PER_WARE 10 #define ORD_PER_DIST 3000` — the constants every OSS loader copies.
* Clause 1.3.1 says "variable text, size N ... If the attribute is stored as a fixed length string ... it must be padded with spaces" and the ORDER table is named ORDER (a reserved word in MySQL; every MySQL implementation names it `orders`).

# What it was used to decide
[TPC-C dataset](/datasets/tpc-c.md) row counts, determinism analysis, naming; [TPC-C implementation choice](/decisions/tpcc-implementation-choice.md).
