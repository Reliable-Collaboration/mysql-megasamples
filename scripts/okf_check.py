#!/usr/bin/env python3
"""OKF v0.2 bundle checker and index generator for knowledge/.

Usage:
  python3 scripts/okf_check.py [--bundle knowledge] [--write-index] [--strict-links]

Requires PyYAML. Enforces the rules marked [checked] in
knowledge/runbooks/knowledge-bundle-conventions.md:
  1. every non-reserved .md has parseable, terminated YAML frontmatter with a non-empty `type`
  2. `status` and `trust` present and in their enums; `generated.at` ISO 8601; `verified` present iff trust == verified;
     `tags` is a list of strings; `sources[]` entries have `resource`; no sources[].title says "not read"
  3. type-specific required section headings, in order (prefix match)
  4. Dataset tier tags from the vocabulary; Decision status/trust agree with the `# Status` section
  5. trust: verified records may say "from memory" only in an **Inferred:**-marked line
  6. every markdown link (concepts, index.md, log.md) and every bundle-path `resource` resolves; broken links are
     warnings while root index.md says `bundle_status: draft`, errors when it says `stable` or with --strict-links
  7. log.md: only ISO-date `##` headings, descending; bullets start with an allowed bold verb
  8. every directory's index.md equals the generated form (--write-index regenerates, then validates)
Exit status 1 on any error, or when the bundle directory is missing or holds no concepts.
"""
import argparse, datetime, os, re, sys

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required: uv pip install pyyaml"); sys.exit(2)

RESERVED = {"index.md", "log.md"}
STATUS = {"draft", "stable", "deprecated"}
TRUST = {"verified", "inferred", "open"}
LOG_VERBS = {"Creation", "Update", "Verification", "Deviation", "Deprecation"}
TIER_TAGS = {"tier-core", "tier-core-medium", "tier-extended", "tier-generated", "tier-user-fetched", "tier-not-shipped"}
SECTIONS = {
    "Source": ["What was read", "Relevant excerpt", "What it was used to decide"],
    "Decision": ["Question", "Options considered", "Evidence", "Outcome", "Status"],
    "Dataset": ["Identity", "Source artifact", "Native format and friendlier forms", "Shape", "Conversion path",
                "Type-mapping hazards", "Programmable objects", "Indexing", "Tests and expected values",
                "Tier assignment", "License and attribution", "Open questions"],
    "License": ["Where the text lives", "Obligations", "Attribution", "Applied to"],
    "Tool": ["Facts", "Limits"],
    "Open Question": ["Question", "Cheapest experiment", "Resolves"],
    "Runbook": [],
}
ISO_DT = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2}))?$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^# (.+?)\s*$", re.M)
INTRO_OPEN, INTRO_CLOSE = "<!-- intro -->", "<!-- /intro -->"


def split_frontmatter(text):
    """Return (frontmatter_text, body, error)."""
    if not text.startswith("---\n"):
        return None, text, "no frontmatter"
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text, "unterminated frontmatter"
    return text[4:end], text[end + 5:], None


def parse_frontmatter(text):
    head, body, err = split_frontmatter(text)
    if err:
        return None, body, err
    try:
        data = yaml.safe_load(head)
    except yaml.YAMLError as e:
        return None, body, f"yaml error: {str(e).splitlines()[0]}"
    if not isinstance(data, dict):
        return None, body, "frontmatter is not a mapping"
    return data, body, None


def is_iso(value):
    if isinstance(value, (datetime.date, datetime.datetime)):
        return True
    return bool(ISO_DT.match(str(value)))


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def headings(body):
    return [h for h in HEADING_RE.findall(body)]


def section_text(body, name):
    m = re.search(r"^# " + re.escape(name) + r"\b.*?$\n(.*?)(?=^# |\Z)", body, re.M | re.S)
    return m.group(1) if m else ""


