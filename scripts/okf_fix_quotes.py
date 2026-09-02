#!/usr/bin/env python3
"""Quote frontmatter scalar values for title/description/resource that contain ': ' or ' #' or start with special chars."""
import os, re, sys
bundle = sys.argv[1] if len(sys.argv) > 1 else "knowledge"
KEYS = ("title", "description", "resource")
n = 0
for root, _, files in os.walk(bundle):
    for f in files:
        if not f.endswith(".md") or f in ("index.md", "log.md"):
            continue
        p = os.path.join(root, f)
        t = open(p, encoding="utf-8").read()
        if not t.startswith("---\n"):
            continue
        end = t.find("\n---\n", 4)
        head, body = t[4:end], t[end:]
        out = []
        changed = False
        for line in head.split("\n"):
            m = re.match(r"^(\s*)(title|description|resource|version|accessed|last_modified|id|note):\s*(.*)$", line)
            if m:
                indent, key, val = m.group(1), m.group(2).strip(), m.group(3)
                if val and not (val[0] in "\"'" ) and (": " in val or " #" in val or val[0] in "[{*&!%@`|>" or val.endswith(":")):
                    val = '"' + val.replace('\\', '\\\\').replace('"', '\\"') + '"'
                    line = f"{indent}{key}: {val}"
                    changed = True
            out.append(line)
        if changed:
            open(p, "w", encoding="utf-8").write("---\n" + "\n".join(out) + body)
            n += 1
print(f"quoted {n} files")
