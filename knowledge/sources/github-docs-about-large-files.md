---
type: Source
title: "GitHub Docs: About large files on GitHub"
description: Repository size guidance (< 1 GB ideal, < 5 GB strongly recommended), 50 MiB warning, 100 MiB block, 25 MiB browser upload, releases for binaries.
resource: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
tags:
- github
- limits
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
sources:
- resource: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
  title: "GitHub Docs: About large files on GitHub"
  accessed: "2026-09-02"
---

# What was read
https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github, accessed 2026-09-02.

# Relevant excerpt
> "We recommend repositories remain small, ideally less than 1 GB, and less than 5 GB is strongly recommended."
* A warning is issued for files over 50 MiB; "GitHub blocks files larger than 100 MiB." "If you add a file to a repository via a browser, the file can be no larger than 25 MiB."
> "To track files beyond this limit, you must use Git Large File Storage (Git LFS)."
* For distributing large binaries the page points to creating releases on GitHub.com.

# What it was used to decide
[GitHub limits](/tools/github-limits.md): no converted data file over 50 MiB is committed; large artifacts go to release assets, not LFS.
