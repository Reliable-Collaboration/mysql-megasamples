---
type: Source
title: "tobymao/sqlglot README and dialect list"
description: "SQLGlot claims: no-dependency parser/transpiler for 30+ dialects, lenient parser (not a validator), best-effort transpilation with warnings, dialect list includes tsql, oracle, mysql, postgres, sqlite, duckdb."
resource: https://raw.githubusercontent.com/tobymao/sqlglot/main/README.md
tags: [python, sql, transpiler]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://raw.githubusercontent.com/tobymao/sqlglot/main/README.md
    title: "tobymao/sqlglot README and dialect list"
    accessed: 2026-09-02
    version: "main branch, read 2026-09-02; repo license MIT; latest PyPI 30.17.0"
---

# What was read
https://raw.githubusercontent.com/tobymao/sqlglot/main/README.md, accessed 2026-09-02; version: main branch, read 2026-09-02; repo license MIT; latest PyPI 30.17.0.

# Relevant excerpt
> "SQLGlot is a no-dependency SQL parser, transpiler, optimizer, and engine. It can be used to format SQL or translate between over 30 dialects ... It aims to read a wide variety of SQL inputs and output syntactically and semantically correct SQL in the targeted dialects."
> "The parser is intentionally lenient, so it can accept queries that a real engine would reject. SQLGlot is a transpiler, not a validator. A query that parses successfully may still fail at execution time."
> "It may not be possible to translate some queries between certain dialects. For these cases, SQLGlot may emit a warning and will proceed to do a best-effort translation by default" (`unsupported_level=sqlglot.ErrorLevel.RAISE` turns that into an error).
> "Some queries need additional information to be transpiled accurately, such as the schemas of the referenced tables ... The qualify and annotate_types optimizer rules can provide this information, but they are not used by default".
> "Transpilation is a hard problem, so SQLGlot solves it incrementally. Some dialect pairs may lack support for certain inputs, but coverage improves over time."
* Always pass `read=`/`dialect=` and `write=`; comments preserved best-effort; `sqlglot[c]` (mypyc) disables runtime dialect subclassing.
* `sqlglot/dialects/` contains: athena bigquery clickhouse databricks dax doris dremio drill druid duckdb dune exasol fabric hive materialize mysql oracle postgres presto prql redshift risingwave singlestore snowflake solr spark spark2 sqlite starrocks tableau teradata trino tsql.

# What it was used to decide
[Python conversion stack](/tools/python-conversion-stack.md): sqlglot is used for TPC-DS/TPC-H query translation and for first-pass DDL translation with `ErrorLevel.RAISE`, never as a correctness oracle; every transpiled statement is executed against MySQL in the build.
