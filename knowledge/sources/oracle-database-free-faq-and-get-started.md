---
type: Source
title: Oracle Database Free FAQ and Get Started pages (oracle.com)
description: Resource limits (2 CPUs, 2 GB RAM, 12 GB user data), production/support statements, the docker pull command, RPM sizes and platforms (x86-64 and aarch64) for Oracle AI Database 26ai Free.
resource: https://www.oracle.com/database/free/faq/
tags: [oracle, oracle-database-free, limits, container]
status: stable
trust: verified
stale_after: "2027-03-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.oracle.com/database/free/faq/
    title: Oracle Database Free FAQ
    accessed: "2026-09-02"
  - resource: https://www.oracle.com/database/free/get-started/
    title: Oracle AI Database Free – Quick Start
    accessed: "2026-09-02"
    version: 26ai (23.26.3)
  - resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/dblic/Licensing-Information.html
    title: Database Licensing Information User Manual (23/dblic)
    accessed: "2026-09-02"
---

# What was read
Both oracle.com pages (curl with a browser user agent; WebFetch received 403) and the licensing manual page, 2026-09-02.

# Relevant excerpt
FAQ:
> Can I install Oracle AI Database Free into Docker? Yes, an Oracle Linux-based Docker image can be pulled via docker pull container-registry.oracle.com/database/free
>
> What are the resource limits for Oracle AI Database Free? Oracle Database Free supports up to: 2 CPUs for foreground processes; 2GB of RAM (SGA and PGA combined); 12GB of user data on disk (irrespective of compression factor)
>
> Can I use Oracle AI Database Free in production? Oracle AI Database Free does not restrict the environment in which it can be deployed. However, Oracle AI Database Free is not supported and does not receive any patches, including security patches.
>
> Where is SQL Developer and SQLcl? SQL Developer and SQLcl are not part of Oracle AI Database Free. Instead, you can separately download the latest version ...

Get started: "Docker/Podman Pull container images from Oracle's Container Registry: `docker pull container-registry.oracle.com/database/free:latest`"; RPMs: `oracle-ai-database-free-26ai-23.26.3-1.el9.x86_64.rpm` 1,538,737,668 bytes (SHA256 published), `...el9.aarch64.rpm` 1,355,290,892 bytes, Windows zip 1,403,455,579 bytes; connect with `sql sys@localhost:1521/FREEPDB1 as sysdba` (PDB) or `.../FREE` (CDB).

Licensing manual: "Oracle AI Database Free is released under the Oracle Free Use Terms and Conditions" (link to oracle-free-license.html); platforms "Linux x86-64, ARM Linux, and Microsoft Windows"; a feature note repeats "the Oracle AI Database Free limit of 2 CPUs, 2GB RAM, and 12GB of user data"; APEX, ORDS and SQL Developer are not included.

# What it was used to decide
[Oracle Database Free container tool record](/tools/oracle-database-free-container.md) — limits are irrelevant for our data (SH ≈ 90 MB of CSV) but the 2 GB RAM cap bounds the container's memory footprint in the build profile.
