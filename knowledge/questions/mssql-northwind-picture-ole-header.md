---
type: Open Question
title: Northwind Categories.Picture / Employees.Photo - strip the OLE wrapper or keep raw bytes?
description: All 17 image literals in instnwnd.sql begin with 151C2F00020000000D000E00 rather than a BMP/GIF signature; this is believed (not verified) to be the 78-byte Access OLE Object header around a Windows bitmap.
resource: /questions/mssql-northwind-picture-ole-header.md
tags: [open-question, northwind, binary]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/northwind-pubs/instnwnd.sql
    title: instnwnd.sql (hex literal prefixes measured)
    accessed: 2026-09-02
---

# Question
Should the MySQL port keep the `image` bytes exactly as in the script (fidelity with every other Northwind port; images are not directly viewable) or strip the leading OLE header so `Picture`/`Photo` become plain `.bmp` files (viewable, but diverges from upstream)?

# Cheapest experiment
Extract one literal (`CategoryID=1`, 10,746 bytes) from the script with a 5-line Python script, check whether bytes 78-79 are `42 4D` ("BM"); if so, `Picture[78:]` opens as a BMP. Decide with the coordinator; if stripping, add a `Picture_Original` note and document in the dataset README. Costs one minute.

# Resolves
`# Type-mapping hazards` in [Northwind](/datasets/northwind.md).
