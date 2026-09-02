---
type: Source
title: "docker-library/mysql 9.7/Dockerfile.oracle"
description: "The official mysql:9.7 image: oraclelinux:9-slim, gosu, Oracle RPM mysql-community-server-minimal 9.7.2-1.el9, mysql-shell 9.7.1-1.el9 installed, /etc/my.cnf patched, VOLUME /var/lib/mysql, ENTRYPOINT docker-entrypoint.sh."
resource: https://raw.githubusercontent.com/docker-library/mysql/master/9.7/Dockerfile.oracle
tags: [docker, mysql, image, dockerfile]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://raw.githubusercontent.com/docker-library/mysql/master/9.7/Dockerfile.oracle
    title: "docker-library/mysql 9.7/Dockerfile.oracle"
    accessed: 2026-09-02
    version: "master @ 2f988f198f35d25b1454fa2504a0e4c348100549 (2026-08-19)"
---

# What was read
https://raw.githubusercontent.com/docker-library/mysql/master/9.7/Dockerfile.oracle, accessed 2026-09-02; version: master @ 2f988f198f35d25b1454fa2504a0e4c348100549 (2026-08-19).

# Relevant excerpt
* Repo layout: `8.4/`, `9.7/`, `innovation/`, each with `Dockerfile.oracle` and `docker-entrypoint.sh`; there is no `config/my.cnf` in the tree.
* `FROM oraclelinux:9-slim`; user/group `mysql` uid/gid 999; gosu 1.19; `microdnf install -y bzip2 gzip openssl xz zstd findutils`.
* `ENV MYSQL_MAJOR 9.7`, `ENV MYSQL_VERSION 9.7.2-1.el9`; yum repo `https://repo.mysql.com/yum/mysql-9.7-community/docker/el/9/$basearch/`; `microdnf install -y "mysql-community-server-minimal-$MYSQL_VERSION"`.
* `/etc/my.cnf` edits: socket changed from `/var/lib/mysql/mysql.sock` to `/var/run/mysqld/mysqld.sock`, a `[client]` socket entry, and `!includedir /etc/mysql/conf.d/` appended; `mkdir -p /var/lib/mysql /var/run/mysqld; chown mysql:mysql ...; chmod 1777 /var/lib/mysql /var/run/mysqld`; `mkdir /docker-entrypoint-initdb.d`.
* `ENV MYSQL_SHELL_VERSION 9.7.1-1.el9`; `microdnf install -y "mysql-shell-$MYSQL_SHELL_VERSION"; mysqlsh --version`.
* `VOLUME /var/lib/mysql`; `COPY docker-entrypoint.sh /usr/local/bin/`; `ENTRYPOINT ["docker-entrypoint.sh"]`; `EXPOSE 3306 33060`; `CMD ["mysqld"]`.

# What it was used to decide
[MySQL Shell utilities](/tools/mysql-shell-utilities.md) (mysqlsh is in the image), [LOAD DATA record](/tools/load-data-infile.md) (RPM my.cnf, no secure-file-priv override in the Dockerfile), [docker multi-stage record](/tools/docker-build-multistage.md) (VOLUME, uid 999, microdnf-only base).
