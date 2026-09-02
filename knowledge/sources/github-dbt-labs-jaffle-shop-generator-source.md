---
type: Source
title: jaffle-shop-generator source (pyproject.toml, jafgen/cli.py, simulation.py, customers.py)
description: Confirms version 0.4.14, dependencies numpy/Faker/typer, the years/days/pre CLI, and unseeded Faker/numpy random usage.
resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-generator/main/pyproject.toml
tags: [jafgen, source, determinism]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-generator/main/pyproject.toml
    title: pyproject.toml
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-generator/main/jafgen/cli.py
    title: jafgen/cli.py (grep)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-generator/main/jafgen/simulation.py
    title: jafgen/simulation.py (grep)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-generator/main/jafgen/customers/customers.py
    title: jafgen/customers/customers.py (grep)
    accessed: "2026-09-02"
  - resource: https://pypi.org/pypi/jafgen/json
    title: PyPI jafgen JSON (version 0.4.14, license Apache-2.0 text, releases 0.3.1 ... 0.4.14)
    accessed: "2026-09-02"
---

# What was read
pyproject.toml in full; the Python modules grepped for seed/random/years; the PyPI JSON; accessed 2026-09-02.

# Relevant excerpt
* pyproject: `name = "jafgen"`, `version = "0.4.14"`, `dependencies = ["numpy", "Faker", "typer"]`, `license = { file = "LICENSE" }`, script `jafgen = "jafgen.cli:app"`.
* cli.py: typer app with `years` argument ("Number of years to simulate. If neither days nor years are provided, the default is 1 year."), `--days`, `--pre`; `Simulation(years, days, pre)`; simulation.py: `self.sim_days = 365 * self.years + self.days`.
* customers.py and the stores modules call `Faker()` and `fake.random.randint/random/choice` and `np.random.random/normal` with no `seed()` call in any grepped module - no fixed seed.
* PyPI: latest 0.4.14; license metadata is the full Apache-2.0 text; releases include 0.3.1, 0.4.6, 0.4.9-0.4.14.

# What it was used to decide
[jafgen tool record](/tools/jafgen.md) (non-deterministic unless the project patches in seeds).
