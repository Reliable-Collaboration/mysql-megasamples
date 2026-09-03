---
type: Source
title: "MySQL Shell 9.7: Batch Code Execution"
description: mysqlsh --file, stdin redirection, --sql/--js/--py modes, batch mode has no interactive commands.
resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-batch-code-execution.html
tags:
- mysql-shell
- cli
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:41:13Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:41:13Z"
sources:
- resource: https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-batch-code-execution.html
  title: "MySQL Shell 9.7: Batch Code Execution"
  accessed: "2026-09-02"
  version: MySQL Shell 9.7 manual, section 5.6
---

# What was read
https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-batch-code-execution.html, accessed 2026-09-02; version: MySQL Shell 9.7 manual, section 5.6.

# Relevant excerpt
* `mysqlsh --file code.js`; `mysqlsh < code.js`; `echo "show databases;" | mysqlsh --sql --uri user@192.0.2.20:33060`; `--pym module_name`; `.js/.py/.sql` extensions select the language regardless of the default mode.
> "In batch mode, all the command logic described at Section 5.2, 'Interactive Code Execution' is not available, only valid code for the active language can be executed."
* The fetched text did not cover `--password`/`--passwords-from-stdin`.

# What it was used to decide
[MySQL Shell utilities](/tools/mysql-shell-utilities.md): loader scripts are `.py` files run with `mysqlsh --py --file`, which keeps option dictionaries in native Python instead of CLI flag conversion.
