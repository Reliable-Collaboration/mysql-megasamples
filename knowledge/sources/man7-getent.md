---
type: Source
title: getent(1) Linux manual page
description: getent ahosts/ahostsv4/ahostsv6 call getaddrinfo with AF_UNSPEC/AF_INET/AF_INET6 and list every address.
resource: https://man7.org/linux/man-pages/man1/getent.1.html
tags:
- ipv6
- glibc
- dns
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
sources:
- resource: https://man7.org/linux/man-pages/man1/getent.1.html
  title: getent(1) Linux manual page
  accessed: "2026-09-02"
---

# What was read
https://man7.org/linux/man-pages/man1/getent.1.html, accessed 2026-09-02.

# Relevant excerpt
* Synopsis `getent [option ...] database key ...`.
* `ahosts`: "pass each key in succession to getaddrinfo(3) with the address family AF_UNSPEC, enumerating each socket address structure returned." `ahostsv4`: "Same as ahosts, but use the address family AF_INET." `ahostsv6`: "Same as ahosts, but use the address family AF_INET6. The call to getaddrinfo(3) in this case includes the AI_V4MAPPED flag."

# What it was used to decide
[IPv6 runbook](/runbooks/ipv6-and-privileges.md): `getent ahosts <host>` shows whether AAAA answers sort ahead of A answers on this host.
