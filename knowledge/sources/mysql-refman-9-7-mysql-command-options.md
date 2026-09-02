---
type: Source
title: "MySQL 9.7 Reference Manual: mysql Client Options"
description: "--default-character-set, --local-infile (default FALSE), --binary-mode and --get-server-public-key for the mysql command-line client."
resource: https://dev.mysql.com/doc/refman/9.7/en/mysql-command-options.html
tags:
- mysql
- docs
- client
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:33:59Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/mysql-command-options.html
  title: "MySQL 9.7 Reference Manual: mysql Client Options"
  accessed: "2026-09-02"
  version: MySQL 9.7 manual, section 6.5.1.1
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/mysql-command-options.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 6.5.1.1.

# Relevant excerpt
* `--default-character-set=charset_name`: "Use charset_name as the default character set for the client and connection."
* `--local-infile[={0|1}]`: Default Value FALSE. "By default, LOCAL capability for LOAD DATA is determined by the default compiled into the MySQL client library. ... When given with no value, the option enables LOCAL data loading." "Successful use of LOCAL load operations within mysql also requires that the server permits local loading".
* `--binary-mode`: "By default, mysql translates \r\n in statement strings to \n and interprets \0 as the statement terminator. --binary-mode disables both features."
* `--get-server-public-key`: "Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching_sha2_password authentication plugin."

# What it was used to decide
[LOAD DATA tool record](/tools/load-data-infile.md): every `mysql` invocation in build scripts passes `--default-character-set=utf8mb4 --local-infile=1`; SQL files containing binary literals are piped with `--binary-mode`.
