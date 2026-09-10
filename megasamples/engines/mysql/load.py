#!/usr/bin/env python3
"""Load one dataset into the build server, following its datasets/<name>/dataset.yaml.

  python3 -m megasamples load sakila [--fresh]

The staged SQL under build/stage/<name>/ (written by `megasamples stage`) is streamed into the
server file by file, in the order dataset.yaml lists. A dataset that appends to another's database
adds its tables without dropping anything; every other load drops and recreates its database.
"""
import argparse, os, sys, time
import yaml
from megasamples.engines.mysql import server as db  # noqa: E402

from megasamples.paths import ROOT, stage_dir


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dataset")
    ap.add_argument("--fresh", action="store_true", help="recreate the build server first")
    a = ap.parse_args(argv)
    d = os.path.join(ROOT, "datasets", a.dataset)
    cfg = yaml.safe_load(open(os.path.join(d, "dataset.yaml"), encoding="utf-8"))
    schema, context = cfg["database"], stage_dir(a.dataset)

    db.start(fresh=a.fresh)
    print(f"  . build server ready")
    for needed in cfg.get("depends", []):
        # a cross-database foreign key needs its target to exist before the ALTER runs
        if not db.rows("SELECT schema_name FROM information_schema.schemata "
                       f"WHERE schema_name = '{needed}'"):
            sys.exit(f"{a.dataset} depends on {needed}, which is not loaded; "
                     f"run: make {needed}")
    # An extended-tier dataset adds tables to a database the core build already made, so it must
    # not drop it. `append: true` in dataset.yaml says so.
    if cfg.get("append"):
        if not db.rows("SELECT schema_name FROM information_schema.schemata "
                       f"WHERE schema_name = '{schema}'"):
            sys.exit(f"{a.dataset} appends to `{schema}`, which is not loaded; "
                     f"run: make {schema}")
        started = time.time()
        for filename in cfg["load"]:
            path = os.path.join(context, filename)
            if not os.path.exists(path):
                sys.exit(f"missing staged file {path}; run: python3 -m megasamples stage {a.dataset}")
            db.sql_file(path)
            print(f"  . loaded {filename} ({os.path.getsize(path):,} bytes)")
        tables = [r[0] for r in db.rows(
            "SELECT table_name FROM information_schema.tables "
            f"WHERE table_schema='{schema}' AND table_type='BASE TABLE'")]
        db.sql("ANALYZE TABLE " + ", ".join(f"`{schema}`.`{t}`" for t in tables))
        size = db.rows("SELECT ROUND(SUM(data_length+index_length)/1048576,1) "
                       f"FROM information_schema.tables WHERE table_schema='{schema}'")[0][0]
        print(f"  . {a.dataset} appended in {time.time()-started:.1f}s; "
              f"`{schema}` is now {size} MB in InnoDB")
        return

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
            sys.exit(f"missing staged file {path}; run: python3 -m megasamples stage {a.dataset}")
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
    sys.exit(main())
