---
type: Source
title: Meta SE 412018 — "Fabricated data in posts.xml for multiple/all data dumps" (2025-08-12)
description: Community discovery, and staff confirmation, that dumps from July 2025 contain two synthetic watermark posts (Ids 1000000001 and 1000000010) — found in the dba.stackexchange dump.
resource: https://meta.stackexchange.com/questions/412018/fabricated-data-in-posts-xml-for-multiple-all-data-dumps
tags: [source, stackexchange, watermark, data-quality]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://api.stackexchange.com/2.3/questions/412018?site=meta&filter=withbody
    title: question body and top answer (Thomas Owens, score 32) via API
    accessed: "2026-09-02"
---

# What was read
Question body and highest-voted answer on 2026-09-02.

# Relevant excerpt
> "I recently pulled down the dba.stackexchange data dump ... The ID values ... for the bottom two rows are bizarrly 1000000001 & 1000000010." Sample row: `<row Id="1000000001" PostTypeId="1" CreationDate="2025-06-01T01:00:00.100" ... Title="Best practice for sharding a SQL Server 2027 database with 100M daily writes on NVMe" Tags="&lt;sharding&gt;" ... ContentLicense="CC BY-SA 4.0" />`
> Top answer quoting the staff answer: "yes, this is a watermark on the data dump." and staff: "When we made the decision to include these posts with security and safety in mind, we knew this would get caught quickly by the community, and that was intentional".

# What it was used to decide
The "delete Id >= 1000000000" rule for any post-2025 dump in [Stack Exchange dataset](/datasets/stackexchange.md) and [terms record](/licenses/stackexchange-data-dump-terms.md).
