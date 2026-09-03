---
type: Source
title: okf.md annotated guide to OKF
description: Third-party annotated guide at okf.md/spec that restates OKF v0.1 with v0.2 additions; used as an entry point, superseded by the GitHub SPEC.md.
resource: https://okf.md/spec/
tags:
- okf
- spec
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:05:32Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:05:32Z"
sources:
- resource: https://okf.md/spec/
  title: Open Knowledge Format (OKF) — An Annotated Guide
  accessed: "2026-09-02"
---

# What was read
https://okf.md/spec/ on 2026-09-02. The page presents itself as "OKF v0.1 — Draft" with v0.2 updates noted separately.

# Relevant excerpt
Paraphrase: only `type` is mandatory; `title`, `description`, `resource`, `tags`, `timestamp` strongly recommended in v0.1; v0.2 adds `sources`, `generated`, `verified`, `status`, `stale_after`, `okf_version`. Concept types are producer-defined ("no central registry"); examples given are BigQuery Table, API Endpoint, Metric, Playbook, Reference, Attested Computation.

# What it was used to decide
Confirmed that the type vocabulary in [the conventions](/runbooks/knowledge-bundle-conventions.md) is legal. The authoritative text is [SPEC.md v0.2](/sources/okf-spec-v0-2.md); where the two differ (e.g. `timestamp`), SPEC.md wins.
