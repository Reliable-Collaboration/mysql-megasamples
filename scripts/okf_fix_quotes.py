#!/usr/bin/env python3
"""Quote frontmatter scalars that PyYAML cannot parse as the intended string.

Usage: python3 scripts/okf_fix_quotes.py [bundle_dir]

Only string-valued keys are touched (title, description, resource, version, accessed, id, note, by, at, and
`title`/`version`/`accessed` inside list items). A value is quoted when parsing `key: value` on its own fails or
yields a non-string (a comment-only value such as `# pending`, a number such as `9.7`, a date, a flow collection),
or when it starts with a YAML indicator character that cannot begin a plain scalar (- ? : , [ ] { } # & * ! | > quote characters % @ backtick).
Block scalar indicators `|` and `>` standing alone are left as they are. Files whose frontmatter is missing or
unterminated are reported and left untouched.
"""
import os, sys, re
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okf_check import split_frontmatter, RESERVED  # noqa: E402

STRING_KEYS = {"title", "description", "resource", "version", "accessed", "last_modified", "id", "note", "by", "at", "stale_after"}
LINE_RE = re.compile(r"^(\s*(?:- )?)([A-Za-z_]+):[ \t]*(.*?)\s*$")
INDICATORS = set("-?:,[]{}#&*!|>'\"%@`")


def needs_quote(value):
    if value == "" or value[0] in "\"'":
        return False
    if value in ("|", ">") or value.startswith(("|", ">")) and value[1:].strip() in ("", "-", "+"):
        return False  # block scalar header
    if value[0] in INDICATORS:
        return True
    try:
        parsed = yaml.safe_load(f"k: {value}")
    except yaml.YAMLError:
        return True
    return not (isinstance(parsed, dict) and isinstance(parsed.get("k"), str))


def quote(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    bundle = sys.argv[1] if len(sys.argv) > 1 else "knowledge"
    changed, skipped = 0, []
    for root, _, files in os.walk(bundle):
        for f in files:
            if not f.endswith(".md") or f in RESERVED:
                continue
            path = os.path.join(root, f)
            text = open(path, encoding="utf-8").read()
            head, body, err = split_frontmatter(text)
            if err:
                skipped.append(f"{path}: {err}"); continue
            out, touched = [], False
            for line in head.split("\n"):
                m = LINE_RE.match(line)
                if m and m.group(2) in STRING_KEYS and needs_quote(m.group(3)):
                    line = f"{m.group(1)}{m.group(2)}: {quote(m.group(3))}"; touched = True
                out.append(line)
            if touched:
                open(path, "w", encoding="utf-8").write("---\n" + "\n".join(out) + "\n---\n" + body)
                changed += 1
    print(f"quoted {changed} files")
    for s in skipped:
        print("SKIPPED (not modified):", s)
    sys.exit(1 if skipped else 0)


if __name__ == "__main__":
    main()
