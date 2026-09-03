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
