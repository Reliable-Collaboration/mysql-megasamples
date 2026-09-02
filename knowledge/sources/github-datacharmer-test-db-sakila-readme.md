---
type: Source
title: test_db sakila/README.md
description: States that the Sakila copy inside test_db is derived from the MySQL "Sakila-spatial" download with conditional FULLTEXT/GEOMETRY.
resource: https://raw.githubusercontent.com/datacharmer/test_db/master/sakila/README.md
tags: [sakila, employees, test_db]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/datacharmer/test_db/master/sakila/README.md
    title: sakila/README.md
    accessed: 2026-09-02
---

# What was read
The 333-byte README, accessed 2026-09-02.

# Relevant excerpt
> This sample database is derived from the Sakila-spatial db, available from the MySQL docs. The changes applied here are quite simple: The FULLTEXT index in InnoDB is added conditionally for MySQL 5.6+; The GEOMETRY column and SPATIAL index are added conditionally for MySQL 5.7+

# What it was used to decide
The project uses the Oracle download for Sakila, not this copy ([Sakila](/datasets/sakila.md)); the copy is a fallback mirror only.
