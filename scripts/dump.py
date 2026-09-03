#!/usr/bin/env python3
"""Dump one loaded database from the build server into the format the image builder consumes.

  python3 scripts/dump.py sakila

Uses MySQL Shell's `util.dumpSchemas`, whose output `util.loadDump` can restore with
`deferTableIndexes`, so the image builder creates secondary indexes after the data is in place
(PLAN.md section 5). The dump directory is content-addressed by a manifest the image build reads.
"""
import argparse, hashlib, json, os, shutil, sys, time
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dump(dataset):
    cfg = yaml.safe_load(open(os.path.join(ROOT, "datasets", dataset, "dataset.yaml"), encoding="utf-8"))
    schema = cfg["database"]
    host_dir = os.path.join(ROOT, "build", "dumps", dataset)
    if os.path.exists(host_dir):
        shutil.rmtree(host_dir)
    os.makedirs(os.path.dirname(host_dir), exist_ok=True)
    started = time.time()
    # mysqlsh needs the directory to not exist; it creates it itself
    script = (f"util.dump_schemas(['{schema}'], '/build/dumps/{dataset}', "
              f"{{'showProgress': False, 'compression': 'zstd', 'threads': 4}})")
    # --no-defaults: mysqlsh reads my.cnf's [client] section and rejects default-character-set,
    # which the MySQL Shell record already flagged as a difference from the mysql client.
    # Run the shell as the host user (over TCP, since the socket is only reachable by uid 999) so
    # the dump files land owned by the caller instead of by the container's mysql user.
    out = db.run(["docker", "exec", "-u", f"{os.getuid()}:{os.getgid()}",
                  "-e", "HOME=/build",          # mysqlsh needs a writable home for its state dir
                  db.NAME,
                  "mysqlsh", "--no-defaults", f"root:{db.PW}@127.0.0.1:3306", "--py", "-e", script])
    if out.returncode != 0:
        sys.exit(f"dump failed:\n{out.stdout}\n{out.stderr}")
    files = sorted(f for f in os.listdir(host_dir))
    digest = hashlib.sha256()
    total = 0
    for name in files:
        path = os.path.join(host_dir, name)
        digest.update(name.encode())
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                digest.update(chunk)
        total += os.path.getsize(path)
    manifest = {"dataset": dataset, "database": schema, "files": len(files),
                "bytes": total, "sha256": digest.hexdigest(),
                "seconds": round(time.time() - started, 2)}
    with open(os.path.join(ROOT, "build", "dumps", f"{dataset}.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
    print(f"  . dumped {schema}: {len(files)} files, {total:,} bytes, sha256 {digest.hexdigest()[:12]}")
    return manifest


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("datasets", nargs="+")
    a = ap.parse_args()
    db.start()
    for name in a.datasets:
        dump(name)
