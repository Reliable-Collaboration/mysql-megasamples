---
type: Source
title: TPC End User License Agreement, Version 2.2 (full text)
description: The license that governs dbgen, qgen, dsdgen, dsqgen and every derivative of them; read in full from tpc.org and compared with the copies shipped in tpch-kit, tpcds-kit and DuckDB.
resource: https://www.tpc.org/TPC_Documents_Current_Versions/txt/EULA_v2.2.0.txt
tags: [tpc, license, eula]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/txt/EULA_v2.2.0.txt
    title: END USER LICENSE AGREEMENT VERSION 2.2
    accessed: 2026-09-02
    version: 2.2 (18,323 bytes; HTTP 200)
  - resource: https://tpc.org/TPC_Documents_Current_Versions/txt/eula.txt
    title: eula.txt linked from the download form
    accessed: 2026-09-02
    version: same text, Version 2.2
  - resource: https://raw.githubusercontent.com/gregrahn/tpch-kit/master/EULA.txt
    title: EULA.txt in tpch-kit
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/gregrahn/tpcds-kit/master/EULA.txt
    title: EULA.txt in tpcds-kit
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/duckdb/duckdb/main/extension/tpch/dbgen/LICENSE
    title: LICENSE bundled with DuckDB's dbgen port
    accessed: 2026-09-02
---

# What was read
The complete EULA text (17 clauses plus EU special provisions). The four copies differ only in whitespace/quote characters (the two kits and DuckDB carry Version 2.2 verbatim; tpch-kit's and tpcds-kit's copies are byte-identical to each other; DuckDB's copy equals the tpc.org text after whitespace normalisation).

# Relevant excerpt (verbatim)
* Scope: "license the Software, including, but not limited to, the source code, scripts, executable programs, drivers, libraries and data files associated with such programs, and modifications thereof (the "Software")".
* 3. License Grant: "TPC grants You a restricted, non-exclusive, revocable license to install and use the Materials ... You may download multiple copies of the Materials and make verbatim copies of the original of the Software so long as Your use of such copies complies with the terms of this Agreement."
* 4.b. "Modification: You may modify the Software."
* 4.c. "Public Disclosure: You may not publicly disclose any performance results produced while using the Software except ... (3) any other use of the Software, provided that any performance results must be clearly identified as not being comparable to TPC Benchmark Results unless specifically authorized by TPC."
* 6. "You may not remove the copyright notice from the original or any copy of the Materials, and You must apply the notice if You extract part of the Materials not bearing a notice."
* 7. Use of Name: "User may only use such names, trademarks and logos in accordance with the usage guidelines specified by the TPC Policies."
* 8. "Any portion of the Materials merged into or integrated with other software or documentation will continue to be subject to the terms and conditions of this Agreement."
* 9. Limited Grants of Sublicense: "You may distribute the Software as provided or as modified as permitted under clause 4 b. ... a. If You distribute any portion of the Software in its original form You may do so only under this Agreement by including a complete copy of this Agreement with Your distribution, and if You distribute the Software in modified form, You may only do so under a license that at a minimum provides all of the protections and conditions of use contained within this Agreement; b. You must include on each copy of the Software that You distribute the following legend in all caps, at the top of the label and license, and in a font not less than 12 point and no less prominent than any other printing: "THE TPC SOFTWARE IS AVAILABLE WITHOUT CHARGE FROM TPC."; c. You must retain all copyright, patent, trademark, and attribution notices that are present in the Software; and d. You may not charge a fee for the distribution of this Software".
* 11–14: "AS IS", no warranty, liability capped at US $100.
* 13. Export Assurance (US EAR applies).
* The EULA never mentions the *output* of the generators (the .tbl/.dat rows) — see [open question](/questions/tpc-eula-generated-data-redistribution.md).

# What it was used to decide
[TPC EULA license record](/licenses/tpc-eula.md); redistribution rules in all four benchmark dataset records.
