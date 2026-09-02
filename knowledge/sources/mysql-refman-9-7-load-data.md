---
type: Source
title: "MySQL 9.7 Reference Manual: LOAD DATA Statement"
description: "Syntax, LOCAL versus server-side file reading, secure_file_priv, default field/line terminators, NULL as \\N, IGNORE/REPLACE and nonrestrictive interpretation, SET transformations."
resource: https://dev.mysql.com/doc/refman/9.7/en/load-data.html
tags: [mysql, docs, load-data]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/load-data.html
    title: "MySQL 9.7 Reference Manual: LOAD DATA Statement"
    accessed: "2026-09-02"
    version: "MySQL 9.7 manual, section 15.2.9"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/load-data.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 15.2.9.

# Relevant excerpt
* Syntax: `LOAD DATA [LOW_PRIORITY | CONCURRENT] [LOCAL] INFILE 'file_name' [REPLACE | IGNORE] INTO TABLE tbl_name [PARTITION (...)] [CHARACTER SET charset_name] [{FIELDS | COLUMNS} [TERMINATED BY 'string'] [[OPTIONALLY] ENCLOSED BY 'char'] [ESCAPED BY 'char']] [LINES [STARTING BY 'string'] [TERMINATED BY 'string']] [IGNORE number {LINES | ROWS}] [(col_name_or_user_var, ...)] [SET col_name={expr | DEFAULT}, ...]`
* Non-LOCAL: file must be on the server host, relative paths resolve against the data directory or the default database directory, and it "Requires the FILE privilege"; LOCAL: "The client program reads the file and sends its contents to the server", the server "creates a copy in its temporary files directory", no FILE privilege needed.
* secure_file_priv: "If the variable value is a nonempty directory name, the file must be located in that directory"; "If the variable value is empty (which is insecure), the file need only be readable by the server".
* "LOCAL works only if the server and your client both have been configured to permit it. If the server was started with the local_infile system variable disabled, LOCAL produces an error."
* Character set: "By default, the server interprets the file contents using the character set indicated by the character_set_database system variable"; "A character set of binary specifies 'no conversion'"; "It is not possible to load data files that use the ucs2, utf16, utf16le, or utf32 character set."
* Defaults when no FIELDS/LINES clause: `FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\' LINES TERMINATED BY '\n' STARTING BY ''`.
* `IGNORE 1 LINES` skips a header line. Column list may contain user variables; `SET column2 = @var1/100` preprocesses; `@dummy` discards a field.
* NULL: "a field value of \N is read as NULL for input (assuming that the ESCAPED BY character is \)"; with a non-empty ENCLOSED BY, an unquoted literal word NULL reads as NULL but a quoted "NULL" is the string.
* REPLACE replaces rows on duplicate unique key, IGNORE discards them; "When IGNORE or LOCAL without REPLACE is specified, data interpretation errors become warnings and the load operation continues, even if the SQL mode is restrictive" (too many fields ignored, too few fields get defaults, NULL into NOT NULL gets the implicit default, invalid values converted to the closest valid value).
* Windows files may need `LINES TERMINATED BY '\r\n'`. LOW_PRIORITY/CONCURRENT only affect table-locking engines (MyISAM). "The LOAD DATA statement reads rows from a text file into a table at a very high speed."

# What it was used to decide
[LOAD DATA tool record](/tools/load-data-infile.md); the converter output format (TSV, `\N` NULLs, backslash escaping) and the strict-versus-nonrestrictive loading rule.
