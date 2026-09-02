---
type: Source
title: "MySQL 9.7 Reference Manual 1.3 \"MySQL Releases: Innovation and LTS\""
description: Oracle's definition of Innovation versus LTS releases, LTS support duration, upgrade path 8.4 to 9.7, and the calendar-versioning change after 9.7.
resource: https://dev.mysql.com/doc/refman/9.7/en/mysql-releases.html
tags: [mysql, lts, versioning]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/mysql-releases.html
    title: MySQL 9.7 Reference Manual, section 1.3
    accessed: 2026-09-02
---

# Relevant excerpt
> "These releases only contain necessary fixes to reduce the risks associated with changes in the database software's behavior. There are no removals within an LTS release. Features can be removed (and added) only in the first LTS release (such as 8.4.0 LTS) but not later."

> "An LTS series follows the Oracle Lifetime Support Policy, which includes 5 years of premier support and 3 years of extended support."

> "MySQL 9.7 is the final release line using the previous sequential versioning model. Subsequent MySQL Innovation and LTS releases use calendar versioning in the YY.M format ... For example, MySQL 26.7 represents the July 2026 release."

> "Upgrading to the next LTS series is supported, such as 8.4.x LTS to 9.7.x LTS, while skipping an LTS series is not supported."

# What it was used to decide
[Target MySQL version decision](/decisions/target-mysql-version.md).
