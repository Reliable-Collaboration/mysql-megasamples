---
type: Decision
title: Two distribution tiers, core and extended, and the opt-in mechanism
description: Core datasets are baked into the image; extended datasets are fetched or generated on demand through Compose profiles and make targets.
resource: /decisions/tier-model.md
tags:
- decision
- tiers
- distribution
status: stable
trust: inferred
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:17:31Z"
sources:
- resource: /sources/docker-library-mysql-readme.md
  title: initdb behaviour
  accessed: "2026-09-02"
---

# Question
How are the two tiers delivered and how does a user opt in to the extended tier?

# Options considered
1. **Core baked into the image; extended delivered as (a) compressed MySQL Shell dump release assets loaded by an `extended-loader` sidecar or `make load-<dataset>`, and (b) generators run on demand** (chosen).
2. Two images (`:core` and `:extended`) — rejected: the extended tier is tens of GB and several datasets (TPC-*, Stack Exchange) cannot be redistributed pre-generated or are click-through downloads, so a self-contained extended image is impossible anyway.
3. Download-at-first-start inside the entrypoint — rejected outright: slow, non-deterministic first start, it breaks the "container starts within budget" test, and the conversion tooling lives in the loader image, not in the MySQL image (the wrapper hands off to the official entrypoint with `exec`, see [bake decision](/decisions/bake-data-vs-initdb.md)).

# Evidence
* [Official image README](/sources/docker-library-mysql-readme.md): initdb runs only on an empty datadir.
* [Compose profiles](/sources/docker-docs-compose-profiles.md): opt-in services.
* Size figures per dataset in [tier assignments](/decisions/tier-assignments.md).

# Outcome
* Tier thresholds: **core** = loaded InnoDB size ≤ 50 MB per dataset, plus a small set of "medium" core datasets (Employees, Sakila-sized and up to roughly 200 MB each) such that the core image stays under 2 GB compressed; **extended** = anything larger, anything generated, anything requiring click-through or login upstream.
* Extended opt-in: `docker compose --profile extended up` starts the same MySQL image plus a `loader` service (built from `engines/mysql/loader.Dockerfile`, containing mysqlsh, duckdb, python) that reads `manifest.yaml`, downloads verified assets into `./downloads/`, and loads them with `util.loadDump`. `make load-<dataset>` does the same for a running container. Generators: `make gen-tpch SF=1` etc.
* Every dataset record states its tier with the size evidence; the summary table lives in PLAN.md §7.

# Status
accepted (thresholds are inferred targets; revisit after the first core build measures real sizes — that measurement is task E-01 in PLAN.md §11)
