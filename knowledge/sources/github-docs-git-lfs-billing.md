---
type: Source
title: "GitHub Docs: Git Large File Storage billing"
description: "10 GiB free storage and 10 GiB/month bandwidth on Free and Pro; data packs replaced by metered billing; downloads count against the repository owner."
resource: https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-git-large-file-storage/about-billing-for-git-large-file-storage
tags: [github, limits, lfs, billing]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-git-large-file-storage/about-billing-for-git-large-file-storage
    title: "GitHub Docs: Git Large File Storage billing"
    accessed: "2026-09-02"
---

# What was read
https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-git-large-file-storage/about-billing-for-git-large-file-storage, accessed 2026-09-02.

# Relevant excerpt
* Pricing table: GitHub Free and GitHub Pro include "10 GiB" of bandwidth and "10 GiB" of storage; enterprise tiers "250 GiB".
> "Git LFS billing used pre-paid data packs. These have been removed and replaced with metered billing and you only pay for what you actually use."
> "Bandwidth is billed for each GiB of data downloaded. Storage is billed by calculating an hourly usage rate."
> "When you download a Git LFS file, the bandwidth you use is included in the repository owner's bandwidth usage."

# What it was used to decide
[GitHub limits](/tools/github-limits.md): LFS is rejected for public distribution because every clone by a stranger consumes the owner's 10 GiB/month bandwidth and then bills the owner.
