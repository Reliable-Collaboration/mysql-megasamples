---
type: Source
title: "Docker Docs: docker network inspect"
description: Synopsis and --format option for inspecting a network's configuration.
resource: https://docs.docker.com/reference/cli/docker/network/inspect/
tags:
- docker
- cli
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
sources:
- resource: https://docs.docker.com/reference/cli/docker/network/inspect/
  title: "Docker Docs: docker network inspect"
  accessed: "2026-09-02"
---

# What was read
https://docs.docker.com/reference/cli/docker/network/inspect/, accessed 2026-09-02.

# Relevant excerpt
* `docker network inspect [OPTIONS] NETWORK [NETWORK...]`; `--format`: "'json': Print in JSON format 'TEMPLATE': Print output using the given Go template." The page's fetched text showed no EnableIPv6 example.

# What it was used to decide
[IPv6 runbook](/runbooks/ipv6-and-privileges.md): `docker network inspect bridge --format '{{.EnableIPv6}}'` is the diagnostic (field name **Inferred** from the JSON structure, verify by running it).
