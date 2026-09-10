---
type: Decision
title: Build orchestration with make, Compose profiles and BuildKit
description: A Python package (`python3 -m megasamples <command>`) drives every step, `make` targets are one-line shims over it, one configuration file names what to build, and verification runs on the build machine in Docker with no CI service.
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
  at: "2026-09-09T18:09:52Z"
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
* The package `megasamples/` is the pipeline; every `make` target is a one-line shim over
  `python3 -m megasamples <command>`, so `make -n` shows what runs and the same code runs without make.
* Conversion runs on the host, not inside a Dockerfile: `megasamples stage` runs the dataset's
  converter into `build/stage/<name>/`; native products (SQL Server for the WideWorldImporters
  export, Oracle for the cross-check) run as transient containers.
* `make <dataset>` is `megasamples build --engine mysql <dataset>`: fetch → stage → load into the
  throwaway MySQL build server → verify. `megasamples build` does the same for the datasets
  `megasamples.yaml` names for an engine; `megasamples run` builds and bakes every configured
  engine; `megasamples image` dumps each dataset with `util.dumpSchemas` into
  `build/mysql/dumps/<name>/` (content-addressed by `<name>.json`), hardlinks exactly the dumps being
  baked into `build/mysql/image/`, writes the registry SQL there, and builds
  `engines/mysql/Dockerfile` with the repository root as context filtered by `.dockerignore`.
  `--from-dumps` re-bakes from existing dumps without the build server.
* The build server is reused across a session and removed when the image is done unless
  `build.keep_build_server` is set; `megasamples clean` removes every container labelled
  `megasamples.transient=true`.
* **No CI service.** The pipeline downloads about 1.4 GB and bakes a 3.5 GB image, a poor use of
  hosted-runner minutes for a project whose content is data, and the build machine has Docker. The
  gates are `make` targets that run the same code (ARCHITECTURE.md section 7): `make check` in
  seconds, the quick subset end to end, `make image` with `make test-image`, and the full core build
  before a release. Two datasets could never run in hosted CI anyway: `lahman` is
  maintainer-supplied, and `chicago_crimes` comes from a live API whose pinned digest changes daily.

# Status
accepted
