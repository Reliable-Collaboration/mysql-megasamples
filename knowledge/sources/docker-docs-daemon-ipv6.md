---
type: Source
title: "Docker Docs: Use IPv6 networking"
description: "IPv6 is Linux-only, enabled per daemon.json (ipv6, fixed-cidr-v6, ip6tables), daemon restart required."
resource: https://docs.docker.com/engine/daemon/ipv6/
tags: [docker, ipv6, daemon]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://docs.docker.com/engine/daemon/ipv6/
    title: "Docker Docs: Use IPv6 networking"
    accessed: 2026-09-02
---

# What was read
https://docs.docker.com/engine/daemon/ipv6/, accessed 2026-09-02.

# Relevant excerpt
> "IPv6 is only supported on Docker daemons running on Linux hosts."
* Enable on the default bridge by editing `/etc/docker/daemon.json`: `{"ipv6": true, "fixed-cidr-v6": "2001:db8:1::/64"}`; `ip6tables` adds IPv6 filter rules (enabled by default).
> "Restart the Docker daemon for your changes to take effect" (`sudo systemctl restart docker`).
* `default-address-pools` can carry IPv6 pools for dynamic subnet allocation; `2001:db8::/64` is documentation-only, use ULA `fd00::/8` subnets.

# What it was used to decide
[docker multi-stage record](/tools/docker-build-multistage.md) and [IPv6 runbook](/runbooks/ipv6-and-privileges.md): the daemon-level switch is `"ipv6": false` (the documented default state), it lives in daemon.json and needs a daemon restart, hence a privileged change on this machine.
