---
type: Source
title: "Bexhoma documentation — Benchmark: TPC-DS (MySQL/MariaDB query adaptations)"
description: An independent project that ran the 99 TPC-DS queries on several engines and lists the MySQL/MariaDB changes it needed.
resource: https://bexhoma.readthedocs.io/en/latest/Example-TPC-DS.html
tags: [tpc-ds, mysql, mariadb, community]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://bexhoma.readthedocs.io/en/latest/Example-TPC-DS.html
    title: "Benchmark: TPC-DS — Bexhoma documentation"
    accessed: "2026-09-02"
---
# What was read
* https://bexhoma.readthedocs.io/en/latest/Example-TPC-DS.html, “Benchmark: TPC-DS — Bexhoma documentation”, accessed 2026-09-02

# Relevant excerpt (verbatim)
* "MySQL is excluded currently because the treatment of NULL during INSERT is complicated."
* Query changes: "MySQL and MariaDB do not have a FULL OUTER JOIN (Q51, Q97, …)"; "MySQL and MariaDB do CASTing to INTEGER differently"; "column names may differ if AS is not used"; "MariaDB does not know GROUPING"; "the DBMS do not sort in the same way when NULL comes into play".
* Schema: "sets primary keys before import, all foreign key constraints and indexes on foreign keys of fact tables and customer table after import".
* Disclaimer: "The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS Specification."

# What it was used to decide
[TPC-DS dataset](/datasets/tpc-ds.md) incompatibility list (FULL OUTER JOIN in Q51/Q97 is confirmed by both this page and the template grep); disclaimer template in [Fair Use record](/sources/tpc-fair-use-quick-reference-v1-0-0.md).
