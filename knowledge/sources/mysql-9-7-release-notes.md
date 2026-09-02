---
type: Source
title: MySQL 9.7 Release Notes index
description: Release list for the 9.7 series; 9.7.0 GA on 2026-04-21, latest 9.7.3 on 2026-08-18.
resource: https://dev.mysql.com/doc/relnotes/mysql/9.7/en/
tags: [mysql, release-notes]
status: stable
trust: verified
stale_after: 2026-10-20
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
sources:
  - resource: https://dev.mysql.com/doc/relnotes/mysql/9.7/en/
    title: MySQL 9.7 Release Notes
    accessed: 2026-09-02
---

# Relevant excerpt
Entries listed, newest first: 9.7.3 (2026-08-18), 9.7.2 (2026-07-28), 9.7.1 (2026-06-16), 9.7.0 (2026-04-21). The index page itself does not carry the LTS label; that comes from [the reference manual](/sources/mysql-refman-9-7-releases.md) and the Docker image tag `lts` in [the image README](/sources/docker-library-mysql-readme.md).

# What it was used to decide
Point-release pin in [Target MySQL version decision](/decisions/target-mysql-version.md). `stale_after` is set to the next expected quarterly release; re-check before pinning.
