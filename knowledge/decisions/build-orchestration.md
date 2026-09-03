---
type: Decision
title: Build orchestration with make, Compose profiles and BuildKit
description: A Makefile drives per-dataset builds; Compose profiles start temporary native database products only for the datasets that need them; the final image is a multi-stage Dockerfile.
resource: /decisions/build-orchestration.md
tags:
- decision
- build
- make
- compose
status: stable
trust: inferred
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:17:31Z"
sources:
- resource: /sources/build-machine-environment-2026-09-02.md
  title: Build machine survey
  accessed: "2026-09-02"
---

# Question
How can one dataset be rebuilt without rebuilding all, while the final image remains a single reproducible artifact?

# Options considered
1. **Makefile with one target per dataset producing `datasets/<name>/build/dump/` (MySQL Shell dump format), then a final `make image` that stages all core dumps into the Dockerfile build context** (chosen). `make` is missing on the host ([survey](/sources/build-machine-environment-2026-09-02.md)); the plan asks the user to install it (`sudo apt-get install make jq zstd bzip2 p7zip-full`) rather than replacing make.
2. A Python task runner (invoke/doit) — rejected: adds a dependency for something make does natively; every contributor has make.
3. Everything inside one Dockerfile — rejected: a single dataset change would invalidate all layers, and native-product containers (SQL Server, Oracle) cannot run inside a `RUN` step without Docker-in-Docker.

# Evidence
* [Build machine survey](/sources/build-machine-environment-2026-09-02.md): 32 CPUs, Docker Desktop, `make` absent.
* [Docker multi-stage record](/tools/docker-build-multistage.md): a `RUN` step cannot run sibling containers, so native products run as Compose services.
* [MySQL Shell utilities](/tools/mysql-shell-utilities.md): `util.dumpSchemas`/`loadDump` provide the per-dataset artifact format.

# Outcome
* Conversion runs on the host via Compose services: `mssql` (profile `build-mssql`), `oracle` (profile `build-oracle`), `work` (the loader image with python/duckdb/mysqlsh; profile `build`), and a scratch `mysql-build` server used to load, index, test and dump each dataset.
* Each dataset target: fetch → convert → load into `mysql-build` → index → constraints → tests → `util.dumpSchemas` into `build/dump/` → write `build/baseline.json`.
* `make image`: copies core `build/dump/` directories into `docker/context/`, builds the multi-stage image where a builder stage starts mysqld, runs `util.loadDump` for each core dataset, creates users, shuts down, and the final stage `COPY --from=builder /var/lib/mysql /var/lib/mysql` (see [bake vs initdb](/decisions/bake-data-vs-initdb.md)).
* `make extended` loads every extended dataset that has a release asset into a running server; generators (`make gen-*`) and the license-gated `load-citibike`/`load-divvy` are separate because they cannot run unattended or produce redistributable assets.
* Caching: BuildKit cache mounts for package installs; dataset dumps are content-addressed (`sha256` of the dump dir recorded in `baseline.json`), so unchanged datasets do not change the image layer input.

# Status
accepted
