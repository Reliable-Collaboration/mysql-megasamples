# Runbooks

## Concepts
* [Executor discipline](executor-discipline.md) - Non-negotiable working rules for the agent or engineer executing PLAN.md; privilege handling, knowledge-bundle upkeep, deviation handling, and verification-first.
* [IPv6 hangs and privileged changes: diagnose, then stop and ask](ipv6-and-privileges.md) - Checklist for the classic symptom (docker pull or curl hangs on a host with AAAA records but no IPv6 route), the diagnostics that need no privileges, the fixes that do (daemon.json ipv6=false, gai.conf precedence, sysctl disable_ipv6), and the request-to-user template; on this WSL2 + Docker Desktop machine the daemon file lives on the Windows side and needs a Desktop restart.
* [Knowledge bundle conventions](knowledge-bundle-conventions.md) - How every record in this OKF v0.2 bundle is written, typed, trusted, indexed, and logged; the executor follows these rules verbatim.
