---
type: Source
title: "Docker Docs: Docker Hub pull usage and limits"
description: "What counts as a pull, multi-arch counting, shared-IP attribution on CI platforms, the rate-limit error text."
resource: https://docs.docker.com/docker-hub/usage/pulls/
tags: [docker, docker-hub, limits]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://docs.docker.com/docker-hub/usage/pulls/
    title: "Docker Docs: Docker Hub pull usage and limits"
    accessed: 2026-09-02
---

# What was read
https://docs.docker.com/docker-hub/usage/pulls/, accessed 2026-09-02.

# Relevant excerpt
* "Version checks do not count towards usage pricing." "A pull for a multi-arch image will count as one pull for each different architecture."
* CI warning: "the platform may use the same IPv4 address or IPv6 /64 subnet to pull images for multiple users. Even if you are authenticated, pulls attributed to a single IPv4 address or IPv6 /64 subnet may cause abuse rate limiting."
* Error text: "You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limits"

# What it was used to decide
[GitHub limits](/tools/github-limits.md): the Actions workflow authenticates to Docker Hub with a repository secret and the runbook recognises the exact error string.
