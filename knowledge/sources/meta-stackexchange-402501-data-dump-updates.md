---
type: Source
title: Meta SE 402501 — "Data Dumps - updates and bug fixes" (staff, 2024-08-29)
description: Staff changelog for the regenerated 2024-Q2 dumps — XML generator reverted to C#, license.txt and schema markdown inside each .7z, SHA256 checksums posted on Meta.
resource: https://meta.stackexchange.com/questions/402501/data-dumps-updates-and-bug-fixes
tags: [source, stackexchange, schema, checksums]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://api.stackexchange.com/2.3/questions/402501?site=meta&filter=withbody
    title: question body via API (owner Berthold, staff)
    accessed: 2026-09-02
---

# What was read
Question body and top answer on 2026-09-02.

# Relevant excerpt
> "Reverted to C# for producing XML to avoid illegal characters SQL Server misses." "ViewCount attribute removed from answers, instead of showing 0". "GUIDs are lower case to match SEDE". "Votes > type 16 are filtered out correctly". "A license.txt is present inside each .7z". "A sede-and-data-dump-schema.md is present inside each .7z, which is a snapshot of this answer's markdown at generation time." "A set of SHA256 checksums for the regenerated 2024-Q2 dumps has been posted in this answer. Future checksums can be published in whatever place makes the most sense, but cannot be distributed as part of the downloads." "stackoverflow.com.7z now contains .xml files, not another level of .7z files."

# What it was used to decide
Hazard list in [Stack Exchange XML parsing](/tools/stackexchange-xml-parsing.md); why the archive.org 2024-04 files (pre-bug) are preferred in [Stack Exchange dataset](/datasets/stackexchange.md).
