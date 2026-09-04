---
type: Source
title: DbGate — predefining connections through environment variables in Docker
description: CONNECTIONS plus LABEL_/SERVER_/USER_/PASSWORD_/PORT_/ENGINE_ suffixed with a connection id define a connection with no user interaction; the container serves on port 3000 and keeps state in /root/.dbgate.
resource: https://github.com/dbgate/dbgate/blob/master/docker-compose.yaml
tags:
- console
- docker
- dbgate
status: stable
trust: verified
generated:
  by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
sources:
- resource: https://raw.githubusercontent.com/dbgate/dbgate/master/docker-compose.yaml
  title: DbGate's own docker-compose.yaml (read in full)
  accessed: "2026-09-03"
- resource: https://docs.dbgate.io/env-variables/
  title: Environment variables page — reached through search results, the page itself would not render
  accessed: "2026-09-03"
- resource: https://hub.docker.com/v2/repositories/dbgate/dbgate/tags?page_size=8&ordering=last_updated
  title: tag listing (API probe)
  accessed: "2026-09-03"
---

# What was read
DbGate's own `docker-compose.yaml` at `master`, read in full; the tag listing through the registry
API; and the documentation's environment-variable page, which is the weaker of the two — the page
would not render for direct fetching and its content was seen only through search results, so the
compose file is what the naming below rests on.

# Relevant excerpt
From the project's compose file, the connection block (commented out there as an example):

```
# CONNECTIONS: mssql
# LABEL_mssql: MS Sql
# SERVER_mssql: mssql
# USER_mssql: sa
# PORT_mssql: 1433
# PASSWORD_mssql: Pwd2020Db
# ENGINE_mssql: mssql@dbgate-plugin-mssql
```

The service maps container port **3000**, mounts a named volume at **`/root/.dbgate`** for state, and
supports `WEB_ROOT` for serving under a path prefix. The documentation additionally names
`PASSWORD_MODE_<id>`, which decides whether the password is stored or asked for.

Tags on 2026-09-03: `alpine`, `7.2.6-alpine`, `latest`, `7.2.6`, `beta-alpine`, `beta`, `7.2.5-alpine`, `7.2.5`.

# What it was used to decide
That DbGate can be fully preconfigured from environment alone, with no config file to mount. The
engine string for MySQL is **Inferred:** `mysql@dbgate-plugin-mysql` by the same pattern as the
documented `mssql@dbgate-plugin-mssql`; confirming it is part of the console task's
[open question](/questions/console-preconfiguration-limits.md). Pinned tag: `7.2.6-alpine`
([decision](/decisions/browsing-console-stack.md)).
