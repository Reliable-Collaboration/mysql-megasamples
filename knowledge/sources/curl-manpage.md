---
type: Source
title: "curl manual page: -4/-6, -I, -s/-S, --connect-timeout, -L, --retry"
description: "Option semantics used by the IPv6 diagnostics."
resource: https://curl.se/docs/manpage.html
tags: [curl, ipv6, cli]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://curl.se/docs/manpage.html
    title: "curl manual page: -4/-6, -I, -s/-S, --connect-timeout, -L, --retry"
    accessed: "2026-09-02"
---

# What was read
https://curl.se/docs/manpage.html, accessed 2026-09-02.

# Relevant excerpt
* `-4, --ipv4`: "Resolve names to IPv4 addresses only." `-6, --ipv6`: "Resolve names to IPv6 addresses only." `-I, --head`: fetch headers only. `-s, --silent` / `-S, --show-error`: silent but show errors. `--connect-timeout`: maximum time for the connection phase. `-L, --location`: follow redirects. `--retry`: retry on transient errors.

# What it was used to decide
[IPv6 runbook](/runbooks/ipv6-and-privileges.md): `curl -4 -sSI --connect-timeout 5 <url>` versus `curl -6 ...` isolates address-family failures.
