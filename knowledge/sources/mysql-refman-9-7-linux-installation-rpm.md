---
type: Source
title: "MySQL 9.7 Reference Manual: Installing MySQL on Linux Using RPM Packages from Oracle"
description: "Installation layout table for Oracle RPM packages: /etc/my.cnf, /var/lib/mysql, secure_file_priv=/var/lib/mysql-files."
resource: https://dev.mysql.com/doc/refman/9.7/en/linux-installation-rpm.html
tags: [mysql, docs, rpm, secure-file-priv]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/linux-installation-rpm.html
    title: "MySQL 9.7 Reference Manual: Installing MySQL on Linux Using RPM Packages from Oracle"
    accessed: 2026-09-02
    version: "MySQL 9.7 manual, section 2.5.4, Table 2.13"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/linux-installation-rpm.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 2.5.4, Table 2.13.

# Relevant excerpt
Table "MySQL Installation Layout for Linux RPM Packages from the MySQL Developer Zone": Configuration file `/etc/my.cnf`; Data directory `/var/lib/mysql`; "Value of secure_file_priv" `/var/lib/mysql-files`; Socket `/var/lib/mysql/mysql.sock`; Keyring directory `/var/lib/mysql-keyring`; client programs `/usr/bin`; mysqld `/usr/sbin`; error log `/var/log/mysqld.log` (RHEL/Oracle Linux family).

# What it was used to decide
[LOAD DATA tool record](/tools/load-data-infile.md) and [docker multi-stage record](/tools/docker-build-multistage.md): the official image installs the Oracle RPM `mysql-community-server-minimal` ([Dockerfile](/sources/docker-library-mysql-9-7-dockerfile-oracle.md)) so its `/etc/my.cnf` and `secure_file_priv=/var/lib/mysql-files` are expected inside the container (**Inferred** until `docker run --rm mysql:9.7.2 cat /etc/my.cnf` confirms).
