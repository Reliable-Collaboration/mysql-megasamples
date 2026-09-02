---
type: Source
title: "MySQL 9.7 Reference Manual: Stored Object Access Control"
description: DEFINER versus INVOKER security context for routines, views and triggers; determines how the read-only demo user is kept read-only.
resource: https://dev.mysql.com/doc/refman/9.7/en/stored-objects-security.html
tags: [mysql, docs, security, accounts]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:24:01Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:24:01Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/stored-objects-security.html
    title: Stored Object Access Control
    accessed: "2026-09-02"
---
# What was read
* https://dev.mysql.com/doc/refman/9.7/en/stored-objects-security.html, “Stored Object Access Control”, accessed 2026-09-02

# Relevant excerpt
> "A stored object that executes in definer security context executes with the privileges of the account named by its DEFINER attribute... during object execution, the invoker's privileges are ignored and only the DEFINER account privileges matter."
> "If the definition omits the SQL SECURITY characteristic, the default is definer context."
> "A stored routine or view that executes in invoker security context can perform only operations for which the invoker has privileges."
> "Triggers and events have no SQL SECURITY characteristic and always execute in definer context."
> "If you have the SET_ANY_DEFINER privilege, you can specify any account as the DEFINER attribute... Otherwise, the only permitted account is your own."

# What it was used to decide
[Naming and accounts decision](/decisions/database-naming-convention.md): every ported routine and view that must be callable by `demo` is created with `SQL SECURITY INVOKER`; routines that write (Sakila `rewards_report`, DVD Store `purchase`/`new_customer`, Oracle HR `add_job_history`, AdventureWorks `uspUpdateEmployee*`) keep DEFINER context with `admin` as definer and are not granted to `demo`. Triggers fire only on writes that `demo` cannot issue.
