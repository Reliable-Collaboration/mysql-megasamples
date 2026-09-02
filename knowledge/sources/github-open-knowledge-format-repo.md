---
type: Source
title: "GoogleCloudPlatform/open-knowledge-format repository tree and reference agent code"
description: "The repo ships SPEC.md, samples, bundles and a reference agent (Apache-2.0 header, google-adk dependency); the only validation is OKFDocument.validate() requiring `type`; no standalone validator CLI or PyPI package."
resource: https://github.com/GoogleCloudPlatform/open-knowledge-format
tags: [okf, validator]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://github.com/GoogleCloudPlatform/open-knowledge-format
    title: "GoogleCloudPlatform/open-knowledge-format repository tree and reference agent code"
    accessed: "2026-09-02"
    version: "main branch, read via GitHub API and raw files on 2026-09-02"
---

# What was read
https://github.com/GoogleCloudPlatform/open-knowledge-format, accessed 2026-09-02; version: main branch, read via GitHub API and raw files on 2026-09-02.

# Relevant excerpt
* Root: `.gitignore CODE_OF_CONDUCT.md CONTRIBUTING.md LICENSE.md README.md SPEC.md bundles/ connectors/ pyproject.toml samples/ src/ tests/`. No `tools/`, `okf/`, `scripts/` or `validator/` directory (each returned 404).
* `pyproject.toml`: project `reference-agent` 0.1.0, "Reference agent that produces Open Knowledge Format bundles", `requires-python >=3.11`, dependencies google-adk>=2.0, google-cloud-bigquery>=3.20, pyyaml>=6.0, pydantic>=2.0, markdownify>=0.11; script `reference-agent = reference_agent.cli:main`; Apache-2.0 license header.
* `src/reference_agent/bundle/`: `document.py` (comment "OKF v0.2 §11: `type` is the only always-required frontmatter key.", `REQUIRED_FRONTMATTER_KEYS = ("type",)`, `OKFDocument.parse/serialize/validate`, `normalize_verified`, `trust_tier`, `is_stale`; a YAML loader that disables timestamp resolution), `index.py` (`regenerate_indexes`), `paths.py`, `synthesizer.py`; `tools/bundle_tools.py`; tests `test_bundle_tools.py test_document.py test_index.py`.
* README mentions no `validate` command (grep for valid/lint/check found only a bundles/ note and a `pip install -e .[dev]` line).

# What it was used to decide
[OKF validator question](/questions/okf-validator-availability.md): nothing reusable beyond the ~100-line `document.py`; the project writes its own 40-line check.
