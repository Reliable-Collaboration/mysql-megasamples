---
type: Source
title: Wikidata:Database download
description: Official description of the Wikidata dump formats (JSON weekly, RDF full/truthy, lexemes, XML warning, incremental).
resource: https://www.wikidata.org/wiki/Wikidata:Database_download
tags: [source, wikidata, dumps]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.wikidata.org/wiki/Wikidata:Database_download
    title: Wikidata:Database download
    accessed: "2026-09-02"
---

# What was read
The page on 2026-09-02.

# Relevant excerpt
> "JSON dumps containing all Wikidata entities in a single JSON array can be found under https://dumps.wikimedia.org/wikidatawiki/entities/." — "being created on a weekly basis" — the recommended format.
> RDF: canonical "Turtle and NTriples formats"; "truthy" dumps contain "direct values of best-rank statements" without qualifiers and references.
> "The dumps of Wikidata Lexeme namespace in Turtle and NTriples formats can be found in the same place with _lexemes_ suffix."
> "The format of the JSON data embedded in the XML dumps is subject to change without notice" — use JSON/RDF instead.
> "Incremental dumps contain stuff that was added in the last 24 hours".
> "All structured data from the main, Property, Lexeme, and EntitySchema namespace is available under the Creative Commons CC0 License."

# What it was used to decide
Extract options and their reproducibility in [Wikidata dataset](/datasets/wikidata.md).
