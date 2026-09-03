# mysql-megasamples

A MySQL 9.7 LTS Docker image preloaded with well-known sample and public
databases, each converted from its authoritative upstream source by a scripted,
rerunnable pipeline.

**Status: in execution.** [`PLAN.md`](PLAN.md) is the executable plan;
[`knowledge/`](knowledge/index.md) is the Open Knowledge Format v0.2 evidence
bundle behind every claim in it. Nothing is published yet.

## Layout

| Path | What it holds |
|---|---|
| `PLAN.md` | the plan: architecture, per-dataset conversion paths, tests, licensing |
| `knowledge/` | OKF v0.2 bundle: datasets, licenses, tools, decisions, sources, runbooks, open questions |
| `scripts/` | shared tooling (fetch, convert helpers, verify, bundle checker) |
| `datasets/<db>/` | per-dataset DDL, converter, tests, license and provenance |
| `docker/` | Dockerfile, compose, config, init SQL |
| `manifest.yaml` | every downloadable artifact with checksum, size and license |
| `downloads/` | git-ignored, checksum-verified upstream artifacts |

## Licensing

Every dataset keeps its own upstream license; this repository does not place a
single license over the data. Per-dataset terms, the required attribution text
and the share-alike obligations are recorded in
[`knowledge/licenses/`](knowledge/licenses/index.md) and are generated into each
dataset's `LICENSE` and `PROVENANCE.md`. Project code is MIT.

Two datasets are deliberately **not** redistributed: Citi Bike and Divvy, whose
licenses forbid publishing the data as a stand-alone dataset. The repository
ships their loaders so a user can fetch them directly.

## Development

```sh
uv sync                                     # Python tooling
python3 scripts/okf_check.py --bundle knowledge   # validate the knowledge bundle
python3 scripts/okf_fix_quotes.py --check         # frontmatter canonical form
```
