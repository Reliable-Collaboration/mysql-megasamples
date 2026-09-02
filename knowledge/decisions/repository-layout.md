---
type: Decision
title: Repository layout, committed versus downloaded content, and the download manifest
description: One directory per dataset with code, DDL, tests, license and provenance committed; all upstream artifacts and generated dumps live in git-ignored folders and are fetched through a single YAML manifest.
resource: /decisions/repository-layout.md
tags: [decision, repository, gitignore, manifest]
status: stable
trust: inferred
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:17:31Z" }
sources:
  - resource: /tools/github-limits.md
    title: GitHub size limits (tools agent)
    accessed: 2026-09-02
---

# Question
What is committed, what is downloaded, and how does the build find downloads without editing build logic?

# Options considered
1. **Commit only code + DDL + tests + small (< 5 MB) source scripts; everything else downloaded via `manifest.yaml`; no Git LFS** (chosen).
2. Git LFS for medium artifacts — rejected: free LFS bandwidth quotas make a public repo's clones fail unpredictably; GitHub Releases assets (2 GB/file) cover the same need without quota. Evidence: [GitHub limits](/tools/github-limits.md).
3. Commit converted `data.sql` for small datasets — accepted only where the upstream artifact itself is a small SQL/CSV file that we redistribute unchanged (Sakila, Chinook, Northwind, Pubs, HR, Jaffle Shop, small CSVs); converted output is never committed, it is rebuilt.

# Outcome
```
.
├── PLAN.md
├── README.md                     # per-dataset license table, attribution notices
├── LICENSES.md                   # generated from knowledge/licenses/*.md
├── Makefile                      # make <dataset>, make core, make image, make test
├── docker/
│   ├── Dockerfile                # multi-stage: builder(s) → final mysql:9.7.2
│   ├── loader.Dockerfile         # extended-tier loader (mysqlsh, duckdb, python, curl)
│   ├── compose.yaml              # services: mysql, loader(profile extended), mssql/oracle (profile build)
│   └── my.cnf                    # utf8mb4, local_infile, innodb settings
├── manifest.yaml                 # every downloadable artifact: url, mirrors, sha256, size, license
├── scripts/                      # shared: fetch.py, load.py, verify.py, checksum.py, okf_check.py
├── datasets/<name>/
│   ├── LICENSE                   # verbatim upstream license (generated from knowledge/licenses)
│   ├── PROVENANCE.md             # generated from knowledge/datasets/<name>.md
│   ├── schema.sql                # MySQL DDL, no secondary indexes / FKs
│   ├── indexes.sql               # secondary indexes, FULLTEXT, SPATIAL
│   ├── constraints.sql           # foreign keys and checks, applied last
│   ├── convert/                  # conversion code (python, sql, shell); or fetch.sh for generators
│   ├── data.sql | data/          # ONLY when the upstream artifact is itself small and redistributable
│   ├── tests/                    # expected_counts.yaml, samples.yaml, checksums.yaml, smoke.sql, explain.yaml
│   └── build/                    # git-ignored output: *.sql.zst, mysqlsh dump dirs, baseline.json
├── downloads/                    # git-ignored, sha256-verified upstream artifacts
├── knowledge/                    # OKF bundle
└── .github/workflows/            # ci.yaml (core), extended.yaml (manual), okf.yaml
```
* `.gitignore`: `downloads/`, `datasets/*/build/`, `*.bak`, `*.7z`, `*.parquet`, `*.zst`, `.venv/`, `work/`.
* `manifest.yaml` entry schema:
```yaml
- id: nyc_taxi/yellow_2025-01
  dataset: nyc_taxi
  url: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet
  mirrors: [https://github.com/<org>/mysql-megasamples/releases/download/data-v1/yellow_tripdata_2025-01.parquet, https://archive.org/download/<item>/yellow_tripdata_2025-01.parquet]
  sha256: "<filled at first verified fetch; build fails if absent and MEGASAMPLES_TRUST_FIRST_FETCH!=1>"
  size_bytes: 0
  license: nyc-open-data-terms
  requires_login: false
  ipv4_only: true         # curl -4 first; hosts with AAAA that hang
```
* `scripts/fetch.py` reads the manifest, tries `url` then `mirrors` in order, uses `curl --fail --location --retry 5 --retry-all-errors -4` (falls back to default stack only if `-4` fails to resolve), verifies sha256, writes `downloads/<id>.ok`, and skips files with a valid `.ok` marker.
* Projected fresh clone size: code + DDL + committed small artifacts, target **< 150 MB**; the largest committed items are the Employees dump files only if they are under 50 MB each (see the dataset record), otherwise they are release assets too.

# Status
accepted; sizes to be confirmed during execution
