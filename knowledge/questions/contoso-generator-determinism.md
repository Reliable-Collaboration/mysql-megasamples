---
type: Open Question
title: Is Contoso Data Generator V2 output byte-identical across runs and platforms for the same config?
description: All RNGs are seeded with constants in source, but .NET Random(seed) algorithms differ between frameworks/versions and the engine mentions multithreading; the published csv-100k.7z may or may not match a regenerated set.
resource: /questions/contoso-generator-determinism.md
tags:
- contoso
- generator
- determinism
status: draft
trust: open
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2/main/DatabaseGenerator/Engine.cs
  title: Engine.cs Random(0) usage
  accessed: "2026-09-02"
---

# Question
Can the project regenerate Contoso at a chosen OrdersCount and get the same row counts/checksums every build? Constant seeds suggest yes for a fixed tool binary; .NET's `Random(int)` sequence is stable within .NET 8 but not guaranteed across major versions, and parallel sections (if any consume `rng`) could reorder draws.

# Cheapest experiment
Run the 2.0.1 linux-x64 binary twice with the `csv-10k` parameters from build_single.cmd on the same machine; compare sha256 of the outputs. Then compare against the published `csv-10k.7z` contents. Record results here; if identical, extended-tier regeneration can use checksum tests; otherwise ship only published archives.

# Related
[Contoso](/datasets/contoso.md), [tool](/tools/contoso-data-generator-v2.md).

# Resolves
Records that depend on the answer:
* [contoso.md](/datasets/contoso.md)
* [github-sql-bi-contoso-v2-generator-source.md](/sources/github-sql-bi-contoso-v2-generator-source.md)
* [contoso-data-generator-v2.md](/tools/contoso-data-generator-v2.md)
* PLAN.md §9 risk register (outside the bundle)
