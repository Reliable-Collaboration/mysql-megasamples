---
type: Runbook
title: "CloudBeaver without the wizard: conf/.cloudbeaver.auto.conf, a seeded connection, and the grant"
description: How a CloudBeaver CE container is brought up fully configured with a working connection and no manual step; the trigger is an undocumented java.util.Properties file at conf/.cloudbeaver.auto.conf, the connection comes from initial-data-sources.conf, and it stays invisible until grantConnectionsAccessToAnonymousTeam is set. Measured against dbeaver/cloudbeaver 25.2.0.
resource: /runbooks/cloudbeaver-unattended-startup.md
tags:
- runbook
- cloudbeaver
- console
- docker
status: stable
trust: verified
generated:
  by: claude-code/claude-opus-5
  at: "2026-09-04T00:00:00Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-04T00:00:00Z"
sources:
- resource: /sources/cloudbeaver-connection-preconfiguration.md
  title: CloudBeaver datasource preconfiguration
  accessed: "2026-09-03"
---

# CloudBeaver without the wizard

<!-- intro -->
A fresh CloudBeaver container answers HTTP 200 while showing its first-launch wizard, so "it started"
proves nothing. Three separate things have to be true before an anonymous visitor sees data, and each
one fails silently on its own. All of it was measured against
`dbeaver/cloudbeaver@sha256:3b4bf822…` (25.2.0); 24.3.5 behaves the same.
<!-- /intro -->

## 1. The server configures itself: `conf/.cloudbeaver.auto.conf`

`CBApplication.performAutoConfiguration` looks for a **`java.util.Properties`** file named
`.cloudbeaver.auto.conf` and, finding it, calls `finishConfiguration(...)` instead of entering
configuration mode. Its **presence is the trigger**. Without it the log says

```
No auto configuration was found. Server must be configured manually
```

and `{serverConfig{configurationMode}}` stays `true`, whatever environment variables are set.

The path must be exactly `/opt/cloudbeaver/conf/.cloudbeaver.auto.conf`. Mounting the same file at
`/opt/cloudbeaver/` or `/opt/cloudbeaver/workspace/` leaves the server in configuration mode — all
three were tried side by side. The keys are read from the file, or from environment variables of the
same name, but the file has to exist either way:

```properties
CB_SERVER_NAME=MySQL Megasamples
CB_SERVER_URL=http://127.0.0.1:8084
CB_ADMIN_NAME=cbadmin
CB_ADMIN_PASSWORD=Megasamples1
```

The password should satisfy the server's own policy (`conf/cloudbeaver.conf`: 8 characters, mixed
case, one digit).

## 2. The connection: `conf/initial-data-sources.conf`

The image's `run-server.sh` copies `conf/initial-data-sources.conf` to
`workspace/GlobalConfiguration/.dbeaver/data-sources.json`, but only while `workspace/.metadata` does
not exist — that is, on a container's first start. Inline `user`/`password` with
`"save-password": true` work, and give `authNeeded: false`.

## 3. The grant: `grantConnectionsAccessToAnonymousTeam`

This is the step that looks like a bug. With 1 and 2 in place the wizard is gone and the connection
is loaded — an administrator session lists it — yet an anonymous visitor sees an **empty sidebar**,
because a global connection is granted to no subject by default. The anonymous user is in the team
`user` (`conf/initial-data.conf`), which holds no grants.

Set `CLOUDBEAVER_APP_GRANT_CONNECTIONS_ACCESS_TO_ANONYMOUS_TEAM=true` and the connection appears.
Equivalently, an administrator can call `addConnectionsAccess(projectId:"g_GlobalConfiguration",
connectionIds:["…"], subjects:["user"])` once, but the environment variable needs no post-start step.
`CLOUDBEAVER_APP_READ_ONLY_CONNECTION_INFO=true` additionally stops the host, port and database being
masked as `********` for non-administrators.

## Two accounts, and the caching_sha2 trap

`connections` may hold more than one entry; the shipped seed has two, one per database account, and
both appear to an anonymous visitor once the grant above is in place. Passwords can come from the
environment — `"password": "${DEMO_PASSWORD:demo}"` — but only with
`CLOUDBEAVER_SYSTEM_VARIABLES_RESOLVING_ENABLED=true`. Without the flag the literal `${DEMO_PASSWORD}`
is sent as the password and the connection fails; both ways were measured.

A connection can list correctly and still refuse to open:

```
Error connecting to database:
Public Key Retrieval is not allowed
```

That is **not** a wrong password. It is MySQL's `caching_sha2_password` full-authentication path: on
a cold server credential cache the JDBC driver must fetch the server's RSA public key, and refuses to
do so over an unencrypted connection. Add it to the seeded connection:

```json
"properties": { "allowPublicKeyRetrieval": "true", "useSSL": "false" }
```

An account that connects constantly — the one in the container healthcheck, say — keeps its cache
warm and hides this, so test with `FLUSH PRIVILEGES` first, which clears the cache. DbGate's `mysql2`
and phpMyAdmin's `mysqli` negotiate the cold path themselves and need nothing.

## Checking it from the command line

Two traps make manual probing misleading:

* **CloudBeaver puts many mutating operations under `Query`.** `configureServer`, `authLogin` and
  `addConnectionsAccess` are `Query` fields; calling `configureServer` as a mutation returns
  `Validation error (FieldUndefined@[configureServer])`, which reads exactly like a missing feature
  and is not one.
* **Local passwords are sent pre-hashed.** `org.jkiss.utils.SecurityUtils.makeDigest` is **MD5, hex,
  upper-cased** (`ECRYPTION_ALGORYTHM = "MD5"`). A raw password over the API always fails with
  `Invalid user credentials`; the browser hashes before sending, so a human still types the plain
  one. Repeated attempts trip brute-force protection (`Too frequent authentication requests`).

```bash
J=$(mktemp)
curl -s -c $J -X POST http://127.0.0.1:8084/api/gql -H 'Content-Type: application/json' \
  -d '{"query":"mutation{openSession{valid}}"}' >/dev/null
curl -s -b $J -X POST http://127.0.0.1:8084/api/gql -H 'Content-Type: application/json' \
  -d '{"query":"{serverConfig{configurationMode} userConnections{id name}}"}'
```

`configurationMode: false` plus a non-empty `userConnections` is the pair worth asserting;
`tests/console_test.py` asserts exactly that, because HTTP 200 does not distinguish a working console
from a wizard.
