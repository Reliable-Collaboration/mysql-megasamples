---
type: Source
title: "GitHub Docs: Actions limits"
description: "6-hour job limit, 35-day workflow limit, 256-job matrix, 10 GB cache per repository, concurrent job counts, GITHUB_TOKEN 1,000 requests/hour."
resource: https://docs.github.com/en/actions/reference/limits
tags: [github, actions, limits]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://docs.github.com/en/actions/reference/limits
    title: "GitHub Docs: Actions limits"
    accessed: 2026-09-02
---

# What was read
https://docs.github.com/en/actions/reference/limits, accessed 2026-09-02.

# Relevant excerpt
> "Each job in a workflow can run for up to 6 hours of execution time."
* Workflow runs are cancelled at 35 days; "A job matrix can generate a maximum of 256 jobs per workflow run."; cache storage "10 GB" per repository; concurrent jobs Free 20, Pro 40, Team 60, Enterprise 500; GITHUB_TOKEN "1,000 requests per hour per repository"; workflow trigger events "1500 events / 10 seconds".

# What it was used to decide
[GitHub limits](/tools/github-limits.md): CI builds the core image only; extended-tier conversions that exceed the 6-hour/14 GB envelope run locally and publish release assets.
