---
type: Source
title: phpMyAdmin official Docker image — connection environment variables and tags
description: PMA_HOST/PMA_PORT/PMA_USER/PMA_PASSWORD configure the server and the `config` auth method (no login form); the apache variant listens on port 80; 5.2.3-apache is the current pinnable tag.
resource: https://hub.docker.com/_/phpmyadmin
tags:
- console
- docker
- phpmyadmin
status: stable
trust: verified
generated:
  by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
sources:
- resource: https://hub.docker.com/_/phpmyadmin
  title: phpMyAdmin official image README
  accessed: "2026-09-03"
- resource: https://hub.docker.com/v2/repositories/library/phpmyadmin/tags?page_size=8&ordering=last_updated
  title: tag listing (API probe)
  accessed: "2026-09-03"
---

# What was read
The official image README on Docker Hub, and the repository's tag listing through the registry API, 2026-09-03.

# Relevant excerpt
* `PMA_HOST` — "define address/host name of the MySQL server"; `PMA_PORT` — "define port of the MySQL server".
* `PMA_USER` / `PMA_PASSWORD` — "define username/password to use **only with the `config` authentication method**", which is what removes the login form.
* `PMA_ARBITRARY` — "when set to 1 connection to the arbitrary server will be allowed".
* `PMA_ABSOLUTE_URI` — "the full URL to phpMyAdmin. Sometimes needed when used in a reverse-proxy configuration".
* Also `PMA_HOSTS`, `PMA_VERBOSE(S)`, `PMA_PORTS`, `PMA_SOCKET(S)`, `PMA_SSL`.
* The **apache** variant listens on **port 80** (`APACHE_PORT` changes it).
* Tags on 2026-09-03: `latest`, `fpm`, `apache`, `5.2.3-fpm`, `5.2.3-apache`, `5.2.3`, `5.2-fpm`, `5.2-apache`.

# What it was used to decide
That phpMyAdmin can be fully preconfigured — server *and* credentials — so the console opens straight
into the data with no login step. `5.2.3-apache` is the tag the console stack pins
([decision](/decisions/browsing-console-stack.md)).
