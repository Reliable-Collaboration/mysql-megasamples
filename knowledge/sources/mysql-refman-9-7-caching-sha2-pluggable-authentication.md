---
type: Source
title: "MySQL 9.7 Reference Manual: Caching SHA-2 Pluggable Authentication"
description: "caching_sha2_password is the default; mysql_native_password is no longer available; connection requirements for clients."
resource: https://dev.mysql.com/doc/refman/9.7/en/caching-sha2-pluggable-authentication.html
tags: [mysql, docs, authentication]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/caching-sha2-pluggable-authentication.html
    title: "MySQL 9.7 Reference Manual: Caching SHA-2 Pluggable Authentication"
    accessed: 2026-09-02
    version: "MySQL 9.7 manual, section 8.4.1.1"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/caching-sha2-pluggable-authentication.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 8.4.1.1.

# Relevant excerpt
> "In MySQL 9.7, caching_sha2_password is the default authentication plugin; mysql_native_password is no longer available."
> "To connect to the server using an account that authenticates with the caching_sha2_password plugin, you must use either a secure connection or an unencrypted connection that supports password exchange using an RSA key pair."
* Client options `--get-server-public-key` and `--server-public-key-path` are supported by mysql, mysqlsh, mysqladmin, mysqlbinlog, mysqlcheck, mysqldump, mysqlimport, mysqlshow, mysqlslap, mysqltest. Example: `mysql --ssl-mode=DISABLED -u sha2user -p --get-server-public-key`.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md) and [Python stack](/tools/python-conversion-stack.md): every client library used at build or test time must implement caching_sha2_password; the Unix socket connection inside the build container counts as secure.
