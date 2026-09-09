#!/usr/bin/env python3
"""The pre-publication checklist (ARCHITECTURE.md section 8), as something you can run.

  python3 -m megasamples prepub-check [--image sql-megasamples-mysql:dev] [--skip-image]

Ten items, each either proved here or delegated to the script that owns it. Written to be re-run:
these are the checks that must still pass the day the release is actually published, which may be
long after the day it was prepared.

Items 4, 5 and 6 (nothing unredistributable in the repo, image or release) are `audit_assets.py`;
item 1 is `gen_provenance.py --check`. This script runs both rather than reimplementing them.
"""
import argparse, os, re, subprocess, sys

import yaml

from megasamples.paths import ROOT
PY = sys.executable
# the share-alike datasets, grouped as the README names them (both Stack Exchange databases carry
# the same obligation and are named once)
SHARE_ALIKE = {"employees": "employees", "lahman": "lahman",
               "Stack Exchange": "stackexchange_beer / stackexchange_dba",
               "wikipedia_simple": "wikipedia_simple"}


def read(path):
    full = os.path.join(ROOT, path)
    return open(full, encoding="utf-8").read() if os.path.exists(full) else ""


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def item(n, title, ok, detail=""):
    print(f"  {'.' if ok else 'x'} {n:>2}. {title}" + (f" — {detail}" if detail else ""))
    return [] if ok else [f"{n}. {title}: {detail or 'failed'}"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--image", default=os.environ.get("MEGASAMPLES_MYSQL_IMAGE", "sql-megasamples-mysql:dev"))
    ap.add_argument("--skip-image", action="store_true")
    a = ap.parse_args(argv)
    f = []
    readme, notice = read("README.md"), read("NOTICE.md")

    # 1 -------------------------------------------------------------------------------------
    p = run([PY, "-m", "megasamples", "provenance", "--check"])
    f += item(1, "generated licence and provenance files are up to date", p.returncode == 0,
              p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr.strip()[:80])

    # 2 -------------------------------------------------------------------------------------
    missing = []
    for d in sorted(os.listdir(os.path.join(ROOT, "datasets"))):
        if not os.path.exists(os.path.join(ROOT, "datasets", d, "dataset.yaml")):
            continue
        for name in ("LICENSE", "PROVENANCE.md"):
            if not os.path.exists(os.path.join(ROOT, "datasets", d, name)):
                missing.append(f"{d}/{name}")
    # A dataset needs pinned digests only if it downloads something. citibike and divvy are fetched
    # by the user and never mirrored; the TPC-family datasets are generated locally. For those the
    # requirement is the opposite: the file must NOT claim to pin bytes it does not have.
    manifest = yaml.safe_load(read("manifest.yaml"))["artifacts"]
    by_id = {x["id"]: x for x in manifest}
    owned = {}
    for x in manifest:
        owned.setdefault(x["dataset"], set()).add(x["id"])
    prov_no_sha, false_claim = [], []
    for d in sorted(os.listdir(os.path.join(ROOT, "datasets"))):
        spec_path = os.path.join(ROOT, "datasets", d, "dataset.yaml")
        if not os.path.exists(spec_path):
            continue
        cfg = yaml.safe_load(open(spec_path, encoding="utf-8")) or {}
        ids = owned.get(d, set()) | {i for i in (cfg.get("artifacts") or []) if i in by_id}
        text = read(f"datasets/{d}/PROVENANCE.md")
        if ids and not re.search(r"\b[0-9a-f]{64}\b", text):
            prov_no_sha.append(d)
        if not ids and "Every byte this database is built from, pinned" in text:
            false_claim.append(d)
    f += item(2, "every dataset has LICENSE and PROVENANCE.md, and pins what it downloads",
              not missing and not prov_no_sha and not false_claim,
              (f"missing {', '.join(missing[:3])}" if missing else "") +
              (f" no sha256 in {', '.join(prov_no_sha[:3])}" if prov_no_sha else "") +
              (f" claims to pin nothing it has: {', '.join(false_claim[:3])}" if false_claim else ""))

    # 3 -------------------------------------------------------------------------------------
    said = "offers those four converted databases under the same" in readme or \
           "under the same licence" in readme
    absent = [k for k in SHARE_ALIKE if k not in readme]
    f += item(3, "README states the share-alike datasets stay under their own licence",
              said and not absent,
              f"not named: {', '.join(absent)}" if absent else f"all {len(SHARE_ALIKE)} named")

    # 4, 5, 6 -------------------------------------------------------------------------------
    cmd = [PY, "-m", "megasamples", "audit-assets", "--image", a.image] + (["--skip-image"] if a.skip_image else [])
    p = run(cmd)
    f += item(4, "no Citi Bike, Divvy or TPC data in the repo, image or release (audit_assets.py)",
              p.returncode == 0, p.stdout.strip().splitlines()[-1] if p.stdout else "")

    tpc_ok = all("TPC Benchmark" in read(f"datasets/{d}/LICENSE") for d in ("tpch", "tpcds", "ssb"))
    metrics = [m for m in ("QphH", "QphDS", "tpmC", "TPC results") if m in readme]
    f += item(5, "TPC licences carry the EULA legend and the README claims no TPC metrics",
              tpc_ok and not metrics, f"metric names used: {metrics}" if metrics else "")

    f += item(6, "no non-redistributable binaries committed or added to the image (audit_assets.py)",
              p.returncode == 0)

    # 7 -------------------------------------------------------------------------------------
    enron = read("datasets/enron/PROVENANCE.md")
    f += item(7, "Enron provenance documents the personal data and the removal procedure",
              "personal" in enron.lower() and ("removal" in enron.lower() or "deletion" in enron.lower()))

    # 8 -------------------------------------------------------------------------------------
    se = read("datasets/stackexchange_beer/PROVENANCE.md") + read("datasets/stackexchange_dba/PROVENANCE.md")
    f += item(8, "Stack Exchange provenance records the 2024-04-02 snapshot and the unaccepted click-through",
              "2024-04-02" in se and "click-through" in se.lower())

    # 9 -------------------------------------------------------------------------------------
    notices = {
        "Chicago disclaimer": "makes no claims as to the content",
        "hbiostat acknowledgement": "courtesy of the Vanderbilt University",
        "Iris attribution": "The use of multiple measurements",
    }
    absent = [k for k, v in notices.items() if v not in readme or v not in notice]
    f += item(9, "the mandatory notices are verbatim in README.md and NOTICE.md",
              not absent, f"missing: {', '.join(absent)}" if absent else "")

    # 10 ------------------------------------------------------------------------------------
    has_notes = "Licensing notes" in readme
    topics = [t for t in ("NYC", "Titanic", "Enron", "DVD Store", "Jaffle") if t in readme]
    f += item(10, "README lists the open licensing questions with their status",
              has_notes and len(topics) == 5, f"{len(topics)} of 5 topics named")

    for x in f:
        print(f"  x {x}")
    print(f"pre-publication: {len(f)} failure(s)")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
