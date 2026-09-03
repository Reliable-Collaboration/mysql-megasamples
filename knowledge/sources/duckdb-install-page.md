---
type: Source
title: DuckDB installation page (version selector)
description: Current stable 1.5.5; LTS 1.4.5; install commands per client.
resource: https://duckdb.org/install/
tags:
- duckdb
- version
status: stable
trust: verified
stale_after: "2026-12-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:41:13Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:41:13Z"
sources:
- resource: https://duckdb.org/install/
  title: DuckDB installation page (version selector)
  accessed: "2026-09-02"
  version: read 2026-09-02
---

# What was read
https://duckdb.org/install/, accessed 2026-09-02; version: read 2026-09-02.

# Relevant excerpt
* Version selector: "1.5.5 (current)" and "1.4.5 (LTS)"; "This page contains links to the current stable and the LTS versions." Examples: `curl https://install.duckdb.org | DUCKDB_VERSION=1.4.5 bash`, `pip install duckdb==1.4.5`, `docker run --rm -it -v "$(pwd):/workspace" -w /workspace duckdb/duckdb:1.4.5`; JDBC `duckdb_jdbc-1.5.5.1.jar`.

# What it was used to decide
[DuckDB record](/tools/duckdb.md): pin 1.5.5 (matches the PyPI wheel and the GitHub release of 2026-07-22).
