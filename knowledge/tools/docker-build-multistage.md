---
type: Tool
title: Docker multi-stage build, BuildKit mounts, and the pre-populated data directory path
description: How the final image is assembled from a builder stage that runs mysqld, what the official entrypoint does with an existing datadir, and the VOLUME/anonymous-volume cost to measure.
resource: https://docs.docker.com/build/building/multi-stage/
tags: [docker, buildkit, image, entrypoint]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T21:00:18Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T21:00:18Z" }
sources:
  - resource: /sources/docker-docs-multi-stage.md
    accessed: "2026-09-02"
  - resource: /sources/docker-docs-dockerfile-reference.md
    accessed: "2026-09-02"
  - resource: /sources/docker-docs-volumes.md
    accessed: "2026-09-02"
  - resource: /sources/docker-library-mysql-9-7-docker-entrypoint.md
    accessed: "2026-09-02"
  - resource: /sources/docker-library-mysql-9-7-dockerfile-oracle.md
    accessed: "2026-09-02"
  - resource: /sources/docker-docs-compose-profiles.md
    accessed: "2026-09-02"
  - resource: /sources/docker-docs-buildx-build.md
    accessed: "2026-09-02"
---

# Facts
* Multi-stage: "Each FROM instruction can use a different base"; `COPY --from=<stage>`; "BuildKit only builds the stages that the target stage depends on" ([multi-stage](/sources/docker-docs-multi-stage.md)).
* `RUN --mount=type=cache` persists between builds but "may be cleared and must not be relied on for correctness"; `RUN --mount=type=bind` is read-only by default and writes are discarded; heredoc `RUN <<EOF` supported; `RUN --network=host` available ([Dockerfile reference](/sources/docker-docs-dockerfile-reference.md)).
* The official image declares `VOLUME /var/lib/mysql`, runs as uid/gid 999 `mysql` via gosu, base `oraclelinux:9-slim` with `microdnf` only, and bundles `mysqlsh` ([Dockerfile](/sources/docker-library-mysql-9-7-dockerfile-oracle.md)).
* VOLUME in build steps: "When using Buildkit, the changes will instead be kept" — so a builder stage derived from `mysql:9.7.2` may write into `/var/lib/mysql` and the result survives into the layer ([Dockerfile reference](/sources/docker-docs-dockerfile-reference.md)).
* Entrypoint with an existing datadir: `DATABASE_ALREADY_EXISTS` is set when `$DATADIR/mysql` exists; then no initialization, no `MYSQL_ROOT_PASSWORD` requirement, no initdb.d processing, just `exec mysqld` ([entrypoint](/sources/docker-library-mysql-9-7-docker-entrypoint.md)).
* Runtime volume semantics: when a container starts with a VOLUME path that has content in the image, "Docker copies the directory's contents into the volume" (anonymous volume, persists unless `--rm`) ([volumes](/sources/docker-docs-volumes.md)).
* Compose profiles select optional services (`--profile extended`) ([profiles](/sources/docker-docs-compose-profiles.md)).

# Inferred
* **Inferred:** the anonymous-volume copy of a multi-GB baked datadir on every `docker run` costs seconds to tens of seconds and doubles disk use. Two designs to measure in task P-03: (A) keep `/var/lib/mysql` (standard, persistent by default); (B) bake into `/var/lib/mysql-baked` and set `datadir` in `/etc/mysql/conf.d/megasamples.cnf`, avoiding the copy (writes then live in the container layer; users mount a volume explicitly for persistence). The plan defaults to (A) unless P-03 shows first start above the 30 s budget for the core tier.
* **Inferred:** `COPY --from=builder --chown=999:999 /var/lib/mysql /var/lib/mysql` preserves ownership; `mysqld` refuses a datadir it cannot write, so P-03 also checks `ls -ln`.
* **Inferred:** running `mysqld` inside a single `RUN` (start → load → shutdown) works because the process tree lives only for that instruction; a clean `mysqladmin shutdown` is required so the redo log is empty and `ALTER INSTANCE ENABLE INNODB REDO_LOG` has been issued.

# Limits
* The builder that runs SQL Server or Oracle cannot be a Dockerfile stage (no Docker-in-Docker); those run as Compose services on the host and only their exported TSV/dump directories enter the build context ([orchestration decision](/decisions/build-orchestration.md)).
* Base is `microdnf`-only; extra tools (python, duckdb, curl) live in the separate `loader` image, never in the final stage.
