#!/usr/bin/env python3
"""Task E-02: time a bulk load with the indexes already in place against load-then-index.

  python3 -m megasamples bench --dataset employees [--repeat 2]

The staged SQL is split into three parts -- the table definitions, the data, and everything after it
-- and loaded twice:

  index-first    the tables as the source declares them (primary keys, unique keys and foreign keys
                 all present), then the data
  load-then-index  the same tables with every secondary and foreign key clause removed, then the
                 data, then one ALTER TABLE per table putting the keys back

Both end with identical schemas, which the script checks rather than assumes: it compares the
information_schema index set and the row counts after each run, so a "faster" ordering that quietly
built a different table is caught.

The primary key stays in place in both arms. Dropping it would change the clustered key and make the
load a heap insert plus a full table rebuild, which is a different experiment from the one the
indexing strategy asks about.
"""
import argparse, os, re, subprocess, sys, time

from megasamples.engines.mysql import server as db  # noqa: E402

from megasamples.paths import ROOT, stage_dir
# clauses inside CREATE TABLE that the second arm defers; PRIMARY KEY and UNIQUE stay, because a
# unique constraint cannot be added afterwards without risking a load that violates it
DEFERRABLE = re.compile(r"(?im)^\s*(?:CONSTRAINT\s+\S+\s+)?(FOREIGN\s+KEY|KEY|INDEX)\b[^\n]*?,?\s*$")


def split_sql(text):
    """(preamble, [create table statements], rest) of a staged dataset script."""
    statements, current, out = [], [], []
    for line in text.split("\n"):
        if re.match(r"(?i)^\s*CREATE\s+TABLE\b", line) or current:
            current.append(line)
            if line.strip().endswith(";"):
                statements.append("\n".join(current))
                current = []
        else:
            out.append(line)
    return "\n".join(out), statements


def defer_keys(create_table):
    """Strip the deferrable key clauses, returning the table plus the ALTERs that restore them."""
    name = re.search(r"(?i)CREATE\s+TABLE\s+`?(\w+)`?", create_table).group(1)
    kept, deferred = [], []
    for line in create_table.split("\n"):
        if DEFERRABLE.match(line) and "PRIMARY" not in line.upper():
            deferred.append(line.strip().rstrip(",").strip())
        else:
            kept.append(line)
    body = "\n".join(kept)
    # a clause removed from the middle can leave "(,"  or ",,"  or a dangling comma before ")"
    body = re.sub(r",(\s*)\)", r"\1)", body)
    alters = [f"ALTER TABLE `{name}` ADD {clause};" for clause in deferred]
    return body, alters


def schema_fingerprint(schema):
    """Index set and row counts, so both arms can be proved to have produced the same thing."""
    indexes = db.rows(
        "SELECT table_name, index_name, GROUP_CONCAT(column_name ORDER BY seq_in_index) "
        f"FROM information_schema.statistics WHERE table_schema='{schema}' "
        "GROUP BY table_name, index_name ORDER BY table_name, index_name")
    tables = [r[0] for r in db.rows(
        "SELECT table_name FROM information_schema.tables "
        f"WHERE table_schema='{schema}' AND table_type='BASE TABLE' ORDER BY table_name")]
    counts = {t: db.rows(f"SELECT COUNT(*) FROM `{t}`", schema)[0][0] for t in tables}
    return indexes, counts


