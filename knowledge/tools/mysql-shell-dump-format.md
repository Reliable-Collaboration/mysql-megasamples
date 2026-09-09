---
type: Tool
title: MySQL Shell dump format as the ports read it (util.dumpSchemas, mysqlsh 9.7.1)
description: What a build/mysql/dumps/<dataset>/ directory holds and the rules the port reader relies on -- UTC timestamps, base64 binary columns, chunk file naming, generated columns absent -- each observed on this project's dumps.
resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-dump-instance-schema.html
tags:
- tool
- mysql-shell
- dump
- port
status: stable
trust: verified
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:44:04Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:44:04Z"
sources:
- resource: /tools/mysql-shell-utilities.md
  title: MySQL Shell utilities record (the dump and load options the project uses)
  accessed: "2026-09-09"
---

# Facts
Observed on 2026-09-09 in `build/mysql/dumps/` written by `mysqlsh Ver 9.7.1` (`@.json` `dumper`), from
`util.dumpSchemas` with `compression: zstd`, `threads: 4` (megasamples/engines/mysql/dump.py):
* `@.json` records `tzUtc: true`, `defaultCharacterSet: utf8mb4`, `bytesPerChunk: 64000000`; every
  timestamp in the data is therefore UTC text, the same rendering the canonical digest uses.
* Per table, `<schema>@<table>.json` carries `options.columns` in order and
  `options.decodeColumns`: binary, blob and geometry columns are written as base64 and marked
  `FROM_BASE64` (30 such columns across the 21 core databases, all `FROM_BASE64`; no `FROM_HEX`).
  Field terminator tab, line terminator newline, escape backslash, no enclosure.
* Escapes in the data are MySQL's LOAD DATA text form: `\\N` for NULL, `\\t`, `\\n`, `\\\\`, `\\0`
  for the characters. In Sakila's chunks only `\\N` occurs (1,189 times); the reader handles the rest.
* Chunk files are `<schema>@<table>@@N.tsv.zst`. A table the dumper cannot chunk by a key -- no
  primary or unique key, such as `dvdstore.cust_hist` -- gets `<schema>@<table>@0.tsv.zst` (one `@`)
  holding the rows and an empty `@@1` beside it; both forms are read, ordered by N.
* A stored generated column is not in the dump (it cannot be inserted): `adventureworks_lt.salesorderheader`
  lists 20 of its 21 columns. The ports load the insertable columns and let the target engine
  compute the rest from the same expression; the digest check then proves the values agree.
* Geometry values carry MySQL's internal form: four bytes of SRID before the WKB
  (`00000000 01010000...` for `sakila.address.location`). The ports drop those four bytes so the
  stored value is what `ST_AsBinary` returns, which is what the digest hashes.
* Python 3.14's `compression.zstd` decompresses the chunks; no zstd binary is needed on the host.

# Limits
1. The reader asserts the terminator and escape options above and refuses a dump written with others.
2. `tzUtc` is relied on: a dump taken without it would render timestamps in the session zone and the
   digests of timestamp columns would differ from the pinned ones.
