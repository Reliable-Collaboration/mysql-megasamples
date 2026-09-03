---
type: Source
title: "Docker Docs: Docker Hub usage and limits"
description: "Pull limits: unauthenticated 100 per 6 hours per IPv4 address or IPv6 /64, Personal 200 per 6 hours, Pro/Team/Business unlimited; 429 on abuse limit."
resource: https://docs.docker.com/docker-hub/usage/
tags:
- docker
- docker-hub
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
- resource: https://docs.docker.com/docker-hub/usage/
  title: "Docker Docs: Docker Hub usage and limits"
  accessed: "2026-09-02"
---

# What was read
https://docs.docker.com/docker-hub/usage/, accessed 2026-09-02.

# Relevant excerpt
* Table: Unauthenticated users "100 per IPv4 address or IPv6 /64 subnet" per 6 hours; Personal (authenticated) "200" per 6 hours; Pro/Team/Business "Unlimited".
* "The abuse limit returns a simple 429 Too Many Requests response".

# What it was used to decide
[GitHub limits](/tools/github-limits.md) and [IPv6 runbook](/runbooks/ipv6-and-privileges.md): CI logs in to Docker Hub (or mirrors the base image to ghcr.io) before pulling `mysql:9.7.2`.
