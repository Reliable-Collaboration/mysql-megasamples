---
type: Source
title: CloudBeaver — preconfiguring server datasources
description: Connections are predefined in a data-sources.json under the server's conf directory; the wiki did not establish how the first-run administrator is set or whether the setup wizard can be skipped unattended.
resource: https://github.com/dbeaver/cloudbeaver/wiki/Configuring-server-and-database-connections
tags:
- console
- docker
- cloudbeaver
status: stable
trust: verified
generated:
  by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
sources:
- resource: https://github.com/dbeaver/cloudbeaver/wiki/Configuring-server-and-database-connections
  title: Configuring server and database connections (wiki index page)
  accessed: "2026-09-03"
- resource: https://hub.docker.com/v2/repositories/dbeaver/cloudbeaver/tags?page_size=8&ordering=last_updated
  title: tag listing (API probe)
  accessed: "2026-09-03"
---

# What was read
The wiki page that indexes CloudBeaver's server and connection configuration, and the image's tag
listing through the registry API, 2026-09-03.

# Relevant excerpt
* Predefined connections live in **`data-sources.json`**, in the server's configuration directory,
  which in the container is under `/opt/cloudbeaver/conf/`. The wiki links separate pages for
  "Configuring server datasources", "data-sources.json reference" and "Pre-Configure Credentials".
* The page does **not** state how the initial administrator is created, whether `CB_ADMIN_NAME` /
  `CB_ADMIN_PASSWORD` exist, or whether the first-launch wizard can be skipped — it refers those to a
  "First launch guide" that was not read.
* Tags on 2026-09-03: `ea`, `26.2.0`, `26.2`, `26`, `latest`, `26.1.5`, `26.1`, `26.1.4`.

# What it was used to decide
That CloudBeaver is the console with the least certain preconfiguration story: the connection can be
supplied as a file, but the wiki does not say how the first administrator is created or whether the
wizard can be skipped, which was the substance of the console task's
[open question](/questions/console-preconfiguration-limits.md).

That question is now closed **by measurement rather than by this page**, and the gap is worth
recording: the mechanism that actually skips the wizard — a `java.util.Properties` file at
`conf/.cloudbeaver.auto.conf` — appears nowhere in the wiki, and was found by reading
`CBApplication` in the shipped jars. Nor does the wiki mention that a seeded global connection is
granted to no subject, so it stays invisible until
`CLOUDBEAVER_APP_GRANT_CONNECTIONS_ACCESS_TO_ANONYMOUS_TEAM` is set. Treat this source as accurate on
the file format and incomplete on startup; the measured procedure is in
[the runbook](/runbooks/cloudbeaver-unattended-startup.md). Shipped by digest, version `25.2.0`
([decision](/decisions/browsing-console-stack.md)).
