---
type: Runbook
title: Knowledge bundle conventions
description: "How every record in this OKF v0.2 bundle is written, typed, trusted, sectioned, indexed and logged; the checker in scripts/okf_check.py enforces the rules marked [checked]."
resource: /runbooks/knowledge-bundle-conventions.md
tags: [okf, conventions, process]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T22:23:40Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T22:23:40Z" }
sources:
  - resource: https://raw.githubusercontent.com/GoogleCloudPlatform/open-knowledge-format/main/SPEC.md
    title: Open Knowledge Format SPEC.md (v0.2)
    accessed: "2026-09-02"
  - resource: https://okf.md/spec/
    title: OKF annotated guide
    accessed: "2026-09-02"
---

# Purpose

This bundle conforms to **OKF v0.2** as published in [the spec record](/sources/okf-spec-v0-2.md). The spec requires only `type`; everything else here is a project convention layered on top, which the spec permits ("producers may add custom fields; consumers must preserve unknown keys"). Rules marked **[checked]** are enforced by `scripts/okf_check.py` (PyYAML is required; there is no fallback parser). Revision 2 of this runbook (2026-09-02, after the first code review) replaced the contradictory trust wording of revision 1 and made the source-granularity and section rules explicit; see [review dispositions](/decisions/review-2026-09-02-dispositions.md).

# Directory groups and concept types

| Directory | `type` value | One file per |
|---|---|---|
| `datasets/` | `Dataset` | dataset in the inventory (source artifact, shape, conversion hazards, tier, tests) |
| `licenses/` | `License` | license text or terms document (where it lives, obligations, attribution wording, which datasets it applies to) |
| `tools/` | `Tool` | tool or product used at build time (version, license, verified behaviour, limits) |
| `decisions/` | `Decision` | judgment call (question, options, evidence links, outcome, status) |
| `sources/` | `Source` | source artifact actually read (see granularity rule) |
| `runbooks/` | `Runbook` | repeatable procedure |
| `questions/` | `Open Question` | unresolved fact plus the cheapest experiment that resolves it |

# Frontmatter template **[checked]**

```yaml
---
type: Dataset                      # one of the seven types above; non-empty
title: "Sakila"                    # quote any scalar containing ': ' or ' #'
description: "One sentence."
resource: https://...              # canonical URI of the thing described (upstream URL, or bundle path for abstract concepts)
tags: [tier-core, mysql-native]    # strings only; quote numeric-looking tags ("9.7")
status: stable                     # required: draft | stable | deprecated
trust: verified                    # required: verified | inferred | open   (see Trust rules)
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }   # ISO 8601; quote it
verified:                          # present if and only if trust == verified
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:05:32Z" }
sources:                           # every URL here was actually opened on the accessed date
  - resource: https://...
    title: "Page title"
    accessed: "2026-09-02"
    version: "v1.2 / commit abc123 / snapshot date"   # when applicable; quote it
stale_after: "2027-03-01"          # optional; version pins and download URLs
---
```

# Trust rules **[checked where noted]**

* `trust: verified`: every **load-bearing** claim (a claim a decision or test relies on) was read in an authoritative source listed under `sources`, or produced by a command whose output is recorded. A verified record **may** contain inferences, provided each is delimited: a sentence or bullet prefixed **Inferred:** or a section headed `# Inferred`. The record-level value therefore describes the load-bearing claims, not every sentence. Rationale: downgrading a record because it carries a clearly marked aside would hide the fact that its quotations were read.
* `trust: inferred`: the record's central claim or outcome rests on reasoning, memory or estimation rather than on a read source. No `verified` key.
* `trust: open`: the record is a question; `status: draft`. Used for `Open Question` records and for a `Decision` whose outcome is still pending.
* Unmarked hedges: the phrase "from memory" may appear in a `trust: verified` record only inside an **Inferred:**-marked sentence **[checked]**. Prefer replacing it with a link to the record that verifies the fact.
* `sources[]` lists only documents that were opened; a document that could not be read is mentioned in the body, never under `sources`. A `sources[].title` containing "not read" is rejected **[checked]**.
* A from-memory fact the plan depends on gets an open question; a from-memory fact that is merely explanatory stays an **Inferred:** aside.

# Source record granularity

