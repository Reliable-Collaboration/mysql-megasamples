#!/usr/bin/env python3
"""OKF v0.2 bundle checker and index generator for knowledge/.

Usage:
  python3 scripts/okf_check.py [--bundle knowledge] [--write-index] [--strict-links]

Checks (spec conformance + project conventions, see knowledge/runbooks/knowledge-bundle-conventions.md):
  1. every non-reserved .md has parseable YAML frontmatter with non-empty `type`
  2. `status` in {draft, stable, deprecated}; `trust` in {verified, inferred, open};
     `generated.at` is ISO 8601; `verified` present iff trust == verified
  3. every absolute bundle link (/dir/file.md) and relative link resolves (reported; fails only with --strict-links)
  4. every directory index.md lists every concept file in that directory (written by --write-index)
  5. log.md date headings are ISO dates in descending order
No third-party dependencies: the frontmatter subset used here is parsed by a tiny reader (key: value,
lists of scalars, one-level mappings, and inline {a: b} / [a, b] forms). PyYAML is used when available.
"""
import argparse, datetime, os, re, sys

RESERVED = {"index.md", "log.md"}
STATUS = {"draft", "stable", "deprecated"}
TRUST = {"verified", "inferred", "open"}

def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, "no frontmatter"
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, "unterminated frontmatter"
    block = text[4:end]
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(block)
        if not isinstance(data, dict):
            return None, "frontmatter is not a mapping"
        return data, None
    except ImportError:
        return _mini_yaml(block), None
    except Exception as e:  # yaml error
        return None, f"yaml error: {e}"

def _mini_yaml(block):
    """Minimal parser sufficient for this bundle's frontmatter."""
    data, stack = {}, []
    cur_list_key, cur_item = None, None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if indent == 0:
            cur_list_key, cur_item = None, None
            k, _, v = line.partition(":")
            v = v.strip()
            if v == "":
                data[k] = None; cur_list_key = k; data[k] = []
            elif v.startswith("{") and v.endswith("}"):
                data[k] = _inline_map(v)
            elif v.startswith("[") and v.endswith("]"):
                data[k] = [s.strip().strip('"\'') for s in v[1:-1].split(",") if s.strip()]
            else:
                data[k] = v.strip('"\'')
        elif line.startswith("- "):
            item = line[2:].strip()
            if item.startswith("{") and item.endswith("}"):
                cur_item = _inline_map(item)
            elif ":" in item:
                kk, _, vv = item.partition(":"); cur_item = {kk.strip(): vv.strip().strip('"\'')}
            else:
                cur_item = item.strip('"\'')
            if isinstance(data.get(cur_list_key), list):
                data[cur_list_key].append(cur_item)
        elif isinstance(cur_item, dict) and ":" in line:
            kk, _, vv = line.partition(":"); cur_item[kk.strip()] = vv.strip().strip('"\'')
    return data

def _inline_map(s):
    out = {}
    for part in s[1:-1].split(","):
        if ":" in part:
            k, _, v = part.partition(":"); out[k.strip()] = v.strip().strip('"\'')
    return out

ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2}))?$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

