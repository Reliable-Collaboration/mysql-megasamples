---
type: Source
title: "docker-library/postgres 18/bookworm/Dockerfile"
description: "The Dockerfile of the official postgres:18-bookworm image, read on 2026-09-09 for PGDATA, VOLUME and the stop signal."
resource: https://raw.githubusercontent.com/docker-library/postgres/master/18/bookworm/Dockerfile
tags:
- source
- postgresql
- docker
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:16:50Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:16:50Z"
sources:
- resource: https://raw.githubusercontent.com/docker-library/postgres/master/18/bookworm/Dockerfile
  title: "docker-library/postgres 18/bookworm/Dockerfile"
  accessed: "2026-09-09"
---

# What was read
The whole file, together with `17/bookworm/Dockerfile` and `19/bookworm/Dockerfile` for comparison.

# Relevant excerpt
18: `ENV PG_MAJOR 18`, `ENV PG_VERSION 18.6-1.pgdg12+2`, `ENV PGDATA /var/lib/postgresql/18/docker`, `VOLUME /var/lib/postgresql`, `STOPSIGNAL SIGINT`, `EXPOSE 5432`, `CMD ["postgres"]`. 17: `ENV PGDATA /var/lib/postgresql/data`, `VOLUME /var/lib/postgresql/data`. 19: `PG_VERSION 19~beta3-1.pgdg12+1`, same layout as 18.

# What it was used to decide
[PostgreSQL official image](/tools/postgres-docker-official-image.md): where a baked cluster lives and that it sits inside the declared volume, as MySQL's does.
