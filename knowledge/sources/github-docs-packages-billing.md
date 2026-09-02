---
type: Source
title: "GitHub Docs: GitHub Packages billing"
description: "Public packages are free; private-package quotas per plan; Actions downloads with GITHUB_TOKEN do not count."
resource: https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-packages/about-billing-for-github-packages
tags: [github, ghcr, billing]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-packages/about-billing-for-github-packages
    title: "GitHub Docs: GitHub Packages billing"
    accessed: 2026-09-02
---

# What was read
https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-packages/about-billing-for-github-packages, accessed 2026-09-02.

# Relevant excerpt
> "GitHub Packages usage is free for public packages."
* Private packages: Free 500 MB storage / 1 GB transfer per month; Pro 2 GB / 10 GB; Team 2 GB / 10 GB; Enterprise Cloud 50 GB / 100 GB. Downloads by Actions using `GITHUB_TOKEN` do not count against the hosting repository.

# What it was used to decide
[GitHub limits](/tools/github-limits.md): a public ghcr.io image costs nothing regardless of pulls, unlike LFS.
