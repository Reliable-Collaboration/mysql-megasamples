#!/usr/bin/env python3
"""Run the verification stages (ARCHITECTURE.md section 5) against a loaded dataset on an engine.

  python3 -m megasamples verify <dataset> [stage ...] [--engine mysql] [--pin]

Stages: counts (S3), digests (S4), fks (S5), indexes (S6), explain (S6), smoke (S7). Default: all
the engine supports. The expectations under datasets/<name>/tests/ are engine-neutral: every engine
is checked against the same counts, the same canonical digests, the same foreign keys and the same
index set, which is what makes a port provably the same data as the MySQL corpus. explain and smoke
are MySQL-only, since their queries are written in MySQL's dialect.

`--pin` writes the observed values into the tests/ files instead of comparing, and is allowed on
MySQL only: expectations come from the hub, never from a port. It is how a native-SQL dataset with
no converter-side baseline gets its first values (knowledge/decisions/test-checksum-method.md).
"""
import argparse, json, os, sys

import yaml

from megasamples.paths import ROOT


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


class Result:
    def __init__(self): self.failures, self.notes = [], []
    def fail(self, msg): self.failures.append(msg)
    def note(self, msg): self.notes.append(msg)


def extended_tables(database):
    """Tables that an `append: true` dataset declares for this database."""
    owned = set()
    root = os.path.join(ROOT, "datasets")
    for name in sorted(os.listdir(root)):
        config = os.path.join(root, name, "dataset.yaml")
        if not os.path.exists(config):
            continue
        other = load_yaml(config) or {}
        if other.get("append") and other.get("database") == database:
            counts = load_yaml(os.path.join(root, name, "tests", "expected_counts.yaml")) or {}
            owned |= set(counts)
    return owned


def own_tables(cfg, d, tables):
    """The tables this dataset is responsible for: all of them, or for an `append: true` dataset the
    ones its own expected_counts.yaml names, so a shared database is not accounted for twice."""
    if not cfg.get("append"):
        return tables
    mine = load_yaml(os.path.join(d, "tests", "expected_counts.yaml")) or {}
    return [t for t in tables if t in mine]


def stage_counts(ad, cfg, schema, d, pin, res):
    path = os.path.join(d, "tests", "expected_counts.yaml")
    observed = {t: ad.count(schema, t) for t in ad.tables(schema)}
    if pin and os.path.exists(path) and open(path, encoding="utf-8").readline().startswith("# authority:"):
        res.note(f"counts not pinned: {os.path.relpath(path)} is generated from the source")
        pin = False
    if pin and cfg.get("append"):
        declared = load_yaml(path)
        if declared is None:
            res.fail(f"{cfg['database']}: an append dataset needs its table list written by hand "
                     f"in {os.path.relpath(path)} before counts can be pinned"); return
        missing = sorted(set(declared) - set(observed))
        if missing:
            res.fail(f"declared table(s) not present: {', '.join(missing)}"); return
        header = "".join(line for line in open(path, encoding="utf-8")
                         if line.startswith("#")) or "# S3: row count per table.\n"
        dump_yaml(path, {t: observed[t] for t in declared}, header.rstrip("\n"))
        res.note(f"counts pinned for the {len(declared)} table(s) this dataset declares"); return
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
    if cfg.get("append"):
        res.note(f"counts OK for {len(expected)} table(s) added to `{cfg['database']}` "
                 f"({len(observed) - len(expected)} more belong to the core dataset)")
        return
    extended = extended_tables(cfg["database"])
    unexpected = sorted(set(observed) - set(expected) - extended)
    shared = sorted((set(observed) - set(expected)) & extended)
    for extra in unexpected:
        res.fail(f"unexpected table {extra} ({observed[extra]} rows)")
    if shared:
        res.note(f"ignoring {len(shared)} extended-tier table(s) also loaded here: " + ", ".join(shared))
    res.note(f"counts OK for {len(expected)} tables")


def stage_digests(ad, cfg, schema, d, pin, res):
    from megasamples import canon
    path = os.path.join(d, "tests", "checksums.yaml")
    excluded = load_yaml(os.path.join(d, "tests", "digest_exclude.yaml"), {}) or {}
    observed = {}
    for table in own_tables(cfg, d, ad.tables(schema)):
        cols = [c for c in ad.columns(schema, table) if c[0] not in (excluded.get(table, {}) or {})]
        n, x, s = ad.fingerprint(schema, table, cols)
        observed[table] = {"n": n, "x": x, "s": s,
                           "columns": [c for c, t in cols if t.lower() not in canon.EXCLUDED],
                           "excluded": [c for c, t in cols if t.lower() in canon.EXCLUDED]}
    if pin:
        dump_yaml(path, observed,
                  "# S4: canonical per-table fingerprint (count, BIT_XOR, SUM mod 2^64) over the\n"
                  "# row digest defined in megasamples/canon.py. float/double/json columns are excluded.")
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


