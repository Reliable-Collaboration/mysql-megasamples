---
type: Source
title: docker-library/mysql versions.json
description: Machine-readable list of versions currently built for the official mysql Docker image; 9.7.2, 8.4.11 and 26.7.0 on 2026-09-02.
resource: https://raw.githubusercontent.com/docker-library/mysql/master/versions.json
tags:
- docker
- mysql
- image
status: stable
trust: verified
stale_after: "2026-10-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:05:32Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:05:32Z"
sources:
- resource: https://raw.githubusercontent.com/docker-library/mysql/master/versions.json
  title: versions.json on master
  accessed: "2026-09-02"
---
# What was read
* https://raw.githubusercontent.com/docker-library/mysql/master/versions.json, “versions.json on master”, accessed 2026-09-02

# Relevant excerpt
Paraphrase of the JSON: `innovation` → 26.7.0 (oracle variant 26.7.0-1.el9, mysql-shell 26.7.1-1.el9); `9.7` → 9.7.2 (9.7.2-1.el9, mysql-shell 9.7.1-1.el9); `8.4` → 8.4.11 (8.4.11-1.el9, mysql-shell 8.4.10-1.el9). All on base OS variant "9-slim" (Oracle Linux 9), architectures amd64 and arm64v8.

Note the lag: Oracle published 9.7.3 and 8.4.12 on 2026-08-18 ([9.7 notes](/sources/mysql-9-7-release-notes.md), [8.4 notes](/sources/mysql-8-4-release-notes.md)) but the official image still lists 9.7.2 / 8.4.11.

# What it was used to decide
The pin in [Target MySQL version decision](/decisions/target-mysql-version.md) and the verification-first step in PLAN.md: run `docker manifest inspect mysql:9.7.3` before pinning; fall back to 9.7.2.
