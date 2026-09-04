---
type: Runbook
title: "IPv6 hangs and privileged changes: diagnose, then stop and ask"
description: Checklist for the classic symptom (docker pull or curl hangs on a host with AAAA records but no IPv6 route), the diagnostics that need no privileges, the fixes that do (daemon.json ipv6=false, gai.conf precedence, sysctl disable_ipv6), and the request-to-user template; on this WSL2 + Docker Desktop machine the daemon file lives on the Windows side and needs a Desktop restart.
resource: /runbooks/ipv6-and-privileges.md
tags:
- runbook
- ipv6
- docker
- privileges
- troubleshooting
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:51:18Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:51:18Z"
sources:
- resource: https://man7.org/linux/man-pages/man1/getent.1.html
  accessed: "2026-09-02"
- resource: https://bind9.readthedocs.io/en/latest/manpages.html
  accessed: "2026-09-02"
- resource: https://curl.se/docs/manpage.html
  accessed: "2026-09-02"
- resource: https://docs.docker.com/engine/daemon/ipv6/
  accessed: "2026-09-02"
- resource: https://docs.docker.com/engine/daemon/
  accessed: "2026-09-02"
- resource: https://docs.docker.com/desktop/settings-and-maintenance/settings/
  accessed: "2026-09-02"
- resource: https://docs.docker.com/reference/cli/docker/buildx/build/
  accessed: "2026-09-02"
- resource: https://docs.docker.com/reference/cli/docker/network/inspect/
  accessed: "2026-09-02"
- resource: https://man7.org/linux/man-pages/man5/gai.conf.5.html
  accessed: "2026-09-02"
- resource: https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt
  accessed: "2026-09-02"
- resource: https://docs.docker.com/docker-hub/usage/pulls/
  accessed: "2026-09-02"
- resource: /sources/build-machine-environment-2026-09-02.md
  accessed: "2026-09-02"
- resource: /runbooks/executor-discipline.md
  accessed: "2026-09-02"
---

# 0. The rule
Any fix in section 3 needs root, an administrator, or a Docker Desktop restart. The executor **stops and asks** using the template in section 4 ([executor discipline](/runbooks/executor-discipline.md) §1). Section 2 fixes need no privileges and are applied first.

# 1. Diagnose (no privileges)
| Step | Command | What it shows | Source |
|---|---|---|---|
| 1a | `getent ahosts registry-1.docker.io` | every address getaddrinfo returns with AF_UNSPEC, in the order the resolver sorts them; IPv6 (`2600:...`) lines before IPv4 lines mean IPv6 is tried first | [getent](/sources/man7-getent.md) |
| 1b | `getent ahostsv6 <host>` / `getent ahostsv4 <host>` | AF_INET6 (with AI_V4MAPPED) versus AF_INET answers only | same |
| 1c | `dig +short AAAA <host>` (if `dig` exists; not on this host) | raw AAAA records regardless of sorting; `-4` forces the query itself over IPv4 | [dig](/sources/bind9-dig-manpage.md) |
| 1d | `curl -4 -sSI --connect-timeout 5 https://<host>/` then `curl -6 -sSI --connect-timeout 5 https://<host>/` | `-4` "Resolve names to IPv4 addresses only", `-6` IPv6 only; a fast IPv4 answer plus an IPv6 timeout/"no route" is the signature | [curl](/sources/curl-manpage.md) |
| 1e | `cat /proc/net/if_inet6`; `sysctl net.ipv6.conf.all.disable_ipv6` | only `fe80::` link-local addresses = no global IPv6, yet IPv6 enabled (`0` = enabled) | [ip-sysctl](/sources/kernel-ip-sysctl.md) |
| 1f | `docker network inspect bridge --format '{{.EnableIPv6}}'` | whether the default bridge hands IPv6 to containers (**Inferred** field name; falls back to `docker network inspect bridge` and read the JSON) | [network inspect](/sources/docker-docs-network-inspect.md) |
| 1g | `docker pull mysql:9.7.2` hanging at "Pulling fs layer"/no progress for > 60 s while `curl -4` to `registry-1.docker.io` answers in < 1 s | **Inferred** symptom pattern of IPv6-first resolution inside the Docker VM | — |
| 1h | Error text "You have reached your pull rate limit" or HTTP 429 | not IPv6: Docker Hub rate limit; log in or mirror ([GitHub limits](/tools/github-limits.md)) | [hub pulls](/sources/docker-docs-hub-pulls.md) |

Observed on this machine on 2026-09-02: only link-local IPv6, `disable_ipv6=0`, `curl -6` to `registry-1.docker.io` fails (no route), `curl -4` answers in 0.13 s; AAAA records exist for `registry-1.docker.io`, `auth.docker.io`, `production.cloudflare.docker.com`, `mcr.microsoft.com`, `container-registry.oracle.com`, `d37ci6vzurychx.cloudfront.net`, `dumps.wikimedia.org`; none for `github.com`, `objects.githubusercontent.com`, `archive.org` ([environment survey](/sources/build-machine-environment-2026-09-02.md)). Docker pulls go through Docker Desktop's VM network stack, so a host-side fix does not necessarily fix pulls.

