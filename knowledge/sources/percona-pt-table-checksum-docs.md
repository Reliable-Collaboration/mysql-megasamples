---
type: Source
title: Percona Toolkit pt-table-checksum documentation
description: Prior art for aggregate table checksums in MySQL; documents the hash-function choice but not the exact aggregation algorithm.
resource: https://docs.percona.com/percona-toolkit/pt-table-checksum.html
tags:
- mysql
- docs
- testing
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:19:13Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:19:13Z"
sources:
- resource: https://docs.percona.com/percona-toolkit/pt-table-checksum.html
  title: Percona Toolkit pt-table-checksum documentation
  accessed: "2026-09-02"
---
# What was read
* https://docs.percona.com/percona-toolkit/pt-table-checksum.html, “Percona Toolkit pt-table-checksum documentation”, accessed 2026-09-02

# Relevant excerpt
> "Hash function for checksums (FNV1A_64, MURMUR_HASH, SHA1, MD5, CRC32, etc). The default is to use CRC32(), but MD5() and SHA1() also work" — CRC32 is described as faster but "prone to hash collisions", MD5/SHA1 as "very CPU-intensive".

The page does not document the BIT_XOR-over-CRC32 chunk algorithm; that detail is known from the tool source and is therefore **inferred** here, not verified.

# What it was used to decide
[Per-table checksum method](/decisions/test-checksum-method.md) adopts the same idea (order-independent aggregate over a per-row hash) but specifies its own normalisation so that the baseline can be computed outside MySQL.
