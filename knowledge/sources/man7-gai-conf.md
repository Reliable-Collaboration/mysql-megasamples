---
type: Source
title: "gai.conf(5) Linux manual page"
description: "getaddrinfo address sorting per RFC 3484 is tunable in /etc/gai.conf with label/precedence lines."
resource: https://man7.org/linux/man-pages/man5/gai.conf.5.html
tags: [ipv6, glibc, dns]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://man7.org/linux/man-pages/man5/gai.conf.5.html
    title: "gai.conf(5) Linux manual page"
    accessed: "2026-09-02"
---

# What was read
https://man7.org/linux/man-pages/man5/gai.conf.5.html, accessed 2026-09-02.

# Relevant excerpt
> "A call to getaddrinfo(3) might return multiple answers. According to RFC 3484 these answers must be sorted so that the answer with the highest success rate is first in the list."
* `precedence`: "This keyword is similar to label, but instead the value is added to the precedence table as specified in RFC 3484."; the default table includes `precedence ::ffff:0:0/96 10`; raising that value (e.g. `precedence ::ffff:0:0/96 100`) sorts IPv4-mapped answers first. `reload` controls re-reading; supported since glibc 2.5.

# What it was used to decide
[IPv6 runbook](/runbooks/ipv6-and-privileges.md): the host-side "prefer IPv4" fix and why it needs root (`/etc/gai.conf` is root-owned — **Inferred**, verify with `ls -l`).