# 2. Work around without privileges (allowed, in this order)
1. Per-command IPv4: `curl -4`, `wget --inet4-only` (**Inferred** wget flag; verify with `wget --help`), Python `requests` via `urllib3.util.connection.HAS_IPV6 = False` (**Inferred**).
2. `scripts/fetch.py` passes `curl -4` for manifest entries flagged `ipv4_first` (hosts with AAAA records that hang) and prefers hosts without AAAA (GitHub release assets, archive.org) as mirrors ([mirroring](/tools/internet-archive-mirroring.md)).
3. Build-time: `docker buildx build --network=host --allow network.host` or `--add-host host:ipv4` for a single stubborn host ([buildx build](/sources/docker-docs-buildx-build.md)); `RUN --network=host` per instruction.
4. Registry: pull the base image once via a proxy/mirror that resolves IPv4 (e.g. a ghcr.io copy), or `docker login` to rule out rate limiting.
If the step still fails, go to section 3.

# 2b. What section 2 looks like in practice (2026-09-03, task X-02)
The Docker Desktop change the user applied at P-02 fixed Docker Hub, **not every registry**.
`docker pull mcr.microsoft.com/mssql/server:2022-latest` still fails with a bare
`failed to do request: Head "https://mcr.microsoft.com/v2/mssql/server/manifests/2022-latest": EOF`,
while from the same shell `curl -4` to that exact URL returns 200 in 0.15 s and `curl -6` fails in
20 ms with "Could not connect". Same signature, different registry: this one has AAAA records too, and
the daemon reaches it through the Desktop VM's stack.

`scripts/pull_image.py` is the section-2 workaround made repeatable. It speaks the OCI distribution
API over `curl -4`: resolve the tag, fetch the config and layer blobs, verify each against the digest
the registry named, assemble an OCI archive and `docker load` it. It handles a 401 by fetching an
anonymous token from the realm the challenge names, so it is not MCR-specific.

    python3 scripts/pull_image.py mcr.microsoft.com/mssql/server:2022-latest

It prints `image@sha256:...` for the caller to pin, which is *stricter* than `docker pull` of a
floating tag. It needs no privileges and changes nothing on the host. The daemon-level fix in section 3
is still the right answer for the machine; this is what unblocks a build without asking for it.

# 3. Fixes that need privileges (never applied by the executor)
| Fix | Exact change | Why it needs asking | Source |
|---|---|---|---|
| Docker daemon IPv6 off | Linux: `/etc/docker/daemon.json` → `{ "ipv6": false }` then `sudo systemctl restart docker`. This machine: Docker Desktop's `daemon.json` (`/mnt/c/Users/mattc/.docker/daemon.json`, currently only builder GC) or Settings → Docker Engine, then restart Docker Desktop | daemon restart / Desktop restart interrupts every container and is outside the executor's remit | [IPv6](/sources/docker-docs-daemon-ipv6.md), [daemon](/sources/docker-docs-daemon-config.md), [Desktop settings](/sources/docker-docs-desktop-settings.md), [survey](/sources/build-machine-environment-2026-09-02.md) |
| Docker DNS | `"dns": ["1.1.1.1", "8.8.8.8"]` in the same file (**Inferred** key, listed in daemon docs but not quoted this session) | same | — |
| Prefer IPv4 in glibc | `sudo sh -c 'echo "precedence ::ffff:0:0/96 100" >> /etc/gai.conf'` — raises the RFC 3484 precedence of IPv4-mapped answers above the default `10`; affects host processes only, not the Docker VM | `/etc/gai.conf` is root-owned (**Inferred**, `ls -l` to confirm) | [gai.conf](/sources/man7-gai-conf.md) |
| Disable IPv6 in the WSL kernel | `sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1` (and `default`), persist in `/etc/sysctl.d/`; "Disable IPv6 operation ... Default: FALSE" | sysctl write is root-only; also does not reach the Docker Desktop VM | [ip-sysctl](/sources/kernel-ip-sysctl.md) |
| Docker Desktop network mode | Settings → Resources → Network: an "IPv4 only" mode may exist in current Desktop versions (**Inferred**, not found in the fetched docs) | GUI on the Windows side | — |
| Package installs | `sudo apt-get install make jq zstd bzip2 p7zip-full` for missing host tools | root | [survey](/sources/build-machine-environment-2026-09-02.md) |

# 4. Request-to-user template (copy, fill, send, wait)
```
BLOCKED on a privileged change.
Problem: docker pull mysql:9.7.2 hangs; curl -6 registry-1.docker.io has no route while curl -4 answers in 0.13 s (IPv6-first resolution in the Docker Desktop VM).
Proposed fix (requires admin / Docker Desktop restart):
  1. Edit C:\Users\mattc\.docker\daemon.json (or Docker Desktop → Settings → Docker Engine) and add  "ipv6": false
  2. Apply & restart Docker Desktop.
  Alternative on the WSL side (sudo): echo 'precedence ::ffff:0:0/96 100' | sudo tee -a /etc/gai.conf
Why this and not a workaround: per-command -4 flags do not reach docker pull, which runs inside the Desktop VM.
Resume with: make verify-pull   (re-runs docker manifest inspect + docker pull mysql:9.7.2)
```

# 5. After the user applies a fix
Re-run section 1 (1d and 1g), log a **Verification** entry in `log.md` with the command output, and update the [environment survey](/sources/build-machine-environment-2026-09-02.md) if the IPv6 posture changed.