def check(bundle, write_index, strict_links):
    errors, warnings = [], []
    concepts = {}  # relpath -> frontmatter
    for root, dirs, files in os.walk(bundle):
        dirs.sort()
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, bundle)
            text = open(path, encoding="utf-8").read()
            if f in RESERVED:
                if f == "log.md" and rel == "log.md":
                    dates = re.findall(r"^## (\d{4}-\d{2}-\d{2})\s*$", text, re.M)
                    if dates != sorted(dates, reverse=True):
                        errors.append(f"{rel}: date headings not in descending order: {dates}")
                continue
            fm, err = parse_frontmatter(text)
            if err:
                errors.append(f"{rel}: {err}"); continue
            if not fm.get("type"):
                errors.append(f"{rel}: missing or empty `type`")
            st = fm.get("status", "stable")
            if st not in STATUS:
                errors.append(f"{rel}: status `{st}` not in {sorted(STATUS)}")
            tr = fm.get("trust")
            if tr not in TRUST:
                errors.append(f"{rel}: trust `{tr}` not in {sorted(TRUST)}")
            gen = fm.get("generated") or {}
            if not isinstance(gen, dict) or not ISO_RE.match(str(gen.get("at", ""))):
                errors.append(f"{rel}: generated.at missing or not ISO 8601")
            has_verified = bool(fm.get("verified"))
            if tr == "verified" and not has_verified:
                errors.append(f"{rel}: trust=verified but no `verified` entries")
            if tr != "verified" and has_verified:
                warnings.append(f"{rel}: trust={tr} but has `verified` entries")
            if tr == "open" and st != "draft":
                warnings.append(f"{rel}: trust=open should have status=draft")
            body_no_code = re.sub(r"`[^`\n]*`", "", re.sub(r"```.*?```", "", text, flags=re.S))
            for target in LINK_RE.findall(body_no_code):
                if target.startswith(("http://", "https://", "mailto:", "file:", "#", "shell:")):
                    continue
                target = target.split("#")[0]
                tp = os.path.join(bundle, target.lstrip("/")) if target.startswith("/") else os.path.normpath(os.path.join(root, target))
                if not os.path.exists(tp):
                    (errors if strict_links else warnings).append(f"{rel}: broken link -> {target}")
            concepts[rel] = fm
    # index files
    for root, dirs, files in os.walk(bundle):
        dirs.sort()
        entries = [f for f in sorted(files) if f.endswith(".md") and f not in RESERVED]
        subdirs = [d for d in dirs if any(x.endswith(".md") for x in os.listdir(os.path.join(root, d)))]
        idx = os.path.join(root, "index.md")
        rel_root = os.path.relpath(root, bundle)
        is_root = rel_root == "."
        lines = []
        if is_root:
            lines += ["---", 'okf_version: "0.2"', "---", ""]
        title = "Knowledge bundle" if is_root else rel_root.replace("/", " / ").title()
        lines.append(f"# {title}")
        lines.append("")
        if is_root:
            lines.append("MySQL LTS sample-database image: research trail and decisions. Read [runbooks/knowledge-bundle-conventions.md](/runbooks/knowledge-bundle-conventions.md) first; change history in [log.md](/log.md).")
            lines.append("")
        if subdirs:
            lines.append("## Directories")
            for d in subdirs:
                lines.append(f"* [{d}/]({d}/index.md) - {len([x for x in os.listdir(os.path.join(root, d)) if x.endswith('.md') and x not in RESERVED])} concepts")
            lines.append("")
        if entries:
            lines.append("## Concepts")
            for f in entries:
                fm = concepts.get(os.path.relpath(os.path.join(root, f), bundle), {})
                lines.append(f"* [{fm.get('title', f)}]({f}) - {fm.get('description', '')}".rstrip())
            lines.append("")
        content = "\n".join(lines)
        if write_index:
            open(idx, "w", encoding="utf-8").write(content)
        elif os.path.exists(idx):
            existing = open(idx, encoding="utf-8").read()
            listed = set(re.findall(r"\]\(([^)/]+\.md)\)", existing))
            missing = [f for f in entries if f not in listed]
            extra = [f for f in listed if f not in entries and f != "index.md"]
            if missing: errors.append(f"{os.path.relpath(idx, bundle)}: not listed: {missing}")
            if extra: errors.append(f"{os.path.relpath(idx, bundle)}: lists nonexistent: {extra}")
        elif entries or subdirs:
            errors.append(f"{os.path.relpath(idx, bundle)}: missing (run with --write-index)")
    return concepts, errors, warnings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", default="knowledge")
    ap.add_argument("--write-index", action="store_true")
    ap.add_argument("--strict-links", action="store_true")
    a = ap.parse_args()
    concepts, errors, warnings = check(a.bundle, a.write_index, a.strict_links)
    types = {}
    for fm in concepts.values():
        types[fm.get("type")] = types.get(fm.get("type"), 0) + 1
    print(f"{len(concepts)} concepts: " + ", ".join(f"{k}={v}" for k, v in sorted(types.items(), key=str)))
    for w in warnings: print("WARN", w)
    for e in errors: print("ERROR", e)
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
