---
type: Tool
title: jafgen (Jaffle Shop Generator) 0.4.14
description: Python CLI that simulates a jaffle shop and writes raw_*.csv files for customers, orders, items, products, supplies, stores, tweets; Apache-2.0; not idempotent (no seed option).
resource: https://github.com/dbt-labs/jaffle-shop-generator
tags: [tool, generator, jaffle-shop, python, apache-2-0]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-generator/main/README.md
    title: jafgen README
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-generator/main/pyproject.toml
    title: pyproject.toml / cli.py / simulation.py
    accessed: "2026-09-02"
  - resource: https://pypi.org/pypi/jafgen/json
    title: PyPI jafgen
    accessed: "2026-09-02"
  - resource: https://api.github.com/repos/dbt-labs/jaffle-shop-generator
    title: GitHub API (Apache-2.0, latest release v0.4.14 2024-04-27, last push 2025-12-17)
    accessed: "2026-09-02"
---

# Facts
* Package `jafgen` 0.4.14 on PyPI; repository latest tag v0.4.14 (2024-04-27), main pushed 2025-12-17; Apache-2.0 ([README](/sources/github-dbt-labs-jaffle-shop-generator-readme.md), [source](/sources/github-dbt-labs-jaffle-shop-generator-source.md)).
* Requires Python >= 3.10; dependencies numpy, Faker, typer.
* CLI: `jafgen [YEARS] [--days N] [--pre PREFIX]`; default 1 year when neither is given; `sim_days = 365*years + days`; output directory `jaffle-data/` with `raw_customers.csv, raw_orders.csv, raw_items.csv, raw_products.csv, raw_stores.csv, raw_supplies.csv` (+ tweets per README; the checked-in 1-year output in dbt-labs/jaffle-shop has six files without tweets - [seeds inspection](/sources/github-dbt-labs-jaffle-shop-seeds-jaffle-data.md)).
* Determinism: README states "jafgen is not idempotent ... the output data is always unique"; the code uses `Faker()` and `numpy.random` without seeding. Reproducible builds therefore require either vendoring a generated snapshot or patching `Faker.seed()`/`np.random.seed()` in - **Inferred:** a small monkey-patch wrapper would make it deterministic, untested.
* Scale: the checked-in 1-year run yields 935 customers, 61,948 orders, 90,900 items (16.4 MB CSV); the public 6-year S3 snapshot is 546 MB of CSV ([S3 HEAD](/sources/dbt-tutorial-public-s3-long-term-dataset.md)). Up to 10 years is documented by the jaffle-shop README.

# Use in this project
Optional extended-tier generator for a larger Jaffle Shop (`pipx run jafgen 3`), run at build time in a python:3.12 stage (**Inferred** container choice). Core ships the static classic seeds and, optionally, the vendored 1-year snapshot.

# Limits
* No seed option and explicitly non-idempotent: two runs differ, so generated data is never a reproducible artifact and is loaded into `jaffle_shop_gen` with counts recorded per run.
* Default one simulated year; larger runs scale roughly 62 K orders per year.
