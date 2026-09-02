---
type: Source
title: "GitHub Docs: Working with the Container registry"
description: "ghcr.io: 10 GB per-layer limit, 10-minute upload timeout, no overall image size limit stated; GITHUB_TOKEN authentication in Actions."
resource: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
tags: [github, ghcr, limits]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
    title: "GitHub Docs: Working with the Container registry"
    accessed: 2026-09-02
---

# What was read
https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry, accessed 2026-09-02.

# Relevant excerpt
> "The Container registry has a 10 GB size limit for each layer."
> "The Container registry has a 10 minute timeout limit for uploads."
* No overall image-size limit is stated. Authentication uses a personal access token (classic) or, in Actions, `GITHUB_TOKEN` with `packages: write`.

# What it was used to decide
[GitHub limits](/tools/github-limits.md) and [docker multi-stage record](/tools/docker-build-multistage.md): the baked `/var/lib/mysql` layer must stay under 10 GB (and each layer must upload in 10 minutes), which caps the core tier and argues for splitting large datasets into separate layers or images.
