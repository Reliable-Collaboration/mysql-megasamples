---
type: Source
title: Build machine environment survey, 2026-09-02
description: Read-only observations of the machine that will execute the plan; Docker Desktop on WSL2, tool inventory, IPv6 posture, registry reachability, and which mysql tags exist.
resource: file:///home/mattc/wsldev/mysql-megasamples
tags: [environment, docker, ipv6, wsl2]
status: stable
trust: verified
stale_after: 2026-10-02
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:17:31Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:17:31Z" }
sources:
  - resource: "shell: docker info; docker --version; id -nG; cat /proc/net/if_inet6; getent ahosts*; curl -4/-6; docker manifest inspect; df; free; nproc"
    title: Commands run on the build machine
    accessed: 2026-09-02
---

# What was observed (commands run 2026-09-02, no state changed)

| Item | Value |
|---|---|
| Kernel | 6.18.33.2-microsoft-standard-WSL2, systemd enabled in `/etc/wsl.conf` |
| Docker | Docker Desktop, engine 29.6.2, overlayfs, cgroup v2, Compose v5.3.1, buildx v0.35.0 |
| Resources visible to Docker | 32 CPUs, 15.48 GiB memory, root disk 1007 GB with 932 GB free (`/dev/sdf`) |
| User | member of `docker` and `sudo` groups (no privilege change needed to run Docker) |
| IPv6 | only link-local `fe80::` on eth0 inside WSL; `disable_ipv6=0`; `curl -6` to registry-1.docker.io fails (no route); `curl -4` returns 401 in 0.13 s (expected for /v2/) |
| DNS | resolver 10.255.255.254 (WSL/Docker Desktop stub); no `precedence` lines in `/etc/gai.conf`; no `/etc/docker/daemon.json` in WSL — the engine config lives at `/mnt/c/Users/mattc/.docker/daemon.json` and Docker Desktop settings at `/mnt/c/Users/mattc/AppData/Roaming/Docker/settings-store.json` |
| Hosts with AAAA records | registry-1.docker.io, auth.docker.io, production.cloudflare.docker.com, mcr.microsoft.com, container-registry.oracle.com, d37ci6vzurychx.cloudfront.net (NYC TLC), dumps.wikimedia.org |
| Hosts without AAAA | github.com, objects.githubusercontent.com, archive.org |
| `docker manifest inspect` | `mysql:9.7.2`, `mysql:9.7`, `mysql:lts` exist; `mysql:9.7.3` and `mysql:8.4.12` do not exist yet (rc=1 immediately, not a timeout) |
| Docker Desktop config | `/mnt/c/Users/mattc/.docker/daemon.json` contains only builder GC (`defaultKeepStorage: 20GB`), no `ipv6` key; `settings-store.json` shows `UseContainerdSnapshotter: true`, `HostNetworkingEnabled: true`, WSL integration with distro `Ubuntu`, proxy mode `system` |
| Host tools present | python3 3.14.4, uv 0.12.6, curl 8.18.0, wget 1.25.0, xz 5.8.3, gh 2.46.0, git |
| Host tools missing | make, jq, zstd, bzip2, 7z, aria2c, mysql client, mysqlsh, duckdb, git-lfs, pip3 |

# Consequences
* Docker Desktop engine settings are edited in the Docker Desktop GUI (Settings → Docker Engine) or the user-writable `daemon.json` above, and require a Docker Desktop restart on Windows; the executing agent cannot restart Docker Desktop, so any such change is handed to the user under the privilege rule even though the file itself is writable.
* IPv6 exposure is inside the Docker Desktop VM, not the WSL distro: Docker pulls go through Docker Desktop's own network stack, so host-side `curl -4` success does not prove `docker pull` will succeed. See [IPv6 and privileges runbook](/runbooks/ipv6-and-privileges.md).
* Missing host packages (`make jq zstd bzip2 p7zip-full`) need `sudo apt-get install`; per project rule the executor asks the user rather than working around it. Everything else runs inside containers.
* Python tooling can be provisioned per-project with `uv` without privileges (normal usage, not a workaround).
* The pin is `mysql:9.7.2` until 9.7.3 is published ([decision](/decisions/target-mysql-version.md)).
