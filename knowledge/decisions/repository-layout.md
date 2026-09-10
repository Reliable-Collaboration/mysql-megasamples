---
type: Decision
title: Repository layout, committed versus downloaded content, and the download manifest
description: One Python package for the pipeline, one directory per engine and per console, one directory per dataset with its contract, converter, tests, licence and provenance; upstream artifacts and every build output live in git-ignored folders, fetched through a single YAML manifest.
resource: /decisions/repository-layout.md
tags:
- decision
- repository
- gitignore
- manifest
status: stable
trust: inferred
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:09:52Z"
sources:
- resource: /tools/github-limits.md
  title: GitHub size limits (tools agent)
  accessed: "2026-09-02"
---

# Question
What is committed, what is downloaded, and how does the build find downloads without editing build logic?

# Options considered
1. **Commit only code + DDL + tests + small (< 5 MB) source scripts; everything else downloaded via `manifest.yaml`; no Git LFS** (chosen).
2. Git LFS for medium artifacts — rejected: free LFS bandwidth quotas make a public repo's clones fail unpredictably; GitHub Releases assets (2 GB/file) cover the same need without quota. Evidence: [GitHub limits](/tools/github-limits.md).
3. Commit converted `data.sql` for small datasets — accepted only where the upstream artifact itself is a small SQL/CSV file that we redistribute unchanged (Sakila, Chinook, Northwind, Pubs, HR, Jaffle Shop, small CSVs); converted output is never committed, it is rebuilt.

# Evidence
* [GitHub limits](/tools/github-limits.md): 100 MiB file cap, 2 GiB release assets, LFS metered billing.
* Per-dataset source sizes in the dataset records (committed artifacts are all under 7 MB per file).

# Outcome
The tree, which ARCHITECTURE.md section 2 carries and this record mirrors:
```
.
├── README.md  ARCHITECTURE.md  PLAN.md  CATALOGUE.md  LICENSES.md  NOTICE.md  LICENSE   # CATALOGUE, LICENSES, NOTICE generated
├── Makefile                    one-line shims over `python3 -m megasamples <command>`
├── manifest.yaml               every downloadable artifact: url, mirrors, sha256, size, licence, flags
├── megasamples.example.yaml    the stack configuration, documented; `make configure` writes megasamples.yaml
├── pyproject.toml  uv.lock     the pinned Python stack
├── megasamples/                the package: pipeline, engines/<engine>/, sources/ (upstream translators), port/
├── engines/<engine>/           Dockerfile, server configuration, init SQL
├── consoles/<console>/         console configuration; consoles/landing/index.html is generated
├── datasets/<name>/            dataset.yaml  convert.py  tests/  LICENSE  PROVENANCE.md  [name_map.yaml]
├── knowledge/                  the OKF bundle
├── release/<set>/              SHA256SUMS and MANIFEST.md committed; the staged files are not
├── downloads/                  git-ignored: verified artifacts, <id>.ok markers, <id>.meta.json
└── build/                      git-ignored: stage/<name>/ (converted SQL), <engine>/ (dumps, image context)
```
* `.gitignore` (the committed file is authoritative): `downloads/`, `build/`, `*.bak`, `*.7z`,
  `*.parquet`, `*.zst`, `*.tsv`, `.venv/`, `work/`, `__pycache__/`, `.env`, `megasamples.yaml`,
  `compose.yaml`, `consoles/landing/index.html`, and everything under `release/*/` except the two
  record files.
* `manifest.yaml` entry schema:
```yaml
- id: nyc_taxi/yellow_2025-01
  dataset: nyc_taxi
  url: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet
  mirrors: []
  sha256: ""            # empty until the first verified fetch; refused unless MEGASAMPLES_TRUST_FIRST_FETCH=1, which writes it back
  size_bytes: 59158238
  license: nyc-open-data-terms
  ipv4_first: false     # curl -4 first, for hosts with AAAA records that hang
```
* `megasamples fetch` reads the manifest, tries `url` then `mirrors` with
  `curl --fail --location --retry 5 --retry-all-errors --connect-timeout 20 -C -` (with `-4` when
  `ipv4_first`, and again over IPv4 when a transfer stalls), verifies sha256, writes
  `downloads/<id>.ok` and `<id>.meta.json`, and never fetches a file whose marker matches.
* Committed size: code, contracts, tests and the bundle; every artifact larger than a small upstream
  script is a download.

# Status
accepted
