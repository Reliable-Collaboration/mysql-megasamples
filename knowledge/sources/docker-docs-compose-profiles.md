---
type: Source
title: "Docker Docs: Using profiles with Compose"
description: "profiles attribute, services without profiles always enabled, --profile / COMPOSE_PROFILES, depends_on caveat."
resource: https://docs.docker.com/compose/how-tos/profiles/
tags: [docker, compose, profiles]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://docs.docker.com/compose/how-tos/profiles/
    title: "Docker Docs: Using profiles with Compose"
    accessed: "2026-09-02"
---

# What was read
https://docs.docker.com/compose/how-tos/profiles/, accessed 2026-09-02.

# Relevant excerpt
> "Profiles help you adjust your Compose application for different environments or use cases by selectively activating services."
* `profiles: [debug]` on a service; "Services without a profiles attribute are always enabled."; enable with `docker compose --profile debug up` or `COMPOSE_PROFILES=debug docker compose up`; multiple profiles `--profile frontend --profile debug` or `COMPOSE_PROFILES=frontend,debug`.
* Explicitly targeting a profiled service starts it and its `depends_on` dependencies, but profiled dependencies must be "in the same profile, started separately, or not assigned to any profile".

# What it was used to decide
[docker multi-stage record](/tools/docker-build-multistage.md) and [tier model](/decisions/tier-model.md): extended datasets are opt-in Compose profiles (`--profile extended`, `--profile tpc`) that run the loader sidecars against the core container.
