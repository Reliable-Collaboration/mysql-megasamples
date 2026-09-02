---
type: Decision
title: Conversion path for AdventureWorks OLTP, DW and LT - load the upstream CSV files directly, no SQL Server
description: The repository's install-script form ships UTF-8 CSVs (OLTP 69 files / DW 30 files, 2025 edition) and the 2012 release ships an LT script zip; DDL is translated from the scripts and data loaded with LOAD DATA, avoiding .bak restores entirely.
resource: /decisions/mssql-adventureworks-conversion-path.md
tags: [decision, adventureworks, conversion-path]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/oltp-install-script/instawdb.sql
    title: instawdb.sql (CODEPAGE 65001, terminators per table)
    accessed: "2026-09-02"
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/contents/samples/databases/adventure-works/oltp-install-script
    title: CSV sampling (UTF-8, LF, hex-encoded binary/hierarchyid/geography)
    accessed: "2026-09-02"
  - resource: https://github.com/microsoft/sql-server-samples/releases/download/adventureworks2012/adventure-works-2012-oltp-lt-script.zip
    title: LT 2012 script zip (Windows-1252 + one UTF-16 CSV)
    accessed: "2026-09-02"
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/releases/tags/adventureworks
    title: .bak asset sizes
    accessed: "2026-09-02"
---

# Question
Should AdventureWorks (OLTP, DW, LT) be produced from the `.bak` backups via a SQL Server container + bcp, or from the script + CSV form?

# Options considered
1. **Script + CSV (chosen)**: OLTP `oltp-install-script/` and DW `data-warehouse-install-script/` at commit `b47eadc852` (UTF-8, `CODEPAGE='65001'`, tab/`0x0a` or `+|`/`&|\n` terminators, DW `|`/`\n`); LT from `adventure-works-2012-oltp-lt-script.zip` (Windows-1252 + UTF-16 `ProductModel.csv`, converted with iconv). DDL derived from `instawdb.sql`/`instawdbdw.sql`/`instawltdb.sql` by a translator; `LOAD DATA LOCAL INFILE` with `ESCAPED BY ''` and the matching multi-character terminators.
2. `.bak` restore in the [SQL Server container](/tools/mssql-server-container.md) + [bcp](/tools/sqlcmd-bcp.md) export: works for every version (2012-2025) and would give the classic 2014-dated data and native `.ToString()` decoding of hierarchyid/geography, but requires amd64, ~1.3 GB image, EULA acceptance, and re-introduces bcp's terminator/NULL hazards.
3. Hybrid: option 1 for everything, with a one-off SQL Server run only to produce a lookup table for hierarchyid paths and geography WKT (or to validate the pure-Python decoders).

# Evidence
[instawdb.sql](/sources/github-microsoft-sql-server-samples-instawdb-sql.md) (68 BULK INSERTs, all 65001/char), [CSV sampling](/sources/github-microsoft-sql-server-samples-oltp-install-script-csvs.md) (UTF-8 LF; hierarchyid as bare hex `58`, geography as `E6100000010C...`, varbinary hex, inline XML), [instawdbdw.sql](/sources/github-microsoft-sql-server-samples-instawdbdw-sql.md), [LT zip](/sources/github-microsoft-sql-server-samples-adventureworks-2012-lt-script.md), [release sizes](/sources/github-microsoft-sql-server-samples-adventureworks-release.md), [README](/sources/github-microsoft-sql-server-samples-adventure-works-readme.md) ("dates have been adjusted" in 2025; 2012-2022 identical apart from name/compat level).

# Outcome
Option 1 with option 3's validation step allowed once (not in the routine build). The OLTP/DW output is the **2025 edition** (AWBuildVersion 17.0.1000.3, shifted dates) - state this in the image README; LT output is the 2012 edition data (name `adventureworks_lt`). Exotic columns: store hierarchyid raw (`VARBINARY`) plus a decoded path column, geography as `POINT SRID 4326` decoded from the 22-byte point serialization, XML as text; drop XML indexes/schema collections/full-text-on-XML. MySQL databases: `adventureworks`, `adventureworks_dw`, `adventureworks_lt`; schema prefixing per [mapping decision](/decisions/schema-to-database-mapping.md).

# Status
accepted, with two open questions: [row counts / ProductReview line anomaly / decoders](/questions/mssql-adventureworks-row-counts.md) and [LT parity](/questions/mssql-adventureworks-lt-script-vs-bak-parity.md).
