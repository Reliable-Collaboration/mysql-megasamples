---
type: Tool
title: PostgreSQL official Docker image (postgres:18.6-bookworm)
description: The image the PostgreSQL engine is built from; where its data directory lives, how its entrypoint treats an existing one, and what was pulled.
resource: https://hub.docker.com/_/postgres
tags:
- tool
- postgresql
- docker
- image
status: stable
trust: verified
stale_after: "2026-12-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:16:50Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:16:50Z"
sources:
- resource: /sources/docker-library-postgres-versions-json.md
  accessed: "2026-09-09"
- resource: /sources/docker-library-postgres-18-dockerfile.md
  accessed: "2026-09-09"
- resource: /sources/docker-library-postgres-entrypoint.md
  accessed: "2026-09-09"
---

# Facts
* Versions published on 2026-09-09 ([versions.json](/sources/docker-library-postgres-versions-json.md)): 18.6 is the newest stable major; 19 is at beta3; 17.11, 16.15, 15.19, 14.24 remain.
* `postgres:18.6-bookworm` pulled on 2026-09-09 with a plain `docker pull`; image id and repo digest `sha256:1c59e2c3c818eaa0f0628f695b36e7c9e362d6b219b36a54a32df645cbd7e1af` (`docker image inspect`).
* Layout of the 18 image ([Dockerfile](/sources/docker-library-postgres-18-dockerfile.md)): `PGDATA=/var/lib/postgresql/18/docker`, `VOLUME /var/lib/postgresql`, `STOPSIGNAL SIGINT`, port 5432, `CMD ["postgres"]`. The 17 image used `/var/lib/postgresql/data` for both; 18 moved the data directory under a per-major path inside a wider volume.
* Entrypoint ([source](/sources/docker-library-postgres-entrypoint.md)): when `$PGDATA/PG_VERSION` is non-empty, `DATABASE_ALREADY_EXISTS` is set and `_main` skips `initdb`, the password setup and `/docker-entrypoint-initdb.d`; the directory is `mkdir -p`'d, `chmod 700` and chowned to `postgres` first when the container starts as root. A baked cluster is therefore started as it is, the same shape as the MySQL image's baked data directory ([bake decision](/decisions/bake-data-vs-initdb.md)).
* `pg_hba.conf` after a bare `initdb` inside the image trusts only the socket and loopback (`local all all trust`,
  `host all all 127.0.0.1/32 trust`, `::1/128`); the rule that admits clients on the network,
  `host all all all scram-sha-256`, is appended by the entrypoint's `pg_setup_hba_conf` during
  initialisation and so never appears in a cluster the builder initialised itself. Observed on 2026-09-09:
  a client on the Docker network got `no pg_hba.conf entry for host` until the builder appended the rule.
* The server refuses a data directory whose mode is not 0700 or 0750 (`data directory ... has invalid
  permissions`); `COPY --from=builder --chown` leaves 0755, so the image and the wrapper `chmod 700` it.
* Identifiers longer than 63 bytes are truncated silently (three of the corpus's MySQL index names, hashed
  to 64 characters by the T-SQL translator, came back shortened); the ports use a 63-byte-safe name.
* `POSTGRES_PASSWORD` is only read by the initialisation path; on a baked cluster passwords are whatever the builder set, so a runtime override needs its own mechanism (the engine's entrypoint wrapper).

# Limits
1. The baked data directory lies inside the declared volume, so each `docker run` copies it into a fresh anonymous volume, as it does for MySQL; the cost is measured by the image test's startup budget rather than assumed.
2. `STOPSIGNAL SIGINT` is a fast shutdown; the builder stage stops the server with `pg_ctl -m fast -w stop` before the directory is copied, so no recovery is needed at first start.
3. The 19 line is a beta and is not pinned.
