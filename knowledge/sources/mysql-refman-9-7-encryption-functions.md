---
type: Source
title: MySQL 9.7 Reference Manual - Encryption and Compression Functions
description: The 9.7 function summary table (AES_*, COMPRESS, RANDOM_BYTES, SHA2, STATEMENT_DIGEST*, UNCOMPRESS*, VALIDATE_PASSWORD_STRENGTH) omits MD5() and SHA()/SHA1().
resource: https://dev.mysql.com/doc/refman/9.7/en/encryption-functions.html
tags:
- mysql
- "9.7"
- functions
- md5
- sha2
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/encryption-functions.html
  title: 14.13 Encryption and Compression Functions
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/mysql-nutshell.html
  title: What Is New in MySQL 9.7 (checked - no mention of MD5/SHA removal; removed features list only names two replication variables)
  accessed: "2026-09-02"
---

# What was read
The function-table page and the 9.7 "What Is New" page, accessed 2026-09-02.

# Relevant excerpt
Table 14.18 lists: AES_DECRYPT(), AES_ENCRYPT(), COMPRESS(), RANDOM_BYTES(), SHA2(), STATEMENT_DIGEST(), STATEMENT_DIGEST_TEXT(), UNCOMPRESS(), UNCOMPRESSED_LENGTH(), VALIDATE_PASSWORD_STRENGTH(). "SHA2() can be considered cryptographically more secure than MD5() or SHA1()." MD5() and SHA()/SHA1() are not in the table. The 9.7 nutshell page's "Features Removed" section lists only `group_replication_allow_local_lower_version_join` and `replica_parallel_type`, because the hash-function relocation happened in 9.6.

# What it was used to decide
[classic_hashing tool note](/tools/mysql-classic-hashing-component.md); corroborates the [9.6.0 release note](/sources/mysql-relnotes-9-6-0-classic-hashing.md).
