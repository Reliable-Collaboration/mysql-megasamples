---
type: Open Question
title: What changed in dsdgen/dsqgen between 2.10.0 (open ports) and the official TPC-DS Tools 4.0.0?
description: The current spec is 4.0.0 but tpcds-kit and DuckDB implement 2.10.0; the v4.0.0 PDF could not be text-extracted in this session and the TPC-DS homepage describes only pricing changes.
resource: /questions/tpcds-dsdgen-version-output-identity.md
tags: [question, tpc-ds, generator]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.tpc.org/tpcds/
    accessed: 2026-09-02
  - resource: https://duckdb.org/docs/current/core_extensions/tpcds.html
    accessed: 2026-09-02
  - resource: https://github.com/gregrahn/tpcds-kit
    accessed: 2026-09-02
---

# Question
DuckDB states its generator "will change in DuckDB version 2.0 to make the generator compatible with TPC-DS version 4", implying v4 (or v3) changed dsdgen output or schema. The tpcds-kit README lists only macOS and template fixes over 2.10.0. Which tables/columns/row counts differ between 2.10.0 and 4.0.0?

# Cheapest experiment
1. Open the v4.0.0 spec PDF in a PDF reader (WebFetch and the local zlib extractor both failed on its fonts) and read its revision history (front matter) and Table 3-2; note any row-count or column changes versus [2.10.0](/sources/tpc-ds-specification-v2-10-0.md).
2. Optionally download TPC-DS_Tools_v4.0.0.zip via the form and `diff -r tools/` against tpcds-kit; generate SF=1 with both and compare counts.
3. Record the outcome in the [TPC-DS record](/datasets/tpc-ds.md) and state the generator version in the README.

# Resolves
Whether `tpcds` should be described as "TPC-DS 2.10-derived" and whether to switch generators when DuckDB 2.0 ships.
