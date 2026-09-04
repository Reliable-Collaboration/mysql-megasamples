---
type: Source
title: Adminer official Docker image — configuration environment variables and tags
description: ADMINER_DEFAULT_SERVER presets the server; the README documents no variable for credentials, so the login form remains. The standalone variant listens on 8080; 6.0.1-standalone is the current pinnable tag.
resource: https://hub.docker.com/_/adminer
tags:
- console
- docker
- adminer
status: stable
trust: verified
generated:
  by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
sources:
- resource: https://hub.docker.com/_/adminer
  title: Adminer official image README
  accessed: "2026-09-03"
- resource: https://hub.docker.com/v2/repositories/library/adminer/tags?page_size=8&ordering=last_updated
  title: tag listing (API probe)
  accessed: "2026-09-03"
---

# What was read
The official image README on Docker Hub, and the repository's tag listing through the registry API, 2026-09-03.

# Relevant excerpt
* `ADMINER_DEFAULT_SERVER` — "useful if you are connecting to an external server or a docker container named something other than the default `db`".
* `ADMINER_PLUGINS` — "a list of filenames" of the bundled official plugins to load.
* `ADMINER_DESIGN` — the name of one of the bundled designs.
* The README documents **no** `ADMINER_DEFAULT_DRIVER`, `ADMINER_DEFAULT_DB`, or any credential variable.
* The **standalone** variant listens on **port 8080**.
* Tags on 2026-09-03: `fastcgi`, `6.0.1-fastcgi`, `6-fastcgi`, `5.5.1-fastcgi`, `5-fastcgi`, `standalone`, `latest`, `6.0.1-standalone`.

# What it was used to decide
That Adminer is the one console of the four that **cannot** be fully preconfigured from the image: the
server can be preset but the login form still asks for a username and password. The landing page
therefore shows the `demo` credentials next to the Adminer link rather than pretending the click leads
straight in ([decision](/decisions/browsing-console-stack.md)).
