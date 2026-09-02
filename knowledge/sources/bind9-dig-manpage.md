---
type: Source
title: "BIND 9 manual pages: dig"
description: "dig synopsis, -4/-6, query type argument (default A; AAAA), +short."
resource: https://bind9.readthedocs.io/en/latest/manpages.html
tags: [dns, ipv6, cli]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://bind9.readthedocs.io/en/latest/manpages.html
    title: "BIND 9 manual pages: dig"
    accessed: 2026-09-02
---

# What was read
https://bind9.readthedocs.io/en/latest/manpages.html, accessed 2026-09-02.

# Relevant excerpt
* `dig [@server] [-b address] [-c class] [-f filename] [-k filename] [-m] [-p port#] [-q name] [-t type] [name] [type] [class] [queryopt...]`; `-4` "only IPv4 should be used", `-6` "only IPv6 should be used"; "The default query type is A, unless the -x option is supplied"; `+short` "toggles whether a terse answer is provided".

# What it was used to decide
[IPv6 runbook](/runbooks/ipv6-and-privileges.md): `dig +short AAAA <host>` lists IPv6 answers independent of the resolver's sorting (dig is not installed by default on this host; `getent` is the fallback — **Inferred**).
