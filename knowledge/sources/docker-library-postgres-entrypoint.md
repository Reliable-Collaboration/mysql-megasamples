---
type: Source
title: "docker-library/postgres docker-entrypoint.sh"
description: "The official image's entrypoint, read on 2026-09-09 for how an existing data directory is detected."
resource: https://raw.githubusercontent.com/docker-library/postgres/master/docker-entrypoint.sh
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
- resource: https://raw.githubusercontent.com/docker-library/postgres/master/docker-entrypoint.sh
  title: "docker-library/postgres docker-entrypoint.sh"
  accessed: "2026-09-09"
---

# What was read
The whole script, in particular `docker_create_db_directories`, `docker_init_database_dir`, `docker_setup_db`, the `DATABASE_ALREADY_EXISTS` detection and `_main`.

# Relevant excerpt
`declare -g DATABASE_ALREADY_EXISTS` ... `# look specifically for PG_VERSION, as it is expected in the DB dir` ... `if [ -s "$PGDATA/PG_VERSION" ]; then DATABASE_ALREADY_EXISTS='true'`; in `_main`: `if [ -z "$DATABASE_ALREADY_EXISTS" ]; then` ... `docker_init_database_dir` ... `docker_setup_db` ... `docker_process_init_files /docker-entrypoint-initdb.d/*`. `docker_create_db_directories` runs `mkdir -p "$PGDATA"`, `chmod 00700`, and chowns to postgres when running as root; `initdb` is called with `--username="$POSTGRES_USER" --pwfile=<(...)`.

# What it was used to decide
[PostgreSQL official image](/tools/postgres-docker-official-image.md): a data directory that already holds `PG_VERSION` is started as it is, with no initdb, no password setup and no init scripts -- the same shape as MySQL's baked data directory.
