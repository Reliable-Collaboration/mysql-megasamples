---
type: Source
title: HammerDB docs 1.12 — Docker container build and run
description: Official HammerDB Docker image names and run commands.
resource: https://www.hammerdb.com/docs/ch01s12.html
tags: [hammerdb, docker]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://www.hammerdb.com/docs/ch01s12.html
    title: HammerDB Docker Container Build & Run
    accessed: 2026-09-02
---

# What was read
The Docker section.

# Relevant excerpt
* Pre-built images: `tpcorg/hammerdb` (all databases), `tpcorg/hammerdb:mysql`, `:maria`, `:oracle`, `:postgres`, `:mssqls`; "docker pull tpcorg/hammerdb"; "docker run -it --name hammerdb hammerdb-v6.0 bash"; "docker run --network=host -it --name hammerdb hammerdb-v6.0 bash".

# What it was used to decide
[TPC-C implementations tool record](/tools/tpcc-implementations.md).
