---
type: Decision
title: Ship Simple English Wikipedia; do not ship a Wikidata extract (coordinator to confirm)
description: Between the two Wikimedia text-heavy candidates, recommend Simple English Wikipedia (356 MB artifact, MySQL-native link tables, CC BY-SA) over any Wikidata extract (43-253 GB official dumps, no reproducible small subset).
resource: /decisions/wikidata-vs-wikipedia-simple.md
tags: [decision, wikidata, wikipedia, scope, text-group]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://dumps.wikimedia.org/wikidatawiki/entities/
    accessed: 2026-09-02
  - resource: https://dumps.wikimedia.org/simplewiki/latest/
    accessed: 2026-09-02
  - resource: https://www.wikidata.org/wiki/Wikidata:Database_download
    accessed: 2026-09-02
---

# Question
Should the image include Wikidata, Simple English Wikipedia, or both?

# Options considered
1. **Simple English Wikipedia only** — one 356 MB XML + ~185 MB of SQL dumps; tables already in MySQL dialect; recognisable "Wikipedia in MySQL" sample; CC BY-SA + GFDL attribution handled per row.
2. Wikidata full — 103 GB JSON (or 43 GB truthy); impossible in a sample image.
3. Wikidata Lexemes (452 MB JSON) — tractable but obscure; bespoke schema.
4. Wikidata subset seeded by simplewiki's `wbc_entity_usage` — reproducible but requires streaming the 103 GB dump at build time.
5. Both 1 and 4 as "extended-large".

# Evidence
[Wikidata entity sizes](/sources/wikimedia-dumps-wikidata-entities-listing.md); [wikidatawiki SQL sizes](/sources/wikimedia-dumps-wikidatawiki-latest-listing.md); [Database download page](/sources/wikidata-database-download-page.md) (JSON weekly; XML discouraged); [simplewiki listing](/sources/wikimedia-dumps-simplewiki-latest-listing.md); dataset records [Wikidata](/datasets/wikidata.md) and [Simple English Wikipedia](/datasets/wikipedia-simple.md).

# Outcome (recommendation)
Option 1 now; document option 4 as a future opt-in. Wikidata's CC0 license is the friendliest of all candidates, but licensing does not compensate for a 100 GB build input with no dated small extract.

# Status
accepted by the coordinator on 2026-09-02: ship Simple English Wikipedia (extended, with a deterministic core sample); Wikidata is not shipped. Option 5 (simplewiki-seeded item subset) stays documented in [the Wikidata record](/datasets/wikidata.md) as a possible future extended-large dataset.
