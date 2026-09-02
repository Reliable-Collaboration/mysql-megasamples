---
type: Tool
title: sqlcmd and bcp (mssql-tools18 / go-sqlcmd)
description: Command-line query and bulk-export tools for SQL Server; bcp (proprietary, ODBC-based, in mssql-tools18) is the export path for .bak-only datasets, go-sqlcmd (MIT) is the redistributable query client. Records the UTF-8 export rules on Linux and bcp's no-quoting hazard.
resource: https://learn.microsoft.com/en-us/sql/tools/bcp-utility
tags: [tool, bcp, sqlcmd, export, build-time-only]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://learn.microsoft.com/en-us/sql/tools/bcp-utility
    title: bcp utility reference (Learn)
    accessed: "2026-09-02"
  - resource: https://learn.microsoft.com/en-us/sql/tools/bcp/bcp-use-utility
    title: How to use the bcp utility (Learn)
    accessed: "2026-09-02"
  - resource: https://learn.microsoft.com/en-us/sql/relational-databases/import-export/specify-field-and-row-terminators-sql-server
    title: Specify field and row terminators (Learn)
    accessed: "2026-09-02"
  - resource: https://learn.microsoft.com/en-us/sql/relational-databases/import-export/use-unicode-character-format-to-import-or-export-data-sql-server
    title: Use Unicode character format (bcp -w) (Learn)
    accessed: "2026-09-02"
  - resource: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/programming-guidelines
    title: ODBC Driver for SQL Server on Linux - character set support (Learn)
    accessed: "2026-09-02"
  - resource: https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools
    title: Install sqlcmd and bcp on Linux (Learn)
    accessed: "2026-09-02"
  - resource: https://api.github.com/repos/microsoft/go-sqlcmd
    title: microsoft/go-sqlcmd (MIT, v1.10.0)
    accessed: "2026-09-02"
  - resource: https://aka.ms/odbc18eula
    title: Microsoft ODBC Driver 18 for SQL Server license terms
    accessed: "2026-09-02"
stale_after: "2027-03-01"
---

# Facts
* **bcp** and **ODBC sqlcmd** ship in the `mssql-tools18` package (depends on `msodbcsql18`, `unixodbc-dev`), installed with `sudo ACCEPT_EULA=Y apt-get install mssql-tools18 unixodbc-dev` into `/opt/mssql-tools18/bin`; available for `x64` and `arm64`; also pre-installed in the SQL Server container image (2022 CU14+/2019 CU28+). License: proprietary Microsoft terms (ODBC 18 EULA "MICROSOFT SOFTWARE LICENSE TERMS MICROSOFT ODBC DRIVER 18 FOR SQL SERVER": "You may install and use any number of copies of the software to develop and test your applications"; distributable-code clauses; the mssql-tools EULA text itself was not located - see open question). Treat as **build-time only; do not redistribute** in the MySQL image.
* **go-sqlcmd** (`github.com/microsoft/go-sqlcmd`, **MIT**, v1.10.0 2026-03-03, Linux amd64/arm64/s390x tarballs): the "modern alternative" per Learn; can create the SQL Server container (`sqlcmd create mssql --tag 2022-latest --accept-eula`, Developer edition only) and run queries, but has **no bcp equivalent**.

# Verified behaviour relevant to exporting a table as UTF-8 text
* Defaults on Linux: field terminator tab, row terminator `\n` (Learn "Considerations for bcp on Linux and macOS"). `-c` = character mode (char storage, no prefixes). `-w` = Unicode character mode: **UTF-16 with a 0xFFFE BOM**, tab/`\n` terminators; `-c` and `-w` are mutually exclusive.
* **`-C 65001` (code page) is Windows-only** ("Not supported on Linux and macOS"), as are `-N`, `-x`, `-V`, `-i`, `-o`, `-h`. On Linux the encoding of `-c` output comes from the ODBC driver: "Upon connection, the driver detects the current locale of the process ... otherwise, it defaults to UTF-8. Since all processes start in the "C" locale by default (and cause the driver to default to UTF-8)". Therefore `LC_ALL=C.UTF-8 bcp ... -c` yields UTF-8 without data loss for nvarchar (the driver converts server UTF-16 to the client encoding; UTF-8 "can represent all the characters"). Verify once ([open question](/questions/mssql-bcp-linux-export-encoding-and-escaping.md)).
* **bcp never quotes or escapes**: "If a terminator character occurs within the data, the character is interpreted as a terminator, not as data ... choose your terminators carefully to make sure that they never appear in your data." Learn's best practice: "Use a long and unique terminator (any sequence of bytes or characters)" and "Consider overriding the default terminators (using -t and -r options) with random hexadecimal values". Terminators may be up to 10 printable characters, `\t \n \r \0` or `0x..` hex. WWI has `NVARCHAR(MAX)` comment/JSON columns that contain newlines and tabs, so the export must use multi-character terminators (e.g. `-t '|~|' -r '|~~|\n'` in the AdventureWorks `+|`/`&|\n` style) and MySQL `LOAD DATA ... FIELDS TERMINATED BY '|~|' ESCAPED BY '' LINES TERMINATED BY '|~~|\n'`, which accepts multi-character terminators. Alternatively export via `queryout` with `FOR JSON`/`STRING_ESCAPE` or `sqlcmd` with `-y0` to sidestep terminators (inferred option).
* NULL handling: on export "represents an empty string as a null, and a null string as an empty string" (an empty string and NULL are indistinguishable in `-c` output) - wrap nullable text columns in `queryout` selects with a sentinel (`ISNULL(col, '\N')`) so `LOAD DATA` restores NULLs (inferred technique).
* `\n` as row terminator on export writes **CRLF**; use `-r '0x0A'` for LF-only files.
* Computed and timestamp columns are exported "as usual" (values appear in the file) - drop them from the `queryout` select or map them to a variable on load.
* Typical export command (build container, ODBC 18 tools 18.x): `LC_ALL=C.UTF-8 /opt/mssql-tools18/bin/bcp "SELECT ... FROM Sales.Orders" queryout /out/Sales_Orders.tsv -c -t '|~|' -r '|~~|\n' -S localhost -U sa -P "$SA_PASSWORD" -d WideWorldImporters -u` (`-u` = trust server certificate; `-Yo` optional encryption; both bcp 18+). For geography use `.STAsText()` and for varbinary `CONVERT(varchar(max), col, 2)` (hex) in the select. Versions 17.x use `-C` ... no: ODBC 17 tools lack `-u/-Y`; they need a trusted certificate or `-N`? - **open**: confirm which flag set the 2022 container's bcp version accepts.

# Limits
* Proprietary; keep to build stage; needs the ODBC driver (`msodbcsql18`, glibc; Alpine unsupported for some locales).
* `-C` unavailable on Linux; rely on locale + driver default UTF-8.
* No quoting; sentinel NULLs; CRLF default.
* go-sqlcmd cannot bulk-export; `sqlcmd -y0 -s` output is padded/tabular and unsuitable for large tables.

# Used by
[WideWorldImporters conversion decision](/decisions/mssql-wideworldimporters-conversion-path.md); [SQL Server container](/tools/mssql-server-container.md).
