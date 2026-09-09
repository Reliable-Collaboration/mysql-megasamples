---
type: Decision
title: "Dispositions of the release-2 code review (Claude code-review, 2026-09-10)"
description: The fifteen confirmed defects the review of the release-2 branch reported (six that break a fresh build or a documented command, five wrong behaviours in what ships, four in reproducibility and checks), each verified against the code and fixed; the four latent translator defects it listed beyond its cap; and the one it named that was not verified.
resource: /decisions/review-2026-09-10-dispositions.md
tags:
- decision
- review
- process
- engines
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-10T02:10:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-10T02:10:00Z"
sources:
- resource: /decisions/review-2026-09-02-dispositions.md
  title: the first review's dispositions, and the rule that every finding is treated as a class
  accessed: "2026-09-10"
- resource: /decisions/programmable-object-parity.md
  title: the work the review covered, with the engine-hub port toolkit
  accessed: "2026-09-10"
---

# Question
The `/code-review` of the `release-2` branch (`main...HEAD`, run 2026-09-09/10, eight of ten finder
angles as agents and two by hand after a rate limit, 37 candidates, 27 confirmed, 8 plausible, 2
refuted, capped at 15 reported) named fifteen defects. Which are real, what class does each belong
to, and what was done?

# Options considered
1. Fix each reported line — rejected: several findings are one instance of a class (everything
   keyed by dataset name breaks for `append: true` datasets in five places; two engines' hub check
   shared the same wrong test), and fixing one line would leave the class.
2. **Verify each finding against the code, fix it as a class, add a test where a unit test can hold
   it, and re-run the gates** (chosen).

# Evidence
Each finding was re-checked before it was touched (the file read at HEAD; the failing path
reproduced in memory where a server was not needed: `fetch tpch` returned 2, `registry.render` of
`dvdstore` with `dvdstore_reviews` emitted two rows named `dvdstore`, `REASSIGN OWNED BY postgres`
is refused for the bootstrap superuser). Dispositions, in the review's severity order:

| # | finding | class | disposition |
|---|---|---|---|
| 1 | `datasets/oracle_oe/oeparse.py` imported `plsql` from the deleted `scripts/`; `make oracle_oe` and `make run` failed at staging | a helper the package move did not reach | imports `megasamples.sources.plsql`; `stage oracle_oe` runs |
| 2 | `build` took fetch's "no matching artifacts" (exit 2) as fatal, so generated and derived datasets could not be built through `make <dataset>` or `make run` | fetch conflated "nothing to fetch" with "bad name" | naming datasets that own no artifact is "nothing to fetch", exit 0; `--id` misses still exit 2 |
| 3 | images, dumps and registry rows keyed by dataset name; an `append: true` pair (the `extended` selector) gave duplicate primary keys on all three engines and a `FileExistsError` in the SQLite image | the database, not the dataset, is the unit everything built is keyed by | dumps, ports, adapters, images, release staging and registry rows are keyed by database (`megasamples.engines.unique_databases`); an append dataset's artifacts, licences and counts fold into its base's row (`tests/test_registry.py`) |
| 4 | a generated column's expression was copied to the target unchecked; a function the target lacks aborted the port after invalid DDL was committed | a not-ported path missing for one object kind | `ddl.UnportableColumn` stops the port before anything is written, naming column and function (`tests/test_port.py`); `ifnull`/`coalesce` allowed |
| 5 | the PostgreSQL and SQLite engines tested "the database exists" to decide whether the hub holds a dataset, so an append dataset's MySQL load was skipped and the port carried only the base tables | the same wrong test in two engines | `MySQL.holds(dataset)` tests the dataset's own tables; a dump lacking any model table is taken again (`dump.complete`) |
| 6 | `from compression import zstd` is Python 3.14 only while pyproject allows 3.11 | interpreter floor undeclared | fallback to `backports.zstd`, declared for `python_version < '3.14'`, with a clear error |
| 7 | every baked PostgreSQL object was owned by `postgres`; `admin` ("full access" in every console) could not ALTER, DROP or index a sample table; `ALTER DEFAULT PRIVILEGES` ran for the wrong role | ownership, not grants, is what "full access" needs | each database is created `OWNER admin` and loaded as admin in the image builder; grants reduced to demo's SELECT and a `FOR ROLE admin` default; the image test alters a baked table as admin |
| 8 | CloudBeaver's three stack-wide settings were emitted by the MySQL engine only; a PostgreSQL- or SQLite-only stack showed guests no connections | a console's setting attached to one engine | the settings live on the console definition (`consoles.py`), merged for every stack |
| 9 | `make up` started Compose before `consoles/landing` existed; Docker created it root-owned and the landing page could not be written | the bind-mount source not created first (the stage directory already was) | created before `compose up` |
| 10 | `export SF` with no default sent `--sf ""` to the generators; `build.scale_factor` was read by nothing | a Make variable exported unconditionally | SF exported only when set; staging falls back to `build.scale_factor` |
| 11 | a port that died mid-load left an incomplete SQLite file or PostgreSQL directory that the image build and release staging accepted on existence | outputs written in place | SQLite built as `<db>.sqlite.building` and moved into place when complete; PostgreSQL writes a `complete` marker last and the image builder requires it |
| 12 | `PROVENANCE.md` read the rename map from git-ignored build output, so `make check` was not reproducible on a fresh clone | a path the staging change did not follow | reads the committed `datasets/<name>/name_map.yaml`; eight files regenerated |
| 13 | `ports-check` expected both engines' records, so a dataset's first single-engine port failed `make check` | the gate stricter than the record it checks | only the engines a dataset has been ported to are compared |
| 14 | `test-console` compared the registry with the landing page when no landing page was configured | an optional console assumed present | the page checks apply only when the landing page is in the stack |
| 15 | connection hints hard-coded `sakila`; the SQLite hint would create an empty file | a default that ignored the configuration | the hint names the first configured database (`engines.first_database`) |

Beyond the cap, the review named four latent translator defects: the trigger port's own statement
splitter took `IF(a, b, c)` for a block (it now shares the routine port's scanner); only the first
`WITH ROLLUP` in a statement was rewritten (all are); the dump reader dropped an empty line, which
is a one-column row holding the empty string (kept; `tests/test_port.py`); and a BIT-column digest
defect it did not describe, which was **not verified** and stands as an open question. Two of its
candidates it refuted itself.

# Outcome
Option 2. After the fixes: 48 unit tests pass; `make check` (bundle, generated files, port records
reproducible for 21 datasets) passes; `sakila` re-ported and verified on both engines through the
new paths; the PostgreSQL image rebuilt with admin as owner and its tests, the stack and the
console tests re-run (see the log for the date). The two refuted candidates and the nineteen
cleanup candidates the reviewer listed as cut (a triplicated image-test harness, string dispatch of
adapters, a module-global for trigger defaults, a dead `build.threads`) are not addressed here.

# Status
accepted
