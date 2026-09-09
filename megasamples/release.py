#!/usr/bin/env python3
"""Stage the `data-v1` release assets. Prepares; never publishes.

  python3 -m megasamples release stage [--set data-v1|sqlite]   copy the assets into release/<set>/ and write the manifest
  python3 -m megasamples release check [--set ...]              re-verify what is staged against SHA256SUMS

Two asset sets exist. `data-v1` mirrors upstream source artifacts a third party could not otherwise
obtain and verify (the rule below). `sqlite` is the SQLite port of every core dataset -- one file per
database plus the registry, from build/sqlite/ -- staged so the files can be published for readers
that want a database without a server.

This script has no network access and creates no release. Uploading the staged directory, tagging
`data-v1` and making it public are the maintainer's decisions, not the build's (ARCHITECTURE.md section 8).

**What belongs in the release, and what does not.** An asset earns its place by being something a
third party cannot otherwise obtain and check for themselves:

* `lahman` is published through a SABR share link with no static URL, so no build can fetch it and
  nobody but the maintainer can verify the digest recorded in `manifest.yaml`.
* `chicago_crimes` comes from an API whose content changes daily -- the 2024 subset the image is
  built from is a snapshot that cannot be re-fetched byte-identically tomorrow.
* The two Stack Exchange archives exist only inside an archive.org item that could be taken down. They carry CC BY-SA and nothing else: the project deliberately sources the 2024-04
  snapshot, which predates the click-through it never accepted
  (knowledge/licenses/stackexchange-data-dump-terms.md).

Everything else in `downloads/` has a stable upstream URL with a pinned sha256, so mirroring it would
add bytes and no verifiability. Two categories may never be staged at all, and `forbidden()` refuses
rather than trusting this list to stay right: Citi Bike and Divvy data, whose licences prohibit
redistribution as a stand-alone dataset, and anything TPC-generated.
"""
import argparse, hashlib, os, shutil, sys

from megasamples.paths import ROOT
STAGE = os.path.join(ROOT, "release", "data-v1")
FORBIDDEN_DATASETS = ("citibike", "divvy", "tpch", "tpcds", "tpcc", "ssb")

# (source path under downloads/, name in the release, dataset, licence id, why it is mirrored)
ASSETS = [
    ("lahman/lahman_1871-2025_csv.zip", "lahman_1871-2025_csv.zip",
     "lahman", "cc-by-sa-3-0", "SABR publishes it through a Box share with no static URL"),
    ("chicago_crimes/crimes_2024.csv", "chicago-crimes-2024.csv",
     "chicago_crimes", "chicago-data-portal-terms", "the portal's data changes daily"),
    ("chicago_crimes/iucr.csv", "chicago-iucr.csv",
     "chicago_crimes", "chicago-data-portal-terms", "the portal's data changes daily"),
    ("stackexchange_dba/dba.stackexchange.com.7z", "dba.stackexchange.com.7z",
     "stackexchange_dba", "cc-by-sa-4-0", "the archive.org item could be taken down"),
    ("stackexchange_beer/beer.stackexchange.com.7z", "beer.stackexchange.com.7z",
     "stackexchange_beer", "cc-by-sa-4-0", "the archive.org item could be taken down"),
]


def forbidden(rel, dataset):
    """Refuse anything whose licence forbids redistribution, whatever ASSETS claims."""
    hay = f"{rel} {dataset}".lower()
    return next((d for d in FORBIDDEN_DATASETS if d in hay), None)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def place(src, dst):
    """Hardlink when the filesystem allows it -- these are large files and a copy is 470 MB of
    duplication for no gain. Falls back to a copy across devices."""
    if os.path.exists(dst):
        os.remove(dst)
    try:
        os.link(src, dst)
        return "linked"
    except OSError:
        shutil.copy2(src, dst)
        return "copied"


