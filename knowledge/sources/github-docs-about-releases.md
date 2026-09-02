---
type: Source
title: "GitHub Docs: About releases"
description: "Release assets: up to 1000 per release, each under 2 GiB, no total size or bandwidth limit."
resource: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
tags:
- github
- limits
- releases
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
sources:
- resource: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
  title: "GitHub Docs: About releases"
  accessed: "2026-09-02"
---

# What was read
https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases, accessed 2026-09-02.

# Relevant excerpt
> "Releases are based on Git tags, which mark a specific point in your repository's history."
> "GitHub will automatically include links to download a zip file and a tarball containing the contents of the repository at the point of the tag's creation."
> "Up to 1000 release assets may be associated with a single release. Each file included in a release must be under 2 GiB. There is no limit on the total size of a release, nor bandwidth usage."

# What it was used to decide
[GitHub limits](/tools/github-limits.md): extended-tier bundles are split into < 2 GiB parts and published as release assets; [tier model](/decisions/tier-model.md).
