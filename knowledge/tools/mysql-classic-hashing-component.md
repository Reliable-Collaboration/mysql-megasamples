---
type: Tool
title: MySQL classic_hashing component (MD5/SHA1 on 9.6+)
description: Since MySQL 9.6.0 MD5() and SHA1() live in an optional component; upstream checksum scripts that call MD5()/SHA() fail on the 9.7 image unless the component is installed or the scripts are rewritten to SHA2().
resource: https://dev.mysql.com/doc/refman/9.7/en/legacy-hashing-component.html
tags: [mysql, 9.7, checksum, md5, sha1, test-design]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://dev.mysql.com/doc/relnotes/mysql/9.6/en/news-9-6-0.html
    title: "MySQL 9.6.0 release notes (WL #16956)"
    accessed: 2026-09-02
  - resource: https://dev.mysql.com/doc/refman/9.7/en/encryption-functions.html
    title: 9.7 encryption functions table
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/datacharmer/test_db/master/README.md
    title: test_db README (MySQL 9.6 note)
    accessed: 2026-09-02
---

# Verified facts
* 9.6.0 release notes: MD5() and SHA1() were relocated "to a separate component"; "You can install the `classic_hashing` component to continue using MD5() and SHA1()" ([source](/sources/mysql-relnotes-9-6-0-classic-hashing.md)).
* The 9.7 manual's function table no longer lists MD5()/SHA()/SHA1(); SHA2() remains.
* datacharmer/test_db reacted by adding `test_employees_sha2.sql` and states its md5/sha tests "will not work on 9.6+" ([README](/sources/github-datacharmer-test-db-readme.md)).

# Consequence for this project
* Write all row-hash tests with `SHA2(..., 256)` or use `CHECKSUM TABLE`; never `MD5()`/`SHA1()`.
* If any upstream test script must run verbatim (Employees md5/sha variants), the image would need `INSTALL COMPONENT 'file://component_classic_hashing';` - **Inferred:** exact component URN and behaviour not read; the legacy-hashing-component manual page was not opened in this session. Verify with `SELECT MD5('x')` on the 9.7 container before relying on it.

# Applies to
[Employees](/datasets/employees.md) (test suite choice) and the test design of all datasets in this group.
