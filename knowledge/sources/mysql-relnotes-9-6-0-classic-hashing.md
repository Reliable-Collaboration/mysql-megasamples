---
type: Source
title: MySQL 9.6.0 release notes - MD5() and SHA1() moved to the classic_hashing component
description: "Security note WL #16956 in the 9.6.0 release notes (2026-01-20) relocating MD5() and SHA1() out of the core server."
resource: https://dev.mysql.com/doc/relnotes/mysql/9.6/en/news-9-6-0.html
tags:
- mysql
- "9.6"
- md5
- sha1
- checksum
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/relnotes/mysql/9.6/en/news-9-6-0.html
  title: Changes in MySQL 9.6.0 (2026-01-20, Innovation Release)
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/refman/9.7/en/encryption-functions.html
  title: 9.7 Reference Manual - Encryption and Compression Functions (function table)
  accessed: "2026-09-02"
---

# What was read
The 9.6.0 release notes page and the 9.7 reference-manual function table, accessed 2026-09-02.

# Relevant excerpt
> MySQL now supports enhanced security and flexibility with the relocation of `MD5()` and `SHA1()` SQL functions to a separate component, allowing for greater control over deprecated hashing algorithms and improved compliance with security standards. You can install the `classic_hashing` component to continue using `MD5()` and `SHA1()` functions in your applications ... (WL #16956; see "Legacy Hashing Component" in the 9.7 manual).

The 9.7 encryption-functions summary table lists AES_DECRYPT, AES_ENCRYPT, COMPRESS, RANDOM_BYTES, SHA2, STATEMENT_DIGEST, STATEMENT_DIGEST_TEXT, UNCOMPRESS, UNCOMPRESSED_LENGTH, VALIDATE_PASSWORD_STRENGTH - MD5() and SHA()/SHA1() are absent; "SHA2() can be considered cryptographically more secure than MD5() or SHA1()".

# What it was used to decide
[classic_hashing tool note](/tools/mysql-classic-hashing-component.md); test design for every dataset (use SHA2 or CHECKSUM TABLE).
