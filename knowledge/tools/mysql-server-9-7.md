---
type: Tool
title: MySQL Server 9.7 LTS
description: The target database engine; LTS status, support window, and the point release to pin.
resource: https://dev.mysql.com/doc/refman/9.7/en/
tags: [mysql, target, lts]
status: stable
trust: verified
stale_after: "2026-10-20"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/mysql-releases.html
    title: MySQL Releases, Innovation and LTS
    accessed: "2026-09-02"
  - resource: https://dev.mysql.com/doc/relnotes/mysql/9.7/en/
    title: 9.7 release notes
    accessed: "2026-09-02"
---

# Facts
* 9.7.0 GA 2026-04-21; latest point release 9.7.3 (2026-08-18) ([release notes](/sources/mysql-9-7-release-notes.md)).
* 9.7 is an LTS series: "Upgrading to the next LTS series is supported, such as 8.4.x LTS to 9.7.x LTS" ([reference manual](/sources/mysql-refman-9-7-releases.md)); 5 years premier + 3 years extended support.
* 9.7 is the last sequentially-numbered line; later releases are calendar-versioned (26.7 = July 2026 Innovation).

# Behaviour that affects conversions (to be verified per feature by the tools research agent)
See [MySQL 9.x feature notes](/tools/mysql-9x-behaviour-notes.md) for utf8mb4 defaults, removal of `mysql_native_password`, `local_infile`/`secure_file_priv`, spatial SRID rules, CHECK constraints and generated columns.

# Limits
* `DATETIME` range 1000-01-01 to 9999-12-31 and `TIMESTAMP` up to 2038-01-19; no `datetimeoffset` or native UUID type; `mysql_native_password` removed; InnoDB partitioned tables cannot carry foreign keys — details and sources in [MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md).
