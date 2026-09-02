---
type: Runbook
title: Knowledge bundle conventions
description: How every record in this OKF v0.2 bundle is written, typed, trusted, indexed, and logged; the executor follows these rules verbatim.
resource: /runbooks/knowledge-bundle-conventions.md
tags: [okf, conventions, process]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
sources:
  - resource: https://raw.githubusercontent.com/GoogleCloudPlatform/open-knowledge-format/main/SPEC.md
    title: Open Knowledge Format SPEC.md (v0.2)
    accessed: 2026-09-02
  - resource: https://okf.md/spec/
    title: OKF annotated guide
    accessed: 2026-09-02
---

# Purpose

This bundle conforms to **OKF v0.2** as published in [the spec record](/sources/okf-spec-v0-2.md).
The spec requires only `type`; everything else here is a project convention layered on top,
which the spec explicitly permits ("producers may add custom fields; consumers must preserve unknown keys").

# Directory groups and concept types

| Directory | `type` value | One file per |
|---|---|---|
| `datasets/` | `Dataset` | dataset in the inventory (source artifact, shape, conversion hazards, tier, tests) |
| `licenses/` | `License` | license text (where the verbatim text lives, attribution wording, share-alike duties) |
| `tools/` | `Tool` | tool or product used at build time (version, license, verified behaviour, limits) |
| `decisions/` | `Decision` | judgment call (question, options, evidence links, outcome, status) |
| `sources/` | `Source` | document actually read during research (URL, access date, version, excerpt, what it decided) |
| `runbooks/` | `Runbook` | repeatable procedure (this file, troubleshooting, executor discipline) |
| `questions/` | `Open Question` | unresolved fact plus the cheapest experiment that resolves it |

# Frontmatter template

```yaml
---
type: Dataset                      # one of the seven types above
title: Sakila
description: One sentence.
resource: https://...              # canonical URI of the thing described (upstream URL, or bundle path for abstract concepts)
tags: [tier-core, mysql-native]
status: stable                     # spec field: draft | stable | deprecated  (draft == still being researched)
trust: verified                    # project field: verified | inferred | open   (see Trust rules)
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }   # spec field, ISO 8601
verified:                          # spec field; OMIT ENTIRELY when trust != verified
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
sources:                           # spec field; every URL here was actually opened on the accessed date
  - resource: https://...
    title: Page title
    accessed: 2026-09-02           # project field
    version: v1.2 / commit abc123 / snapshot date   # project field, when applicable
stale_after: 2027-03-01            # optional spec field; use for version pins and download URLs
---
```

# Trust rules

* `trust: verified` — every load-bearing claim in the body was read in an authoritative source listed under `sources`, and the `verified` list is present. Authoritative means: the vendor's documentation, the upstream repository, the license file itself, or output of a command the author ran.
* `trust: inferred` — derived by reasoning (size estimates, expected type-mapping behaviour, load-time guesses). No `verified` key. The body says what it was inferred from.
* `trust: open` — the record poses a question; `status: draft`; the body names the cheapest experiment that resolves it. Lives in `questions/` or is a `Decision` whose outcome is pending.
* A single file may contain both verified and inferred statements; in that case `trust` describes the file as a whole (use the weaker value) and inferred sentences inside a verified file are prefixed with **Inferred:**.
* Never cite a source that was not opened. If a fact came from memory, mark it inferred and add an open question to verify it.

# Source record body template (`sources/`)

```markdown
# What was read
URL, access date, version/commit/snapshot date, file size if a download.

# Relevant excerpt
> verbatim quotation (short) or close paraphrase marked as paraphrase

# What it was used to decide
Links to the Dataset / Decision / Tool records that rely on it.
```

# Decision record body template (`decisions/`)

```markdown
# Question
# Options considered
# Evidence
Links to sources/tools/datasets.
# Outcome
# Status
accepted | pending | superseded-by [link]
```

# Dataset record body template (`datasets/`)

Sections, in order: `# Identity`, `# Source artifact` (URL, version/snapshot, format, size, auth required?, checksum or how to obtain it),
`# Native format and friendlier forms`, `# Shape` (tables, row counts, sizes, encoding hazards),
`# Conversion path` (chosen tool + link to decision), `# Type-mapping hazards`, `# Programmable objects` (ported / stubbed / dropped),
`# Indexing`, `# Tests and expected values`, `# Tier assignment` (with evidence link), `# License and attribution` (link to `licenses/`),
`# Open questions`.

# Links

Use absolute bundle links (`/datasets/sakila.md`). Broken links are legal in OKF and mark records still to be written; a CI check reports them but does not fail on them until the executor marks the bundle `stable`.

# index.md and log.md

* Every directory has an `index.md` with no frontmatter (root `index.md` carries only `okf_version: "0.2"`), listing `* [Title](file.md) - description` for each concept.
* `log.md` at the root: ISO-date headings newest first; bullets start with a bold verb: **Creation**, **Update**, **Deprecation**, **Deviation**, **Verification**.
* A **Deviation** entry is mandatory whenever the executor departs from `PLAN.md`; it links to the updated Decision record that carries the evidence.

# When to update versus create

* New fact about an existing dataset/tool → update that record, bump `generated.at`, add the new source to `sources`, log an **Update**.
* New document read → new `sources/` record (never fold two documents into one source record).
* New judgment call → new `decisions/` record; if it replaces an earlier one, set the old one `status: deprecated` and link `superseded-by`.
* Measurement taken during execution (row count, checksum, load time, tool version) → update the dataset record's `# Tests and expected values` and log a **Verification** with the command that produced it.
