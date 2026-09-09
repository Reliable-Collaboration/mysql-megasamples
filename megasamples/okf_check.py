#!/usr/bin/env python3
"""OKF v0.2 bundle checker and index generator for knowledge/.

Usage:
  python3 -m megasamples okf-check [--bundle knowledge] [--write-index] [--strict-links]

Requires PyYAML. Enforces the rules marked [checked] in
knowledge/runbooks/knowledge-bundle-conventions.md:
  1. every non-reserved .md has parseable, terminated YAML frontmatter with a non-empty string `type`
  2. `status` and `trust` are strings in their enums; `generated.at` ISO 8601; `verified` is a list of {by, at}
     present iff trust == verified; `tags` is a list of strings; `sources[]` entries have `resource`; no
     sources[].title says "not read"
  3. type-specific required section headings, in order (prefix match, code fences ignored)
  4. Dataset tier tags from the vocabulary; a Decision's `# Status` text agrees with `status`/`trust`/tags
     (accepted / pending / superseded-by)
  5. a trust: verified record says "from memory" only inside an **Inferred:**-marked paragraph or a `# Inferred`
     section (title and description included in the scan)
  6. every License record's `# Applied to` lists exactly the Dataset and Tool records that link it
  7. every markdown link (concepts, index.md, log.md) and every bundle-path `resource` resolves; broken links are
     warnings while root index.md says `bundle_status: draft`, errors when it says `stable` or with --strict-links
  8. log.md: only ISO-date `##` headings, descending; every bullet (`*` or `-`) starts with an allowed bold verb
  9. every directory's index.md equals the generated form; --write-index writes every index first, then validates
Exit status: 0 clean, 1 errors, 2 usage/environment problem (missing PyYAML).
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
LINK_RE = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
HEADING_RE = re.compile(r"^# (.+?)\s*$", re.M)
INTRO_OPEN, INTRO_CLOSE = "<!-- intro -->", "<!-- /intro -->"
EXTERNAL = ("http://", "https://", "mailto:", "file:", "s3://", "oci://", "ftp://")


def split_frontmatter(text):
    """Return (frontmatter_text, body, error). Tolerates a UTF-8 BOM and CRLF line endings."""
    text = text.lstrip("﻿").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None, text, "no frontmatter"
    end = text.find("\n---\n", 4)
    if end < 0:
        if text.endswith("\n---"):
            return text[4:-4], "", None
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
    return isinstance(value, str) and bool(ISO_DT.match(value))


def strip_code(text):
    """Blank out fenced code blocks and inline code so prose scans cannot see code content.

    A fence opens with three or more backticks or tildes and closes only with the same character and at
    least as many of them; an unclosed fence swallows the rest of the file (the safe reading).
    """
    out, fence = [], None
    for line in text.split("\n"):
        stripped = line.strip()
        m = re.match(r"^(`{3,}|~{3,})(.*)$", stripped)
        if fence is None:
            if m:
                fence = m.group(1)
                out.append("")
                continue
        else:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
                fence = None
            out.append("")
            continue
        out.append(line)
    return re.sub(r"`[^`\n]*`", "", "\n".join(out))


def headings(body):
    return HEADING_RE.findall(strip_code(body))


def section_text(body, name):
    m = re.search(r"^# " + re.escape(name) + r"\b.*?$\n(.*?)(?=^# |\Z)", strip_code(body), re.M | re.S)
    return m.group(1) if m else ""


def hedge_ok(body, title, description):
    """True unless 'from memory' appears outside an Inferred-marked paragraph or `# Inferred` section."""
    if re.search(r"from memory", f"{title} {description}", re.I):
        return False
    in_inferred_section, in_inferred_para = False, False
    for line in strip_code(body).splitlines():
        m = re.match(r"^(#+) (.*)$", line)
        if m:
            in_inferred_section = m.group(1) == "#" and m.group(2).strip().lower().startswith("inferred")
            in_inferred_para = False
        if not line.strip():
            in_inferred_para = False
        if "**Inferred" in line:
            in_inferred_para = True
        if re.search(r"from memory", line, re.I) and not (in_inferred_section or in_inferred_para):
            return False
    return True


class Checker:
    def __init__(self, bundle, strict_links):
        self.bundle = os.path.normpath(bundle)
        self.strict_links = strict_links
        self.errors, self.warnings = [], []
        self.concepts = {}   # rel -> frontmatter
        self.bodies = {}     # rel -> body
        self.links = {}      # rel -> set of bundle-relative link targets
        self.bundle_status = "draft"

    def err(self, rel, msg): self.errors.append(f"{rel}: {msg}")
    def warn(self, rel, msg): self.warnings.append(f"{rel}: {msg}")

    def link_problem(self, rel, msg):
        (self.err if self.strict_links or self.bundle_status == "stable" else self.warn)(rel, msg)

    def target_path(self, root, target):
        target = target.split("#")[0]
        if not target or target.startswith(EXTERNAL):
            return None
        if target.startswith("/"):
            return os.path.join(self.bundle, target.lstrip("/"))
        return os.path.normpath(os.path.join(root, target))

    def resolve(self, rel, root, target):
        path = self.target_path(root, target)
        if path is not None and not os.path.exists(path):
            self.link_problem(rel, f"broken link -> {target}")

    def bundle_rel(self, root, target):
        """Bundle-relative path ('/dir/file.md') of a link target, or None."""
        path = self.target_path(root, target)
        if path is None:
            return None
        return "/" + os.path.relpath(path, self.bundle).replace(os.sep, "/")

    # ---- per-file checks -------------------------------------------------
    def check_concept(self, rel, root, text):
        fm, body, err = parse_frontmatter(text)
        if err:
            self.err(rel, err); return None
        typ = fm.get("type")
        if not isinstance(typ, str) or not typ:
            self.err(rel, f"`type` must be a non-empty string, got {typ!r}"); typ = ""
        st, tr = fm.get("status"), fm.get("trust")
        if not isinstance(st, str) or st not in STATUS: self.err(rel, f"status must be one of {sorted(STATUS)}, got {st!r}")
        if not isinstance(tr, str) or tr not in TRUST: self.err(rel, f"trust must be one of {sorted(TRUST)}, got {tr!r}")
        gen = fm.get("generated")
        if not isinstance(gen, dict) or not is_iso(gen.get("at", "")):
            self.err(rel, "generated.at missing or not ISO 8601")
        ver = fm.get("verified")
        if ver is not None and (not isinstance(ver, list) or not ver or any(not isinstance(v, dict) or not v.get("by") or not is_iso(v.get("at", "")) for v in ver)):
            self.err(rel, "`verified` must be a non-empty list of {by, at} entries with ISO 8601 `at`"); ver = None
        if tr == "verified" and not ver: self.err(rel, "trust=verified but no `verified` entries")
        if tr != "verified" and ver: self.err(rel, f"trust={tr} but has `verified` entries")
        if tr == "open" and st != "draft": self.err(rel, "trust=open requires status=draft")
        tags = fm.get("tags") or []
        if not isinstance(tags, list) or any(not isinstance(t, str) for t in tags):
            self.err(rel, f"tags must be a list of strings (quote numeric-looking tags): {tags!r}")
            tags = [str(t) for t in tags] if isinstance(tags, list) else []
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
        # sections (code fences ignored)
        hs = headings(body)
        if typ and typ not in SECTIONS:
            self.err(rel, f"unknown type `{typ}` (allowed: {sorted(SECTIONS)})")
        req = SECTIONS.get(typ, [])
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
            status_text = re.sub(r"[*_`]", "", section_text(body, "Status")).strip().lower()
            head = re.sub(r"^status:\s*", "", status_text)
            desc = f"{fm.get('title', '')} {fm.get('description', '')}"
            if head.startswith("accepted"):
                if st != "stable" or tr == "open": self.err(rel, "Status says accepted but status/trust say draft/open")
                if "pending" in tags: self.err(rel, "accepted decision still tagged `pending`")
                if re.search(r"pending coordinator|coordinator to confirm|outcome pending", desc, re.I):
                    self.err(rel, "accepted decision still described as pending in title/description")
            elif head.startswith("pending"):
                if st != "draft" or tr != "open": self.err(rel, "Status says pending but status/trust are not draft/open")
            elif head.startswith("superseded"):
                if st != "deprecated": self.err(rel, "Status says superseded-by but status is not deprecated")
                if not LINK_RE.search(section_text(body, "Status")): self.err(rel, "superseded-by needs a link to the replacing decision")
            elif st == "deprecated":
                self.err(rel, "status: deprecated requires a `# Status` beginning with superseded-by <link>")
            elif not head:
                self.err(rel, "Decision `# Status` section is empty")
            else:
                self.err(rel, f"Decision `# Status` must begin with accepted, pending or superseded-by (got `{head[:30]}`)")
        if typ == "License" and not section_text(body, "Attribution").strip():
            self.err(rel, "License record has an empty `# Attribution` section")
        if tr == "verified" and not hedge_ok(body, fm.get("title", ""), fm.get("description", "")):
            self.err(rel, "verified record says 'from memory' outside an **Inferred:** paragraph or `# Inferred` section")
        targets = LINK_RE.findall(strip_code(body))
        for target in targets:
            self.resolve(rel, root, target)
        self.bodies[rel] = body
        self.links[rel] = {bl for bl in (self.bundle_rel(root, t) for t in targets) if bl}
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
            if re.match(r"^\s*[*-] ", line):
                m = re.match(r"^\s*[*-] \*\*([A-Za-z]+)\*\*:", line)
                if not m or m.group(1) not in LOG_VERBS:
                    self.err(rel, f"log bullet must start with a bold verb from {sorted(LOG_VERBS)}: `{line.strip()[:60]}`")
        for target in LINK_RE.findall(strip_code(text)):
            self.resolve(rel, self.bundle, target)

    def check_license_coverage(self):
        """Each License's `# Applied to` lists exactly the Dataset and Tool records that link it."""
        applies = {"Dataset", "Tool"}
        for lic_rel, fm in self.concepts.items():
            if fm.get("type") != "License":
                continue
            lic_link = "/" + lic_rel.replace(os.sep, "/")
            lic_root = os.path.join(self.bundle, os.path.dirname(lic_rel))
            applied = section_text(self.bodies[lic_rel], "Applied to")
            # omissions: any mention in the section counts as listed (generous, so only a record the
            # license never mentions is reported); stale entries: only a bullet's subject link is an
            # assertion that the license applies (conservative, so asides and negatives are not reported).
            mentioned = {bl for bl in (self.bundle_rel(lic_root, t) for t in LINK_RE.findall(applied)) if bl}
            subjects = set()
            for line in applied.splitlines():
                if not re.match(r"^\s*[*-] ", line):
                    continue
                text = re.sub(r"^\s*[*-] ", "", line)
                if re.match(r"(\*\*)?(not applied|see also|related|note)\b", text, re.I):
                    continue
                first = LINK_RE.search(text)
                if first:
                    bl = self.bundle_rel(lic_root, first.group(1))
                    if bl:
                        subjects.add(bl)
            linkers = {"/" + rel.replace(os.sep, "/") for rel, links in self.links.items()
                       if lic_link in links and self.concepts[rel].get("type") in applies}
            for link in sorted(linkers - mentioned):
                self.err(lic_rel, f"`# Applied to` omits {link}, which links this license")
            for link in sorted(subjects - linkers):
                rel = os.path.normpath(link.lstrip("/"))
                if rel in self.concepts and self.concepts[rel].get("type") in applies:
                    self.err(lic_rel, f"`# Applied to` lists {link}, which does not link this license")

    # ---- index generation -------------------------------------------------
    def dir_has_md(self, d):
        """True when the tree holds at least one concept file (a stale index.md alone does not count)."""
        for r, _, fs in os.walk(d):
            if any(f.endswith(".md") and f not in RESERVED for f in fs):
                return True
        return False

    def count_concepts(self, d):
        n = 0
        for r, _, fs in os.walk(d):
            n += sum(1 for f in fs if f.endswith(".md") and f not in RESERVED)
        return n

    def expected_index(self, root, existing):
        rel_root = os.path.relpath(root, self.bundle)
        is_root = rel_root == "."
        files = sorted(f for f in os.listdir(root) if f.endswith(".md") and f not in RESERVED and os.path.isfile(os.path.join(root, f)))
        subdirs = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and self.dir_has_md(os.path.join(root, d)))
        lines = []
        if is_root:
            lines += ["---", 'okf_version: "0.2"', f"bundle_status: {self.bundle_status}", "---", ""]
        lines.append("# Knowledge bundle" if is_root else f"# {rel_root.replace(os.sep, '/')}")
        lines.append("")
        if is_root:
            intro = ""
            if existing and INTRO_OPEN in existing and INTRO_CLOSE in existing:
                intro = existing[existing.index(INTRO_OPEN) + len(INTRO_OPEN):existing.index(INTRO_CLOSE)].strip("\n")
            lines += [INTRO_OPEN, intro, INTRO_CLOSE, ""]
        if subdirs:
            lines.append("## Directories")
            for d in subdirs:
                lines.append(f"* [{d}/]({d}/index.md) - {self.count_concepts(os.path.join(root, d))} concepts")
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
        self.check_license_coverage()
        # pass 2: indexes — write all first, then validate links
        index_dirs = [root for root, _, _ in os.walk(self.bundle) if self.dir_has_md(root)]
        contents = {}
        for root in index_dirs:
            idx = os.path.join(root, "index.md")
            existing = open(idx, encoding="utf-8").read() if os.path.exists(idx) else ""
            expected = self.expected_index(root, existing)
            if write_index and existing != expected:
                open(idx, "w", encoding="utf-8").write(expected); existing = expected
            contents[root] = (existing, expected)
        for root, (existing, expected) in contents.items():
            rel = os.path.relpath(os.path.join(root, "index.md"), self.bundle)
            if existing != expected:
                self.err(rel, "index.md differs from the generated form (run --write-index)")
            for target in LINK_RE.findall(strip_code(existing)):
                self.resolve(rel, root, target)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", default="knowledge")
    ap.add_argument("--write-index", action="store_true")
    ap.add_argument("--strict-links", action="store_true")
    a = ap.parse_args(argv)
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
