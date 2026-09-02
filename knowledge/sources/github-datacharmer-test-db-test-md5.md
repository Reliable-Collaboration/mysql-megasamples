---
type: Source
title: test_db test_employees_md5.sql (MD5 integrity test, MySQL 8.0-9.5 only)
description: Expected MD5 chained checksums per table; same recipe as the SHA-256 test but with MD5(); will not run on 9.6+ without the classic_hashing component.
resource: https://raw.githubusercontent.com/datacharmer/test_db/master/test_employees_md5.sql
tags: [employees, checksum, md5, test]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/datacharmer/test_db/master/test_employees_md5.sql
    title: test_employees_md5.sql
    accessed: "2026-09-02"
    version: master @ e324b56
---

# What was read
The whole file (4,711 bytes), accessed 2026-09-02. Header carries the CC BY-SA 3.0 notice and the "data is fabricated" disclaimer.

# Relevant excerpt
Expected `(table, recs, crc_sha, crc_md5)`: employees 300024 `4d4aa689914d8fd41db7e45c2168e7dcb9697359` / `4ec56ab5ba37218d187cf6ab09ce1aa1`; departments 9 `4b315afa0e35ca6649df897b958345bcb3d2b764` / `d1af5e170d2d1591d776d5638d71fc5f`; dept_manager 24 `9687a7d6f93ca8847388a42a6d8d93982a841c6c` / `8720e2f0853ac9096b689c14664f847e`; dept_emp 331603 `d95ab9fe07df0865f592574b3b33b9c741d9fd1b` / `ccf6fe516f990bdaa49713fc478701b7`; titles 443308 `d12d5f746b88f07e69b9e36675b6067abb01b60e` / `bfa016c472df68e70a03facafa1bc0a8`; salaries 2844047 `b5a1785c27d75e33a4173aaa22ccf41ebd7d4a9f` / `fd220654e95aea1b169624ffe3fca934`. Uses `MD5(CONCAT_WS('#',@crc, ...))` with the same column lists and ORDER BY as the sha2 test.

# What it was used to decide
Secondary evidence for row counts in [Employees](/datasets/employees.md); flagged as unusable on 9.7 ([classic_hashing](/tools/mysql-classic-hashing-component.md)). The dept_emp values differ from the ones printed on dev.mysql.com ([employee manual](/sources/mysql-employee-manual.md)), which are stale.
