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
- accepted
status: stable
trust: verified
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-04T00:00:00Z"
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
| CloudBeaver 25.2.0 | **fully** (measured) | `conf/initial-data-sources.conf` for the connection, `conf/.cloudbeaver.auto.conf` to skip the wizard, and `CLOUDBEAVER_APP_GRANT_CONNECTIONS_ACCESS_TO_ANONYMOUS_TEAM` to make it visible | [runbook](/runbooks/cloudbeaver-unattended-startup.md) |

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

# Built (2026-09-04, task C-01)
All four consoles ship. `docker compose --profile console up -d` starts nginx serving a generated
landing page on 8080, phpMyAdmin on 8081, Adminer on 8082, DbGate on 8083 and CloudBeaver on 8084,
all bound to `127.0.0.1`.

**The `console` profile is gone**, at the user's direction: the database and the consoles are
persistent services that should come up and go down together, so they are one Compose project with
no profile. `docker compose up -d mysql` still starts the database alone, which is what the profile
was really protecting, and nothing is baked into the published image either way. The distinction the
profile was drawing turned out to be the wrong one: the useful split is not console-vs-database but
**persistent-vs-transient**, and the transient containers -- the build server, the WWI export's SQL
Server, the loader, the test servers -- are now labelled `megasamples.transient=true` and removed by
`make clean` rather than lingering for days.

Each console offers **both** accounts and opens on the read-only one: `demo` (`SELECT`, `SHOW VIEW`)
and `admin` (`ALL PRIVILEGES`). phpMyAdmin needs a mounted `config.user.inc.php` for this, because
the image's own config generator applies a single `PMA_USER` to every server it builds; DbGate takes
two `CONNECTIONS`, CloudBeaver two seeded connections, and Adminer's form takes either. Passwords are
boilerplate and committed, overridable in one place through `.env` (`DEMO_PASSWORD`,
`ADMIN_PASSWORD` -- the names the image's entrypoint already applies with `ALTER USER`), which
compose passes to the server and to every console so they cannot drift apart.

CloudBeaver's seeded connections carry `allowPublicKeyRetrieval`: without it the `admin` connection
fails with `Public Key Retrieval is not allowed` on a cold server credential cache, which is MySQL's
`caching_sha2_password` full-auth path rather than a bad password. `demo` masked the problem because
the healthcheck keeps its cache warm.

CloudBeaver was briefly dropped on this decision's own unattended-startup rule, and that was
withdrawn the same day: it *does* start unattended, through a route its wiki does not mention. A
`java.util.Properties` file at exactly `conf/.cloudbeaver.auto.conf` is what makes the server
configure itself rather than show its wizard — its presence is the trigger, and environment variables
alone never are. The connection comes from `conf/initial-data-sources.conf`, and
`CLOUDBEAVER_APP_GRANT_CONNECTIONS_ACCESS_TO_ANONYMOUS_TEAM=true` is what makes it visible to a
visitor, since a global connection is granted to nobody by default. The mechanism, and the two API
traps that hid it, are in [the runbook](/runbooks/cloudbeaver-unattended-startup.md).

The landing page is generated by `scripts/console_page.py` from `megasamples.datasets` inside the
running image, so it lists the 21 databases actually present with their real table counts, row counts
and sizes -- 248 tables and 9,056,697 rows -- and cannot drift. `tests/console_test.py` is S10: five
endpoints answering 200, every registry name present on the page, the credentials on it because
Adminer's login form is not preset, and CloudBeaver asserted to be out of configuration mode and
showing the connection to an anonymous session -- it answers 200 while showing its wizard, so the
status code alone would not catch a regression.

Images are pinned by digest rather than tag, which is good practice and, on this machine, also the
only thing that works: the daemon cannot fetch blobs from Docker Hub's CDN, so `scripts/pull_image.py`
fetches them over IPv4 and compose refers to the digests it reports.

# Status
accepted. All four consoles ship. CloudBeaver meets the unattended-startup condition this decision set for it, once the undocumented `conf/.cloudbeaver.auto.conf` trigger and the anonymous-team grant are both in place ([runbook](/runbooks/cloudbeaver-unattended-startup.md)). The [preconfiguration question](/questions/console-preconfiguration-limits.md) is answered.
