---
type: Decision
title: Small teaching datasets (titanic, iris, penguins) - one database each versus a shared `smallsets` database
description: Recommend separate databases `titanic`, `iris`, `penguins` (uniform per-dataset tooling and license mapping); record `smallsets` as the alternative; all three are loaded from vendored CSV via build-time generated INSERT scripts.
resource: /decisions/smallsets-database-layout.md
tags: [decision, smallsets, titanic, iris, penguins, naming]
status: stable
trust: inferred
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:48:59Z" }
sources:
  - resource: https://hbiostat.org/data/repo/titanic3.csv
    title: titanic3.csv (117 KB)
    accessed: 2026-09-02
  - resource: https://archive.ics.uci.edu/static/public/53/iris.zip
    title: iris.zip (3.7 KB)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv
    title: penguins.csv (15 KB)
    accessed: 2026-09-02
---

# Question
Three single-table teaching datasets with three different licenses: separate databases or one `smallsets` database?

# Options considered
1. Separate databases `titanic`, `iris`, `penguins` - one dataset = one database = one license notice = one init script, identical to every other dataset in the image; `SHOW DATABASES` grows by three tiny entries.
2. One database `smallsets` with tables `titanic`, `iris`, `penguins`, `penguins_raw` - tidier listing, but mixes CC0 / CC BY 4.0-or-BSD / hbiostat-permission content in one schema and breaks the "database name = dataset" convention used for tests and docs.

# Evidence
Sizes (all under 120 KB) make either option free; the difference is purely organisational. Each dataset record already lists its own attribution block ([Titanic](/datasets/titanic.md), [Iris](/datasets/iris.md), [Palmer Penguins](/datasets/palmer-penguins.md)).

# Outcome
The coordinator's [database naming convention](/decisions/database-naming-convention.md) already fixes option 2: database `smallsets` with tables `titanic`, `iris`, `penguins`, `penguins_raw`. This group's preference was option 1 (separate databases) for one-dataset-one-license uniformity; the difference is organisational only, so option 2 is adopted and the `smallsets` README must carry all three notices (hbiostat permission, Fisher/UCI CC BY 4.0 or scikit-learn BSD-3, CC0 + penguin citations). Loading: vendored CSVs converted to INSERT scripts at build time (header skip, `NA`/empty -> NULL, explicit DECIMAL types), so no `local_infile` is required at runtime.

# Status
accepted (follows /decisions/database-naming-convention.md)
