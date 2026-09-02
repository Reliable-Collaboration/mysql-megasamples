---
type: Source
title: MySQL 9.7 Reference Manual — Date and Time Literals
description: Confirms MySQL accepts the standard SQL DATE 'str' literal used by TPC-H/TPC-DS query text.
resource: https://dev.mysql.com/doc/refman/9.7/en/date-and-time-literals.html
tags: [mysql, sql-syntax]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:30:00Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/date-and-time-literals.html
    title: Date and Time Literals
    accessed: 2026-09-02
---

# Relevant excerpt (verbatim)
* "Standard SQL requires temporal literals to be specified using a type keyword and a string. The space between the keyword and string is optional. DATE 'str' TIME 'str' TIMESTAMP 'str' MySQL recognizes but, unlike standard SQL, does not require the type keyword."
* "MySQL also recognizes the ODBC syntax ... { d 'str' } { t 'str' } { ts 'str' }".

# What it was used to decide
TPC-H query porting rules in [TPC-H dataset](/datasets/tpc-h.md).
