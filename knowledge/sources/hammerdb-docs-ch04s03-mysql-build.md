---
type: Source
title: HammerDB docs 4.3 — MySQL schema build options
description: The MySQL TPROC-C build parameters (warehouses, virtual users, storage engine, order_line partitioning, history PK).
resource: https://www.hammerdb.com/docs/ch04s03.html
tags: [hammerdb, mysql, tpc-c]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.hammerdb.com/docs/ch04s03.html
    title: MySQL Schema Build Options
    accessed: "2026-09-02"
---

# What was read
The MySQL build-options section.

# Relevant excerpt
* Options: "Number of Warehouses"; "Virtual Users to Build Schema" (set to the warehouse count or the load server's core/thread count); "Transactional Storage Engine" (InnoDB default); "Partition Order Line Table"; "History Table Primary Key" ("creates an invisible primary key for replication compatibility"); "The MySQL User is the user which has permission to create a database".
* No statement about reproducible/seeded data; no row counts.

# What it was used to decide
[TPC-C implementations tool record](/tools/tpcc-implementations.md).
