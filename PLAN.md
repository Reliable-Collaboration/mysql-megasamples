# Plan

What is being built next. `ARCHITECTURE.md` describes what exists; this file stops describing
something once it does.

## 1. Where things stand

The three engines are built: every core dataset is verified on MySQL, and ported and verified on
PostgreSQL and SQLite by one deterministic program whose output is committed and reproducibility-
checked (`ARCHITECTURE.md` sections 3 and 4). One configuration names any combination of engines,
datasets and consoles, and `make run` then `make up` builds and starts it.

## 2. Next: the Dolt comparison

`dolt-megasamples` reads the MySQL image and compares Dolt with MySQL on disk, time and memory. It
now has the inputs to add Dolt's siblings:

* **DoltgreSQL** (PostgreSQL wire protocol): loaded from the PostgreSQL port through `pg_dump` and
  `psql`, one Dolt database per sample database, the same disk, time and memory measurements as Dolt.
* **DoltLite** (a SQLite fork that reads stock SQLite files): opened directly on the files
  `make release SET=sqlite` stages, then committed, so the measurement is what the file costs once
  it is history rather than what a load costs.

Both go into `dolt-megasamples`, not here. Before either starts, its plan there answers: which
versions to pin, what a "commit per row" means for a file-based engine, and how memory is bounded
per container, as the earlier experiment had to learn.

## 3. Open in this repository

* **Views on the ports.** Sixty-nine MySQL views are not ported. sqlglot (already a dependency) is
  the candidate for translating them statement by statement, verified by executing each view on the
  target and comparing its row count and digest with MySQL's; `megasamples/sources/tsqlbody.py`
  records why it is not used for procedural bodies. Routines and triggers stay MySQL-only.
* **Extended-tier ports.** The ports cover what is loaded in the MySQL build server, so an extended
  dataset ports once it is built there; the `append: true` datasets (reviews, yellow trips, the
  full Chicago set) add tables to a core database and the port has to run after the append.
* **A PostgreSQL browser.** pgAdmin or pgweb is evaluated and recorded before being added to the
  console registry; Adminer, DbGate and CloudBeaver already browse PostgreSQL.
* **Publishing.** Nothing is published yet: the images, the `data-v1` assets and the `sqlite` set
  are staged and checked by `make prepub-check`; publishing them is the maintainer's step.
