---
type: Source
title: "Docker Docs: Volumes"
description: "A new volume is populated from the image's directory contents; anonymous volumes persist unless --rm; performance note."
resource: https://docs.docker.com/engine/storage/volumes/
tags: [docker, volumes]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://docs.docker.com/engine/storage/volumes/
    title: "Docker Docs: Volumes"
    accessed: "2026-09-02"
---

# What was read
https://docs.docker.com/engine/storage/volumes/, accessed 2026-09-02.

# Relevant excerpt
> "If you start a container which creates a new volume, and the container has files or directories in the directory to be mounted such as /app/, Docker copies the directory's contents into the volume."
* Anonymous volumes get "a random name that's guaranteed to be unique within a given Docker host"; "Anonymous volumes persist even if you remove the container that uses them, except if you use the --rm flag when creating the container, in which case the anonymous volume associated with the container is destroyed."

# What it was used to decide
[docker multi-stage record](/tools/docker-build-multistage.md): because the base image declares `VOLUME /var/lib/mysql`, every `docker run` of the baked image copies the whole data directory into a fresh anonymous volume (start-up cost and disk use proportional to data size) unless the image moves `datadir` elsewhere — an explicit trade-off in [bake-data decision](/decisions/bake-data-vs-initdb.md).
