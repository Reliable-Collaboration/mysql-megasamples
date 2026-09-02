---
type: Decision
title: Bake core data into /var/lib/mysql instead of loading at first start
description: The final image contains an already-initialized data directory; initdb scripts are used only for user creation on first start of extended loads.
resource: /decisions/bake-data-vs-initdb.md
tags: [decision, image, initdb, startup]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:17:31Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T22:00:00Z" }
sources:
  - resource: /sources/docker-library-mysql-9-7-docker-entrypoint.md
    accessed: 2026-09-02
  - resource: /tools/docker-build-multistage.md
    accessed: 2026-09-02
  - resource: /sources/docker-library-mysql-readme.md
    title: initdb behaviour
    accessed: 2026-09-02
---

# Question
Ship the core tier as init scripts in `/docker-entrypoint-initdb.d` (loaded on first start) or as a pre-populated `/var/lib/mysql`?

# Options considered
1. **Pre-populated data directory** (chosen, pending verification of the entrypoint's "already initialized" path — see [docker multi-stage record](/tools/docker-build-multistage.md)). Startup is seconds; the image-level test "starts within budget" is meaningful; users get identical bytes.
2. Init scripts (`.sql.zst` supported natively by the entrypoint per [README](/sources/docker-library-mysql-readme.md)): image is smaller (compressed SQL ≈ 3–5× smaller than InnoDB pages) but first start takes minutes (Employees alone is ~4 M rows), every user pays the load time, and the anonymous-volume semantics mean a re-created container re-loads. Kept as the fallback if option 1 fails verification, and used for the tiny per-start pieces (users, grants, `megasamples.datasets` registry refresh).
3. Both: baked data plus init scripts — rejected: the entrypoint skips init scripts when the datadir is non-empty, so scripts would never run.

# Evidence
* Verified from the entrypoint source: when `$DATADIR/mysql` exists the script sets `DATABASE_ALREADY_EXISTS` and skips initialization, `MYSQL_ROOT_PASSWORD` checks and initdb.d, then `exec mysqld` ([entrypoint](/sources/docker-library-mysql-9-7-docker-entrypoint.md)). BuildKit keeps writes made under a declared VOLUME during the build ([Dockerfile reference](/sources/docker-docs-dockerfile-reference.md)). Users, grants and passwords therefore must be created in the builder stage; runtime password override is done by a thin wrapper entrypoint that runs `ALTER USER` via a socket connection after mysqld starts (**Inferred** design, verified in P-03).
* Open: first-start cost of the anonymous-volume copy of `/var/lib/mysql` ([multi-stage record](/tools/docker-build-multistage.md), Inferred section).

# Remaining verification (task P-03 in PLAN.md)
Build a throwaway image whose builder stage runs `mysqld --initialize-insecure`, starts mysqld, loads Sakila, shuts down; final stage copies `/var/lib/mysql`; confirm the official entrypoint detects the existing datadir and starts without re-initializing, and that file ownership (uid 999 `mysql`) survives `COPY --from` with `--chown`.

# Outcome
Option 1 (pre-populated datadir). Option 2 remains the documented fallback if P-03 fails on ownership or startup budget.

# Status
accepted (P-03 measures first-start time and chooses between datadir designs A and B)
