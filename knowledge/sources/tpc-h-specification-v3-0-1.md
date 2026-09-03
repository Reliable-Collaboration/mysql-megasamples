---
type: Source
title: TPC Benchmark H Standard Specification Revision 3.0.1
description: The current TPC-H spec; read for table cardinalities, scale factors, permitted query modifications, the Q1 validation output and the revision history.
resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf
tags:
- tpc-h
- specification
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:30:00Z"
sources:
- resource: https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf
  title: TPC BENCHMARK H (Decision Support) Standard Specification Revision 3.0.1
  accessed: "2026-09-02"
  version: Revision 3.0.1, © 1993-2022, 1.7 MB PDF (text extracted locally)
---

# What was read
Title page, revision history, Clauses 2.1.4, 2.2.3, 2.4.1, 4.1.3, 4.2.5, 4.3.

# Relevant excerpt (verbatim)
* Revision history: "10 February 2021 Revision 3.0.0 Change price performance metric to Price-per-kQphH@Size Affected clauses are: 0.1, 4.1.3.1, 5.4, 5.4.4.1, 5.4.4.2, 5.4.6, 8.4.2.1, 8.4.4.1 Appendix E"; "28 April 2022 Revision 3.0.1 Clarify change log history for Revisions 2.17.3 and 2.18.0 Add comment to Clause 9.2.4.3 Add comment to Clause 2.4.19.5". Neither 3.0.x entry touches Clause 4 data generation; **Inferred:** dbgen output at 2.17.3 and 3.0.1 is identical (open question [dbgen version identity](/questions/tpch-dbgen-version-output-identity.md)).
* Trademark/copying: "TPC Benchmark, TPC-H, QppH, QthH, and QphH are trademarks of the Transaction Processing Performance Council. All parties are granted permission to copy and distribute to any party without fee all or part of this material provided that: 1) copying and distribution is done for the primary purpose of disseminating TPC material; 2) the TPC copyright notice, the title of the publication, and its date appear, and notice is given that copying is by permission of the Transaction Processing Performance Council."
* 4.1.3.1: "Scale factors used for the test database must be chosen from the set of fixed scale factors defined as follows: 1, 10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000 The database size is defined with reference to scale factor 1 (i.e., SF = 1; approximately 1GB as per Clause 4.2.5), the minimum required size for a test database." The qualification database "must be exactly equal to a scale factor, SF, of 1".
* 4.2.5.1 Table 3 (SF=1): SUPPLIER 10,000 (159 B/row, 2 MB); PART 200,000 (155 B, 30 MB); PARTSUPP 800,000 (144 B, 110 MB); CUSTOMER 150,000 (179 B, 26 MB); ORDERS 1,500,000 (104 B, 149 MB); LINEITEM 6,001,215 (112 B, 641 MB); NATION 25; REGION 5; "Total 8,661,245 ... 956" MB. "1 MB is defined to be 2^20 bytes." Footnote 3: "The cardinality of the LINEITEM table is not a strict multiple of SF since the number of lineitems in an order is chosen at random with an average of four".
* 4.2.5.2 Table 4 LINEITEM cardinality: SF1 6001215; SF10 59986052; SF30 179998372; SF100 600037902; SF300 1799989091; SF1000 5999989709.
* 4.3.3: data may be generated to files ("Load from stored records") or piped ("In-line load").
* 2.1.4.1: "QGen is a TPC provided software package that must be used to generate the query text."
* 2.2.3.3 minor query modifications (allowed without approval): a) table/view names; b) select-list aliases; c) "Date expressions - ... vendor-specific syntax may be used instead of the specified SQL-92 syntax"; (further items on row limits per Clause 2.1.2.9).
* 2.4.1 Q1: "DELTA is randomly selected within [60. 120]"; validation "DELTA = 90"; 2.4.1.5 sample output row "A F 37734107.00 56586554400.73 53758257134.87 ... 55909065222.83 25.52 38273.13 .05 1478493".

# What it was used to decide
[TPC-H dataset](/datasets/tpc-h.md) shape, tests and licensing.
