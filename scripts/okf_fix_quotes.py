#!/usr/bin/env python3
"""Canonicalize OKF frontmatter so that PyYAML implicit typing cannot change a value's type.

Usage: python3 scripts/okf_fix_quotes.py [bundle_dir] [--check]

The frontmatter is parsed with PyYAML (so block scalars, flow mappings, comments and list items are all
understood), then normalized and re-emitted:
  * dates and datetimes become quoted ISO 8601 strings (YAML 1.1 parsers would otherwise type them, YAML 1.2
    parsers would not, which makes a field's type parser-dependent);
  * `tags` become strings; `title`, `description`, `resource`, `version`, `accessed`, `id`, `note`, `by`, `at`,
    `stale_after` become strings wherever they occur (top level or inside lists and mappings);
  * key order is preserved; the body is untouched except that CRLF line endings and a UTF-8 BOM are removed.
Comments inside frontmatter are not preserved (the bundle keeps none). A file whose frontmatter is missing,
unterminated or unparseable is reported and left untouched; with --check the tool only reports files that
would change. Exit status: 0 nothing to do or changed successfully, 1 files skipped or (with --check) not canonical.
"""
import datetime, os, sys
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okf_check import split_frontmatter, RESERVED  # noqa: E402

STRING_KEYS = {"title", "description", "resource", "version", "accessed", "last_modified", "id", "note",
               "by", "at", "stale_after", "type", "status", "trust", "okf_version", "bundle_status"}


def to_iso(v):
    if isinstance(v, datetime.datetime):
        s = v.isoformat()
        return s.replace("+00:00", "Z") if v.tzinfo else s
    return v.isoformat()


def normalize(node, key=None):
    if isinstance(node, dict):
        return {k: normalize(v, k) for k, v in node.items()}
    if isinstance(node, list):
        return [normalize(v, key) for v in node]
    if isinstance(node, (datetime.date, datetime.datetime)):
        return to_iso(node)
    if key == "tags":
        return str(node)
    if key in STRING_KEYS and node is not None and not isinstance(node, str):
        return str(node)
    return node


class Dumper(yaml.SafeDumper):
    pass


def _str_presenter(dumper, data):
    style = '"' if (data == "" or data[0] in "-?:,[]{}#&*!|>'\"%@`" or ": " in data or " #" in data
                    or data.strip() != data or data.lower() in {"true", "false", "null", "yes", "no", "on", "off", "~"}
                    or _looks_typed(data)) else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


def _looks_typed(s):
    try:
        v = yaml.safe_load(s)
    except yaml.YAMLError:
        return True
    return not isinstance(v, str)


Dumper.add_representer(str, _str_presenter)


def canonical(head):
    data = yaml.safe_load(head)
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return yaml.dump(normalize(data), Dumper=Dumper, sort_keys=False, allow_unicode=True, width=10000).rstrip("\n")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    bundle = args[0] if args else "knowledge"
    changed, skipped, would = 0, [], []
    for root, _, files in os.walk(bundle):
        for f in files:
            if not f.endswith(".md") or f in RESERVED:
                continue
            path = os.path.join(root, f)
            raw = open(path, encoding="utf-8").read()
            head, body, err = split_frontmatter(raw)
            if err:
                skipped.append(f"{path}: {err}"); continue
            try:
                new_head = canonical(head)
            except (yaml.YAMLError, ValueError) as e:
                skipped.append(f"{path}: {str(e).splitlines()[0]}"); continue
            new_text = "---\n" + new_head + "\n---\n" + body
            if new_text != raw:
                if check:
                    would.append(path)
                else:
                    open(path, "w", encoding="utf-8").write(new_text); changed += 1
    if check:
        print(f"{len(would)} files not canonical"); [print("  " + p) for p in would]
    else:
        print(f"canonicalized {changed} files")
    for s in skipped:
        print("SKIPPED (not modified):", s)
    sys.exit(1 if skipped or would else 0)


if __name__ == "__main__":
    main()
