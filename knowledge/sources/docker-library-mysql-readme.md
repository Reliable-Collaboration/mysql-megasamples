---
type: Source
title: Official mysql Docker image README (docker-library/docs)
description: Documented tags, entrypoint initialization behaviour, environment variables, data directory and licensing pointer for the official mysql image.
resource: https://raw.githubusercontent.com/docker-library/docs/master/mysql/README.md
tags: [docker, mysql, image, entrypoint]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
sources:
  - resource: https://raw.githubusercontent.com/docker-library/docs/master/mysql/README.md
    title: mysql image README
    accessed: "2026-09-02"
---
# What was read
* https://raw.githubusercontent.com/docker-library/docs/master/mysql/README.md, “mysql image README”, accessed 2026-09-02

# Relevant excerpt
* Tags: `26.7.0, 26.7, 26, latest, innovation`; `9.7.2, 9.7, 9, lts`; `8.4.11, 8.4, 8`; variants `oraclelinux9` and `oracle` (default).
* > "When a container is started for the first time, a new database with the specified name will be created and initialized with the provided configuration variables. Furthermore, it will execute files with extensions `.sh`, `.sql`, `.sql.gz`, `.sql.bz2`, `.sql.xz`, and `.sql.zst` that are found in `/docker-entrypoint-initdb.d`. Files will be executed in alphabetical order."
* Initialization runs only when the data directory is empty. Shell scripts without the executable bit are sourced, not executed.
* `MYSQL_ROOT_PASSWORD` is "mandatory"; `MYSQL_DATABASE`, `MYSQL_USER`/`MYSQL_PASSWORD` optional; `MYSQL_INITDB_SKIP_TZINFO`: "By default, the entrypoint script automatically loads the timezone data needed for the CONVERT_TZ() function. If it is not needed, any non-empty value disables timezone loading."
* Data directory: `/var/lib/mysql`. License: "View license information (https://www.mysql.com/about/legal/) for the software contained in this image."
* No default character set documented for the image; set explicitly via config.

# What it was used to decide
[Official image tool record](/tools/mysql-docker-official-image.md); [data delivery decision](/decisions/bake-data-vs-initdb.md) (compressed `.sql.zst` init scripts are natively supported, which matters for repository size).
