# mysql-megasamples

A MySQL 9.7 LTS Docker image preloaded with 21 well-known sample and public databases, each
converted from its authoritative upstream source by a scripted, rerunnable pipeline — and a set of
four web consoles that come up beside it, already connected, so you can start looking at data
instead of configuring clients.

|  |  |
|---|---|
| databases | 21 (`sakila`, `northwind`, `chinook`, `pubs`, `employees`, `adventureworks`, `contoso`, `lahman`, `enron`, `nyc_taxi`, `chicago_crimes`, `wikipedia_simple`, the four Oracle schemas, and more) |
| tables / rows | 248 tables, 9,056,697 rows |
| data size | ~660 MB loaded; the built image is ~3.5 GB |
| server | MySQL 9.7.2, `utf8mb4`, InnoDB |
| consoles | phpMyAdmin, Adminer, DbGate, CloudBeaver, plus a generated index page |
| accounts | `demo` (read-only) and `admin` (full privileges) |

Every dataset keeps its own upstream licence — this project never places a single licence over the
data. See [Licensing](#licensing), which is worth reading before you publish anything built from it.

**Status: not published yet.** There is no image to `docker pull`; you build it locally, which is
what the rest of this page is about. [`PLAN.md`](PLAN.md) is the plan being executed and
[`knowledge/`](knowledge/index.md) is the evidence bundle behind every claim in it.

## What you need

* **Docker** (Desktop or Engine) with ~10 GB free: 1.4 GB of downloads, 145 MB of dumps, a build
  server holding a copy of the data, and the ~3.5 GB image.
* **Python 3.11+**, and [`uv`](https://docs.astral.sh/uv/).
* Time. A full build fetches 155 artifacts and loads 9 million rows; it is not a five-minute job.

```sh
uv sync          # .venv with PyYAML, PyMySQL, duckdb, lxml, sqlglot, py7zr
```

Every command below is a `make` target, and every target is a thin shim over a script in
`scripts/` — so nothing here is magic, and `make -n <target>` shows you exactly what will run.

## Build it

```sh
make image
```

That fetches every core dataset (verifying each download against a recorded SHA-256), loads it into
a throwaway MySQL "build server", tests it, dumps it, and bakes the result into
`mysql-megasamples:dev`.

**When the build finishes it removes the build containers**, because at that point they hold nothing
you need — a second copy of every dataset in a container nobody will remember starting. To keep them
up, which is what you want while developing a converter:

```sh
make image KEEP_BUILD_RESOURCES=1     # keep the build server so the next load reuses it
```

You can remove them later at any time with `make clean`.

### A shorter build

`make image` builds all 21. To try the pipeline without the large downloads, build the fifteen-dataset
subset CI uses — 203 MB instead of 1.4 GB:

```sh
make image DATASETS="$(make print-core-fast)"
```

### One dataset you have to supply yourself

`lahman` (baseball, 27 tables) is published behind a SABR share link that a build cannot fetch. If
you run the full `make image` without it, the fetch stops and names both the exact URL to get it from
and the path to put it at (`downloads/lahman/lahman_1871-2025_csv.zip`); its checksum is then
verified like every other artifact. Leave `lahman` out of `DATASETS` if you would rather skip it:

```sh
make image DATASETS="$(make print-core | tr ' ' '\n' | grep -v '^lahman$' | tr '\n' ' ')"
```

## Run it, and open the console

```sh
make up
```

One stack, up together — the database and all four consoles:

| | address | notes |
|---|---|---|
| **console index** | **<http://127.0.0.1:8080/>** | **start here**: every database with its size, licence and provenance |
| phpMyAdmin | <http://127.0.0.1:8081/> | signed in already; the server menu switches account |
| Adminer | <http://127.0.0.1:8082/> | its login form remains — type either account |
| DbGate | <http://127.0.0.1:8083/> | both connections preconfigured in the sidebar |
| CloudBeaver | <http://127.0.0.1:8084/> | opens as a guest; both connections in the sidebar |
| MySQL itself | `127.0.0.1:3306` | for `mysql`, DBeaver, DataGrip, an application |

Every port binds to `127.0.0.1`, not `0.0.0.0`: an unauthenticated database UI should not appear on
the network because someone opened a laptop in a café. Publishing them more widely is a deliberate
edit to `compose.yaml`.

```sh
make down        # all of it down again
```

`make up` is `docker compose up -d` with the index page regenerated from the running database first,
so it always matches what is actually loaded; `make down` is `docker compose down`. If you want only
the database: `docker compose up -d mysql`.

### The two accounts

| account | password | privileges |
|---|---|---|
| `demo` | `demo` | `SELECT`, `SHOW VIEW`. Cannot write anything, anywhere |
| `admin` | `admin` | `ALL PRIVILEGES WITH GRANT OPTION` |

Each console opens on `demo`, because the safe account should be the one you get without choosing.
Both are offered everywhere, so switching to `admin` is a menu, not a config edit.

These are boilerplate credentials for a disposable local database and they are committed on purpose,
so `make up` needs no setup. To change them, copy `.env.example` to `.env` and edit it — the same
value reaches the server (applied with `ALTER USER` at startup) and every console, so the two cannot
drift apart. `.env` is gitignored.

```sh
mysql -h 127.0.0.1 -P 3306 -u demo -pdemo sakila
```

## Housekeeping

Two kinds of container exist here, and they are not the same kind of thing:

```sh
make status      # the stack, and any transient container, listed separately
make clean       # remove the transient ones; the stack keeps running
make clean-all   # remove the transient ones and take the stack down
```

The **stack** is the six services in `compose.yaml`. Everything else — the build server, the SQL
Server behind `make wwi-export`, the loader image, the servers the tests start — is **transient**,
carries the label `megasamples.transient=true`, and is what `make clean` removes. Nothing removes
the build server on a timer, because doing so discards every dataset loaded into it and reloading
takes hours; `make image` removes it when the build is done, and `make clean` is how you end a
session you kept it for.

## Licensing

**Every dataset keeps its own upstream licence.** This repository does not place a single licence
over the data, and several of the licences have obligations that travel with the data — attribution,
and in a few cases share-alike. Before you redistribute anything built from this, read:

* [`LICENSES.md`](LICENSES.md) — every licence in play, and which datasets it covers
* [`NOTICE.md`](NOTICE.md) — the attribution notices that must travel with the data
* `datasets/<name>/LICENSE` and `datasets/<name>/PROVENANCE.md` — per dataset, generated from
  [`knowledge/licenses/`](knowledge/licenses/index.md), never hand-written

Project **code** is MIT. The console index page shows each database's licence beside it, so the
answer to "what am I allowed to do with this table" is one click from the data.

### Two datasets are never redistributed

Citi Bike and Divvy licences forbid publishing their data as a stand-alone dataset. The loaders ship;
the data does not. They download to *your* machine, which is where the licence attaches, and refuse
to run until you accept it:

```sh
MEGASAMPLES_ACCEPT_BIKESHARE_LICENSE=1 make load-citibike
```

TPC-H, TPC-DS, SSB and TPC-C are **generated on your machine** for the same reason: nothing
TPC-authored is shipped or committed.

### One dataset needs proprietary software to *rebuild* — not to use

WideWorldImporters is published by Microsoft only as a SQL Server backup: its transactional rows are
generated by randomised T-SQL, so no script or CSV form of the released data exists. Re-deriving it
means running **SQL Server 2022 Developer Edition** in a container and accepting
[Microsoft's Developer EULA](https://go.microsoft.com/fwlink/?linkid=857698):

> BY USING THE SOFTWARE, YOU ACCEPT THESE TERMS. IF YOU DO NOT ACCEPT THEM, DO NOT USE THE SOFTWARE.
> … to design, develop, test and demonstrate your programs. You may not use the software on a device
> or server in a production environment.

**Using the image does not involve that licence.** No SQL Server code, tool or layer is in it; the
container is deleted when the export finishes — including if it fails — and the data it produced is
MIT, like AdventureWorks and Northwind. Building any other dataset does not involve it either.

You accept it only if you re-run the export yourself, and the target refuses to start until you do:

```sh
MEGASAMPLES_ACCEPT_MSSQL_EULA=1 make wwi-export   # prints the terms first
```

The acceptance is recorded with the image digest and engine build in
`downloads/wideworldimporters/export/server.json`.

## Beyond the 21

The image holds the *core* tier. Others are opt-in, because they are large, licence-gated, or
generated:

| tier | what | how |
|---|---|---|
| extended | AdventureWorks DW, BTS on-time, WideWorldImporters (+DW), and bigger versions of datasets already in the image (8.2 M Chicago crimes, 3.5 M yellow-cab trips, 10 M-row Contoso, full Enron, full Simple Wikipedia) | `make adventureworks_dw`, `make chicago-full`, `make nyc-taxi-yellow`, … |
| generated | TPC-H, TPC-DS, SSB, TPC-C at a scale factor you choose | `make gen-tpch SF=1`, `make gen-tpcds`, `make gen-ssb`, `make load-tpcc W=1` |
| user-fetched | Citi Bike, Divvy | `make load-citibike`, `make load-divvy` (licence gate above) |

`make help` lists every target.

## How the repository is laid out

| Path | What it holds |
|---|---|
| `PLAN.md` | the plan: architecture, per-dataset conversion paths, tests, licensing |
| `knowledge/` | OKF v0.2 evidence bundle: datasets, licences, tools, decisions, sources, runbooks, open questions |
| `scripts/` | the pipeline: fetch, stage, load, verify, dump, plus the converters |
| `datasets/<db>/` | per-dataset DDL, converter, tests, licence and provenance |
| `docker/` | Dockerfile, MySQL config, init SQL, console configuration |
| `compose.yaml` | the stack: database + four consoles |
| `manifest.yaml` | every downloadable artifact with checksum, size and licence |
| `downloads/` | gitignored, checksum-verified upstream artifacts |

Every factual claim in `PLAN.md` traces to a record in `knowledge/`, and
`python3 scripts/okf_check.py` enforces that the bundle stays internally consistent. If you want to
know *why* a dataset was converted the way it was, that is where the answer is.

## Development

```sh
make check                       # the local gate: bundle validation + generated files up to date
make test-image                  # assert the built image's row counts and checksums
make test-console                # assert the consoles are up and the two accounts behave
make build-server                # a MySQL to load into by hand
make build-server-stop           # remove it (this discards everything loaded into it)
```

If a `docker pull` or a download hangs with no error, suspect IPv6 first — see
[`knowledge/runbooks/ipv6-and-privileges.md`](knowledge/runbooks/ipv6-and-privileges.md), which also
covers the `scripts/pull_image.py` workaround this project uses to fetch images over IPv4.
