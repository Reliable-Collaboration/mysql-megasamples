---
type: Source
title: TPC-DS homepage (tpc.org/tpcds) — V4 change note
description: States that TPC-DS V4 changed pricing (Dynamic Pricing Model) and that V4 results are not comparable with earlier versions; says nothing about data-generator changes.
resource: https://www.tpc.org/tpcds/
tags: [tpc-ds, versions]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.tpc.org/tpcds/
    title: TPC-DS Homepage
    accessed: "2026-09-02"
---

# What was read
The landing page.

# Relevant excerpt
* "V4 results are not comparable with any previous versions of the benchmark"; V4 introduces a Dynamic Pricing Model (compute decoupled from storage) and a "Pricing Period Cost" definition.
* "The current TPC-DS specification can be found on the TPC Documentation Webpage." No mention of dsdgen/dsqgen changes.

# What it was used to decide
Supports (does not prove) the inference that V3/V4 changed pricing/metric clauses rather than dsdgen output — see [open question](/questions/tpcds-dsdgen-version-output-identity.md).
