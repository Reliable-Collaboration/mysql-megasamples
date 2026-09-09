---
type: Source
title: "docker-library/postgres versions.json"
description: "The version table the official PostgreSQL image is built from, read on 2026-09-09."
resource: https://raw.githubusercontent.com/docker-library/postgres/master/versions.json
tags:
- source
- postgresql
- docker
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:16:50Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:16:50Z"
sources:
- resource: https://raw.githubusercontent.com/docker-library/postgres/master/versions.json
  title: "docker-library/postgres versions.json"
  accessed: "2026-09-09"
---

# What was read
The whole file (`curl -4`), which lists every major the official image publishes with its exact version and variants.

# Relevant excerpt
`19`: version `19beta3`; `18`: version `18.6`; `17`: `17.11`; `16`: `16.15`; `15`: `15.19`; `14`: `14.24`. Variants for each: `trixie`, `bookworm`, `alpine3.24`, `alpine3.23`.

# What it was used to decide
[Target PostgreSQL version](/decisions/target-postgres-version.md): 18.6 is the newest stable major; 19 is a beta.
