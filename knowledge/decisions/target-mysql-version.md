---
type: Decision
title: Target MySQL version is 9.7 LTS, pinned to the latest published official image point release
description: Choose MySQL 9.7.x LTS (currently 9.7.3 upstream, 9.7.2 in the official image) over 8.4.x LTS as the image base.
resource: /decisions/target-mysql-version.md
tags:
- decision
- mysql
- version
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
- resource: https://dev.mysql.com/doc/refman/9.7/en/mysql-releases.html
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/relnotes/mysql/9.7/en/
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/docker-library/mysql/master/versions.json
  accessed: "2026-09-02"
---

# Question
The brief said "the current MySQL LTS release ... e.g. mysql:8.4.x". As of 2026-09-02 there are two supported LTS lines, 8.4 (April 2024) and 9.7 (April 2026). Which one is the target?

# Options considered
1. **MySQL 9.7.x LTS** — newest LTS, supported for ~8 years from 2026-04; Docker tag `lts` points here.
2. MySQL 8.4.x LTS — older LTS, still supported; more third-party tools tested against it.
3. MySQL 26.7 Innovation — rejected outright: Innovation releases are supported only until the next Innovation release ([manual](/sources/mysql-refman-9-7-releases.md)).

# Evidence
* [MySQL Releases: Innovation and LTS](/sources/mysql-refman-9-7-releases.md) — 8.4→9.7 is the supported LTS upgrade path; LTS = 5+3 years.
* [9.7 release notes](/sources/mysql-9-7-release-notes.md) — 9.7.3 is current upstream.
* [docker-library versions.json](/sources/docker-library-mysql-versions-json.md) — official image at 9.7.2 on 2026-09-02.

# Outcome
Target **MySQL 9.7 LTS**. Pin the Dockerfile `ARG MYSQL_VERSION=9.7.2` — verified on 2026-09-02 that `mysql:9.7.3` is not yet published on Docker Hub while `mysql:9.7.2` is ([environment survey](/sources/build-machine-environment-2026-09-02.md)). The executor re-runs `docker manifest inspect mysql:9.7.3` at the start of execution and bumps the ARG (and this record) if it exists. Everything in the plan that is 9.x-specific (no `mysql_native_password`, utf8mb4 default) is called out so an 8.4 rebuild is a one-line change; the plan does not otherwise target 8.4.

# Status
accepted
