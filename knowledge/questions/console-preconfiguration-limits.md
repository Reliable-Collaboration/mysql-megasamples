---
type: Open Question
title: How far can each of the four database consoles be preconfigured without a manual step?
description: phpMyAdmin and DbGate look fully preconfigurable and Adminer clearly is not; CloudBeaver's unattended startup is unknown, and DbGate's MySQL engine string is inferred from the documented MSSQL one.
resource: /questions/console-preconfiguration-limits.md
tags:
- question
- console
- docker
- cloudbeaver
- dbgate
status: deprecated
trust: verified
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-04T00:00:00Z"
generated:
  by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
sources:
- resource: /sources/cloudbeaver-connection-preconfiguration.md
  title: CloudBeaver datasource preconfiguration
  accessed: "2026-09-03"
- resource: /sources/dbgate-docker-configuration.md
  title: DbGate connection environment variables
  accessed: "2026-09-03"
- resource: /sources/docker-hub-adminer-image.md
  title: Adminer image environment variables
  accessed: "2026-09-03"
---

# Question
1. **CloudBeaver, the one that decides whether it ships.** Can a fresh `dbeaver/cloudbeaver:26.2.0`
   container come up with the megasamples connection already present and **no first-launch wizard and
   no manually created administrator**? Which files must be mounted (`data-sources.json`, a server
   config, a `.credentials` file?), where exactly, and do `CB_ADMIN_NAME` / `CB_ADMIN_PASSWORD` exist?
   If the answer is no, CloudBeaver is dropped from the profile per the decision.
2. **DbGate's engine string.** The documented example is `ENGINE_mssql: mssql@dbgate-plugin-mssql`;
   `mysql@dbgate-plugin-mysql` is inferred from the pattern, not read. Confirm it.
3. **Adminer's login.** `ADMINER_DEFAULT_SERVER` presets the server, and the README documents nothing
   for credentials. Confirm the login form really does still appear, and whether a bundled plugin
   (`login-password-less`, or the `loginPasswordLess` sample) can preset the `demo` account safely for
   a read-only user.
4. **phpMyAdmin under a path.** If the landing page and the consoles are served from one host, does
   phpMyAdmin need `PMA_ABSOLUTE_URI`, and does DbGate need `WEB_ROOT`?

# Cheapest experiment
Bring each container up alone against the built image and look:

```
docker run --rm -p 127.0.0.1:8081:80 -e PMA_HOST=host.docker.internal -e PMA_USER=demo \
  -e PMA_PASSWORD=demo phpmyadmin:5.2.3-apache
docker run --rm -p 127.0.0.1:8083:3000 -e CONNECTIONS=mega -e SERVER_mega=... \
  -e ENGINE_mega=mysql@dbgate-plugin-mysql dbgate/dbgate:7.2.6-alpine
docker run --rm -p 127.0.0.1:8084:8978 dbeaver/cloudbeaver:26.2.0
```
then `curl -sI` each and open it once. For CloudBeaver, inspect `/opt/cloudbeaver/conf/` inside the
running container to see the shape of the files it actually reads, which is faster than the wiki.

# Resolves
[The console decision](/decisions/browsing-console-stack.md) and task C-01: specifically which of the
four consoles ship, and whether the landing page must show credentials for any of them.

# Answer (2026-09-04, task C-01)
All four questions, answered by bringing each container up against the built image rather than by
reading a wiki.

1. **CloudBeaver: no, and it is dropped.** `dbeaver/cloudbeaver:25.2.0` stays in
   `configurationMode: true` however it is configured. Mounting an `initial-data-sources.conf` with
   the connection, setting `CLOUDBEAVER_APP_ANONYMOUS_ACCESS_ENABLED=true`, and setting both
   `CB_ADMIN_NAME`/`CB_ADMIN_PASSWORD` and `CLOUDBEAVER_ADMIN_NAME`/`CLOUDBEAVER_ADMIN_PASSWORD`
   were each tried; the GraphQL `serverConfig{configurationMode}` returned `true` every time. Its
   first-launch wizard cannot be skipped by configuration, so per the decision it ships nothing
   rather than shipping a manual step. The three that remain all come up unattended.
2. **DbGate's engine string is `mysql@dbgate-plugin-mysql`** — confirmed, not inferred. The
   container's own log prints `"engine":"mysql@dbgate-plugin-mysql"` under
   `DBGM-00005 Using connections from ENV variables`, and the connection is present in the UI.
3. **Adminer's login form does remain.** With `ADMINER_DEFAULT_SERVER` set, the page still serves
   `auth[username]`, `auth[password]`, `auth[server]` and `auth[db]` fields under
   `<title>Login - Adminer</title>`. The landing page therefore states the credentials, and the S10
   test asserts they are on it. No password-less plugin was used: presetting a login for a UI that
   can reach a database is worse than showing a read-only account's password.
4. **Neither `PMA_ABSOLUTE_URI` nor `WEB_ROOT` is needed.** The consoles are served on their own
   ports rather than under a path on one host, so the question does not arise in this shape.
   phpMyAdmin signs in from `PMA_USER`/`PMA_PASSWORD` and opens straight into the data: its title is
   `127.0.0.1:8081 / mysql | phpMyAdmin 5.2.3` with a navigation panel and no login form.
