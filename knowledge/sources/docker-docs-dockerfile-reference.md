---
type: Source
title: "Docker Docs: Dockerfile reference"
description: "RUN --mount=type=cache/bind/secret options, RUN --network, RUN --security, COPY --from/--link, heredocs, and the VOLUME rule: legacy builder discards changes, BuildKit keeps them."
resource: https://docs.docker.com/reference/dockerfile/
tags:
- docker
- build
- buildkit
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
sources:
- resource: https://docs.docker.com/reference/dockerfile/
  title: "Docker Docs: Dockerfile reference"
  accessed: "2026-09-02"
---

# What was read
https://docs.docker.com/reference/dockerfile/, accessed 2026-09-02.

# Relevant excerpt
* `RUN --mount=type=cache`: options id, target, ro/readonly, sharing (shared|private|locked, default shared), from, source, mode 0755, uid/gid 0; contents persist between builder invocations but may be cleared and must not be relied on for correctness.
* `RUN --mount=type=bind`: target, source, from, rw/readwrite — "Written data will be discarded after the RUN instruction completes and will not be committed to the image layer."; read-only by default.
* `RUN --network=default|none|host` ("Run in the host's network environment"); `RUN --security=sandbox|insecure` (insecure "equivalent to running docker run --privileged").
* `COPY --from` copies from stages, contexts or images; `COPY --link` copies into an empty destination as an independent layer.
* VOLUME: "If any build steps change the data within the volume after it has been declared, those changes will be discarded when using the legacy builder. When using Buildkit, the changes will instead be kept."
* Heredoc form `RUN <<EOF ... EOF` is supported.

# What it was used to decide
[docker multi-stage record](/tools/docker-build-multistage.md): the base image declares `VOLUME /var/lib/mysql`, so baking data there is only safe under BuildKit (default in Docker Desktop/buildx); cache mounts hold downloaded upstream archives across rebuilds.
