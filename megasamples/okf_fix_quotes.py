#!/usr/bin/env python3
"""Quote OKF frontmatter scalars whose YAML type would otherwise depend on the parser.

Usage: python3 -m megasamples okf-fix-quotes [--bundle knowledge] [--check]

A field that a YAML 1.1 parser types (PyYAML turns `2026-09-02` into a date, `9.7` into a float, `yes` into
True, `010` into 8, `12:30` into 750) but a YAML 1.2 core-schema parser leaves as a string makes a record's
type parser-dependent, which defeats OKF's "consume without an SDK" promise. This tool adds double quotes
around exactly those scalars, for the keys that must always be strings and for every `tags` entry.

It works by splicing quotes into the raw frontmatter text at the positions PyYAML's composer reports, so the
author's token is preserved verbatim (`version: 1.10` becomes `version: "1.10"`, never `"1.1"`), and comments,
key order, block scalars and formatting are untouched. Nothing else in the file is rewritten.

`--check` reports files that are not canonical and changes nothing. A file whose frontmatter is missing,
unterminated or unparseable is reported and left untouched.
Exit status: 0 clean, 1 files changed/not canonical or files skipped, 2 usage or environment problem.
"""
import argparse, os, sys
import yaml
from megasamples.okf_check import split_frontmatter, RESERVED  # noqa: E402

STRING_KEYS = {"title", "description", "resource", "version", "accessed", "last_modified", "id", "note",
               "by", "at", "stale_after", "type", "status", "trust", "okf_version", "bundle_status"}
STR_TAG, NULL_TAG = "tag:yaml.org,2002:str", "tag:yaml.org,2002:null"


def spans_to_quote(head):
    """[(start, end)] of plain scalars whose resolved type is not str, under a string-typed key."""
    spans = []

    def walk(node, key):
        if isinstance(node, yaml.MappingNode):
            for k, v in node.value:
                walk(v, k.value if isinstance(k, yaml.ScalarNode) else key)
        elif isinstance(node, yaml.SequenceNode):
            for item in node.value:
                walk(item, key)
        elif isinstance(node, yaml.ScalarNode):
            if node.style is None and node.tag not in (STR_TAG, NULL_TAG) and node.value != "" \
                    and (key in STRING_KEYS or key == "tags"):
                spans.append((node.start_mark.index, node.end_mark.index))

    root = yaml.compose(head)
    if root is not None:
        walk(root, None)
    return spans


def canonical(head):
    """Return the frontmatter text with the offending scalars quoted, verbatim otherwise."""
    for start, end in sorted(spans_to_quote(head), reverse=True):
        raw = head[start:end].rstrip()
        end = start + len(raw)
        head = head[:start] + '"' + raw.replace("\\", "\\\\").replace('"', '\\"') + '"' + head[end:]
    yaml.safe_load(head)  # must still parse
    return head


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("bundle", nargs="?", default="knowledge", help="bundle directory (default: knowledge)")
    ap.add_argument("--bundle", dest="bundle_opt", help=argparse.SUPPRESS)
    ap.add_argument("--check", action="store_true", help="report non-canonical files, change nothing")
    a = ap.parse_args(argv)
    bundle = a.bundle_opt or a.bundle
    if not os.path.isdir(bundle):
        print(f"ERROR bundle directory does not exist: {bundle}"); sys.exit(2)
    changed, skipped, would, seen = 0, [], [], 0
    for root, _, files in os.walk(bundle):
        for f in sorted(files):
            if not f.endswith(".md") or f in RESERVED:
                continue
            seen += 1
            path = os.path.join(root, f)
            raw = open(path, encoding="utf-8").read()
            head, body, err = split_frontmatter(raw)
            if err:
                skipped.append(f"{path}: {err}"); continue
            try:
                new_head = canonical(head)
            except (yaml.YAMLError, ValueError) as e:
                skipped.append(f"{path}: {str(e).splitlines()[0]}"); continue
            if new_head != head:
                if a.check:
                    would.append(path)
                else:
                    open(path, "w", encoding="utf-8").write("---\n" + new_head + "\n---\n" + body)
                    changed += 1
    if not seen:
        print(f"ERROR no concept files under {bundle}"); sys.exit(2)
    print(f"{len(would)} of {seen} files not canonical" if a.check else f"quoted {changed} of {seen} files")
    for p in would: print("  " + p)
    for s in skipped: print("SKIPPED (not modified):", s)
    sys.exit(1 if skipped or would else 0)


if __name__ == "__main__":
    main()
