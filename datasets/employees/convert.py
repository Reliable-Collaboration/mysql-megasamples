#!/usr/bin/env python3
"""Employees (test_db): assemble the upstream loader into a single stream.

The upstream `employees.sql` drives the load with the mysql client's own `source` command and a
`flush binary logs`. Neither survives being piped: `source` resolves its path against the client's
working directory, and the flush needs RELOAD and is pointless during a build. Both are replaced by
splicing the dump files inline, in the upstream order.

Record: knowledge/datasets/employees.md   Decision: knowledge/decisions/employees-conversion-path.md
"""
import os, re, sys

HEADER = """-- Employees (test_db), assembled by datasets/employees/convert.py from the upstream loader.
-- Upstream: github.com/datacharmer/test_db, CC BY-SA 3.0. See datasets/employees/LICENSE.
-- Original data by Fusheng Wang and Carlo Zaniolo (Siemens Corporate Research); schema by
-- Giuseppe Maxia; XML-to-relational conversion by Patrick Crews. The data is fabricated.
SET NAMES utf8mb4;
DROP DATABASE IF EXISTS `employees`;
"""


def main():
    downloads, dest = sys.argv[1], sys.argv[2]
    driver = open(os.path.join(downloads, "employees.sql"), encoding="utf-8").read()
    out, spliced, skipped = [HEADER], [], []
    for line in driver.split("\n"):
        stripped = line.strip()
        if re.match(r"(?i)^flush\s", stripped):
            continue                                   # needs RELOAD; meaningless mid-build
        m = re.match(r"(?i)^source\s+(\S+?)\s*;?$", stripped)
        if m:
            path = os.path.join(downloads, os.path.basename(m.group(1)))
            if not os.path.exists(path):
                # the driver also sources helpers such as show_elapsed.sql, which print timings
                # rather than data; they are not part of the dataset and are not fetched
                skipped.append(os.path.basename(path))
                continue
            out.append(f"-- spliced: {os.path.basename(path)} ({os.path.getsize(path):,} bytes)")
            out.append(open(path, encoding="utf-8").read())
            spliced.append(os.path.basename(path))
            continue
        out.append(line)
    # objects.sql adds the optional views, functions and procedures; it is not sourced by the driver
    objects = os.path.join(downloads, "objects.sql")
    if os.path.exists(objects):
        out.append("\n-- objects.sql: optional views, functions and procedures")
        out.append(open(objects, encoding="utf-8").read())
    open(dest, "w", encoding="utf-8").write("\n".join(out))
    print(f"  . assembled {len(spliced)} dump file(s): {', '.join(spliced)}")
    if skipped:
        print(f"  . skipped non-data helper(s): {', '.join(skipped)}")


if __name__ == "__main__":
    main()
