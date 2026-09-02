---
type: Source
title: gvenzl/oci-oracle-free README and Docker Hub tag sizes (gvenzl/oracle-free)
description: Community-maintained slimmed Oracle Database Free images with init-script support; tag families, multi-arch support from 23.5, environment variables, and measured compressed sizes from the Docker Hub API.
resource: https://github.com/gvenzl/oci-oracle-free
tags: [oracle, docker, oracle-database-free, community]
status: stable
trust: verified
stale_after: 2026-12-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/gvenzl/oci-oracle-free/main/README.md
    title: README.md (main, repo pushed 2026-08-30; GitHub license detection Apache-2.0, LICENSE.txt)
    accessed: 2026-09-02
  - resource: https://hub.docker.com/v2/repositories/gvenzl/oracle-free/tags/?page_size=100
    title: Docker Hub tags API (full_size per architecture)
    accessed: 2026-09-02
---

# What was read
The README via gh api and the Docker Hub tags JSON, 2026-09-02.

# Relevant excerpt
* Supported tags: `latest[-faststart]`, `slim[-faststart]`, `full[-faststart]` always; `23.26.3*` supported, `23.26.2*` deprecated, older unsupported. "Starting with Oracle Database 23.5 Free, Oracle provides ARM ports for Oracle Database Free. Multi-platform (multi-arch) images are provided starting with 23.5."
* Flavours: Slim ("smallest possible image size"), Regular, Full ("all functionality"), Faststart ("already expanded and ready-to-go database inside the image").
* Env: `ORACLE_PASSWORD` (SYS/SYSTEM), `APP_USER`/`APP_USER_PASSWORD` (created in `FREEPDB1`), `ORACLE_DATABASE` (extra PDB); scripts in `/container-entrypoint-initdb.d` run once after DB creation, `/container-entrypoint-startdb.d` on every start; `sqlplus test/test@//localhost/FREEPDB1` examples; built-in `createAppUser` command.
* Docker Hub compressed sizes (amd64 / arm64): `latest` = `23` = `23.26.3` **1,186 MB / 1,002 MB**; `slim` **848 MB / 714 MB**; `full` 2,252 MB / 2,009 MB; `latest-faststart` 1,661 MB / 1,493 MB.
* Repository scripts are Apache-2.0; **Inferred:** the Oracle binaries inside the images remain under the Oracle Free Use Terms and Conditions.

# What it was used to decide
[Oracle Database Free container tool record](/tools/oracle-database-free-container.md): the gvenzl regular/slim image is the cheaper option (≈1.2 GB vs 3.7 GB) if the Oracle verification profile is ever used.
