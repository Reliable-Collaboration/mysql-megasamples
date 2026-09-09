---
type: Decision
title: Target PostgreSQL version is 18, pinned to the official image's 18.6 bookworm variant
description: The PostgreSQL engine is built from postgres:18.6-bookworm, the newest stable major the official image publishes; 19 is a beta.
resource: /decisions/target-postgres-version.md
tags:
- decision
- postgresql
- version
status: stable
trust: verified
stale_after: "2026-12-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:16:50Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:16:50Z"
sources:
- resource: /sources/docker-library-postgres-versions-json.md
  accessed: "2026-09-09"
- resource: /tools/postgres-docker-official-image.md
  accessed: "2026-09-09"
---

# Question
Which PostgreSQL major, and which image, does the PostgreSQL engine build from?

# Options considered
1. **18.x, the newest stable major, pinned to `postgres:18.6-bookworm`** (chosen).
2. 17.x — rejected: a year older with no feature this project needs, and its data-directory layout differs from 18's, so the engine would change again on the next bump.
3. 19 — rejected: beta3 on 2026-09-09; not a release.
4. The alpine variant — rejected: the bookworm variant matches the MySQL image's Debian-family base and `glibc` locale behaviour, which matters for collation.

# Evidence
* [versions.json](/sources/docker-library-postgres-versions-json.md): 18 → 18.6; 19 → 19beta3.
* [Image record](/tools/postgres-docker-official-image.md): layout, entrypoint behaviour, digest of the pulled image.

# Outcome
`engines/postgres/Dockerfile` starts `FROM postgres:18.6-bookworm` (digest
`sha256:1c59e2c3c818eaa0f0628f695b36e7c9e362d6b219b36a54a32df645cbd7e1af`); the cluster is built
in a builder stage at the image's own `PGDATA` and copied into the final stage. Image tag
`sql-megasamples-postgres:dev`.

# Status
accepted
