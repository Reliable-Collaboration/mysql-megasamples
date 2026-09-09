#!/usr/bin/env python3
"""Run the verification stages (ARCHITECTURE.md section 5) against a loaded database on the build server.

  python3 -m megasamples verify <dataset> [stage ...] [--pin]

Stages: counts (S3), digests (S4), fks (S5), indexes (S6), explain (S6), smoke (S7). Default: all.
`--pin` writes the observed values into the dataset's tests/ files instead of comparing, which is how a
baseline is first established for the native-SQL datasets that have no converter (the documented
exception in knowledge/decisions/test-checksum-method.md).
"""
import argparse, json, os, sys
import yaml
from megasamples import canon
from megasamples.engines.mysql import server as db  # noqa: E402

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


def stage_counts(cfg, schema, d, pin, res):
    path = os.path.join(d, "tests", "expected_counts.yaml")
    observed = {t: int(db.rows(f"SELECT COUNT(*) FROM `{schema}`.`{t}`")[0][0]) for t in base_tables(schema)}
    # A file that names an authority outside this database is not ours to overwrite: pinning it
    # would replace "what the source says" with "what we happened to load", which is the one
    # substitution that makes a lost row look correct.
    if pin and os.path.exists(path) and open(path, encoding="utf-8").readline().startswith(
            "# authority:"):
        res.note(f"counts not pinned: {os.path.relpath(path)} is generated from the source")
        pin = False
    if pin and cfg.get("append"):
        # Which tables an append dataset owns is a declaration, not something the database can be
        # asked: it shares its schema with the core dataset that made it. Pinning refreshes the
        # values of the tables already listed and never adds to the list -- otherwise the first
        # --pin quietly claims the core dataset's tables as well, which is what happened here.
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
        # an extended-tier dataset adds tables to a database the core build already made, so the
        # other tables in it are not this dataset's to account for -- the core dataset checks those
        res.note(f"counts OK for {len(expected)} table(s) added to `{cfg['database']}` "
                 f"({len(observed) - len(expected)} more belong to the core dataset)")
        return
    # tables an extended-tier dataset owns are not this one's to account for, when both are loaded
    extended = extended_tables(cfg["database"])
    unexpected = sorted(set(observed) - set(expected) - extended)
    shared = sorted((set(observed) - set(expected)) & extended)
    for extra in unexpected:
        res.fail(f"unexpected table {extra} ({observed[extra]} rows)")
    if shared:
        res.note(f"ignoring {len(shared)} extended-tier table(s) also loaded here: "
                 + ", ".join(shared))
    res.note(f"counts OK for {len(expected)} tables")


def own_tables(cfg, d, schema):
    """The tables this dataset is responsible for.

    An `append: true` dataset shares a database with the core dataset that made it, so it must
    account for its own tables and no others -- otherwise the same expectation is stored twice and
    the two copies drift.
    """
    tables = base_tables(schema)
    if not cfg.get("append"):
        return tables
    mine = load_yaml(os.path.join(d, "tests", "expected_counts.yaml")) or {}
    return [t for t in tables if t in mine]


def stage_digests(cfg, schema, d, pin, res):
    path = os.path.join(d, "tests", "checksums.yaml")
    # Columns whose value is not reproducible across builds (a DEFAULT CURRENT_TIMESTAMP that the
    # upstream data leaves unset, for instance) are excluded from the digest and listed with a
    # reason, so the exclusion is visible rather than hidden inside a passing test.
    excluded = load_yaml(os.path.join(d, "tests", "digest_exclude.yaml"), {}) or {}
    observed = {}
    for table in own_tables(cfg, d, schema):
        cols = [c for c in columns_of(schema, table)
                if c[0] not in (excluded.get(table, {}) or {})]
        row = db.rows(canon.fingerprint_sql(schema, table, cols))[0]
        observed[table] = {"n": int(row[0]), "x": int(row[1]), "s": int(row[2]),
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


def stage_fks(cfg, schema, d, pin, res):
    # kcu.referenced_table_schema, not the constraint's own schema: Oracle OE's orders and
    # customers reference oracle_hr, and joining against the wrong database finds no table at all
    fks = db.rows(
        "SELECT rc.constraint_name, rc.table_name, kcu.column_name, "
        "kcu.referenced_table_schema, rc.referenced_table_name, "
        "kcu.referenced_column_name FROM information_schema.referential_constraints rc "
        "JOIN information_schema.key_column_usage kcu ON kcu.constraint_name=rc.constraint_name "
        "AND kcu.constraint_schema=rc.constraint_schema "
        f"WHERE rc.constraint_schema='{schema}' ORDER BY 1,3")
    orphans, external = 0, 0
    for name, table, col, rschema, rtable, rcol in fks:
        external += rschema != schema
        n = int(db.rows(
            f"SELECT COUNT(*) FROM `{schema}`.`{table}` c LEFT JOIN `{rschema}`.`{rtable}` p "
            f"ON c.`{col}` = p.`{rcol}` WHERE c.`{col}` IS NOT NULL AND p.`{rcol}` IS NULL")[0][0])
        if n:
            res.fail(f"foreign key {name} ({table}.{col} -> {rschema}.{rtable}.{rcol}) "
                     f"has {n} orphan rows")
            orphans += n
    across = f" ({external} across databases)" if external else ""
    res.note(f"{len(fks)} foreign keys validated{across}, {orphans} orphans")


def stage_indexes(cfg, schema, d, pin, res):
    path = os.path.join(d, "tests", "indexes.yaml")
    observed = {}
    mine = set(own_tables(cfg, d, schema))
    for table, index, nonuniq, itype, cols in [
        (r[0], r[1], r[2], r[3], r[4]) for r in db.rows(
            "SELECT table_name, index_name, MAX(non_unique), MAX(index_type), "
            "GROUP_CONCAT(column_name ORDER BY seq_in_index) "
            f"FROM information_schema.statistics WHERE table_schema='{schema}' "
            "GROUP BY table_name, index_name ORDER BY table_name, index_name")]:
        if table not in mine:
            continue
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
                # A unique-index lookup on a constant can be resolved before execution, and the
                # table then does not appear in the plan at all. That is the strongest possible
                # access path, not a missing table -- but a typo in the test would look the same,
                # so it only passes when the plan says the rows were fetched before execution.
                if "Rows fetched before execution" in blob or '"const"' in blob:
                    continue
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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dataset")
    ap.add_argument("stages", nargs="*", default=[])
    ap.add_argument("--pin", action="store_true")
    a = ap.parse_args(argv)
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
    return 1 if res.failures else 0


if __name__ == "__main__":
    sys.exit(main())