One `Source` record per **source artifact**: a single web page or document, a repository at a pinned commit (several files may be read), a set of manual pages read for one purpose, or one API probe. Every URL read is listed under `sources` (this is what OKF's list-valued `sources` is for). A record must not mix unrelated artifacts (two vendors, two repositories) and must not be split into one record per file when the files belong to one artifact.

# Required sections per type **[checked]** (heading prefix match; a parenthetical suffix is allowed)

| Type | Required `#` headings, in this order |
|---|---|
| Source | `What was read`, `Relevant excerpt`, `What it was used to decide` |
| Decision | `Question`, `Options considered`, `Evidence`, `Outcome`, `Status` |
| Dataset | `Identity`, `Source artifact`, `Native format and friendlier forms`, `Shape`, `Conversion path`, `Type-mapping hazards`, `Programmable objects`, `Indexing`, `Tests and expected values`, `Tier assignment`, `License and attribution`, `Open questions` |
| License | `Where the text lives`, `Obligations`, `Attribution`, `Applied to` |
| Tool | `Facts`, `Limits` (optional: `Inferred`, `Open questions`, `Decision`) |
| Open Question | `Question`, `Cheapest experiment`, `Resolves` |
| Runbook | free |

The `# Attribution` section of a License record holds the exact wording the repository ships (or "None required" plus any courtesy line); `scripts/gen_provenance.py` reads it. The `# Applied to` section lists every dataset or tool record that links to the license.

# Decision status consistency **[checked]**

A Decision whose `# Status` section begins with `accepted` has `status: stable` and `trust` ≠ `open`, and carries no `pending` tag. A Decision whose `# Status` begins with `pending` has `status: draft` and `trust: open`. Deprecated decisions have `status: deprecated` and a `superseded-by` link in `# Status`.

# Tier tags for Dataset records **[checked]**

Vocabulary: `tier-core`, `tier-core-medium`, `tier-extended`, `tier-generated`, `tier-user-fetched`, `tier-not-shipped`. A dataset shipped as a core subset plus an extended full load carries both `tier-core` and `tier-extended`. The authoritative table is [tier assignments](/decisions/tier-assignments.md); a record's tags and its `# Tier assignment` section must agree with it.

# Links **[checked]**

Absolute bundle links (`/datasets/sakila.md`) are preferred. Links in every file (concepts, `index.md`, `log.md`) and bundle paths in `resource` / `sources[].resource` are resolved; a broken link is a warning while the root `index.md` declares `bundle_status: draft` and an error once it declares `bundle_status: stable` (or with `--strict-links`).

# index.md and log.md **[checked]**

* Every directory has an `index.md` generated by `scripts/okf_check.py --write-index` (no frontmatter except the root's `okf_version: "0.2"` and `bundle_status`); the root intro paragraph between `<!-- intro -->` markers is preserved across regenerations. A hand-edited index that differs from the generated form fails the check.
* `log.md` at the root: `## YYYY-MM-DD` headings only, newest first; every bullet starts with one of **Creation**, **Update**, **Verification**, **Deviation**, **Deprecation**.
* A **Deviation** entry is mandatory whenever the executor departs from `PLAN.md`; it links to the updated Decision record that carries the evidence.

# Templates

Source body: `# What was read` (URL, access date, version/commit/snapshot, size if a download), `# Relevant excerpt` (verbatim quotation, or paraphrase marked as such), `# What it was used to decide` (links).
Decision body: `# Question`, `# Options considered` (each with the reason it lost), `# Evidence` (links), `# Outcome`, `# Status` (`accepted` | `pending` | `superseded-by <link>`).
Open Question body: `# Question`, `# Cheapest experiment`, `# Resolves` (what it unblocks).

# When to update versus create

* New fact about an existing dataset/tool → update that record, bump `generated.at`, add the new source to `sources`, log an **Update**. Re-stamp `verified` only when the load-bearing claims were re-checked.
* New artifact read → new `sources/` record.
* New judgment call → new `decisions/` record; if it replaces an earlier one, set the old one `status: deprecated` and link `superseded-by`.
* Measurement taken during execution (row count, checksum, load time, tool version) → update the dataset record's `# Tests and expected values` and log a **Verification** with the command that produced it.
