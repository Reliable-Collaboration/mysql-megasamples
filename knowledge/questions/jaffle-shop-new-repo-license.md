---
type: Open Question
title: Under what license are the new dbt-labs/jaffle-shop seeds and the S3 long_term_dataset distributed?
description: dbt-labs/jaffle-shop (main, 2026-07) has no LICENSE file and GitHub reports none; the 6-year S3 CSVs carry no license statement either. Only jaffle-shop-classic and jafgen are Apache-2.0.
resource: /questions/jaffle-shop-new-repo-license.md
tags: [jaffle-shop, license, open]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://api.github.com/repos/dbt-labs/jaffle-shop
    title: repository metadata (license null; /license 404)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop/main/README.md
    title: README (no license section)
    accessed: "2026-09-02"
---

# Question
Can the project redistribute `seeds/jaffle-data/*.csv` from dbt-labs/jaffle-shop or the S3 `long_term_dataset` CSVs? Without a license grant, GitHub's terms allow viewing/forking only. The data is jafgen output (Apache-2.0 tool), but tool output is not automatically licensed.

# Cheapest experiment
Open an issue on dbt-labs/jaffle-shop asking for a LICENSE file (or confirmation that the seeds are Apache-2.0 like the classic repo). Until answered: ship only the classic seeds (Apache-2.0) in core, and generate larger data with jafgen at build time (our own output) instead of vendoring the unlicensed files.

# Related
[Jaffle Shop](/datasets/jaffle-shop.md), [decision](/decisions/jaffle-shop-conversion-path.md).

# Resolves
Records that depend on the answer:
* [jaffle-shop.md](/datasets/jaffle-shop.md)
* [jaffle-shop-conversion-path.md](/decisions/jaffle-shop-conversion-path.md)
* [apache-2-0.md](/licenses/apache-2-0.md)
* [dbt-tutorial-public-s3-long-term-dataset.md](/sources/dbt-tutorial-public-s3-long-term-dataset.md)
* [github-dbt-labs-jaffle-shop-readme.md](/sources/github-dbt-labs-jaffle-shop-readme.md)
* PLAN.md §9 risk register (outside the bundle)
