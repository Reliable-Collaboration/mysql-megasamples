---
type: Decision
title: A browsing console — a landing page linking four preconfigured database UIs, run by Compose
description: Ship phpMyAdmin, Adminer, DbGate and CloudBeaver alongside the image as an opt-in Compose profile, fronted by a static landing page generated from the megasamples registry, bound to loopback and connected as the read-only demo user.
resource: /decisions/browsing-console-stack.md
tags:
- console
- docker
- compose
- ui
- pending
status: draft
trust: open
generated:
  by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
sources:
- resource: /sources/docker-hub-phpmyadmin-image.md
  title: phpMyAdmin image environment variables
  accessed: "2026-09-03"
- resource: /sources/docker-hub-adminer-image.md
  title: Adminer image environment variables
  accessed: "2026-09-03"
- resource: /sources/dbgate-docker-configuration.md
  title: DbGate connection environment variables
  accessed: "2026-09-03"
- resource: /sources/cloudbeaver-connection-preconfiguration.md
  title: CloudBeaver datasource preconfiguration
  accessed: "2026-09-03"
- resource: /decisions/database-naming-convention.md
  title: the demo and admin accounts the consoles connect as
  accessed: "2026-09-03"
---

# Question
The image holds 21 databases and nine million rows, and the only way to see any of it is to know
some SQL and have a client. How should the project make the data browsable to someone who has just
run `docker compose up`, without compromising the image itself?

# Options considered
1. **Document the connection string and stop there.** Zero cost, zero risk, and it is what most
   sample-data images do. Rejected as the whole answer: the project's stated purpose is that the data
   be *reachable*, and a connection string is not a way of looking at 249 tables.
2. **Bake a UI into the MySQL image.** Rejected outright. It would put PHP or a Node runtime and a web
   server into an image whose entire design is "`mysql:9.7.2` plus data plus a 20-line wrapper"
   (§2), enlarge the attack surface of the thing users actually run in CI, and couple the database's
   release cadence to a UI's.
3. **One UI beside the image.** Better, but picking a single one is a taste judgement the project
   should not make for its users: phpMyAdmin is what most MySQL tutorials assume, Adminer is a single
   file, DbGate and CloudBeaver are the modern web IDEs. They also fail differently, which is useful.
4. **Four UIs plus a landing page, as a separate opt-in Compose profile.** Chosen.

# Evidence
Read on 2026-09-03, one record per vendor:

| console | preconfigurable? | how | source |
|---|---|---|---|
| phpMyAdmin 5.2.3-apache | **fully** | `PMA_HOST`, `PMA_PORT`, `PMA_USER`, `PMA_PASSWORD` — the last two only take effect with the `config` auth method, which is what removes the login form. Serves on port 80 | [record](/sources/docker-hub-phpmyadmin-image.md) |
| Adminer 6.0.1-standalone | **server only** | `ADMINER_DEFAULT_SERVER`; the README documents no credential variable, so the login form stays. Serves on port 8080 | [record](/sources/docker-hub-adminer-image.md) |
| DbGate 7.2.6-alpine | **fully** | `CONNECTIONS` plus `LABEL_`/`SERVER_`/`USER_`/`PASSWORD_`/`PORT_`/`ENGINE_` suffixed with a connection id, taken from the project's own compose file. Serves on 3000, state in `/root/.dbgate` | [record](/sources/dbgate-docker-configuration.md) |
| CloudBeaver 26.2.0 | **unknown** | a `data-sources.json` under `/opt/cloudbeaver/conf/`; the wiki does not say how the first administrator is created or whether the wizard can be skipped | [record](/sources/cloudbeaver-connection-preconfiguration.md) |

All four images exist with pinnable version tags, checked through the registry API on the same day.

# Outcome
**Option 4.** A `console` Compose profile, off by default, that starts the image plus four UIs and a
tiny static landing page. Specified in PLAN.md §12; built by task C-01.

Decisions inside that:

* **Opt-in, never default.** `docker compose up` starts the database only. The consoles need
  `--profile console`. Nothing about the published image changes, and the image keeps its current
  contents exactly.
* **Loopback only.** Every published port binds `127.0.0.1:<port>`, so a laptop on a café network does
  not expose an unauthenticated database UI. Overriding that is the user's deliberate act.
* **They connect as `demo`, the read-only account**, not as root. Someone exploring cannot damage the
  data, and the consoles demonstrate the read-only grant working. A commented-out admin block is
  provided for those who want to write.
* **Pinned image tags**, like every other artifact here: `phpmyadmin:5.2.3-apache`,
  `adminer:6.0.1-standalone`, `dbgate/dbgate:7.2.6-alpine`, `dbeaver/cloudbeaver:26.2.0`, and a pinned
  `nginx` for the landing page. `latest` is not used anywhere in this project and is not used here.
* **The landing page is generated, not written.** It is built from the `megasamples.datasets`
  registry — the same table the image test asserts against — so it lists the databases that are
  actually present, with their row counts and their upstream licence, and cannot drift from the image.
* **Honesty about what "preconfigured" means per tool.** phpMyAdmin and DbGate take both server and
  credentials from environment and open straight into the data. Adminer's image documents no
  credential variable, so its login form remains and the landing page shows the credentials beside the
  link. CloudBeaver needs a mounted `data-sources.json`, and whether it can start unattended at all is
  the open question below. **A console that cannot be brought up unattended will be dropped rather
  than shipped with a manual setup step** — the value here is that the link works.

# Consequences
* A second Compose profile and five more pinned images to keep current; the tags are checked at
  release time with the rest of the manifest.
* The landing-page generator needs the registry, so the console profile is only meaningful against a
  built image — it is not part of `make core-fast`.
* CI runs the profile up, curls each of the five endpoints for a 200, and tears it down. That is the
  whole test: it catches an image tag that has gone away or a UI that no longer starts, which is what
  actually breaks over time.

# Status
pending — recorded 2026-09-03 at the user's request; executed by task C-01.
