---
type: Source
title: GitHub release "Wide World Importers sample database v1.0" (tag wide-world-importers-v1.0)
description: Asset list with exact byte sizes for the WideWorldImporters and WideWorldImportersDW Full/Standard .bak and .bacpac files plus the ETL and script assets.
resource: https://github.com/microsoft/sql-server-samples/releases/tag/wide-world-importers-v1.0
tags: [wideworldimporters, release, download]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/releases/tags/wide-world-importers-v1.0
    title: releases/tags/wide-world-importers-v1.0 (published 2016-06-08T19:25:10Z)
    accessed: "2026-09-02"
stale_after: "2027-03-01"
---

# What was read
GitHub releases API for the tag. Download URL pattern `https://github.com/microsoft/sql-server-samples/releases/download/wide-world-importers-v1.0/<asset>`; no auth or click-through; no checksums published.

# Relevant excerpt
* WideWorldImporters-Full.bak 127,111,168; WideWorldImporters-Full.bacpac 61,291,839; WideWorldImporters-Full_old.bak 127,056,896; WideWorldImporters-Full_old.bacpac 62,009,561
* **WideWorldImporters-Standard.bak 126,951,424**; WideWorldImporters-Standard.bacpac 60,996,994; -Standard_old.bak 126,938,624; -Standard_old.bacpac 61,294,900
* WideWorldImportersDW-Full.bak 50,044,416; WideWorldImportersDW-Full.bacpac 20,566,783
* **WideWorldImportersDW-Standard.bak 53,865,472**; WideWorldImportersDW-Standard.bacpac 22,448,674
* Daily.ETL.ispac 62,618; sample-scripts.zip 23,606; workload-drivers.zip 23,043

The release page/API carries no description of what "Standard" removes; that comes from the Learn pages (Full requires Evaluation/Developer/Enterprise edition; the `Application.Configuration_*` procedures apply columnstore, in-memory, partitioning, PolyBase, full-text to a Standard database).

# What it was used to decide
Source-artifact sections of [WideWorldImporters](/datasets/wideworldimporters.md) and [WideWorldImportersDW](/datasets/wideworldimporters-dw.md); [conversion-path decision](/decisions/mssql-wideworldimporters-conversion-path.md).
