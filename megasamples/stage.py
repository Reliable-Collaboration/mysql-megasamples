#!/usr/bin/env python3
"""Stage one dataset: turn its downloaded artifacts into the SQL the MySQL build server loads.

  python3 -m megasamples stage <dataset> [--dry-run]

Conversion runs on the host, into build/stage/<name>/, and the build server reads that directory
(mounted read-only at /context). The base image is oraclelinux:9-slim with microdnf only -- no
unzip, no python3 -- so every archive is opened here and only plain files cross into the server.

How a dataset is staged is declared by the `stage:` block of its dataset.yaml; the output file is
the first entry of its `load:` list:

    stage: {extract: {sakila/sakila-db.zip: [sakila-db/sakila-schema.sql, sakila-db/sakila-data.sql]}}
        copy members out of an archive unchanged (native MySQL scripts)
    stage: {input: artifact}
        convert.py <downloads/<first artifact>> <out.sql> <datasets/<name>/name_map.yaml>
    stage: {input: dir, source: contoso, converter: contoso, args: [--size, 1m]}
        convert.py <downloads/<source>> <out.sql> [args]; `source` and `converter` default to the
        dataset's own name, so a dataset that reuses another's converter names it
    stage: {input: export}
        convert.py <downloads/<name>/export> <out.sql>; the export is made once by `wwi-export`
    stage: {input: none, scale_factor: true}
        generators: convert.py <out.sql> --sf <SF>, from the SF environment variable, else
                    megasamples.yaml build.scale_factor (default 1)

A dataset with no `stage:` block and an empty `load:` list (the licence-gated bike-share datasets)
has nothing to stage: its loader writes the SQL itself.
"""
import argparse, os, subprocess, sys, zipfile

from megasamples import datasets as inventory
from megasamples.paths import DATASETS, DOWNLOADS, ROOT, rel, stage_dir


def plan(name):
    """[(description, action)] for one dataset; each action is a list of steps to run in order."""
    cfg = inventory.load(name)
    spec = cfg.get("stage")
    loads = cfg.get("load") or []
    if not spec:
        if loads:
            raise SystemExit(f"{name}: dataset.yaml lists files to load but has no `stage:` block")
        return []
    dest = stage_dir(name)
    steps = []
    if "extract" in spec:
        for artifact, members in spec["extract"].items():
            src = os.path.join(DOWNLOADS, artifact)
            steps.append((f"extract {len(members)} file(s) from {rel(src)}", ("extract", src, members, dest)))
        return steps
    if not loads:
        raise SystemExit(f"{name}: a `stage:` block needs a `load:` list naming its output")
    out = os.path.join(dest, loads[0])
    converter = os.path.join(DATASETS, spec.get("converter") or name, "convert.py")
    kind = spec.get("input", "dir")
    argv = [sys.executable, converter]
    if kind == "artifact":
        artifacts = cfg.get("artifacts") or []
        if not artifacts:
            raise SystemExit(f"{name}: input: artifact but dataset.yaml lists no artifacts")
        argv += [os.path.join(DOWNLOADS, artifacts[0]), out, os.path.join(DATASETS, name, "name_map.yaml")]
    elif kind == "dir":
        argv += [os.path.join(DOWNLOADS, spec.get("source") or name), out]
    elif kind == "export":
        export = os.path.join(DOWNLOADS, name, "export")
        steps.append((f"require {rel(export)}/meta.json", ("require", os.path.join(export, "meta.json"),
                      f"{name}: no export in {rel(export)}. It is produced once, by:\n"
                      f"    MEGASAMPLES_ACCEPT_MSSQL_EULA=1 make wwi-export\n"
                      f"which runs SQL Server under Microsoft's Developer EULA -- see "
                      f"knowledge/licenses/microsoft-sql-server-developer-eula.md")))
        argv += [export, out]
    elif kind == "none":
        argv += [out]
    else:
        raise SystemExit(f"{name}: unknown stage input kind {kind!r}")
    argv += [str(a) for a in (spec.get("args") or [])]
    if spec.get("scale_factor"):
        from megasamples import config as stack
        argv += ["--sf", os.environ.get("SF") or str(stack.load().build.get("scale_factor", 1))]
    steps.append((f"run {rel(converter)} -> {rel(out)}", ("run", argv, dest)))
    return steps


def execute(name, step):
    kind = step[0]
    if kind == "extract":
        _, src, members, dest = step
        os.makedirs(dest, exist_ok=True)
        with zipfile.ZipFile(src) as z:
            for member in members:
                out = os.path.join(dest, os.path.basename(member))
                with open(out, "wb") as fh:
                    fh.write(z.read(member))
                print(f"  . staged {os.path.basename(member)} ({os.path.getsize(out):,} bytes)")
    elif kind == "require":
        _, path, message = step
        if not os.path.exists(path):
            sys.exit(message)
    elif kind == "run":
        _, argv, dest = step
        os.makedirs(dest, exist_ok=True)
        if subprocess.run(argv, cwd=ROOT, text=True).returncode != 0:
            sys.exit(f"{name} conversion failed")


def stage(name, dry_run=False):
    steps = plan(name)
    if not steps:
        print(f"  . {name}: nothing to stage")
        return 0
    for description, step in steps:
        print(f"  {'~' if dry_run else '.'} {name}: {description}")
        if not dry_run:
            execute(name, step)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("datasets", nargs="+")
    ap.add_argument("--dry-run", action="store_true", help="print the steps without running them")
    a = ap.parse_args(argv)
    for name in a.datasets:
        stage(name, a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
