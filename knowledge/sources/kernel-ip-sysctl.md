---
type: Source
title: "Linux kernel documentation: ip-sysctl (disable_ipv6)"
description: net.ipv6.conf.*.disable_ipv6 default FALSE; TRUE disables IPv6 operation on the interface.
resource: https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt
tags:
- ipv6
- kernel
- sysctl
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:37:05Z"
sources:
- resource: https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt
  title: "Linux kernel documentation: ip-sysctl (disable_ipv6)"
  accessed: "2026-09-02"
---

# What was read
https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt, accessed 2026-09-02.

# Relevant excerpt
> disable_ipv6: "Disable IPv6 operation. If accept_dad is set to 2, this value will be dynamically set to TRUE if DAD fails for the link-local address. Default: FALSE (enable IPv6 operation)"

# What it was used to decide
[IPv6 runbook](/runbooks/ipv6-and-privileges.md): `sysctl -w net.ipv6.conf.all.disable_ipv6=1` is the kernel-level switch (root only, and it does not reach into the Docker Desktop VM).
