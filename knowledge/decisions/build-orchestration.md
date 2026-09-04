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

# Amendment (2026-09-03, maintainer decision)
**No CI service.** The plan assumed GitHub Actions workflows (`ci.yaml`, `okf.yaml`, `native.yaml`,
`extended.yaml`); the maintainer decided against them for this repository. The pipeline downloads
about 1.5 GB and bakes a 3.46 GB image, which is a poor use of hosted-runner minutes for a project
whose entire content is data, and the build machine already has Docker.

Nothing about the verification is lost — only the automation of when it runs. The workflows are
replaced by `make` targets that run exactly the same code: `make check` (bundle validation and the
generated licence files, seconds, no Docker), `make core-fast` (the 15-dataset subset end to end),
`make image-only` + `make test-image` (bake and S8), and `make core` before a release. PLAN.md §4.3
carries the table of gates.

Two datasets could never have run in a hosted CI anyway, which is worth stating because it is a
property of the data rather than of the choice: `lahman` is maintainer-supplied and has no fetchable
URL, and `chicago_crimes` is a live API whose pinned digest changes daily.

# Status
accepted
