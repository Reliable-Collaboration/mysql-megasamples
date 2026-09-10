---
type: Runbook
title: "The clean-room build: prove the README's quick start from a fresh clone with nothing pre-built"
description: How the project is tested as a first-time user would meet it -- its images, containers, volumes and build servers removed, a fresh clone, uv sync, the example configuration with all three engines, make run, make up and the tests -- what was measured on 2026-09-09/10 (1.4 GB fetched in 8 minutes, all 21 core datasets on three engines in 39 minutes, every test green), which two artifacts a first-time user cannot fetch until the data-v1 release is published, and the defects the first attempts surfaced.
resource: /runbooks/clean-room-build.md
tags:
- runbook
- verification
- release
- build
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-10T00:30:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-10T00:30:00Z"
sources:
- resource: /decisions/review-2026-09-10-dispositions.md
  title: the review whose fixes this run then exercised from a fresh clone
  accessed: "2026-09-10"
- resource: /decisions/engine-hub.md
  title: MySQL as the hub; the ports built from it
  accessed: "2026-09-10"
---

# The clean-room build

The README's quick start (`uv sync`, a configuration, `make run`, `make up`) is proved from a fresh
clone on a machine with nothing of the project's left on it. It is the one test that finds what a
developer's machine hides: files left over from an earlier layout, an image that still exists, a
lock file that was never regenerated, an upstream download that has changed since it was pinned.

## Procedure

1. **Remove what the project made**, and only that. In the working copy: `make down`, `make clean`
   (the transient containers, the build servers included), `docker compose -f compose.yaml down -v`
   (the `megasamples-sqlite` volume), then `docker rmi sql-megasamples-mysql:dev
   sql-megasamples-postgres:dev sql-megasamples-sqlite:dev`. Remove the pinned upstream images too
   where nothing else on the machine holds them (`postgres:18.6-bookworm` went; `mysql:9.7.2` and
   the console images stayed, since another project's containers reference them -- Docker refuses
   without `--force`, which is the right answer). The working copy's own `build/` and `downloads/`
   are not the test's concern and stay.
2. **Clone fresh**: `gh repo clone Reliable-Collaboration/sql-megasamples <dir> -- -b release-2`;
   confirm `build/`, `downloads/`, `.venv`, `megasamples.yaml` and `compose.yaml` are absent.
3. **Follow the README**: `uv sync`; the example configuration copied to `megasamples.yaml` with
   all three engines on `core` (the interactive `make configure` cannot be driven from a script);
   `make run` under `nohup` with its output kept; then `make up`, `make test-console`,
   `make test-image ENGINE=` for each engine, `make check`.
4. **Two artifacts need the maintainer** until the `data-v1` release assets are published
   (`release/data-v1/MANIFEST.md`): `lahman/lahman_1871-2025_csv.zip` (a Box share, no static URL)
   and `chicago_crimes/crimes_2024.csv` (the portal's 2024 extract has changed since it was
   pinned: 74,885,948 bytes on 2026-09-09 against 74,811,578 pinned). The fetch reports both and
   the build goes on without them. For the test they were placed under `downloads/` from the
   maintainer's verified copies, whose digests the fetcher checked against the manifest -- the
   same bytes the release asset will deliver, so the run is what a user gets once it is published.

## Measured, 2026-09-09/10, on the build machine (WSL2, 20 GB RAM)

| step | result |
|---|---|
| fetch, first attempt | 155 artifacts, 1.4 GB listed; 153 fetched (1.3 GB) in 8 min 7 s, 2 failed as above |
| `make run` (head bf7aaf2) | 39 min 13 s: MySQL 21 datasets converted, loaded, verified, dumped and baked in about 12 min; then the PostgreSQL and SQLite phases, each of which rebuilt every dataset on MySQL first (the defect below), ported, verified and baked |
| verification | 0 failures on every dataset on every engine, three times over |
| images | `sql-megasamples-mysql:dev` 3.46 GB, `-postgres:dev` 4.05 GB, `-sqlite:dev` 1.26 GB |
| `make up`, `make test-console` | the stack up, the landing page with 21 databases on each engine, 0 failures |
| `make test-image` ×3, `make check` | 0 failures each |

## What the first attempts surfaced, each fixed before the run above passed

* `make run` stopped after the downloads because one artifact failed; a dataset whose download is
  not in place is now left out of every engine's build and image and named at the end, and the
  fetcher tries each `mirrors` entry when the upstream bytes are not the pinned ones, with the
  five data-v1 release assets as mirrors.
* `make check` failed on a fresh clone: the catalogue read its numbers from a running image; it
  now reads the pinned counts from the repository, with identical numbers.
* `uv sync` rewrote `uv.lock`, which had not been regenerated for a dependency marker; the lock is
  committed regenerated.
* Baking the MySQL image removed the build server, so the PostgreSQL phase converted, loaded and
  verified all 21 datasets on MySQL again before porting them, and the SQLite phase a third time
  (the 39 minutes above include that). `run` now keeps the build servers up across engines, and a
  port whose dataset is no longer in the hub restores it from its complete dump in about a
  minute instead of building it again.
* On the run that followed, the PostgreSQL phase's first statement found no server: both build
  servers' readiness checks asked over the Unix socket, which the official images' first-start
  initialisation answers from a temporary server (PostgreSQL's with `listen_addresses=''`, MySQL's
  with `--skip-networking`) that is stopped 109 ms later, before the real one starts. Both checks
  now ask over TCP, which only the real server listens on; three fresh starts followed by an
  immediate statement passed.

# Status
accepted
