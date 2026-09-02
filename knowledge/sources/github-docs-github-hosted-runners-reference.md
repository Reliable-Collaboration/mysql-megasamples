---
type: Source
title: "GitHub Docs: GitHub-hosted runners reference"
description: "Standard public-repository Linux runner: 4 vCPU, 16 GB RAM, 14 GB SSD (ubuntu-latest/24.04/22.04); private repositories 2 vCPU / 8 GB; ubuntu-slim 1 vCPU / 5 GB."
resource: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
tags:
- github
- actions
- runners
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
sources:
- resource: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
  title: "GitHub Docs: GitHub-hosted runners reference"
  accessed: "2026-09-02"
---

# What was read
https://docs.github.com/en/actions/reference/runners/github-hosted-runners, accessed 2026-09-02.

# Relevant excerpt
* Public repositories: Linux x64 4 CPU, "16 GB" RAM, "14 GB" SSD, labels `ubuntu-latest`, `ubuntu-24.04`, `ubuntu-22.04`; Windows 4 CPU / 16 GB / 14 GB; macOS Intel 4 CPU / 14 GB / 14 GB; macOS arm64 "3 (M1)" / "7 GB"; `ubuntu-slim` 1 CPU / "5 GB" / "14 GB".
* Private repositories: Linux x64 2 CPU / 8 GB / 14 GB.
> "The -latest runner images are the latest stable images" but may not be the newest OS version.

# What it was used to decide
[GitHub limits](/tools/github-limits.md): the 14 GB SSD is the binding constraint for building a multi-GB data image in CI; the core-tier image must stay well under it including the builder stage.
