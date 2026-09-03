---
type: Tool
title: Official mysql Docker image
description: Base image for the final stage; tag family, initdb behaviour, variants, and the verification step for the 9.7.3 tag.
resource: https://hub.docker.com/_/mysql
tags:
- docker
- base-image
- mysql
status: stable
trust: verified
stale_after: "2026-10-20"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:05:32Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:05:32Z"
sources:
- resource: https://raw.githubusercontent.com/docker-library/docs/master/mysql/README.md
  title: mysql image README
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/docker-library/mysql/master/versions.json
  title: versions.json
  accessed: "2026-09-02"
---

# Facts
* Tag `lts` currently resolves to 9.7.2; `9.7` floats within the series; base OS Oracle Linux 9 slim; amd64 and arm64v8 ([versions.json](/sources/docker-library-mysql-versions-json.md)).
* Bundled `mysql-shell` version tracks the server (9.7.1 for the 9.7 image), so `mysqlsh` is available in the final image without extra packages.
* Entrypoint processes `.sh .sql .sql.gz .sql.bz2 .sql.xz .sql.zst` in `/docker-entrypoint-initdb.d` in alphabetical order, only on an empty data directory ([README](/sources/docker-library-mysql-readme.md)).
* `MYSQL_ROOT_PASSWORD` required unless `MYSQL_ALLOW_EMPTY_PASSWORD` / `MYSQL_RANDOM_ROOT_PASSWORD` are used.

# Verification-first step for the executor
```
docker manifest inspect mysql:9.7.3 >/dev/null && echo available || echo "not yet published; pin 9.7.2"
```
Result on 2026-09-02: `9.7.3` not available, `9.7.2` available ([environment survey](/sources/build-machine-environment-2026-09-02.md)).
If the pull hangs, apply the IPv6 checklist in [the troubleshooting runbook](/runbooks/ipv6-and-privileges.md) before anything else.

# Inferred
* **Inferred:** the `oracle` variant lacks `apt`; extra tools for the build stage must come from a separate builder image rather than being installed into the base image. Verify with `docker run --rm mysql:9.7 sh -c 'command -v microdnf dnf apt'`.

# Limits
* Base is `oraclelinux:9-slim` with `microdnf` only; conversion tooling cannot be installed into it and lives in the separate loader image ([multi-stage record](/tools/docker-build-multistage.md)).
* `VOLUME /var/lib/mysql` is declared upstream; a baked data directory is copied into an anonymous volume on first `docker run` (cost measured in task P-03).
* The `lts` and `9.7` tags float; only the full `9.7.2` tag is a pin.