def run_arm(name, sql, schema, context):
    path = os.path.join(context, f"_bench_{name}.sql")
    open(path, "w", encoding="utf-8").write(sql)
    db.sql(f"SET FOREIGN_KEY_CHECKS = 0; DROP DATABASE IF EXISTS `{schema}`")
    started = time.time()
    db.sql_file(path)
    elapsed = time.time() - started
    os.remove(path)
    # ANALYZE first: a fresh load leaves statistics ungathered and data_length then under-reports by
    # a wide margin, which would make one arm look four times smaller than the other
    tables = [r[0] for r in db.rows(
        "SELECT table_name FROM information_schema.tables "
        f"WHERE table_schema='{schema}' AND table_type='BASE TABLE'")]
    if tables:
        db.sql("ANALYZE TABLE " + ", ".join(f"`{schema}`.`{t}`" for t in tables))
    size = db.rows("SELECT ROUND(SUM(data_length+index_length)/1048576,1) "
                   f"FROM information_schema.tables WHERE table_schema='{schema}'")[0][0]
    return elapsed, size, schema_fingerprint(schema)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dataset", default="employees")
    ap.add_argument("--repeat", type=int, default=1, help="run each arm this many times, keep the best")
    a = ap.parse_args(argv)

    context = stage_dir(a.dataset)
    staged = os.path.join(context, f"{a.dataset}.sql")
    if not os.path.exists(staged):
        sys.exit(f"{staged} is not staged; run: make {a.dataset}")
    text = open(staged, encoding="utf-8").read()
    found = re.search(r"(?im)^\s*USE\s+`?(\w+)`?\s*;", text)
    if not found:
        sys.exit(f"cannot tell which database {staged} loads into")
    schema = found.group(1)

    rest, creates = split_sql(text)
    head = text[:text.index(creates[0])]
    tail = text[text.index(creates[-1]) + len(creates[-1]):]

    index_first = head + "\n".join(creates) + tail
    deferred_tables, alters = [], []
    for create in creates:
        body, table_alters = defer_keys(create)
        deferred_tables.append(body)
        alters += table_alters
    # The deferred keys are added with foreign_key_checks off, because the index-first arm loads
    # with them off too: otherwise this would compare "no validation" against "validate six foreign
    # keys over 3.9 M rows", which is a different question from the order the indexes are built in.
    load_then_index = (head + "\n".join(deferred_tables) + tail + "\nSET FOREIGN_KEY_CHECKS = 0;\n"
                       + "\n".join(alters) + "\nSET FOREIGN_KEY_CHECKS = 1;\n")
    # a third arm prices the validation the strategy asks for after a deferred load
    validated = (head + "\n".join(deferred_tables) + tail + "\n" + "\n".join(alters) + "\n")

    if not alters:
        sys.exit(f"{a.dataset} declares no deferrable keys; nothing to compare")

    db.start()
    results = {}
    arms = (("index-first", index_first), ("load-then-index", load_then_index),
            ("load-then-index+validate", validated))
    for name, sql in arms:
        best = None
        for _ in range(a.repeat):
            elapsed, size, fingerprint = run_arm(name, sql, schema, context)
            if best is None or elapsed < best[0]:
                best = (elapsed, size, fingerprint)
        results[name] = best
        print(f"  . {name:<16} {best[0]:6.1f}s   {best[1]} MB")

    (a_time, a_size, a_fp) = results["index-first"]
    (b_time, b_size, b_fp) = results["load-then-index"]
    (c_time, _, c_fp) = results["load-then-index+validate"]
    if a_fp[0] != b_fp[0]:
        only_a = [r for r in a_fp[0] if r not in b_fp[0]]
        only_b = [r for r in b_fp[0] if r not in a_fp[0]]
        sys.exit(f"the two arms produced different indexes; index-first only {only_a}, "
                 f"load-then-index only {only_b}")
    if a_fp[1] != b_fp[1]:
        sys.exit(f"the two arms produced different row counts: {a_fp[1]} vs {b_fp[1]}")

    if a_fp != c_fp:
        sys.exit("the validating arm produced a different schema")
    print(f"  . all three arms produced the same {len(a_fp[0])} indexes, row counts and size")
    faster, slower = ("load-then-index", "index-first") if b_time < a_time else ("index-first", "load-then-index")
    ratio = max(a_time, b_time) / min(a_time, b_time)
    print(f"  . {faster} is {ratio:.2f}x faster than {slower} "
          f"({min(a_time, b_time):.1f}s vs {max(a_time, b_time):.1f}s), "
          f"deferring {len(alters)} key(s)")
    print(f"  . validating those keys afterwards costs a further {c_time - b_time:.1f}s "
          f"({c_time:.1f}s total)")


if __name__ == "__main__":
    main()
