---
type: Open Question
title: Can a WideWorldImporters .bacpac be read without SQL Server (to allow arm64 builders)?
description: A .bacpac is documented only as an importable DacFx package ("compressed but not encrypted"); its internal layout (zip with model.xml and per-table BCP-native data files) is not documented on the page read, so direct parsing is inferred and unverified.
resource: /questions/mssql-bacpac-readable-without-sql-server.md
tags:
- open-question
- wideworldimporters
- bacpac
status: draft
trust: open
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:20:00Z"
sources:
- resource: https://learn.microsoft.com/en-us/sql/relational-databases/data-tier-applications/data-tier-applications
  title: Data-tier applications overview (Learn)
  accessed: "2026-09-02"
---

# Question
**Inferred from general knowledge:** a `.bacpac` is a ZIP containing `model.xml` (schema), `Origin.xml`, and `Data/<schema>.<table>/TableData-*.BCP` files in SQL Server *native* bcp format (binary, length-prefixed, no terminators). If that holds, a Python reader could decode it using `model.xml` types, which would let arm64 builders skip the [SQL Server container](/tools/mssql-server-container.md). Native format handling of nvarchar, datetime2, decimal, geography, varbinary and NULLs is intricate and undocumented for third parties, so this is unlikely to be cheaper than the container.

# Cheapest experiment
`curl -L -o wwidw.bacpac https://github.com/microsoft/sql-server-samples/releases/download/wide-world-importers-v1.0/WideWorldImportersDW-Standard.bacpac` (22 MB) then `unzip -l wwidw.bacpac | head -50` and `xxd Data/Dimension.City/TableData-000.BCP | head`. If the layout matches, estimate decoder effort before committing; otherwise close the question in favour of the container path.

# Resolves
"Native format and friendlier forms" in [WideWorldImporters](/datasets/wideworldimporters.md) / [DW](/datasets/wideworldimporters-dw.md); option 3 of the [conversion decision](/decisions/mssql-wideworldimporters-conversion-path.md).
