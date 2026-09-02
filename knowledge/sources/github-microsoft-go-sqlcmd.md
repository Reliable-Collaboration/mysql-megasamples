---
type: Source
title: microsoft/go-sqlcmd repository (license and latest release)
description: The new Go-based sqlcmd is MIT licensed; v1.10.0 (2026-03-03) ships Linux amd64/arm64/s390x tarballs.
resource: https://github.com/microsoft/go-sqlcmd
tags: [sqlcmd, mit, tool]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://api.github.com/repos/microsoft/go-sqlcmd
    title: repository metadata (license.spdx_id MIT; description "The new sqlcmd, CLI for SQL Server and Azure SQL (winget install sqlcmd / sqlcmd create mssql / sqlcmd open ads)")
    accessed: 2026-09-02
  - resource: https://api.github.com/repos/microsoft/go-sqlcmd/releases/latest
    title: latest release v1.10.0, published 2026-03-03T17:02:18Z
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/microsoft/go-sqlcmd/main/LICENSE
    title: LICENSE (first lines read)
    accessed: 2026-09-02
stale_after: 2027-03-01
---

# What was read
GitHub API metadata, the latest release, and the head of the LICENSE file.

# Relevant excerpt
> MIT License (MIT)  Copyright © Microsoft Corp.  Permission is hereby granted, free of charge, to any person obtaining a copy ...

Release v1.10.0 Linux assets: `sqlcmd-linux-amd64.tar.bz2` 22,736,361 bytes; `sqlcmd-linux-arm64.tar.bz2` 20,715,402; `sqlcmd-linux-s390x.tar.bz2` 22,049,108.

# What it was used to decide
[sqlcmd/bcp tool record](/tools/sqlcmd-bcp.md): go-sqlcmd is the redistributable, arm64-capable query client; it has no `bcp` equivalent.