class Checker:
    def __init__(self, bundle, strict_links):
        self.bundle = bundle
        self.strict_links = strict_links
        self.errors, self.warnings = [], []
        self.concepts = {}
        self.bundle_status = "draft"

    def err(self, rel, msg): self.errors.append(f"{rel}: {msg}")
    def warn(self, rel, msg): self.warnings.append(f"{rel}: {msg}")

    def link_problem(self, rel, msg):
        if self.strict_links or self.bundle_status == "stable":
            self.err(rel, msg)
        else:
            self.warn(rel, msg)

    def resolve(self, rel, root, target):
        target = target.split("#")[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "file:", "s3://", "oci://")):
            return
        if target.startswith("/"):
            path = os.path.join(self.bundle, target.lstrip("/"))
        else:
            path = os.path.normpath(os.path.join(root, target))
        if not os.path.exists(path):
            self.link_problem(rel, f"broken link -> {target}")

    # ---- per-file checks -------------------------------------------------
    def check_concept(self, rel, root, text):
        fm, body, err = parse_frontmatter(text)
        if err:
            self.err(rel, err); return None
        typ = fm.get("type")
        if not typ or not isinstance(typ, str):
            self.err(rel, "missing or empty `type`")
        st, tr = fm.get("status"), fm.get("trust")
        if st not in STATUS: self.err(rel, f"status `{st}` not in {sorted(STATUS)}")
        if tr not in TRUST: self.err(rel, f"trust `{tr}` not in {sorted(TRUST)}")
        gen = fm.get("generated")
        if not isinstance(gen, dict) or not is_iso(gen.get("at", "")):
            self.err(rel, "generated.at missing or not ISO 8601")
        has_verified = bool(fm.get("verified"))
        if tr == "verified" and not has_verified: self.err(rel, "trust=verified but no `verified` entries")
        if tr != "verified" and has_verified: self.err(rel, f"trust={tr} but has `verified` entries")
        if tr == "open" and st != "draft": self.err(rel, "trust=open requires status=draft")
        tags = fm.get("tags", [])
        if tags is None: tags = []
        if not isinstance(tags, list) or any(not isinstance(t, str) for t in tags):
            self.err(rel, f"tags must be a list of strings (quote numeric-looking tags): {tags}")
            tags = [str(t) for t in (tags if isinstance(tags, list) else [])]
        for s in fm.get("sources") or []:
            if not isinstance(s, dict) or not s.get("resource"):
                self.err(rel, "sources[] entry without `resource`"); continue
            if re.search(r"\bnot read\b", str(s.get("title", "")), re.I):
                self.err(rel, "sources[] lists a document marked 'not read' (cite only what was opened)")
            if isinstance(s["resource"], str) and s["resource"].startswith("/"):
                self.resolve(rel, root, s["resource"])
        res = fm.get("resource")
        if isinstance(res, str) and res.startswith("/"):
            self.resolve(rel, root, res)
        # sections
        hs = headings(body)
        req = SECTIONS.get(typ, [])
        if typ not in SECTIONS:
            self.err(rel, f"unknown type `{typ}` (allowed: {sorted(SECTIONS)})")
        found = []
        for name in req:
            idx = next((i for i, h in enumerate(hs) if h == name or h.startswith(name + " ") or h.startswith(name + ":")), None)
            if idx is None:
                self.err(rel, f"{typ} record missing section `# {name}`")
            else:
                found.append(idx)
        if found != sorted(found):
            self.err(rel, f"{typ} sections out of order: {[hs[i] for i in found]} (expected {req})")
        if typ == "Dataset":
            tiers = [t for t in tags if t.startswith("tier-")]
            bad = [t for t in tiers if t not in TIER_TAGS]
            if bad: self.err(rel, f"tier tags {bad} not in vocabulary {sorted(TIER_TAGS)}")
            if not tiers: self.err(rel, "Dataset record has no tier-* tag")
        if typ == "Decision":
            status_text = section_text(body, "Status").strip().lower()
            if status_text.startswith("accepted"):
                if st != "stable" or tr == "open": self.err(rel, "Status says accepted but status/trust say draft/open")
                if "pending" in tags: self.err(rel, "accepted decision still tagged `pending`")
                if re.search(r"pending coordinator|coordinator to confirm", str(fm.get("title", "")) + str(fm.get("description", "")), re.I):
                    self.err(rel, "accepted decision still described as pending in title/description")
            elif status_text.startswith("pending"):
                if st != "draft" or tr != "open": self.err(rel, "Status says pending but status/trust are not draft/open")
        if typ == "License":
            if not section_text(body, "Attribution").strip(): self.err(rel, "License record has an empty `# Attribution` section")
        if tr == "verified":
            for line in body.splitlines():
                if re.search(r"from memory", line, re.I) and "**Inferred" not in line:
                    self.err(rel, "verified record says 'from memory' outside an **Inferred:** line")
                    break
        # links
        for target in LINK_RE.findall(strip_code(body)):
            self.resolve(rel, root, target)
        return fm

    def check_log(self, rel, text):
        heads = re.findall(r"^## (.*)$", text, re.M)
        dates = []
        for h in heads:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", h.strip()):
                self.err(rel, f"log heading is not a bare ISO date: `{h}`")
            else:
                dates.append(h.strip())
        if dates != sorted(dates, reverse=True):
            self.err(rel, f"date headings not in descending order: {dates}")
        for line in text.splitlines():
            if line.startswith("* "):
                m = re.match(r"\* \*\*([A-Za-z]+)\*\*:", line)
                if not m or m.group(1) not in LOG_VERBS:
                    self.err(rel, f"log bullet must start with a bold verb from {sorted(LOG_VERBS)}: `{line[:60]}`")
        for target in LINK_RE.findall(strip_code(text)):
            self.resolve(rel, os.path.join(self.bundle), target)

    # ---- index generation -------------------------------------------------
    def expected_index(self, root, existing):
        rel_root = os.path.relpath(root, self.bundle)
        is_root = rel_root == "."
        files = sorted(f for f in os.listdir(root) if f.endswith(".md") and f not in RESERVED and os.path.isfile(os.path.join(root, f)))
        subdirs = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))
                         and any(x.endswith(".md") for x in os.listdir(os.path.join(root, d))))
        lines = []
        if is_root:
            lines += ["---", 'okf_version: "0.2"', f"bundle_status: {self.bundle_status}", "---", ""]
        lines.append("# Knowledge bundle" if is_root else f"# {rel_root}")
        lines.append("")
        if is_root:
            intro = ""
            if existing and INTRO_OPEN in existing and INTRO_CLOSE in existing:
                intro = existing[existing.index(INTRO_OPEN) + len(INTRO_OPEN):existing.index(INTRO_CLOSE)].strip("\n")
            lines += [INTRO_OPEN, intro, INTRO_CLOSE, ""]
        if subdirs:
            lines.append("## Directories")
            for d in subdirs:
                n = len([x for x in os.listdir(os.path.join(root, d)) if x.endswith(".md") and x not in RESERVED])
                lines.append(f"* [{d}/]({d}/index.md) - {n} concepts")
            lines.append("")
        if files:
            lines.append("## Concepts")
            for f in files:
                fm = self.concepts.get(os.path.relpath(os.path.join(root, f), self.bundle)) or {}
                title = str(fm.get("title") or f)
                desc = str(fm.get("description") or "")
                lines.append(f"* [{title}]({f}) - {desc}".rstrip(" -"))
            lines.append("")
        return "\n".join(lines)

    def run(self, write_index):
        if not os.path.isdir(self.bundle):
            self.err(self.bundle, "bundle directory does not exist"); return
        root_index = os.path.join(self.bundle, "index.md")
        if os.path.exists(root_index):
            fm, _, _ = parse_frontmatter(open(root_index, encoding="utf-8").read())
            if isinstance(fm, dict):
                self.bundle_status = str(fm.get("bundle_status", "draft"))
                if str(fm.get("okf_version")) != "0.2": self.err("index.md", "root index must declare okf_version: \"0.2\"")
        if self.bundle_status not in {"draft", "stable"}:
            self.err("index.md", f"bundle_status must be draft or stable, got {self.bundle_status}")
        # pass 1: concepts and log
        for root, dirs, files in os.walk(self.bundle):
            dirs.sort()
            for f in sorted(files):
                if not f.endswith(".md"): continue
                path = os.path.join(root, f)
                rel = os.path.relpath(path, self.bundle)
                try:
                    text = open(path, encoding="utf-8").read()
                except UnicodeDecodeError as e:
                    self.err(rel, f"not UTF-8: {e}"); continue
                if f == "log.md":
                    self.check_log(rel, text); continue
                if f == "index.md":
                    continue
                fm = self.check_concept(rel, root, text)
                if fm is not None:
                    self.concepts[rel] = fm
        if not self.concepts:
            self.err(self.bundle, "no concept files found")
        # pass 2: indexes
        for root, dirs, files in os.walk(self.bundle):
            dirs.sort()
            has_md = any(f.endswith(".md") for f in files) or any(
                any(x.endswith(".md") for x in os.listdir(os.path.join(root, d))) for d in dirs)
            if not has_md: continue
            idx = os.path.join(root, "index.md")
            rel = os.path.relpath(idx, self.bundle)
            existing = open(idx, encoding="utf-8").read() if os.path.exists(idx) else ""
            expected = self.expected_index(root, existing)
            if write_index and existing != expected:
                open(idx, "w", encoding="utf-8").write(expected); existing = expected
            if existing != expected:
                self.err(rel, "index.md differs from the generated form (run --write-index)")
            for target in LINK_RE.findall(strip_code(existing)):
                self.resolve(rel, root, target)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", default="knowledge")
    ap.add_argument("--write-index", action="store_true")
    ap.add_argument("--strict-links", action="store_true")
    a = ap.parse_args()
    c = Checker(a.bundle, a.strict_links)
    c.run(a.write_index)
    types = {}
    for fm in c.concepts.values():
        types[str(fm.get("type"))] = types.get(str(fm.get("type")), 0) + 1
    print(f"{len(c.concepts)} concepts: " + ", ".join(f"{k}={v}" for k, v in sorted(types.items())) + f"; bundle_status={c.bundle_status}")
    for w in c.warnings: print("WARN", w)
    for e in c.errors: print("ERROR", e)
    print(f"{len(c.errors)} errors, {len(c.warnings)} warnings")
    sys.exit(1 if c.errors else 0)


if __name__ == "__main__":
    main()
