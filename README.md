# sql-megasamples

Sample databases for **MySQL, PostgreSQL and SQLite**: 38 well-known sample and public datasets,
each converted from its authoritative upstream source by a scripted, rerunnable pipeline and
verified against pinned expectations, shipped as engine images and files — with a set of web
consoles that come up beside them, already connected, so you can start looking at data instead of
configuring clients. You choose the engines, the databases and the consoles; one file holds the
choice and one command builds it.

| engine | what ships | status |
|---|---|---|
| **MySQL 9.7 LTS** | `sql-megasamples-mysql`, an image with the databases baked into its data directory | built and tested |
| **PostgreSQL** | an image, ported from the verified MySQL corpus | in progress — [`PLAN.md`](PLAN.md) |
| **SQLite** | one file per database, plus an image carrying the `sqlite3` CLI | in progress — [`PLAN.md`](PLAN.md) |

Every dataset keeps its own upstream licence — this project never places a single licence over the
data. [`CATALOGUE.md`](CATALOGUE.md) lists all 38 datasets with what each licence asks of you, and
[Licensing](#licensing) is worth reading before you publish anything built from this.

**Status: not published yet.** There is no image to `docker pull`; you build it locally, which is
what the rest of this page is about. [`ARCHITECTURE.md`](ARCHITECTURE.md) describes how the pieces
fit, [`PLAN.md`](PLAN.md) what is being built next, and [`knowledge/`](knowledge/index.md) is the
evidence bundle behind every claim in both.

## Quick start

```sh
uv sync            # the Python stack (PyYAML, PyMySQL, duckdb, lxml, sqlglot, py7zr)
make configure     # choose engines x databases and consoles; writes megasamples.yaml
make run           # fetch (once), convert, load, verify, bake the images
make up            # start the stack, then open http://127.0.0.1:8080/
```

`make configure` is a full-screen chooser: the engines, then a matrix of every dataset against
every engine — with each dataset's tier, download size and whether that download is already
verified on this machine — then the consoles. It writes `megasamples.yaml`, which every other
command reads. You can also copy [`megasamples.example.yaml`](megasamples.example.yaml) and edit
it, or run with no file at all: the built-in default is MySQL with the 21 core databases and the
four consoles.

You need **Docker** (Desktop or Engine), **Python 3.11+** with [`uv`](https://docs.astral.sh/uv/),
and room: the core tier is 1.4 GB of downloads, a build server holding a copy of the data, and a
3.5 GB MySQL image. A full core build loads nine million rows and is not a five-minute job; the
15-dataset **quick** subset (196 MB of downloads) builds in minutes.

## The databases

Each one is converted from its authoritative upstream source; the description is the one its own
research record carries, so it says what the thing actually is rather than what a blurb writer
guessed. These 21 are the **core** tier, the ones an image holds by default; full detail — every
tier, licence and obligation — is in [`CATALOGUE.md`](CATALOGUE.md), and `make list` prints every
dataset with its tier, download size and shape.

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
[Beyond the core](#beyond-the-core).

## The engines

**MySQL is the hub.** Every dataset is converted into MySQL first, loaded into a throwaway build
server, verified there — row counts, a canonical content digest of every table, foreign-key
integrity, the index set, query plans, canonical query results — and dumped. The other engines are
ports of that verified corpus, checked against the same expectations, so a database in PostgreSQL
or SQLite is provably the same rows as in MySQL.

### MySQL

`sql-megasamples-mysql:dev` is `mysql:9.7.2` (`utf8mb4`, InnoDB) with the chosen databases already
in its data directory: first start answers a real query in about two seconds, and nothing is loaded
at startup. Two accounts are offered from every console, and both are usable from any client:

| account | password | privileges |
|---|---|---|
| `demo` | `demo` | `SELECT`, `SHOW VIEW`. Cannot write anything, anywhere |
| `admin` | `admin` | `ALL PRIVILEGES WITH GRANT OPTION` |

Each console opens on `demo`, because the safe account should be the one you get without choosing.
The passwords are boilerplate for a disposable local database and are committed on purpose; to
change them, copy `.env.example` to `.env` — the same value reaches the server (applied at startup)
and every console, so the two cannot drift apart.

```sh
mysql -h 127.0.0.1 -P 3306 -u demo -pdemo sakila
docker compose up -d mysql        # the database alone, no consoles
```

A `megasamples` database inside the image holds the provenance registry: one row per dataset with
its tier, knowledge record, licences, source artifacts and digests, and pinned row counts. The
catalogue, the landing page and the image tests all read it, so none can drift from what was baked.

### PostgreSQL and SQLite

Both are being added as ports of the MySQL corpus; [`PLAN.md`](PLAN.md) has the design, the
measured inventory of what the ports must translate, and the status. When they land, the same
`megasamples.yaml` names them and the same `make run` builds them.

## The consoles

`make up` brings the engines and the consoles up as one stack, and `make down` takes it away again.
Every port binds to `127.0.0.1`: an unauthenticated database UI should not appear on the network
because someone opened a laptop in a café. Publishing one more widely is a deliberate edit.

| | address | browses | notes |
|---|---|---|---|
| **console index** | **<http://127.0.0.1:8080/>** | — | **start here**: every database with its size, licence and provenance, generated from the running stack |
| phpMyAdmin | <http://127.0.0.1:8081/> | MySQL | signed in already; the server menu switches account |
| Adminer | <http://127.0.0.1:8082/> | MySQL, PostgreSQL, SQLite | its login form remains — type either account |
| DbGate | <http://127.0.0.1:8083/> | MySQL, PostgreSQL, SQLite | both connections preconfigured in the sidebar |
| CloudBeaver | <http://127.0.0.1:8084/> | MySQL, PostgreSQL, SQLite | opens as a guest; both connections in the sidebar |

A console starts only when an engine it can browse is in the stack, and is configured for every
engine present. `compose.yaml` is generated from `megasamples.yaml` by `make up` (or `make compose`)
so the stack is exactly what you chose; every service carries a memory limit and every image is
pinned by digest.

## The configuration file

```yaml
engines:
  mysql: {datasets: core}          # core | quick | all | a tier name | [sakila, chinook, ...]
consoles: [landing, phpmyadmin, adminer, dbgate, cloudbeaver]
ports: {mysql: 3306, landing: 8080, phpmyadmin: 8081, adminer: 8082, dbgate: 8083, cloudbeaver: 8084}
build: {threads: 4, keep_build_server: false, scale_factor: 1}
downloads: {concurrency: 3}
```

`make run` reads it and, for every engine named, fetches the datasets' artifacts, converts and
loads them, verifies them and bakes the image; `make up` starts what was built. Naming a dataset
for any engine also builds it in the MySQL build server, because that is where every port comes
from. [`megasamples.example.yaml`](megasamples.example.yaml) documents every key.

## Downloads: once, verified, watched

`make fetch` (which `make run` and `make <dataset>` call first) downloads each artifact in
`manifest.yaml`, verifies its SHA-256 against the recorded value, and writes a marker beside it.
**A verified file is never fetched again**, on this run or the next, so an interrupted build resumes
where it stopped. While transfers run, a monitor shows each one — bytes, rate, time left, then the
verification pass — and prints one permanent line per artifact; several run at once. A transfer
that makes no progress for two minutes is retried over IPv4, which on this project's build machines
is what a hang usually means, and the fallback is recorded with the file.

One core dataset has to be supplied by hand: `lahman` (baseball, 27 tables) is published behind a
SABR share link that no build can fetch. The fetch names the exact URL and the path to put it at
(`downloads/lahman/lahman_1871-2025_csv.zip`), and verifies its checksum like every other artifact.
Leave `lahman` out of your dataset list if you would rather skip it.

## Building piece by piece

Every command is a `make` target, and every target is a one-line shim over
`python3 -m megasamples <command>` — `make -n <target>` shows exactly what will run, and
`python3 -m megasamples --help` lists every command.

```sh
make sakila                        # fetch, convert, load and verify one dataset on MySQL
make build D="sakila chinook"      # the same for several
make image                         # bake the configured datasets into the MySQL image
make image FROM_DUMPS=1            # re-bake from the dumps already built, without the build server
make test-image                    # assert the image: counts, accounts, CHECK TABLE, overrides
make test-console                  # assert the consoles are up and the two accounts behave
make status                        # the stack, and any transient container
make clean                         # remove the transient containers; the stack keeps running
```

The build server is reused across a session, because reloading everything takes hours;
`make image` removes it when the image is done, and `KEEP_BUILD_RESOURCES=1` (or
`build.keep_build_server: true`) keeps it, which is what you want while developing a converter.

## Licensing

**Every dataset keeps its own upstream licence.** This repository does not place a single licence
over the data, and several of the licences have obligations that travel with the data — attribution,
and in a few cases share-alike. Before you redistribute anything built from this, read:

* [`LICENSES.md`](LICENSES.md) — every licence in play, and which datasets it covers
* [`NOTICE.md`](NOTICE.md) — the attribution notices that must travel with the data
* `datasets/<name>/LICENSE` and `datasets/<name>/PROVENANCE.md` — per dataset, generated from
  [`knowledge/licenses/`](knowledge/licenses/index.md), never hand-written

Project **code** is **Apache-2.0** — [`LICENSE`](LICENSE) — and that covers the package, converters,
tests, Dockerfiles, knowledge bundle and generated documentation. It covers **none of the data**, and
is not a relicensing of anything upstream: the share-alike datasets stay CC BY-SA and are offered as
such. Where the two could appear to conflict, the dataset's licence governs the dataset and
Apache-2.0 governs the code that processed it. The console index page shows each database's licence
beside it, so the answer to "what am I allowed to do with this table" is one click from the data.

### Share-alike: four datasets must stay under their own licence

`employees`, `lahman`, the Stack Exchange datasets and `wikipedia_simple` are CC BY-SA. A converted
database is an adaptation, so **this project offers those four converted databases under the same
licence** — CC BY-SA 3.0 for `employees` and `lahman`, CC BY-SA 4.0 for Stack Exchange and
`wikipedia_simple` — and so must anyone who redistributes a modified version, in any engine.
[`CATALOGUE.md`](CATALOGUE.md) marks every dataset with what its licence asks of a redistributor.

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

**Using the images does not involve that licence.** No SQL Server code, tool or layer is in any of
them; the container is deleted when the export finishes — including if it fails — and the data it
produced is MIT, like AdventureWorks and Northwind. Building any other dataset does not involve it
either. You accept it only if you re-run the export yourself, and the target refuses to start until
you do:

```sh
MEGASAMPLES_ACCEPT_MSSQL_EULA=1 make wwi-export   # prints the terms first
```

The acceptance is recorded with the image digest and engine build in
`downloads/wideworldimporters/export/server.json`.

## Beyond the core

The core tier is what an image holds by default. The others are opt-in, because they are large,
licence-gated, or generated — name them in `megasamples.yaml`, or build one directly:

| tier | what | how |
|---|---|---|
| extended | AdventureWorks DW, BTS on-time, WideWorldImporters (+DW), and bigger versions of core datasets (8.2 M Chicago crimes, 3.5 M yellow-cab trips, 1 M- and 10 M-row Contoso, full Enron, full Simple Wikipedia, dba.stackexchange.com, DVD Store reviews) | `make adventureworks_dw`, `make chicago_crimes_full`, `make nyc_taxi_yellow`, … |
| generated | TPC-H, TPC-DS, SSB, TPC-C at a scale factor you choose | `make tpch SF=1`, `make tpcds`, `make ssb`, `make load-tpcc W=1` |
| user-fetched | Citi Bike, Divvy | `make load-citibike`, `make load-divvy` (licence gate above) |

`make help` lists every target; `make list` every dataset.

## Built on this

[`dolt-megasamples`](https://github.com/Reliable-Collaboration/dolt-megasamples) loads these same
databases into [Dolt](https://github.com/dolthub/dolt) — a SQL database with Git-like versioning —
and measures what the same data costs in each engine, in disk, time and memory. It reads the MySQL
image as its input and does not modify it.

It is worth a look if you are choosing between the two, or if you want a worked example of what this
corpus is useful for: twenty-one databases of varied shape and size, all licensed for
redistribution, are a better basis for a storage comparison than any one dataset.

## How the repository is laid out

| Path | What it holds |
|---|---|
| `ARCHITECTURE.md` | how it works: layout, the dataset contract, the MySQL hub, engines, verification, the stack, gates, licensing and release |
| `PLAN.md` | what is being built next |
| `CATALOGUE.md` | every dataset: tier, shape, licence, and what that licence asks of a redistributor (generated) |
| `megasamples/` | the package: the pipeline, one subpackage per engine, the upstream-format translators |
| `engines/<engine>/` | each engine's Dockerfile, server configuration and init SQL |
| `consoles/<console>/` | each console's configuration; the generated index page |
| `datasets/<name>/` | per-dataset contract, converter, pinned expectations, licence and provenance |
| `knowledge/` | OKF v0.2 evidence bundle: datasets, licences, tools, decisions, sources, runbooks, open questions |
| `manifest.yaml` | every downloadable artifact with checksum, size and licence |
| `megasamples.example.yaml` | the stack configuration, documented |
| `downloads/`, `build/` | gitignored: verified upstream artifacts; everything a build produces |

Every factual claim in `ARCHITECTURE.md` and `PLAN.md` traces to a record in `knowledge/`, and
`make check` enforces that the bundle stays internally consistent. If you want to know *why* a
dataset was converted the way it was, that is where the answer is.

## Development

```sh
make check                       # the local gate: bundle validation + generated files up to date
uv run pytest -q                 # unit tests for the inventory, configuration and staging logic
make build D="$(make -s list-quick)"   # the quick subset end to end, before a push that touches the pipeline
```

If a `docker pull` or a download hangs with no error, suspect IPv6 first — see
[`knowledge/runbooks/ipv6-and-privileges.md`](knowledge/runbooks/ipv6-and-privileges.md), which also
covers the `make pull-image` workaround this project uses to fetch images over IPv4.
