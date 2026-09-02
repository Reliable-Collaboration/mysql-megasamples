---
type: Dataset
title: Wikidata (candidate — not recommended; prefer Simple English Wikipedia)
description: CC0 structured data whose official dumps are 43-253 GB; no small official relational-friendly extract exists, so a reproducible bundle is impractical; recorded as a candidate with the extract options evaluated.
resource: https://dumps.wikimedia.org/wikidatawiki/entities/
tags:
- tier-not-shipped
- dataset
- candidate
- cc0
- wikidata
- text-group
status: draft
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
stale_after: "2026-12-01"
sources:
- resource: https://dumps.wikimedia.org/wikidatawiki/entities/
  title: entity dump listing (2026-09-02)
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/wikidatawiki/latest/
  title: wikidatawiki SQL/XML listing
  accessed: "2026-09-02"
- resource: https://www.wikidata.org/wiki/Wikidata:Licensing
  title: Wikidata:Licensing
  accessed: "2026-09-02"
- resource: https://www.wikidata.org/wiki/Wikidata:Database_download
  title: Wikidata:Database download
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/legal.html
  title: dumps legal notice
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/simplewiki/latest/
  title: simplewiki listing (wbc_entity_usage.sql.gz)
  accessed: "2026-09-02"
---

# Identity
Wikidata, the Wikimedia knowledge base. Proposed MySQL database name if ever built: **`wikidata`**. Status: candidate; recommendation below is to ship [Simple English Wikipedia](/datasets/wikipedia-simple.md) instead ([decision, accepted](/decisions/wikidata-vs-wikipedia-simple.md)).

# Source artifact
Official dumps ([listing](/sources/wikimedia-dumps-wikidata-entities-listing.md), 2026-09-02): `latest-all.json.bz2` **102,943,257,005 bytes** (weekly, "the recommended format" — [Database download](/sources/wikidata-database-download-page.md)); `latest-all.json.gz` 155.9 GB; `latest-all.ttl.bz2` 125.2 GB; `latest-all.nt.bz2` 195.3 GB; `latest-truthy.nt.bz2` 43.3 GB; `latest-lexemes.json.bz2` 452.0 MB; `latest-lexemes.ttl.bz2` 635.7 MB. MediaWiki-table dumps of wikidatawiki ([listing](/sources/wikimedia-dumps-wikidatawiki-latest-listing.md)): `page.sql.gz` 3.61 GB, `page_props.sql.gz` 1.56 GB, `pagelinks.sql.gz` 9.42 GB — metadata only, no entity content, still multi-GB. No auth. Checksums exist per run directory (md5sums.txt, 55,722 bytes for wikidatawiki-latest).

# Native format and friendlier forms
JSON array of entity documents (labels/descriptions/aliases per language, claims with qualifiers/references/ranks, sitelinks); RDF (Turtle/N-Triples); XML dumps embed the JSON and are explicitly discouraged ("subject to change without notice"). Nothing relational is published; a faithful relational model needs ≥ 8 tables (entity, label, description, alias, claim, qualifier, reference, sitelink) and bespoke code.

# Shape
Not measured (nothing was downloaded). Entity counts are not stated on the pages read; **Inferred:** > 100 M items. The only sub-GB official entity dump is Lexemes (452 MB bz2 JSON).

# Conversion path (options evaluated)
1. Full JSON → relational: 103 GB download per build; out of scope for a sample image.
2. `latest-truthy.nt.bz2` (43 GB) → triple table: still 43 GB and a triple store, not a sample schema.
3. SPARQL-derived topical subset (query.wikidata.org): **not reproducible** — the endpoint is live (no dated snapshot), queries time out at 60 s, results change daily, and the service is not a download artifact with a checksum.
4. Lexemes JSON (452 MB) → `lexeme/form/sense/claim` tables: feasible size, CC0, weekly dated files with checksums; but Lexemes are an obscure corner of Wikidata and would not be recognisable as "the Wikidata sample".
5. Reproducible items subset seeded by simplewiki: `simplewiki-20260901-wbc_entity_usage.sql.gz` (9.9 MB) lists every Wikidata entity used by Simple English Wikipedia pages; filter a *dated* `wikidata-<date>-all.json.bz2` stream to those ids (**Inferred:** a few hundred thousand items). Deterministic given the two dated inputs, but the build must stream ~100 GB once — acceptable only as an "extended-large" opt-in.
Chosen: none for now (option 5 is the documented path if the coordinator wants Wikidata later).

# Type-mapping hazards
Multilingual labels (utf8mb4, all scripts, RTL); claim values are typed (time with precision/calendar, quantity with unit URI, globe-coordinate, monolingual text, external ids) → a value-type column plus JSON column; ranks and deprecated statements; snak types `novalue`/`somevalue` (NULL semantics).

# Programmable objects
None.

# Indexing
n/a.

# Tests and expected values
n/a until a path is chosen; a Lexeme/subset build would test entity count against the number of JSON documents streamed.

# Tier assignment
**None (not shipped).** Evidence: smallest general entity dump 43 GB; recommended JSON dump 103 GB. If option 5 is built: extended, opt-in.

# License and attribution
[CC0 1.0](/licenses/cc0-1-0.md): "All structured data in the main, property and lexeme namespaces is made available under the Creative Commons CC0 License" ([Wikidata:Licensing](/sources/wikidata-licensing-page.md)); text in other namespaces CC BY-SA 4.0. No attribution required; README courtesy line: "Data from Wikidata (https://www.wikidata.org/), CC0 1.0."

# Open questions
* Whether the coordinator wants an "extended-large" Wikidata subset at all — see [decision](/decisions/wikidata-vs-wikipedia-simple.md). No cheaper experiment than building option 5 once and timing it.
