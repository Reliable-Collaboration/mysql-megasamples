---
type: Source
title: "Docker Docs: Docker daemon configuration overview"
description: "daemon.json lives at /etc/docker/daemon.json on Linux; flags and file must not duplicate a setting."
resource: https://docs.docker.com/engine/daemon/
tags: [docker, daemon]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://docs.docker.com/engine/daemon/
    title: "Docker Docs: Docker daemon configuration overview"
    accessed: 2026-09-02
---

# What was read
https://docs.docker.com/engine/daemon/, accessed 2026-09-02.

# Relevant excerpt
* The daemon configuration file is `/etc/docker/daemon.json` on Linux; settings can also be passed as daemon flags; the same setting in both places prevents the daemon from starting.

# What it was used to decide
[IPv6 runbook](/runbooks/ipv6-and-privileges.md): on this WSL2/Docker Desktop machine the effective file is the Docker Desktop one ([environment survey](/sources/build-machine-environment-2026-09-02.md)), not /etc/docker/daemon.json.
