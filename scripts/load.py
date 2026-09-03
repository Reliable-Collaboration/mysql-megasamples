#!/usr/bin/env python3
"""Load one dataset into the build server, following its datasets/<name>/dataset.yaml.

  python3 scripts/load.py sakila [--fresh]

Native-SQL datasets (converter: none) have their upstream files staged into docker/context/<name>/ by
scripts/stage.py and are streamed straight into the server. Datasets with a converter produce contract
TSV plus build/baseline.json first; that path arrives with the first converted dataset.
"""
import argparse, os, sys, time
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dataset")
    ap.add_argument("--fresh", action="store_true", help="recreate the build server first")
    a = ap.parse_args()
    d = os.path.join(ROOT, "datasets", a.dataset)
    cfg = yaml.safe_load(open(os.path.join(d, "dataset.yaml"), encoding="utf-8"))
    schema, context = cfg["database"], os.path.join(ROOT, "docker", "context", a.dataset)

    if cfg.get("converter") not in (None, "none"):
        sys.exit(f"{a.dataset}: converter '{cfg['converter']}' is not implemented yet")

    db.start(fresh=a.fresh)
    print(f"  . build server ready")
    for needed in cfg.get("depends", []):
        # a cross-database foreign key needs its target to exist before the ALTER runs
        if not db.rows("SELECT schema_name FROM information_schema.schemata "
                       f"WHERE schema_name = '{needed}'"):
            sys.exit(f"{a.dataset} depends on {needed}, which is not loaded; "
                     f"run: make {needed}")
    # A cross-database foreign key blocks DROP DATABASE on the referenced side, and a key left
    # dangling also stops the referenced tables being recreated -- MySQL re-resolves it while the
    # new table still has no unique key. So the dependent keys go first and their database is
    # reloaded afterwards, which is what `depends` in dataset.yaml orders.
    inbound = db.rows(
        "SELECT DISTINCT rc.constraint_schema, rc.table_name, rc.constraint_name "
        "FROM information_schema.referential_constraints rc "
        "JOIN information_schema.key_column_usage kcu USING (constraint_schema, constraint_name) "
        f"WHERE kcu.referenced_table_schema = '{schema}' AND rc.constraint_schema <> '{schema}'")
    for other, table, constraint in inbound:
        db.sql(f"ALTER TABLE `{other}`.`{table}` DROP FOREIGN KEY `{constraint}`")
    if inbound:
        print(f"  ! dropped {len(inbound)} foreign key(s) into {schema} from "
              f"{', '.join(sorted({r[0] for r in inbound}))}; reload those datasets")
    db.sql(f"DROP DATABASE IF EXISTS `{schema}`")
    started = time.time()
    for filename in cfg["load"]:
        path = os.path.join(context, filename)
        if not os.path.exists(path):
            sys.exit(f"missing staged file {path}; run scripts/stage.py {a.dataset}")
        db.sql_file(path)
        print(f"  . loaded {filename} ({os.path.getsize(path):,} bytes)")
    db.sql(f"ANALYZE TABLE " + ", ".join(
        f"`{schema}`.`{r[0]}`" for r in db.rows(
            "SELECT table_name FROM information_schema.tables "
            f"WHERE table_schema='{schema}' AND table_type='BASE TABLE'")))
    size = db.rows("SELECT ROUND(SUM(data_length+index_length)/1048576,1) "
                   f"FROM information_schema.tables WHERE table_schema='{schema}'")[0][0]
    print(f"  . {a.dataset} loaded in {time.time()-started:.1f}s, {size} MB in InnoDB")


if __name__ == "__main__":
    main()
