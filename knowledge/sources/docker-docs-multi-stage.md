---
type: Source
title: "Docker Docs: Multi-stage builds"
description: Multiple FROM stages, COPY --from, --target, external images as stages, BuildKit builds only needed stages.
resource: https://docs.docker.com/build/building/multi-stage/
tags:
- docker
- build
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
sources:
- resource: https://docs.docker.com/build/building/multi-stage/
  title: "Docker Docs: Multi-stage builds"
  accessed: "2026-09-02"
---

# What was read
https://docs.docker.com/build/building/multi-stage/, accessed 2026-09-02.

# Relevant excerpt
> "With multi-stage builds, you use multiple FROM statements in your Dockerfile. Each FROM instruction can use a different base, and each of them begins a new stage of the build."
> "The end result is a tiny production image with nothing but the binary inside. None of the build tools required to build the application are included in the resulting image."
* `FROM <image> AS <name>` + `COPY --from=<name>`; `--target` stops at a stage; `COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf` copies from an external image; "BuildKit only builds the stages that the target stage depends on".

# What it was used to decide
[docker multi-stage record](/tools/docker-build-multistage.md): converters and the temporary mysqld run in builder stages; only the finished data directory is copied into the final `mysql:9.7.2`-based stage.
