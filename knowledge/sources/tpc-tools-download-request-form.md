---
type: Source
title: TPC tools download request form (TPC-H 3.0.1)
description: The registration form behind every TPC tools download; requires personal details and an EULA click-through, then e-mails a download link.
resource: https://www.tpc.org/TPC_Documents_Current_Versions/download_programs/tools-download-request5.asp?bm_type=TPC-H&bm_vers=3.0.1&mode=CURRENT-ONLY
tags: [tpc, download, click-through]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.tpc.org/TPC_Documents_Current_Versions/download_programs/tools-download-request5.asp?bm_type=TPC-H&bm_vers=3.0.1&mode=CURRENT-ONLY
    title: TPC-H Tools download request
    accessed: "2026-09-02"
---

# What was read
The request form page for TPC-H_Tools_v3.0.1.zip (the TPC-DS form is the same page with bm_type=TPC-DS).

# Relevant excerpt
* Required fields: First Name, Last Name, Company/Affiliation, Occupation, Country, Email.
* Checkbox: "I have read and agree to the TPC End User License Agreement - (.txt file)", linking to https://tpc.org/TPC_Documents_Current_Versions/txt/eula.txt (same text as EULA_v2.2.0.txt, see [EULA record](/sources/tpc-eula-v2-2.md)).
* "The TPC Tools are available free of charge, however all users must agree to the licensing terms and register prior to use."
* After submitting: "receive an E-mail at the address that you entered above with a link to the files to download."

# What it was used to decide
The official zips cannot be fetched by an unattended build (form + e-mailed link), so the build clones the GitHub mirrors or uses DuckDB's bundled generators instead — see [TPC-H generator decision](/decisions/tpch-generator-path.md) and [TPC-DS generator decision](/decisions/tpcds-generator-path.md).
