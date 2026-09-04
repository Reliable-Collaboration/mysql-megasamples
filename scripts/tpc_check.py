#!/usr/bin/env python3
"""Run the TPC-H queries against MySQL and compare with the reference answers.

  python3 scripts/tpc_check.py [--sf 1]

This is what makes the port a port rather than a translation that happens to parse. DuckDB's
`tpch_answers()` carries the specification's validation output for scale factors 0.01, 0.1 and 1, so
every one of the 22 queries can be checked against a number somebody else computed.

Comparison is numeric, not textual, and deliberately so: MySQL returns `37734107.00` from a
DECIMAL(15,2) sum where the reference prints `37734107`, and averages differ in the last places
because the two engines carry different intermediate precision. A field that parses as a number is
compared with a relative tolerance; anything else must match exactly.
"""
import argparse, os, sys

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import db  # noqa: E402

TOLERANCE = 1e-6


def number(text):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def compare(got, want, tolerance=TOLERANCE):
    """(ok, first difference). Both are lists of rows of string fields."""
    if len(got) != len(want):
        return False, f"{len(got)} rows, reference has {len(want)}"
    for i, (g, w) in enumerate(zip(got, want)):
        if len(g) != len(w):
            return False, f"row {i + 1}: {len(g)} columns, reference has {len(w)}"
        for j, (a, b) in enumerate(zip(g, w)):
            x, y = number(a), number(b)
            if x is not None and y is not None:
                if abs(x - y) > tolerance * max(1.0, abs(y)):
                    return False, f"row {i + 1} column {j + 1}: {a} vs {b}"
            elif a.strip() != b.strip():
                return False, f"row {i + 1} column {j + 1}: {a!r} vs {b!r}"
    return True, ""


def reference(con, sf, nr):
    row = con.execute("SELECT answer FROM tpch_answers() WHERE scale_factor = ? AND query_nr = ?",
                      [sf, nr]).fetchone()
    if not row:
        return None
    lines = [l for l in row[0].splitlines() if l.strip()]
    return [l.split("|") for l in lines[1:]]          # drop the header line


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sf", type=float, default=1.0)
    ap.add_argument("--database", default="tpch")
    a = ap.parse_args()
    queries = os.path.join(ROOT, "docker", "context", a.database, "queries")
    con = duckdb.connect()
    con.execute("INSTALL tpch; LOAD tpch;")

    passed, failed, skipped = [], [], []
    for nr in range(1, 23):
        path = os.path.join(queries, f"q{nr:02d}.sql")
        if not os.path.exists(path):
            skipped.append((nr, "no query file")); continue
        want = reference(con, a.sf, nr)
        if want is None:
            skipped.append((nr, f"no reference answer at SF {a.sf:g}")); continue
        sql = open(path, encoding="utf-8").read()
        try:
            raw = db.sql(sql, database=a.database)
        except Exception as exc:
            failed.append((nr, f"MySQL rejected it: {str(exc).splitlines()[-1][:110]}")); continue
        got = [l.split("\t") for l in raw.splitlines() if l.strip()]
        ok, why = compare(got, want)
        (passed if ok else failed).append((nr, why))

    for nr, why in failed:
        print(f"  x Q{nr:02d}: {why}")
    for nr, why in skipped:
        print(f"  . Q{nr:02d} skipped: {why}")
    print(f"{len(passed)}/22 queries match the reference answers at SF {a.sf:g}"
          + (f"; {len(failed)} differ; {len(skipped)} skipped" if failed or skipped else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
