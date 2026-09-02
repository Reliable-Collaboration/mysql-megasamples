---
type: Tool
title: Oracle Database Free container (container-registry.oracle.com/database/free, alternative gvenzl/oracle-free)
description: The only way to execute Oracle-specific install scripts (OE/PM object types, XMLType, SQLcl LOAD) during the build; sizes, licensing, arm64 support, login requirement, and connection details verified for an optional build-oracle Compose profile.
resource: https://container-registry.oracle.com/database/free
tags: [oracle, docker, build-stage, oracle-database-free, oracle-group]
status: stable
trust: verified
stale_after: "2026-12-01"
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: /sources/oracle-container-registry-database-free-api-probe.md
    title: Registry API probe (anonymous token, tags, sizes)
    accessed: "2026-09-02"
  - resource: /sources/oracle-database-free-faq-and-get-started.md
    title: Oracle Database Free FAQ / get-started / licensing manual
    accessed: "2026-09-02"
  - resource: /sources/oracle-free-use-terms-and-conditions.md
    title: Oracle Free Use Terms and Conditions
    accessed: "2026-09-02"
  - resource: /sources/github-oracle-docker-images-singleinstance-readme.md
    title: oracle/docker-images SingleInstance README
    accessed: "2026-09-02"
  - resource: /sources/github-gvenzl-oci-oracle-free-readme.md
    title: gvenzl/oci-oracle-free README + Docker Hub sizes
    accessed: "2026-09-02"
---

# Facts (verified 2026-09-02)
* **Image and version.** `container-registry.oracle.com/database/free:latest` = Oracle AI Database 26ai Free 23.26.3.0 (also tagged `23.26.3.0`, `-amd64`, `-arm64`, `-lite`). Multi-arch index: `linux/amd64` and `linux/arm64`. Compressed size **3.7 GB** (amd64, 29 layers), 3.5 GB (arm64); `latest-lite` **0.9 GB** (7 layers, amd64). RPM equivalents on oracle.com: 1.54 GB x86-64, 1.36 GB aarch64.
* **Login.** The registry issued an anonymous pull token for `repository:database/free:pull` and served the tag list and manifests with it, so `docker pull` needs **no `docker login`** (probe recorded in the source). The FAQ confirms: "an Oracle Linux-based Docker image can be pulled via docker pull container-registry.oracle.com/database/free".
* **License.** Oracle Free Use Terms and Conditions (9 June 2021): internal use "for the purposes of developing, testing, prototyping and demonstrating your applications" is granted; redistribution of the unmodified program is allowed with a copy of the license. Using it in a build/verification stage is squarely internal use; the mysql-megasamples image never contains Oracle binaries. Product limits (FAQ): "2 CPUs for foreground processes; 2GB of RAM (SGA and PGA combined); 12GB of user data on disk" — far above our ≈100 MB of sample data. "Not supported and does not receive any patches".
* **Fixed names.** SID `FREE`, PDB `FREEPDB1` ("cannot be changed"); port 1521; env `ORACLE_PWD` (SYS/SYSTEM/PDBADMIN password), `ORACLE_CHARACTERSET` default `AL32UTF8`, `AUTO_MEM_CALCULATION` (honours `docker run --memory`); connect `sql sys@localhost:1521/FREEPDB1 as sysdba`. Init scripts: official image runs `/opt/oracle/scripts/setup` (**Inferred** from the docker-images repo layout; verify), gvenzl image runs `/container-entrypoint-initdb.d`.
* **Cheaper alternative.** `gvenzl/oracle-free:23.26.3` (Docker Hub) 1.19 GB amd64 / 1.00 GB arm64 compressed; `-slim` 0.85/0.71 GB; multi-arch since 23.5; env `ORACLE_PASSWORD`, `APP_USER`, `APP_USER_PASSWORD`; scripts Apache-2.0, binaries still under the Oracle Free Use Terms (**inferred**).
* **SQLcl is not inside the image** (FAQ). The SH installer needs SQLcl's `LOAD` command; to run `sh_install.sql` unchanged one must add SQLcl (≈121 MB zip, OTN license — see [SQLcl/python-oracledb record](/tools/sqlcl-and-python-oracledb.md)) and a JDK to the build container.

# Verified behaviour relevant to this project
* Every v23.3 install script drops and recreates its user, needs a privileged connection, prompts for password and tablespace (`SYSTEM`/`USERS` on Free), and prints a row-count verification table at the end ([HR](/sources/github-oracle-samples-db-sample-schemas-hr-scripts.md), [CO](/sources/github-oracle-samples-db-sample-schemas-co-scripts.md), [SH](/sources/github-oracle-samples-db-sample-schemas-sh-scripts.md)). Archived OE/PM use the old positional `oe_main.sql`/`pm_main.sql` drivers, need the HR and SYS passwords, a `perl` path substitution, `sqlldr` for PM, and XML DB privileges — they were written for "19c and lower" and are **not guaranteed to run on 26ai Free** (open question in the [OE record](/datasets/oracle-oe-pm-ix.md)).

# Cost model (inferred)
Pull 3.7 GB (or 1.2 GB gvenzl) + ≈2–5 min first start (database creation) + SQLcl/JDK ≈ 400 MB; RAM cap 2 GB. Acceptable for an opt-in `build-oracle` verification profile, not for the default build. See [conversion path decision](/decisions/oracle-conversion-path.md).

# Limits
* Oracle Free Use Terms cap the database at 2 CPUs, 2 GB RAM and 12 GB of user data; the image is 3.7 GB compressed (`-lite` 0.9 GB).
* Used only by the opt-in `make verify-oracle` cross-check; the archived OE/PM installers target 19c and may not run on 26ai ([question](/questions/oracle-oe-xml-purchase-orders-scope.md)).
