---
type: Source
title: dbt-labs/jaffle-shop-generator README (jafgen)
description: jafgen CLI - Python >= 3.10, `jafgen [years] --days N --pre PREFIX`, seven entity tables, explicitly non-idempotent (no seed).
resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-generator/main/README.md
tags: [jafgen, generator, readme]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-generator/main/README.md
    title: README.md (4,993 bytes)
    accessed: 2026-09-02
    version: main @ 01c0e83 (2025-12-17); latest tag v0.4.14 (2024-04-27)
---

# What was read
README in full, accessed 2026-09-02.

# Relevant excerpt
* "This is not an official dbt Labs project. It is maintained on a volunteer basis by dbt Labs employees".
* Tables: "Customers (who place Orders), Orders, Products, Order Items, Supplies, Stores, Tweets".
* "Requires Python 3.10 or higher"; `pipx run jafgen [options]` or `pip install jafgen`.
* "`jafgen` takes one argument: `[int]` Years to generate data for. The default is 1 year." Options `--days [int]`, `--pre` (prefix, default `raw`). Example: "Generate a simulation spanning 3 years from 2016-2019 with a prefix of cool: `jafgen 3 --pre cool`".
* "An important caveat is that `jafgen` is _not_ idempotent. By design, it generates new data every time you run it based on the simulation's interactions. ... the output data is always unique."

# What it was used to decide
[jafgen tool record](/tools/jafgen.md); determinism finding in [Jaffle Shop](/datasets/jaffle-shop.md).
