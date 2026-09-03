---
type: Source
title: "MySQL 9.7 Reference Manual: Privileges Provided by MySQL"
description: Definitions of SELECT, SHOW VIEW, EXECUTE, PROCESS, SHOW DATABASES, USAGE, ALL and CREATE USER used by the account grants.
resource: https://dev.mysql.com/doc/refman/9.7/en/privileges-provided.html
tags:
- mysql
- docs
- security
- accounts
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:24:01Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:24:01Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/privileges-provided.html
  title: Privileges Provided by MySQL
  accessed: "2026-09-02"
---
# What was read
* https://dev.mysql.com/doc/refman/9.7/en/privileges-provided.html, “Privileges Provided by MySQL”, accessed 2026-09-02

# Relevant excerpt
Summary table: SELECT (tables or columns), SHOW VIEW (views), EXECUTE (stored routines), PROCESS / SHOW DATABASES (server administration), USAGE ("synonym for no privileges"). `ALL [PRIVILEGES]` is "shorthand for all privileges available at a given privilege level (except GRANT OPTION)". CREATE USER "Enables use of the ALTER USER, CREATE ROLE, CREATE USER, DROP ROLE, DROP USER, RENAME USER, and REVOKE ALL PRIVILEGES statements." Dynamic privileges (ROLE_ADMIN, SET_ANY_DEFINER, ...) are granted separately from static ALL.

# What it was used to decide
Grants in [naming and accounts decision](/decisions/database-naming-convention.md): `demo` gets `SELECT, SHOW VIEW ON *.*` plus `EXECUTE` on named read-only routines; `admin` gets `ALL PRIVILEGES ON *.* WITH GRANT OPTION` plus `CREATE USER`, `ROLE_ADMIN`, `SET_ANY_DEFINER` so it can recreate dataset objects with their intended definers.
