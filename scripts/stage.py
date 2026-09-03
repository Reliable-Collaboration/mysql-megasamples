#!/usr/bin/env python3
"""Extract a dataset's downloaded artifacts into docker/context/<name>/ for the build server.

The base image is oraclelinux:9-slim with microdnf only -- no unzip, no python3 (found at P-03) -- so
every archive is opened here on the host and only plain files cross into the image.
"""
import os, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STAGERS = {}


def stager(name):
    def wrap(fn): STAGERS[name] = fn; return fn
    return wrap


@stager("sakila")
def stage_sakila(dest):
    src = os.path.join(ROOT, "downloads", "sakila", "sakila-db.zip")
    with zipfile.ZipFile(src) as z:
        for member in ("sakila-db/sakila-schema.sql", "sakila-db/sakila-data.sql"):
            out = os.path.join(dest, os.path.basename(member))
            with open(out, "wb") as fh:
                fh.write(z.read(member))
            print(f"  . staged {os.path.basename(member)} ({os.path.getsize(out):,} bytes)")
    # sakila.mwb is a Workbench model and is NOT under the BSD licence: never stage or ship it.


@stager("chinook")
def stage_chinook(dest):
    """Run the dataset's own converter; it owns every Chinook-specific rewrite."""
    _run_converter("chinook", os.path.join(ROOT, "downloads", "chinook", "Chinook_MySql.sql"),
                   os.path.join(dest, "chinook.sql"))


@stager("northwind")
def stage_northwind(dest):
    _run_converter("northwind", os.path.join(ROOT, "downloads", "northwind", "instnwnd.sql"),
                   os.path.join(dest, "northwind.sql"))


@stager("pubs")
def stage_pubs(dest):
    _run_converter("pubs", os.path.join(ROOT, "downloads", "pubs", "instpubs.sql"),
                   os.path.join(dest, "pubs.sql"))


def _run_converter(name, src, out):
    import subprocess
    conv = os.path.join(ROOT, "datasets", name, "convert.py")
    name_map = os.path.join(ROOT, "datasets", name, "name_map.yaml")
    if subprocess.run([sys.executable, conv, src, out, name_map], text=True).returncode != 0:
        sys.exit(f"{name} conversion failed")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in STAGERS:
        sys.exit(f"usage: stage.py <{'|'.join(sorted(STAGERS))}>")
    name = sys.argv[1]
    dest = os.path.join(ROOT, "docker", "context", name)
    os.makedirs(dest, exist_ok=True)
    STAGERS[name](dest)


if __name__ == "__main__":
    main()
