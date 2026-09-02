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
The authoritative tree is PLAN.md §2.1; this record mirrors it and is updated in the same commit whenever it changes.
```
.
├── PLAN.md  README.md  LICENSES.md  NOTICE.md   # LICENSES/NOTICE generated from knowledge/licenses
├── Makefile                                     # targets listed in PLAN.md §2.4
├── manifest.yaml                                # every downloadable artifact: url, mirrors, sha256, size, license, flags
├── uv.lock  pyproject.toml
├── docker/  Dockerfile  loader.Dockerfile  compose.yaml  my.cnf  init/00-users.sql  entrypoint-wrapper.sh
├── scripts/  fetch.py  canon.py  canon.sql  verify.py  load.py  dumps.py  registry.py  gen_provenance.py  okf_check.py  okf_fix_quotes.py  mirror.sh (maintainer upload wrapper)
├── datasets/<db_name>/
│   ├── dataset.yaml                             # db name, tier, tables and load order, manifest ids, routines security
│   ├── LICENSE  PROVENANCE.md  name_map.yaml    # generated
│   ├── schema.sql  indexes.sql  constraints.sql  routines.sql
│   ├── convert/                                 # converter or generator runner
│   ├── data/                                    # only small upstream artifacts that are themselves redistributable
│   ├── tests/                                   # expected_counts.yaml  samples.yaml  indexes.yaml  explain.yaml  smoke.sql  smoke.expected.yaml
│   └── build/                                   # git-ignored: tsv/, dump/, baseline.json, load.log
├── downloads/                                   # git-ignored, sha256-verified upstream artifacts (+ <id>.meta.json)
├── knowledge/                                   # OKF bundle
└── .github/workflows/  ci.yaml  native.yaml  extended.yaml  okf.yaml
```
* `.gitignore` (the committed file is authoritative): `downloads/`, `datasets/*/build/`, `docker/context/`, `*.bak`, `*.7z`, `*.parquet`, `*.zst`, `*.tsv`, `.venv/`, `work/`, `__pycache__/`.
* `manifest.yaml` entry schema:
```yaml
- id: nyc_taxi/yellow_2025-01
  dataset: nyc_taxi
  url: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet
  mirrors: [https://github.com/<org>/mysql-megasamples/releases/download/data-v1/yellow_tripdata_2025-01.parquet, https://archive.org/download/<item>/yellow_tripdata_2025-01.parquet]
  sha256: ""            # empty until the first verified fetch; the build refuses to proceed unless MEGASAMPLES_TRUST_FIRST_FETCH=1, then writes the value back
  size_bytes: 59158238
  license: nyc-open-data-terms
  requires_login: false
  ipv4_first: true      # curl -4 first; set for hosts with AAAA records that hang (cloudfront, wikimedia); default false
```
* `scripts/fetch.py` reads the manifest, tries `url` then `mirrors` in order with `curl --fail --location --retry 5 --retry-all-errors --connect-timeout 20 -C -` (adding `-4` when `ipv4_first`), verifies sha256, writes `downloads/<id>.ok` and `<id>.meta.json` (size, Last-Modified, source used), and skips files with a valid `.ok` marker.
* Projected fresh clone size: code + DDL + committed small artifacts, target **< 60 MB** (ceiling 150 MB); the Employees dumps (172 MB) and everything larger are downloads mirrored as release assets.

# Status
accepted; sizes to be confirmed during execution
