#!/usr/bin/env python3
"""Run the test stages of PLAN.md section 4 against a loaded database on the build server.

  python3 scripts/verify.py <dataset> [stage ...] [--pin]

Stages: counts (S3), digests (S4), fks (S5), indexes (S6), explain (S6), smoke (S7). Default: all.
`--pin` writes the observed values into the dataset's tests/ files instead of comparing, which is how a
baseline is first established for the native-SQL datasets that have no converter (the documented
exception in knowledge/decisions/test-checksum-method.md).
"""
import argparse, json, os, sys
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon, db  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dataset_dir(name):
    return os.path.join(ROOT, "datasets", name)


def load_yaml(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def dump_yaml(path, data, header):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(header.rstrip("\n") + "\n")
        yaml.safe_dump(data, fh, sort_keys=True, default_flow_style=False, allow_unicode=True)


def base_tables(schema):
    return [r[0] for r in db.rows(
        "SELECT table_name FROM information_schema.tables "
        f"WHERE table_schema='{schema}' AND table_type='BASE TABLE' ORDER BY table_name")]


def columns_of(schema, table):
    return [(r[0], r[1]) for r in db.rows(
        "SELECT column_name, data_type FROM information_schema.columns "
        f"WHERE table_schema='{schema}' AND table_name='{table}' ORDER BY ordinal_position")]


class Result:
    def __init__(self): self.failures, self.notes = [], []
    def fail(self, msg): self.failures.append(msg)
    def note(self, msg): self.notes.append(msg)


def stage_counts(cfg, schema, d, pin, res):
    path = os.path.join(d, "tests", "expected_counts.yaml")
    observed = {t: int(db.rows(f"SELECT COUNT(*) FROM `{schema}`.`{t}`")[0][0]) for t in base_tables(schema)}
    if pin:
        dump_yaml(path, observed, "# S3: row count per table. Pinned from a verified load.")
        res.note(f"counts pinned for {len(observed)} tables"); return
    expected = load_yaml(path)
    if expected is None:
        res.fail(f"no expected_counts.yaml for {cfg['database']}; run with --pin"); return
    for table, want in sorted(expected.items()):
        got = observed.get(table)
        if got is None:
            res.fail(f"table {table} missing (expected {want} rows)")
        elif got != want:
            res.fail(f"{table}: {got} rows, expected {want}")
    for extra in sorted(set(observed) - set(expected)):
        res.fail(f"unexpected table {extra} ({observed[extra]} rows)")
    res.note(f"counts OK for {len(expected)} tables")


def stage_digests(cfg, schema, d, pin, res):
    path = os.path.join(d, "tests", "checksums.yaml")
    # Columns whose value is not reproducible across builds (a DEFAULT CURRENT_TIMESTAMP that the
    # upstream data leaves unset, for instance) are excluded from the digest and listed with a
    # reason, so the exclusion is visible rather than hidden inside a passing test.
    excluded = load_yaml(os.path.join(d, "tests", "digest_exclude.yaml"), {}) or {}
    observed = {}
    for table in base_tables(schema):
        cols = [c for c in columns_of(schema, table)
                if c[0] not in (excluded.get(table, {}) or {})]
        row = db.rows(canon.fingerprint_sql(schema, table, cols))[0]
        observed[table] = {"n": int(row[0]), "x": int(row[1]), "s": int(row[2]),
                           "columns": [c for c, t in cols if t.lower() not in canon.EXCLUDED],
                           "excluded": [c for c, t in cols if t.lower() in canon.EXCLUDED]}
    if pin:
        dump_yaml(path, observed,
                  "# S4: canonical per-table fingerprint (count, BIT_XOR, SUM mod 2^64) over the\n"
                  "# row digest defined in scripts/canon.py. float/double/json columns are excluded.")
        res.note(f"digests pinned for {len(observed)} tables"); return
    expected = load_yaml(path)
    if expected is None:
        res.fail(f"no checksums.yaml for {cfg['database']}; run with --pin"); return
    for table, want in sorted(expected.items()):
        got = observed.get(table)
        if not got:
            res.fail(f"table {table} missing for digest"); continue
        if got["columns"] != want["columns"]:
            res.fail(f"{table}: digested column set changed {want['columns']} -> {got['columns']}"); continue
        for k in ("n", "x", "s"):
            if got[k] != want[k]:
                res.fail(f"{table}: digest {k} {got[k]} != expected {want[k]}")
    res.note(f"digests OK for {len(expected)} tables")


def stage_fks(cfg, schema, d, pin, res):
    fks = db.rows(
        "SELECT rc.constraint_name, rc.table_name, kcu.column_name, rc.referenced_table_name, "
        "kcu.referenced_column_name FROM information_schema.referential_constraints rc "
        "JOIN information_schema.key_column_usage kcu ON kcu.constraint_name=rc.constraint_name "
        "AND kcu.constraint_schema=rc.constraint_schema "
        f"WHERE rc.constraint_schema='{schema}' ORDER BY 1,3")
    orphans = 0
    for name, table, col, rtable, rcol in fks:
        n = int(db.rows(
            f"SELECT COUNT(*) FROM `{schema}`.`{table}` c LEFT JOIN `{schema}`.`{rtable}` p "
            f"ON c.`{col}` = p.`{rcol}` WHERE c.`{col}` IS NOT NULL AND p.`{rcol}` IS NULL")[0][0])
        if n:
            res.fail(f"foreign key {name} ({table}.{col} -> {rtable}.{rcol}) has {n} orphan rows")
            orphans += n
    res.note(f"{len(fks)} foreign keys validated, {orphans} orphans")


def stage_indexes(cfg, schema, d, pin, res):
    path = os.path.join(d, "tests", "indexes.yaml")
    observed = {}
    for table, index, nonuniq, itype, cols in [
        (r[0], r[1], r[2], r[3], r[4]) for r in db.rows(
            "SELECT table_name, index_name, MAX(non_unique), MAX(index_type), "
            "GROUP_CONCAT(column_name ORDER BY seq_in_index) "
            f"FROM information_schema.statistics WHERE table_schema='{schema}' "
            "GROUP BY table_name, index_name ORDER BY table_name, index_name")]:
        observed.setdefault(table, {})[index] = {
            "unique": nonuniq == "0", "type": itype, "columns": cols.split(",")}
    if pin:
        dump_yaml(path, observed, "# S6: every index that must exist after load.")
        res.note(f"indexes pinned for {len(observed)} tables"); return
    expected = load_yaml(path)
    if expected is None:
        res.fail(f"no indexes.yaml for {cfg['database']}; run with --pin"); return
    for table, want in sorted(expected.items()):
        got = observed.get(table, {})
        for index, spec in sorted(want.items()):
            if index not in got:
                res.fail(f"{table}: index {index} missing"); continue
            for k in ("unique", "type", "columns"):
                if got[index][k] != spec[k]:
                    res.fail(f"{table}.{index}: {k} {got[index][k]} != expected {spec[k]}")
        for extra in sorted(set(got) - set(want)):
            res.fail(f"{table}: unexpected index {extra}")
    res.note(f"indexes OK for {len(expected)} tables")


def stage_explain(cfg, schema, d, pin, res):
    spec = load_yaml(os.path.join(d, "tests", "explain.yaml"))
    if not spec:
        res.note("no explain.yaml, skipped"); return
    for case in spec:
        plan = json.loads(db.sql(f"EXPLAIN FORMAT=JSON {case['query']}", database=schema))
        blob = json.dumps(plan)
        for table in case.get("must_not_full_scan", []):
            marker = f'"table_name": "{table}"'
            idx = blob.find(marker)
            if idx < 0:
                res.fail(f"{case['name']}: table {table} not in the plan"); continue
            window = blob[idx:idx + 400]
            if '"access_type": "ALL"' in window:
                res.fail(f"{case['name']}: {table} is a full scan")
    res.note(f"explain OK for {len(spec)} queries")


def stage_smoke(cfg, schema, d, pin, res):
    path = os.path.join(d, "tests", "smoke.expected.yaml")
    spec = load_yaml(os.path.join(d, "tests", "smoke.yaml"))
    if not spec:
        res.note("no smoke.yaml, skipped"); return
    observed = {c["name"]: db.sql(c["query"], database=schema).strip() for c in spec}
    if pin:
        dump_yaml(path, observed, "# S7: canonical query results, tab-separated as the client prints them.")
        res.note(f"smoke results pinned for {len(observed)} queries"); return
    expected = load_yaml(path)
    if expected is None:
        res.fail(f"no smoke.expected.yaml for {cfg['database']}; run with --pin"); return
    for name, want in sorted(expected.items()):
        got = observed.get(name)
        if got != want:
            res.fail(f"smoke {name}:\n    expected {want!r}\n    got      {got!r}")
    res.note(f"smoke OK for {len(expected)} queries")


STAGES = {"counts": stage_counts, "digests": stage_digests, "fks": stage_fks,
          "indexes": stage_indexes, "explain": stage_explain, "smoke": stage_smoke}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dataset")
    ap.add_argument("stages", nargs="*", default=[])
    ap.add_argument("--pin", action="store_true")
    a = ap.parse_args()
    d = dataset_dir(a.dataset)
    cfg = load_yaml(os.path.join(d, "dataset.yaml"))
    if not cfg:
        sys.exit(f"no datasets/{a.dataset}/dataset.yaml")
    schema = cfg["database"]
    stages = a.stages or list(STAGES)
    res = Result()
    for name in stages:
        if name not in STAGES:
            sys.exit(f"unknown stage {name}; choose from {list(STAGES)}")
        STAGES[name](cfg, schema, d, a.pin, res)
    for n in res.notes:
        print(f"  . {n}")
    for f in res.failures:
        print(f"  x {f}")
    print(f"{a.dataset}: {len(res.failures)} failure(s)")
    sys.exit(1 if res.failures else 0)


if __name__ == "__main__":
    main()
