# mysql-megasamples

A MySQL 9.7 LTS Docker image preloaded with 21 well-known sample and public databases, each
converted from its authoritative upstream source by a scripted, rerunnable pipeline — and a set of
four web consoles that come up beside it, already connected, so you can start looking at data
instead of configuring clients.

|  |  |
|---|---|
| databases | 21, listed below |
| tables / rows | 248 tables, 9,056,697 rows |
| data size | ~660 MB loaded; the built image is ~3.5 GB |
| server | MySQL 9.7.2, `utf8mb4`, InnoDB |
| consoles | phpMyAdmin, Adminer, DbGate, CloudBeaver, plus a generated index page |
| accounts | `demo` (read-only) and `admin` (full privileges) |

Every dataset keeps its own upstream licence — this project never places a single licence over the
data. [`CATALOGUE.md`](CATALOGUE.md) lists all 38 datasets with what each licence asks of you, and
[Licensing](#licensing) is worth reading before you publish anything built from this.

**Status: not published yet.** There is no image to `docker pull`; you build it locally, which is
what the rest of this page is about. [`PLAN.md`](PLAN.md) is the plan being executed and
[`knowledge/`](knowledge/index.md) is the evidence bundle behind every claim in it.

## The 21 databases

Each one is converted from its authoritative upstream source; the description is the one its own
research record carries, so it says what the thing actually is rather than what a blurb writer
guessed. Full detail — every tier, licence and obligation — is in [`CATALOGUE.md`](CATALOGUE.md).

<!-- databases:start -->
| database | what it is | tables | rows |
|---|---|---:|---:|
| `adventureworks` | Microsoft's flagship 68-table, 5-schema OLTP sample (bicycle manufacturer) | 69 | 759,240 |
| `adventureworks_lt` | The lightweight 12-table AdventureWorks (SalesLT schema) | 12 | 4,277 |
| `chicago_crimes` | The City of Chicago's 8.6 M-row reported-crime extract plus the 434-row IUCR code lookup | 2 | 259,702 |
| `chinook` | Luis Rocha's digital media store sample (v1.4.5, 2024-02-12) | 11 | 15,607 |
| `contoso` | SQLBI's synthetic Contoso retail star schema V2 | 8 | 753,467 |
| `dvdstore` | Dell/VMware's open-source OLTP benchmark schema (DVD e-commerce with reviews and memberships) | 9 | 174,716 |
| `employees` | The MySQL "Employees Sample Database" - 300,024 fabricated employees with 2.8 M salary rows | 6 | 3,919,015 |
| `enron` | About 517k real corporate emails from 150 Enron custodians, distributed by CMU as a maildir-style tree of RFC 822 files | 3 | 48,778 |
| `jaffle_shop` | dbt Labs' fictional jaffle (toasted sandwich) shop | 3 | 312 |
| `lahman` | Sean Lahman's historical MLB statistics 1871-2025, now published by SABR as 27 CSV tables (plus Access and SQL Server forms) under CC BY-SA 3.0 | 27 | 706,466 |
| `northwind` | Microsoft's classic 13-table trading-company sample (SQL Server 2000 era) shipped as a single 1 MB T-SQL script with all data inline | 13 | 3,308 |
| `nyc_taxi` | New York City yellow and green taxi trip records in Parquet, plus the 265-row taxi zone lookup | 2 | 48,591 |
| `oracle_co` | Oracle's "modern" e-commerce sample (7 tables, 8,783 rows) with identity columns, a JSON check constraint on a BLOB | 7 | 8,783 |
| `oracle_hr` | The 7-table, 216-row teaching schema from Oracle's db-sample-schemas v23.3, converted from its plain INSERT scripts | 7 | 216 |
| `oracle_oe` | The object-relational Order Entry schema | 9 | 11,518 |
| `oracle_sh` | Oracle's star-schema data-warehouse sample | 9 | 1,063,396 |
| `pubs` | Microsoft's tiny 11-table publishers/authors sample (SQL Server 2000 era) shipped as a 126 KB T-SQL script with inline data | 11 | 255 |
| `sakila` | Oracle's DVD-rental sample database for MySQL (Version 1.5), 16 tables / 7 views / 3 procedures / 3 functions / 6 triggers, 46,268 rows | 16 | 47,268 |
| `smallsets` | Three classic teaching datasets in one database — the Titanic passenger list, Fisher's Iris measurements and the Palmer Penguins | 4 | 2,147 |
| `stackexchange_beer` | CC BY-SA XML dump of a Stack Exchange Q&A site (Posts, Users, Comments, Votes, Badges, Tags, PostLinks, PostHistory) converted to MySQL with FULLTEXT | 11 | 62,523 |
| `wikipedia_simple` | Current-revision article text plus MediaWiki link tables of the Simple English Wikipedia | 9 | 1,167,112 |
<!-- databases:end -->

Beyond these, the extended, generated and user-fetched datasets are in
[Beyond the 21](#beyond-the-21).

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

Project **code** is **Apache-2.0** — [`LICENSE`](LICENSE) — and that covers the scripts, converters,
tests, Dockerfiles, knowledge bundle and generated documentation. It covers **none of the data**, and
is not a relicensing of anything upstream: the share-alike datasets stay CC BY-SA and are offered as
such. Where the two could appear to conflict, the dataset's licence governs the dataset and
Apache-2.0 governs the code that processed it. The console index page shows each database's licence
beside it, so the answer to "what am I allowed to do with this table" is one click from the data.

### Share-alike: four datasets must stay under their own licence

`employees`, `lahman`, the Stack Exchange datasets and `wikipedia_simple` are CC BY-SA. A converted
database is an adaptation, so **this project offers those four converted databases under the same
licence** — CC BY-SA 3.0 for `employees` and `lahman`, CC BY-SA 4.0 for Stack Exchange and
`wikipedia_simple` — and so must anyone who redistributes a modified version. The project's own MIT
licence covers the code, and carves these datasets out. [`CATALOGUE.md`](CATALOGUE.md) marks every
dataset with what its licence asks of a redistributor.

### Notices that must travel with the data

Chicago's terms require this paragraph **verbatim** wherever the data appears, and reserve the City's
right to require distribution to stop:

> This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago. The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site. The data provided at this site is subject to change at any time. It is understood that the data provided at this site is being used at one's own risk.

Two more are required by the terms they were obtained under:

> Data obtained from http://hbiostat.org/data courtesy of the Vanderbilt University Department of Biostatistics.

> Iris data set: Fisher, R. A. (1936), The use of multiple measurements in taxonomic problems, Annals of Eugenics 7(2):179–188. Distributed via the UCI Machine Learning Repository, https://doi.org/10.24432/C56C76, under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Two values corrected per Fisher's paper, as in R and scikit-learn (BSD-3-Clause).

[`NOTICE.md`](NOTICE.md) carries these and every other attribution in full.

### Licensing notes: what is still unresolved

Five licensing questions are genuinely open. None of them blocks using the data; each is recorded
with what was actually read, so you can form your own view rather than inherit an assumption:

| question | status |
|---|---|
| **NYC TLC terms.** The Open Data FAQ says there are no restrictions; the NYC.gov Terms of Use it incorporates reserve all rights | unresolved on the City's own pages; treated as reusable with attribution ([record](knowledge/questions/nyc-open-data-reuse-terms.md)) |
| **Titanic.** hbiostat grants blanket permission with an acknowledgement request, but names no licence | permission relied on, acknowledgement shipped ([record](knowledge/questions/titanic-hbiostat-license-status.md)) |
| **Enron.** No licence text exists; FERC public-record material redistributed by CMU with a privacy request | status inferred, not stated by anyone; CMU's deletion list is applied ([record](knowledge/licenses/enron-public-record.md)) |
| **DVD Store data.** The kit is GPL-2.0-or-later, but the CSVs are generator *output*, which GPL §0 covers only if it is a work based on the Program | treated as redistributable program output ([record](knowledge/questions/dvdstore-generated-data-license.md)) |
| **Jaffle Shop.** The newer dbt-labs/jaffle-shop seeds and the 6-year S3 set carry no licence at all | **not vendored**; only the Apache-2.0 classic seeds are used ([record](knowledge/questions/jaffle-shop-new-repo-license.md)) |

Iris was a sixth: UCI labels it CC BY 4.0 rather than public domain, which is the stricter reading,
so that is the one the project follows ([record](knowledge/questions/iris-uci-cc-by-vs-public-domain.md)).

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
| `CATALOGUE.md` | every dataset: tier, shape, licence, and what that licence asks of a redistributor (generated) |
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
