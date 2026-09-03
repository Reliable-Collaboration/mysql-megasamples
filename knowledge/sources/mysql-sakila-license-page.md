---
type: Source
title: License for the Sakila Sample Database (manual chapter 9)
description: The page that states which Sakila files are under the New BSD license and that the other distributed materials are not open-licensed.
resource: https://dev.mysql.com/doc/sakila/en/sakila-license.html
tags:
- sakila
- license
- bsd
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/sakila/en/sakila-license.html
  title: 9 License for the Sakila Sample Database
  accessed: "2026-09-02"
  version: manual revision 84779 (2026-08-04)
---

# What was read
Chapter 9 of the Sakila manual, accessed 2026-09-02.

# Relevant excerpt
> The contents of the sakila-schema.sql and sakila-data.sql files are licensed under the New BSD license.
>
> Information on the New BSD license can be found at http://www.opensource.org/licenses/bsd-license.php and http://en.wikipedia.org/wiki/BSD_License.
>
> The additional materials included in the Sakila distribution, including this documentation, are not licensed under an open license. Use of this documentation is subject to the terms described in Legal Notices.

The page does not reproduce the BSD text itself; the text is embedded as a comment header in both .sql files (see [the zip inspection](/sources/mysql-sakila-db-zip.md)).

# What it was used to decide
[BSD-3-Clause (Sakila) license record](/licenses/bsd-3-clause-sakila.md); the finding that `sakila.mwb` and the manual must not be redistributed ([dataset record](/datasets/sakila.md)).
