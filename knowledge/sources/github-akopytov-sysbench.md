---
type: Source
title: akopytov/sysbench README and repository metadata (license, LuaJIT, --rand-seed)
description: sysbench itself is GPL-2.0, embeds LuaJIT, and exposes --rand-seed; Debian packages it as sysbench 1.0.20+ds.
resource: https://github.com/akopytov/sysbench
tags: [sysbench, gpl, luajit]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/akopytov/sysbench/master/README.md
    title: sysbench README
    accessed: 2026-09-02
    version: master; GitHub API license GPL-2.0, latest release tag 1.0.20 (2020-04-24), pushed_at 2025-03-09
  - resource: https://packages.debian.org/trixie/sysbench
    title: Debian trixie package sysbench
    accessed: 2026-09-02
    version: 1.0.20+ds-7
---

# What was read
README option tables and the Debian package page.

# Relevant excerpt
* README: sysbench is "based on LuaJIT"; `--rand-type` "random numbers distribution {uniform, gaussian, special, pareto, zipfian} ... default special"; `--rand-seed` "seed for random number generator. When 0, the current time is used as an RNG seed." default 0; `--luajit-cmd`.
* GitHub license: GPL-2.0.
* Debian trixie: package `sysbench` 1.0.20+ds-7, "multi-threaded benchmark tool for database systems", depends on libluajit-5.1-2, libmariadb3 (>= 3.0.0), libpq5, libaio1t64, libc6 (>= 2.38) — so a MySQL-capable sysbench is one `apt-get install sysbench` away in a Debian-based loader image.

# What it was used to decide
[TPC-C implementation choice](/decisions/tpcc-implementation-choice.md); [GPL-2.0 license record](/licenses/gpl-2-0.md).
