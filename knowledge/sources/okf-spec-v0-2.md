---
type: Source
title: Open Knowledge Format SPEC.md v0.2 (GitHub)
description: Authoritative OKF specification text, version 0.2, read from the GoogleCloudPlatform/open-knowledge-format repository.
resource: https://raw.githubusercontent.com/GoogleCloudPlatform/open-knowledge-format/main/SPEC.md
tags: [okf, spec]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
sources:
  - resource: https://raw.githubusercontent.com/GoogleCloudPlatform/open-knowledge-format/main/SPEC.md
    title: SPEC.md at main
    accessed: 2026-09-02
    version: main branch as of 2026-09-02 (commit not captured; executor should pin it)
---

# What was read
SPEC.md on branch main of https://github.com/GoogleCloudPlatform/open-knowledge-format, accessed 2026-09-02. Version stated in the document: **0.2**.

# Relevant excerpt
* Required field: `type` — "A short string identifying the kind of concept. Consumers use it for routing, filtering, and presentation."
* Recommended: `title`, `description`, `resource`, `tags`.
* v0.2 trust fields: `sources` (list; each entry has a required `resource`, optional `id`, `title`, `author`, `last_modified`, `usage_count`, `usage_window`), `generated: { by, at }` ("An ISO 8601 datetime marking the content's last meaningful change"), `verified` (list of `{ by, at }`).
* Trust tiers derived from `verified`: no key → unverified; only non-human actors → machine-confirmed; a human actor → human-reviewed.
* Actor identifiers: `<producer>/<version>` for agents, `human:<id>`, `process:<id>`.
* Lifecycle: `status: draft | stable | deprecated` (absent means stable); `stale_after` is "an absolute instant. A concept is stale when now >= stale_after".
* Reserved filenames: only `index.md` and `log.md`. `index.md` has no frontmatter except optional `okf_version: "0.2"` at the bundle root; body is sections of `* [Title](url) - description`.
* `log.md`: "A flat list of date-grouped entries, newest first", ISO 8601 date headings, bold verbs (**Update**, **Creation**, **Deprecation**).
* Links: absolute links begin with `/` relative to bundle root (recommended); "Consumers MUST tolerate broken links".
* Conformance: every non-reserved .md has parseable YAML frontmatter with non-empty `type`; reserved files follow their sections when present. Consumers must not reject for missing optional fields, unknown types, unknown keys, broken links, or missing index files.
* Versioning: `<major>.<minor>`; bundles may declare `okf_version: "0.2"` in the root `index.md`.
* Breaking changes from v0.1: `timestamp` superseded by `generated`; body `# Citations` superseded by frontmatter `sources`.
* v0.2 adds a prescribed type `Attested Computation` (not used by this project).

# What it was used to decide
[Knowledge bundle conventions](/runbooks/knowledge-bundle-conventions.md); the bundle root pins `okf_version: "0.2"`.
