---
type: Open Question
title: Does downloads.mysql.com regenerate sakila-db.zip, invalidating a pinned checksum?
description: The archive's HTTP Last-Modified (2026-08-31) is newer than the manual revision (2026-08-04) and zip entries are dated 2026-09-01, suggesting periodic regeneration.
resource: /questions/sakila-download-checksum-drift.md
tags: [sakila, checksum, build]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://downloads.mysql.com/docs/sakila-db.zip
    title: sakila-db.zip (HEAD and content inspection)
    accessed: "2026-09-02"
---

# Question
The zip fetched 2026-09-02 had md5 `a80df38456f8d4f36903771b67a1129a` and inner file timestamps of 2026-09-01 00:05, while the content still says "Version 1.5". If Oracle rebuilds the archive (new zip timestamps, same content), an archive-level checksum pin breaks even though the SQL is unchanged.

# Cheapest experiment
Pin checksums on the extracted files instead of the archive: `sakila-schema.sql` md5 `fcf59afd9117470f6cd45f948a3e9dcb`, `sakila-data.sql` md5 `799d84daf7137bc341770c3070013668`. Re-download in one week and compare both the zip md5 and the inner-file md5s; if only the zip md5 changed, the build should verify inner files only. Alternatively vendor the two .sql files into the repository (BSD allows it) and drop the download entirely.

# Related
[Sakila dataset](/datasets/sakila.md), [conversion decision](/decisions/sakila-conversion-path.md).

# Resolves
Records that depend on the answer:
* [sakila.md](/datasets/sakila.md)
* [sakila-conversion-path.md](/decisions/sakila-conversion-path.md)
* [mysql-sakila-db-zip.md](/sources/mysql-sakila-db-zip.md)
* PLAN.md §9 risk register (outside the bundle)
