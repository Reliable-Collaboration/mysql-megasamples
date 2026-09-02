---
type: Source
title: "MySQL 9.7 Reference Manual: EXPLAIN Output Format"
description: Meaning of the access type values ALL, index, range, ref, eq_ref, const, fulltext and of Using index; basis for the index-usage test.
resource: https://dev.mysql.com/doc/refman/9.7/en/explain-output.html
tags: [mysql, docs, testing]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:19:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:19:13Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/explain-output.html
    title: "MySQL 9.7 Reference Manual: EXPLAIN Output Format"
    accessed: "2026-09-02"
---
# What was read
* https://dev.mysql.com/doc/refman/9.7/en/explain-output.html, “MySQL 9.7 Reference Manual: EXPLAIN Output Format”, accessed 2026-09-02

# Relevant excerpt
* ALL: "A full table scan is done for each combination of rows from the previous tables. This is normally not good if the table is the first table not marked const, and usually very bad in all other cases."
* index: "same as ALL, except that the index tree is scanned."
* range: "Only rows in a given range are retrieved using an index to select rows."
* ref / eq_ref / const / fulltext as defined on the page ("The join is performed using a FULLTEXT index").
* Using index: "The column information is retrieved from the table using only information in the index tree without having to do an additional seek to read the actual row." Shown for TRADITIONAL, JSON and TREE formats.
* Formats available: TRADITIONAL, JSON, TREE. The page does not state the default for 9.x; the executor checks `SELECT @@explain_format`.

# What it was used to decide
[Indexing strategy](/decisions/indexing-strategy.md): the EXPLAIN test asserts `access_type != "ALL"` (JSON) for each smoke query table that the plan expects to be indexed; `index` is tolerated only when the plan says the query is a covering scan.
