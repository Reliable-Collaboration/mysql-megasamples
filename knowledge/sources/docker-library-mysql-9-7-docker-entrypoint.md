---
type: Source
title: "docker-library/mysql 9.7/docker-entrypoint.sh"
description: "Entrypoint logic: DATADIR from `mysqld --verbose --help`, DATABASE_ALREADY_EXISTS when $DATADIR/mysql exists, init path with temporary server and initdb.d processing, else straight exec."
resource: https://raw.githubusercontent.com/docker-library/mysql/master/9.7/docker-entrypoint.sh
tags: [docker, mysql, image, entrypoint]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://raw.githubusercontent.com/docker-library/mysql/master/9.7/docker-entrypoint.sh
    title: "docker-library/mysql 9.7/docker-entrypoint.sh"
    accessed: "2026-09-02"
    version: "master @ 2f988f198f35d25b1454fa2504a0e4c348100549 (2026-08-19)"
---

# What was read
https://raw.githubusercontent.com/docker-library/mysql/master/9.7/docker-entrypoint.sh, accessed 2026-09-02; version: master @ 2f988f198f35d25b1454fa2504a0e4c348100549 (2026-08-19).

# Relevant excerpt
* `mysql_get_config()` reads values from `"$@" --verbose --help` ("We use mysqld --verbose --help instead of my_print_defaults because the latter only show values present in config files, and not server defaults").
* `docker_setup_env()`: `DATADIR="$(mysql_get_config 'datadir' "$@")"`, `SOCKET=...`; then `declare -g DATABASE_ALREADY_EXISTS; if [ -d "$DATADIR/mysql" ]; then DATABASE_ALREADY_EXISTS='true'; fi`.
* `docker_create_db_directories()` creates and chowns (when running as root) the datadir, socket dir and the directories named by `general-log-file`, `keyring_file_data`, `pid-file`, `secure-file-priv`, `slow-query-log-file`.
* `_main()`: if `$1` is `mysqld`: `mysql_note "Entrypoint script for MySQL Server ${MYSQL_VERSION} started."`, `mysql_check_config`, `docker_setup_env`, `docker_create_db_directories`; if uid 0 → `mysql_note "Switching to dedicated user 'mysql'"; exec gosu mysql "$BASH_SOURCE" "$@"`; then `if [ -z "$DATABASE_ALREADY_EXISTS" ]; then docker_verify_minimum_env; ls /docker-entrypoint-initdb.d/ > /dev/null; docker_init_database_dir "$@" (mysqld --initialize-insecure --default-time-zone=SYSTEM); mysql_note "Starting temporary server"; docker_temp_server_start (mysqld --daemonize --skip-networking --default-time-zone=SYSTEM --socket=...); mysql_socket_fix; docker_setup_db; docker_process_init_files /docker-entrypoint-initdb.d/*; mysql_expire_root_user; mysql_note "Stopping temporary server"; docker_temp_server_stop (mysqladmin shutdown); mysql_note "MySQL init process done. Ready for start up."; else mysql_socket_fix; fi; exec "$@"`.
* Consequences: with a pre-populated datadir the entrypoint performs no initialization, requires no `MYSQL_ROOT_PASSWORD`, runs no initdb.d scripts, and simply `exec mysqld`.

# What it was used to decide
[docker multi-stage record](/tools/docker-build-multistage.md) and [bake-data decision](/decisions/bake-data-vs-initdb.md): the "datadir already exists" branch is exactly the bake-data path; root password and users must therefore be created in the build stage.
