---
type: Source
title: "Docker Docs: docker buildx build reference"
description: "--network, --build-arg, --secret, --target, --cache-from/--cache-to, --output type=local, --allow network.host entitlement."
resource: https://docs.docker.com/reference/cli/docker/buildx/build/
tags:
- docker
- build
- buildx
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
sources:
- resource: https://docs.docker.com/reference/cli/docker/buildx/build/
  title: "Docker Docs: docker buildx build reference"
  accessed: "2026-09-02"
---

# What was read
https://docs.docker.com/reference/cli/docker/buildx/build/, accessed 2026-09-02.

# Relevant excerpt
* `--network`: "default (default): Run in the default network. none: Run with no network access. host: Run in the host's network environment."
* `--build-arg`: "These values don't persist in the intermediate or final images like ENV values do." Proxy build args are predefined.
* `--secret`: "Exposes secrets (authentication credentials, tokens) to the build. A secret can be mounted into the build using a RUN --mount=type=secret mount".
* `--output type=local`: "writes all result files to a directory on the client"; `--cache-from`/`--cache-to` support registry, local, GitHub Actions, S3, Azure backends.
* `--allow`: `network.host` and `security.insecure` entitlements; "network=host requires the --allow network.host entitlement."

# What it was used to decide
[docker multi-stage record](/tools/docker-build-multistage.md): `--output type=local` exports the baked datadir or converted TSVs for inspection; `--network=host` needs `--allow network.host` and is only a last resort for DNS/IPv6 trouble ([runbook](/runbooks/ipv6-and-privileges.md)).
