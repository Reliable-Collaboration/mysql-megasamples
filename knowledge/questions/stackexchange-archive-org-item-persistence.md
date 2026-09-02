---
type: Open Question
title: Will the archive.org Stack Exchange item remain available, and should the project mirror the chosen .7z files?
description: The build depends on a 2024 upload that Stack Overflow said it would prefer not to see mirrored; the item has not been touched since 2025-06-24, but nothing guarantees it stays.
resource: /questions/stackexchange-archive-org-item-persistence.md
tags:
- question
- stackexchange
- availability
- text-group
status: draft
trust: open
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://archive.org/metadata/stackexchange
  accessed: "2026-09-02"
- resource: https://meta.stackexchange.com/questions/401324/announcing-a-change-to-the-data-dump-process
  accessed: "2026-09-02"
---

# Question
If the item disappears, the extended build breaks. CC BY-SA permits the project to mirror the two .7z files (with license.txt) in a GitHub Release; is that desirable given Stack Overflow's stated preference ("We would really rather users do not upload the file to archive.org or similar data pile sites") — a preference, not a term?

# Cheapest experiment
Add a CI step that fetches `https://archive.org/metadata/stackexchange` and compares the md5 of `dba.stackexchange.com.7z` with the pinned value; on failure, fall back to a project-hosted mirror (decision for the coordinator: mirror pre-emptively or on failure).

# Resolves
Build resilience for [Stack Exchange](/datasets/stackexchange.md).
