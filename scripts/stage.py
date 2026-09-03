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


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in STAGERS:
        sys.exit(f"usage: stage.py <{'|'.join(sorted(STAGERS))}>")
    name = sys.argv[1]
    dest = os.path.join(ROOT, "docker", "context", name)
    os.makedirs(dest, exist_ok=True)
    STAGERS[name](dest)


if __name__ == "__main__":
    main()