def stage_sqlite():
    """The SQLite files under build/sqlite/, hardlinked into release/sqlite/ with checksums."""
    from megasamples import datasets as inventory
    from megasamples.engines.sqlite import port as sqlite_port
    from megasamples.paths import engine_build_dir
    stage_dir = os.path.join(ROOT, "release", "sqlite")
    os.makedirs(stage_dir, exist_ok=True)
    rows, missing = [], []
    for name in inventory.core():
        db = inventory.load(name)["database"]
        src = os.path.join(engine_build_dir("sqlite"), db, f"{db}.sqlite")
        if not os.path.exists(src):
            missing.append(name)
            print(f"  x {db}.sqlite: not built -- make build ENGINE=sqlite D={name}")
            continue
        how = place(src, os.path.join(stage_dir, f"{db}.sqlite"))
        digest, size = sha256(os.path.join(stage_dir, f"{db}.sqlite")), os.path.getsize(src)
        rows.append((f"{db}.sqlite", digest, size, name, ", ".join(inventory.load(name).get("licenses") or []), "the port of this dataset"))
        print(f"  . {db + '.sqlite':<34} {size/1e6:>8.1f} MB  {digest[:12]} ({how})")
    registry = os.path.join(stage_dir, "megasamples.sqlite")
    sqlite_port.write_registry(registry, [n for n in inventory.core() if n not in missing])
    rows.append(("megasamples.sqlite", sha256(registry), os.path.getsize(registry), "-", "-", "the provenance registry"))
    with open(os.path.join(stage_dir, "SHA256SUMS"), "w", encoding="utf-8") as fh:
        for r in sorted(rows):
            fh.write(f"{r[1]}  {r[0]}\n")
    lines = ["# sqlite release assets", "",
             "Staged by `python3 -m megasamples release stage --set sqlite`. **Not published**: creating the",
             "release, uploading these files and making them public is the maintainer's decision.", "",
             "One SQLite file per core database, ported from the verified MySQL corpus and checked against the",
             "same counts, content digests, foreign keys and indexes (`knowledge/decisions/sqlite-file-conventions.md`),",
             "plus `megasamples.sqlite`, the provenance registry. Each database keeps its own upstream licence,",
             "named below and in full in `datasets/<name>/LICENSE`; the share-alike ones stay under their terms.", "",
             "Verify with `sha256sum -c SHA256SUMS`, or `python3 -m megasamples release check --set sqlite`.", "",
             "| file | size | dataset | licence |", "|---|---:|---|---|"]
    for name, _d, size, dataset, licence, _why in sorted(rows):
        lines.append(f"| `{name}` | {size/1e6:.1f} MB | `{dataset}` | {licence} |")
    with open(os.path.join(stage_dir, "MANIFEST.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    total = sum(r[2] for r in rows)
    print(f"\nstaged {len(rows)} file(s), {total/1e6:.0f} MB, in {os.path.relpath(stage_dir, ROOT)}")
    print("nothing has been published; creating the release is the maintainer's step")
    return 1 if missing else 0


def stage():
    os.makedirs(STAGE, exist_ok=True)
    rows, missing = [], []
    for rel, name, dataset, licence, why in ASSETS:
        bad = forbidden(rel, dataset)
        if bad:
            sys.exit(f"refusing to stage {name}: {bad} data is not redistributable")
        src = os.path.join(ROOT, "downloads", rel)
        if not os.path.exists(src):
            missing.append(rel)
            print(f"  x {name}: not in downloads/ -- fetch it before staging")
            continue
        how = place(src, os.path.join(STAGE, name))
        digest, size = sha256(os.path.join(STAGE, name)), os.path.getsize(src)
        rows.append((name, digest, size, dataset, licence, why))
        print(f"  . {name:<34} {size/1e6:>8.1f} MB  {digest[:12]} ({how})")

    with open(os.path.join(STAGE, "SHA256SUMS"), "w", encoding="utf-8") as fh:
        for name, digest, *_ in sorted(rows):
            fh.write(f"{digest}  {name}\n")

    write_manifest(rows)
    total = sum(r[2] for r in rows)
    print(f"\nstaged {len(rows)} asset(s), {total/1e6:.0f} MB, in {os.path.relpath(STAGE, ROOT)}")
    if missing:
        print(f"missing {len(missing)}: " + ", ".join(missing))
    print("nothing has been published; creating the release is the maintainer's step")
    return 1 if missing else 0


def write_manifest(rows):
    lines = [
        "# data-v1 release assets",
        "",
        "Staged by `python3 -m megasamples release stage`. **Not published**: creating the GitHub release,",
        "uploading these files and making them public is the maintainer's decision (ARCHITECTURE.md section 8).",
        "",
        "Each file here is an *upstream source artifact*, not a converted database. It is mirrored",
        "because a third party cannot otherwise obtain and verify it — either upstream has no stable",
        "URL, or its content changes underneath the recorded checksum. Everything else the build",
        "downloads has a stable URL with a pinned sha256 in `manifest.yaml` and is deliberately absent.",
        "",
        "Verify with `sha256sum -c SHA256SUMS`, or `python3 -m megasamples release check`.",
        "",
        "| asset | size | licence | mirrored because |",
        "|---|---:|---|---|",
    ]
    for name, _digest, size, _dataset, licence, why in sorted(rows):
        lines.append(f"| `{name}` | {size/1e6:.1f} MB | [{licence}](../../knowledge/licenses/{licence}.md) | {why} |")
    lines += [
        "",
        "## Attribution travels with these files",
        "",
        "* **Lahman** is CC BY-SA 3.0: the SABR notice in `datasets/lahman/LICENSE` must accompany any",
        "  redistribution, and a modified database must be offered under the same licence.",
        "* **Chicago** data carries a **mandatory verbatim disclaimer**, reproduced in `NOTICE.md` and",
        "  `README.md`; the City also reserves the right to require distribution to stop.",
        "* **Stack Exchange** content is CC BY-SA 4.0 with per-post attribution requirements; the",
        "  `contentlicense` column is preserved per row. The project sources the 2024-04 archive.org",
        "  snapshot, which predates the current click-through — a contract it has never accepted.",
        "",
        "No Citi Bike or Divvy data is here, and none may be added: both licences prohibit",
        "redistribution as a stand-alone dataset. No TPC-generated data is here either.",
        "`megasamples/release.py` refuses either regardless of what its asset list says.",
    ]
    with open(os.path.join(STAGE, "MANIFEST.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def check(stage_dir=None):
    sums = os.path.join(stage_dir or STAGE, "SHA256SUMS")
    if not os.path.exists(sums):
        sys.exit(f"nothing staged: {os.path.relpath(sums, ROOT)} does not exist")
    failures = 0
    for line in open(sums, encoding="utf-8"):
        want, name = line.strip().split("  ", 1)
        path = os.path.join(stage_dir or STAGE, name)
        if not os.path.exists(path):
            print(f"  x {name}: missing"); failures += 1; continue
        got = sha256(path)
        print(f"  {'.' if got == want else 'x'} {name:<34} {got[:12]}")
        failures += got != want
    print(f"release: {failures} failure(s)")
    return 1 if failures else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", choices=["stage", "check"], nargs="?", default="stage")
    ap.add_argument("--set", default="data-v1", choices=["data-v1", "sqlite"])
    a = ap.parse_args(argv)
    if a.set == "sqlite":
        return stage_sqlite() if a.action == "stage" else check(os.path.join(ROOT, "release", "sqlite"))
    return stage() if a.action == "stage" else check()


if __name__ == "__main__":
    sys.exit(main())
