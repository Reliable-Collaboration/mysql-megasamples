---
type: Source
title: GitHub release "AdventureWorks sample databases" (tag adventureworks) and older tags
description: Asset list with exact byte sizes for the adventureworks, adventureworks2012 and adventureworks2008r2 release tags, read through the GitHub releases API.
resource: https://github.com/microsoft/sql-server-samples/releases/tag/adventureworks
tags: [adventureworks, release, download]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:20:00Z" }
sources:
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/releases/tags/adventureworks
    title: releases/tags/adventureworks (published 2017-12-12, assets updated since)
    accessed: 2026-09-02
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/releases/tags/adventureworks2012
    title: releases/tags/adventureworks2012 (published 2018-02-28)
    accessed: 2026-09-02
  - resource: https://api.github.com/repos/microsoft/sql-server-samples/releases/tags/adventureworks2008r2
    title: releases/tags/adventureworks2008r2 (published 2017-09-22)
    accessed: 2026-09-02
stale_after: 2027-03-01
---

# What was read
`gh api repos/microsoft/sql-server-samples/releases/tags/<tag>` for the three tags; asset `name` and `size` fields. Download URLs follow `https://github.com/microsoft/sql-server-samples/releases/download/<tag>/<asset>`; no authentication or click-through is required. GitHub does not publish checksums for release assets (none in the API response).

# Assets, tag `adventureworks` (bytes)
* OLTP .bak: AdventureWorks2012.bak 47,078,400; AdventureWorks2014.bak 46,759,936; AdventureWorks2016.bak 48,749,568; AdventureWorks2016_EXT.bak 131,107,840; AdventureWorks2017.bak 50,286,592; AdventureWorks2019.bak 208,789,504; AdventureWorks2022.bak 209,838,080; AdventureWorks2025.bak 50,229,248.
* DW .bak: AdventureWorksDW2012.bak 22,822,912; DW2014 22,450,176; DW2016 22,484,480; DW2016_EXT 926,232,064; DW2017 23,436,800; DW2019 101,834,752; DW2022 101,834,752; DW2025 25,305,088.
* LT .bak: AdventureWorksLT2012.bak 14,077,952; LT2014 13,983,744; LT2016 7,458,816; LT2017 7,458,816; LT2019 8,511,488; LT2022 8,511,488; LT2025 1,765,376.
* Script zips: AdventureWorks-oltp-install-script.zip 17,486,641; AdventureWorksDW-data-warehouse-install-script.zip 16,765,004; adventure-works-2014-oltp-in-memory-sample.zip 12,169; sql-server-2016-samples.zip 6,679,391.
* No LT install-script zip exists on this tag.

# Assets, tag `adventureworks2012`
adventure-works-2012-oltp-script.zip 20,542,928; adventure-works-2012-oltp-lt-script.zip **937,314** (the AdventureWorksLT install-script form, see [its source record](/sources/github-microsoft-sql-server-samples-adventureworks-2012-lt-script.md)); adventure-works-2012-oltp-cs-script.zip 20,543,448; .mdf/.ldf data files (oltp 198,180,864; dw 211,025,920; lt 6,225,920 + 2,097,152 log); adventure-works-2012-oltp-full-database-backup.zip 38,050,469; adventure-works-2012-dw-images.zip 7,989,008.

# Assets, tag `adventureworks2008r2`
adventure-works-2008r2-oltp.bak 189,906,944; -dw.bak 77,709,312; -lt.bak 6,406,144; -oltp-script.zip 20,554,971; -dw-script.zip 9,233,425; -lt-script.zip 937,692; .mdf files; -full-database-backup.zip 36,940,053.

# What it was used to decide
Source-artifact sections of [AdventureWorks OLTP](/datasets/adventureworks-oltp.md), [DW](/datasets/adventureworks-dw.md), [LT](/datasets/adventureworks-lt.md); [conversion-path decision](/decisions/mssql-adventureworks-conversion-path.md).
