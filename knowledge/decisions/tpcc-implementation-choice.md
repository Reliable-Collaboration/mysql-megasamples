---
type: Decision
title: TPC-C population uses sysbench-tpcc (Apache-2.0 scripts on the packaged GPL sysbench), with HammerDB TPROC-C as reference and fallback; tpcc-mysql rejected
description: Pick the open-source loader that creates and fills the tpcc database in the loader container.
resource: /decisions/tpcc-implementation-choice.md
tags: [decision, tpc-c, loader]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://github.com/Percona-Lab/sysbench-tpcc
    accessed: "2026-09-02"
  - resource: https://github.com/Percona-Lab/tpcc-mysql
    accessed: "2026-09-02"
  - resource: https://github.com/TPC-Council/HammerDB
    accessed: "2026-09-02"
  - resource: https://packages.debian.org/trixie/sysbench
    accessed: "2026-09-02"
---

# Question
Which of Percona-Lab/tpcc-mysql, Percona-Lab/sysbench-tpcc (+sysbench) and HammerDB should `make gen-tpcc W=n` run?

# Options considered
1. **sysbench-tpcc**: Apache-2.0 Lua (5 files) + distro package `sysbench` 1.0.20 (GPL-2.0, MySQL driver via libmariadb3, LuaJIT) — a 2-line addition to the loader image; scriptable; `--rand-seed`; disclaimer wording in its README; tables get a numeric suffix that we rename away. **Chosen.**
2. HammerDB v6.0 TPROC-C: TPC-Council-hosted, GPL-3.0, official multi-arch image with the MySQL client, CLI (`dbset/diset/buildschema`); canonical "derived from TPC-C" naming; but a separate large image, Tcl, unseeded RNG, MySQL-specific DDL we cannot copy without GPL. **Reference for naming/DDL comparison and fallback loader.**
3. tpcc-mysql: no license → cannot be redistributed or safely vendored; archived 2017; /dev/urandom seed; ubuntu:16.04 Dockerfile. **Rejected** (its `create_table.sql`/`add_fkey_idx.sql` are still the community reference for the MySQL index/FK set, which sysbench-tpcc reproduces).
4. Own seeded Python populator writing `.tbl` files from spec Clause 4.3.3/A.6: fully deterministic and license-clean, ~150 lines, no external dependency; **deferred** — adopted only if option 1 cannot be made reproducible ([question](/questions/tpcc-loader-determinism.md)).

# Evidence
[TPC-C implementations record](/tools/tpcc-implementations.md); [sysbench-tpcc source](/sources/github-percona-lab-sysbench-tpcc.md); [sysbench/Debian](/sources/github-akopytov-sysbench.md); [HammerDB source](/sources/github-tpc-council-hammerdb.md) and [docs](/sources/hammerdb-docs-ch03s02-tproc-c.md); [tpcc-mysql source](/sources/github-percona-lab-tpcc-mysql.md); [TPC-C spec](/sources/tpc-c-specification-v5-11.md).

# Outcome
`apt-get install sysbench` + `git clone --depth 1 … sysbench-tpcc` (pinned commit f110afa) in `docker/loader.Dockerfile`; `make gen-tpcc W=10 THREADS=4 SEED=42` runs `prepare` with `--tables=1 --use_fk=0`, renames the nine tables, applies our `indexes.sql`/`constraints.sql`, computes the baseline from MySQL. Naming and README disclaimer follow HammerDB's "derived from TPC-C" formula. The first execution task: connect with MySQL 9.7 (`caching_sha2_password`), load W=1 twice with the same seed and `--threads=1`, and diff digests.

# Status
accepted (pending [tpcc-loader-determinism](/questions/tpcc-loader-determinism.md))
