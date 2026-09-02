---
type: Open Question
title: How can the Lahman 2025 CSV set be fetched non-interactively (or should it be vendored)?
description: SABR distributes the CSVs via a Box shared folder without a static download URL; guessed shared/static .zip links return 404; sizes are unknown.
resource: /questions/lahman-box-direct-download.md
tags: [lahman, download, build]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://sabr.box.com/s/y1prhc795jk8zvmelfd3jq7tl389y6cd
    title: Box share page probe
    accessed: "2026-09-02"
  - resource: https://sabr.app.box.com/public/static/qtgh1olzcaauz5x234wqx8huixizff8l.txt
    title: readme (license permits redistribution)
    accessed: "2026-09-02"
---

# Question
Build automation needs a URL. Box shared folders can be downloaded via the Box "download folder" endpoint (`https://app.box.com/index.php?rm=box_download_shared_file&shared_name=<share>&file_id=f_<id>` for files; folder zips via `rm=box_v2_zip_shared_folder` - **Inferred**, not verified) or via the Box API with a developer token, neither of which is stable for a public build.

# Cheapest experiment
1. In a browser, download the CSV folder once from https://sabr.box.com/s/y1prhc795jk8zvmelfd3jq7tl389y6cd, record per-file sizes, sha256 and whether files start with a UTF-8 BOM (SABR's page says BOMs were "updated" 2026-02-18).
2. Vendor the CSVs into the repository (CC BY-SA 3.0 permits redistribution with attribution and share-alike; see [license](/licenses/cc-by-sa-3-0.md)), which removes the download problem entirely. Also try `curl -sI` on the SQL-version share to see if SABR later exposes a static link.

# Related
[Lahman](/datasets/lahman.md), [decision](/decisions/lahman-conversion-path.md).

# Resolves
Records that depend on the answer:
* [lahman.md](/datasets/lahman.md)
* [sabr-box-lahman-csv-share.md](/sources/sabr-box-lahman-csv-share.md)
* [sabr-lahman-database-page.md](/sources/sabr-lahman-database-page.md)
* PLAN.md §9 risk register (outside the bundle)
