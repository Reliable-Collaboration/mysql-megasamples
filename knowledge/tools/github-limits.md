---
type: Tool
title: GitHub, GitHub Actions, ghcr.io and Docker Hub limits
description: "Hard numbers that size the repository, the release assets, the CI build and the registry image: 100 MiB file block, < 1 GB repo guidance, 2 GiB per release asset with no total, LFS 10 GiB/month bandwidth then metered, 4 vCPU/16 GB/14 GB SSD runners with 6-hour jobs, 10 GB ghcr layers, Docker Hub 100 anonymous pulls per 6 hours."
resource: https://docs.github.com/
tags:
- tool
- github
- limits
- ci
- registry
- docker-hub
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:49:47Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:49:47Z"
sources:
- resource: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
  accessed: "2026-09-02"
- resource: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
  accessed: "2026-09-02"
- resource: https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-git-large-file-storage/about-billing-for-git-large-file-storage
  accessed: "2026-09-02"
- resource: https://docs.github.com/en/actions/reference/limits
  accessed: "2026-09-02"
- resource: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/actions/runner-images/main/README.md
  accessed: "2026-09-02"
- resource: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
  accessed: "2026-09-02"
- resource: https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-packages/about-billing-for-github-packages
  accessed: "2026-09-02"
- resource: https://docs.docker.com/docker-hub/usage/
  accessed: "2026-09-02"
- resource: https://docs.docker.com/docker-hub/usage/pulls/
  accessed: "2026-09-02"
---

# Facts
| Limit | Value | Source |
|---|---|---|
| Repository size | "ideally less than 1 GB, and less than 5 GB is strongly recommended" | [large files](/sources/github-docs-about-large-files.md) |
| File size | warning over 50 MiB; "GitHub blocks files larger than 100 MiB"; browser upload 25 MiB | same |
| Release assets | "Up to 1000 release assets may be associated with a single release. Each file included in a release must be under 2 GiB. There is no limit on the total size of a release, nor bandwidth usage." | [releases](/sources/github-docs-about-releases.md) |
| Git LFS | Free/Pro include 10 GiB storage and 10 GiB/month bandwidth; data packs "have been removed and replaced with metered billing"; downloads count against the repository owner | [LFS billing](/sources/github-docs-git-lfs-billing.md) |
| Actions job time | "Each job in a workflow can run for up to 6 hours of execution time." | [Actions limits](/sources/github-docs-actions-limits.md) |
| Actions other | 35-day workflow limit, 256-job matrix, 10 GB cache per repository, Free plan 20 concurrent jobs, GITHUB_TOKEN 1,000 API requests/hour/repo | same |
| Public-repo runner | Linux 4 vCPU, 16 GB RAM, 14 GB SSD (`ubuntu-latest`, `ubuntu-24.04`, `ubuntu-22.04`); `ubuntu-latest` = Ubuntu 24.04 | [runners](/sources/github-docs-github-hosted-runners-reference.md), [runner-images](/sources/github-actions-runner-images-readme.md) |
| Private-repo runner | 2 vCPU, 8 GB RAM, 14 GB SSD | same |
| ghcr.io | "10 GB size limit for each layer"; "10 minute timeout limit for uploads"; no overall image limit stated; "GitHub Packages usage is free for public packages" | [container registry](/sources/github-docs-container-registry.md), [packages billing](/sources/github-docs-packages-billing.md) |
| Docker Hub pulls | unauthenticated "100 per IPv4 address or IPv6 /64 subnet" per 6 hours; Personal 200 per 6 hours; Pro/Team/Business unlimited; multi-arch pulls count per architecture; CI platforms share IPs and "may cause abuse rate limiting"; error text "You have reached your pull rate limit." | [hub usage](/sources/docker-docs-hub-usage.md), [hub pulls](/sources/docker-docs-hub-pulls.md) |

# Inferred
* **Inferred:** the 14 GB runner disk is shared with the OS image's preinstalled toolchains; usable free space is materially less than 14 GB, so the CI build must stay a few GB total (base image + builder layers + baked datadir + exported image). Measure with `df -h /` as the first workflow step.
* **Inferred:** a public ghcr.io image is the right distribution channel (free, no pull limits documented), and a release asset (< 2 GiB each) is the right channel for extended-tier bundles; Git LFS is wrong for both (owner pays bandwidth).
* **Inferred:** Docker Hub anonymous pulls from shared CI egress are unreliable; log in with a `DOCKERHUB_TOKEN` secret before `docker pull mysql:9.7.2`, or mirror the base image to `ghcr.io/<org>/mysql-base:9.7.2` once and build from that.

# Limits
1. No converted data or upstream archive over 50 MiB is committed; upstream artifacts are fetched at build time from their canonical URL with sha256 pinning, or from a release asset / [archive.org mirror](/tools/internet-archive-mirroring.md).
2. The core image (baked datadir) must fit one ghcr layer < 10 GB and upload within 10 minutes; split datasets across layers (one `COPY --from` per dataset directory) so no single layer approaches the limit.
3. CI builds only the core tier; extended datasets that need more than ~6 hours or ~10 GB scratch are built locally and published as release assets.
4. Docker Hub rate limits are the first suspect after IPv6 when a CI pull fails ([runbook](/runbooks/ipv6-and-privileges.md)).

# Open questions
* Actual free disk on `ubuntu-24.04` runners after checkout (measure in the first CI run, record as a Verification entry).