def stage_fks(ad, cfg, schema, d, pin, res):
    fks = ad.foreign_keys(schema)
    orphans, external = 0, 0
    for name, table, col, rschema, rtable, rcol in fks:
        external += rschema != schema
        n = ad.orphans(schema, table, col, rschema, rtable, rcol)
        if n:
            res.fail(f"foreign key {name} ({table}.{col} -> {rschema}.{rtable}.{rcol}) has {n} orphan rows")
            orphans += n
    across = f" ({external} across databases)" if external else ""
    res.note(f"{len(fks)} foreign keys validated{across}, {orphans} orphans")


def stage_indexes(ad, cfg, schema, d, pin, res):
    path = os.path.join(d, "tests", "indexes.yaml")
    mine = set(own_tables(cfg, d, ad.tables(schema)))
    observed = {t: idx for t, idx in ad.indexes(schema).items() if t in mine}
    if pin:
        dump_yaml(path, observed, "# S6: every index that must exist after load.")
        res.note(f"indexes pinned for {len(observed)} tables"); return
    expected = load_yaml(path)
    if expected is None:
        res.fail(f"no indexes.yaml for {cfg['database']}; run with --pin"); return
    skipped = 0
    for table, want in sorted(expected.items()):
        got = observed.get(table, {})
        for index, spec in sorted(want.items()):
            if not ad.carries_index(spec):
                skipped += 1
                continue
            if index not in got:
                res.fail(f"{table}: index {index} missing"); continue
            for k in ("unique", "type", "columns"):
                if got[index][k] != spec[k]:
                    res.fail(f"{table}.{index}: {k} {got[index][k]} != expected {spec[k]}")
        for extra in sorted(set(got) - set(want)):
            res.fail(f"{table}: unexpected index {extra}")
    res.note(f"indexes OK for {len(expected)} tables" + (f" ({skipped} not carried by {ad.name})" if skipped else ""))


def stage_explain(ad, cfg, schema, d, pin, res):
    spec = load_yaml(os.path.join(d, "tests", "explain.yaml"))
    if not spec:
        res.note("no explain.yaml, skipped"); return
    for case in spec:
        plan = json.loads(ad.explain_json(schema, case["query"]))
        blob = json.dumps(plan)
        for table in case.get("must_not_full_scan", []):
            marker = f'"table_name": "{table}"'
            idx = blob.find(marker)
            if idx < 0:
                # A unique-index lookup on a constant can be resolved before execution, and the
                # table then does not appear in the plan at all -- the strongest access path, not
                # a missing table -- but a typo would look the same, so it only passes when the plan
                # says the rows were fetched before execution.
                if "Rows fetched before execution" in blob or '"const"' in blob:
                    continue
                res.fail(f"{case['name']}: table {table} not in the plan"); continue
            window = blob[idx:idx + 400]
            if '"access_type": "ALL"' in window:
                res.fail(f"{case['name']}: {table} is a full scan")
    res.note(f"explain OK for {len(spec)} queries")


def stage_smoke(ad, cfg, schema, d, pin, res):
    path = os.path.join(d, "tests", "smoke.expected.yaml")
    spec = load_yaml(os.path.join(d, "tests", "smoke.yaml"))
    if not spec:
        res.note("no smoke.yaml, skipped"); return
    observed = {c["name"]: ad.query_text(schema, c["query"]) for c in spec}
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


def adapter_for(engine, dataset):
    if engine == "mysql":
        from megasamples.engines.mysql.adapter import MySQLAdapter
        return MySQLAdapter()
    if engine == "postgres":
        from megasamples.engines.postgres.adapter import PostgresAdapter
        return PostgresAdapter(dataset)
    if engine == "sqlite":
        from megasamples.engines.sqlite.adapter import SQLiteAdapter
        return SQLiteAdapter(dataset)
    raise SystemExit(f"no verification adapter for engine {engine!r}")


def verify(dataset, stages=None, engine="mysql", pin=False):
    """Run the stages; returns the number of failures. Prints one line per note and failure."""
    d = dataset_dir(dataset)
    cfg = load_yaml(os.path.join(d, "dataset.yaml"))
    if not cfg:
        sys.exit(f"no datasets/{dataset}/dataset.yaml")
    if pin and engine != "mysql":
        sys.exit("--pin is for the hub only: expectations come from MySQL, never from a port")
    ad = adapter_for(engine, dataset)
    schema = cfg["database"]
    res = Result()
    for name in (stages or list(STAGES)):
        if name not in STAGES:
            sys.exit(f"unknown stage {name}; choose from {list(STAGES)}")
        if not ad.supports(name):
            res.note(f"{name}: not run on {ad.name} (MySQL-dialect queries)")
            continue
        STAGES[name](ad, cfg, schema, d, pin, res)
    for n in res.notes:
        print(f"  . {n}")
    for f in res.failures:
        print(f"  x {f}")
    print(f"{dataset} on {ad.name}: {len(res.failures)} failure(s)")
    return len(res.failures)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dataset")
    ap.add_argument("stages", nargs="*", default=[])
    ap.add_argument("--engine", default="mysql")
    ap.add_argument("--pin", action="store_true")
    a = ap.parse_args(argv)
    return 1 if verify(a.dataset, a.stages, a.engine, a.pin) else 0


if __name__ == "__main__":
    sys.exit(main())
