---
type: Open Question
title: "Is there an OKF v0.2 validator we can run in CI?"
description: "Neither GoogleCloudPlatform/open-knowledge-format nor knowledge-catalog ships a validator (only the reference agent's OKFDocument.validate requiring ); the PyPI  package is an unrelated stub; proposal: a 40-line Python check owned by this repository."
resource: /questions/okf-validator-availability.md
tags: [okf, validator, ci, process]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:51:18Z" }
sources:
  - resource: https://github.com/GoogleCloudPlatform/open-knowledge-format
    title: "open-knowledge-format repository tree, pyproject.toml, src/reference_agent/bundle/document.py and index.py"
    accessed: 2026-09-02
  - resource: https://github.com/GoogleCloudPlatform/knowledge-catalog
    title: "knowledge-catalog repository tree (okf/, toolbox/)"
    accessed: 2026-09-02
  - resource: https://pypi.org/pypi/okf/json
    accessed: 2026-09-02
  - resource: /sources/okf-spec-v0-2.md
    accessed: 2026-09-02
---

# What exists (verified)
* `open-knowledge-format` root: `SPEC.md`, `bundles/`, `connectors/`, `samples/`, `src/`, `tests/`, `pyproject.toml`; no `tools/`, `okf/`, `scripts/` or `validator/` (404 for each). The package is `reference-agent` 0.1.0 (Apache-2.0 header, `requires-python >=3.11`, depends on `google-adk>=2.0`, `google-cloud-bigquery`, `pyyaml`, `pydantic`, `markdownify`), a bundle-*producing* agent, not a checker ([repo record](/sources/github-open-knowledge-format-repo.md)).
* The only validation code: `src/reference_agent/bundle/document.py` — comment "OKF v0.2 §11: `type` is the only always-required frontmatter key.", `REQUIRED_FRONTMATTER_KEYS = ("type",)`, `OKFDocument.parse()` (YAML frontmatter with a loader that keeps timestamps as strings), `validate()` (missing `type` → error), plus `normalize_verified`, `trust_tier`, `is_stale`; `index.py` has `regenerate_indexes()`. No link checking, no index completeness check, no CLI entry point for validation (the only script is `reference-agent`).
* `knowledge-catalog` mirrors the same layout under `okf/` and adds `toolbox/` (Metadata-as-Code and an enrichment agent for Google's Knowledge Catalog) — nothing about OKF validation ([repo record](/sources/github-knowledge-catalog-repo.md)).
* PyPI `okf` 0.1.0 is "A CLI for OKF — Currently in development" by an individual author with no project URLs; not usable ([pypi record](/sources/pypi-okf.md)).
* Conformance rules to check come from the spec: frontmatter parseable YAML with non-empty `type`; reserved files `index.md`/`log.md`; consumers must tolerate broken links and unknown keys ([spec record](/sources/okf-spec-v0-2.md)); project conventions add `trust`, `verified` presence when `trust: verified`, absolute links, and an `index.md` per directory listing every file ([conventions](/runbooks/knowledge-bundle-conventions.md)).

# Cheapest experiment / proposal
Own the check. `scripts/okf_check.py` (PyYAML only), run in CI as a warning until the bundle is marked stable, then as a failure:

```python
#!/usr/bin/env python3
"""Minimal OKF v0.2 + project-convention check: frontmatter, type, trust/verified, links, index coverage."""
import re, sys, pathlib, yaml
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "knowledge")
TYPES = {"Dataset","License","Tool","Decision","Source","Runbook","Open Question"}
LINK = re.compile(r"\]\((/[^)#]+)")
errors, listed = [], {}
for md in ROOT.rglob("*.md"):
    rel = "/" + md.relative_to(ROOT).as_posix()
    text = md.read_text(encoding="utf-8")
    if md.name in ("index.md", "log.md"):
        if md.name == "index.md":
            listed[md.parent] = set(re.findall(r"\]\(([^)]+\.md)\)", text))
        continue
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{rel}: no YAML frontmatter"); continue
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        errors.append(f"{rel}: bad YAML: {e}"); continue
    if not fm.get("type"):
        errors.append(f"{rel}: missing required 'type'")
    elif fm["type"] not in TYPES:
        errors.append(f"{rel}: unknown type {fm['type']!r}")
    if fm.get("trust") == "verified" and not fm.get("verified"):
        errors.append(f"{rel}: trust: verified without a 'verified' list")
    if fm.get("trust") != "verified" and fm.get("verified"):
        errors.append(f"{rel}: 'verified' present but trust != verified")
    for link in LINK.findall(text):
        if not (ROOT / link.lstrip("/")).exists():
            errors.append(f"{rel}: broken link {link} (allowed while draft)")
    if md.name not in listed.get(md.parent, set()):
        errors.append(f"{rel}: not listed in {md.parent.name}/index.md")
print("\n".join(errors) or "OK")
sys.exit(1 if any("missing required" in e or "bad YAML" in e or "no YAML" in e for e in errors) else 0)
```
Exit status is non-zero only for spec violations (frontmatter/type); broken links and index gaps are reported but tolerated, matching the spec's consumer rules and the project's "broken links are legal until stable" convention.

# Status
Open until the script exists in the repository and has run once over this bundle (task P-00).
