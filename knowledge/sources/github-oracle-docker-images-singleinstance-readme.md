---
type: Source
title: oracle/docker-images — OracleDatabase/SingleInstance README
description: Official build scripts for Oracle Database container images, including the 26ai (23.26.1) Free Containerfile; fixed SID/PDB names, environment variables, ARM64 note, and the UPL 1.0 license of the scripts.
resource: https://github.com/oracle/docker-images/blob/main/OracleDatabase/SingleInstance/README.md
tags: [oracle, docker, oracle-database-free]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/oracle/docker-images/main/OracleDatabase/SingleInstance/README.md
    title: SingleInstance README (main)
    accessed: "2026-09-02"
  - resource: https://api.github.com/repos/oracle/docker-images/contents/OracleDatabase/SingleInstance/dockerfiles/23.26.1
    title: dockerfiles/23.26.1 directory listing (Containerfile.free, runOracle.sh, createDB.sh, license.txt ...)
    accessed: "2026-09-02"
---

# What was read
The README (via gh api) and the `dockerfiles/23.26.1` listing, 2026-09-02.

# Relevant excerpt
* "This project offers sample Dockerfiles for: Oracle Database 26ai (23.26.1) Enterprise Edition and Free ..."; `./buildContainerImage.sh -f -v 23.26.1` builds the Free image; "You will have to provide the installation binaries of Oracle Database (except for Oracle Database 18c XE, 21c XE and 26ai Free)" — the Free build downloads the RPM itself.
* "**Linux ARM64 Support:** Oracle Database 19c Enterprise Edition and 26ai Free Edition are now supported on ARM64 platforms."
* "The ORACLE_SID for Oracle Database 26ai Free is always `FREE` and the PDB_NAME is always `FREEPDB1`. They cannot be changed"; connect `sqlplus sys/<pwd>@//localhost:1521/FREE as sysdba`, `sqlplus pdbadmin/<pwd>@//localhost:1521/FREEPDB1`; env `ORACLE_PWD`, `ORACLE_CHARACTERSET` (default AL32UTF8), `INIT_SGA_SIZE`, `INIT_PGA_SIZE`, `INIT_CPU_COUNT`, `AUTO_MEM_CALCULATION` ("can be constrained using the `docker run --memory` option. If set to 'false', the total memory will be set as 2GB (default: true)"); podman secrets `oracle_pwd`.
* License: "To download and run Oracle Database, regardless whether inside or outside a container, you must download the binaries from the Oracle website and accept the license indicated at that page. All scripts and files hosted in this project ... are, unless otherwise noted, released under UPL 1.0 license."

# What it was used to decide
[Oracle Database Free container tool record](/tools/oracle-database-free-container.md) (connection strings and env vars for the `build-oracle` Compose profile).
