---
type: Source
title: "MySQL 9.7 Reference Manual: CHECK TABLE Statement"
description: "CHECK TABLE options, InnoDB behaviour (QUICK/EXTENDED semantics, corruption handling), output columns."
resource: https://dev.mysql.com/doc/refman/9.7/en/check-table.html
tags: [mysql, docs, testing]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/check-table.html
    title: "MySQL 9.7 Reference Manual: CHECK TABLE Statement"
    accessed: 2026-09-02
    version: "MySQL 9.7 manual, section 15.7.3.2"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/check-table.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 15.7.3.2.

# Relevant excerpt
* Syntax `CHECK TABLE tbl_name [, tbl_name] ... [option] ...` with FOR UPGRADE, QUICK, FAST, MEDIUM, EXTENDED, CHANGED; FAST, CHANGED, MEDIUM and EXTENDED are MyISAM-only and ignored for InnoDB; QUICK skips row scanning for InnoDB and MyISAM.
* Output columns Table, Op (`check`), Msg_type (status/error/info/note/warning), Msg_text; the last row is normally `status` / `OK`.
* InnoDB: surveys index page structure and key entries, may mark indexes or tables corrupt, may exit the server on a corrupt page; does not validate the first 3 pages of `.ibd` files (use innochecksum); supports parallel clustered-index reads when `innodb_parallel_read_threads > 1`.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): the image-level test runs `CHECK TABLE ... QUICK` over every table of the baked data directory after the clean shutdown in the build stage.
