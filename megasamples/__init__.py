"""sql-megasamples: sample databases for MySQL, PostgreSQL and SQLite, built from their upstream
sources by a scripted pipeline and shipped as Docker images plus a browsing console.

    python3 -m megasamples <command> [args]      every command; `--help` lists them
    make <target>                                 thin shims over the same commands

The package is laid out by responsibility:

    megasamples/            the pipeline: fetch, stage, verify, registry, catalogue, release, checks
    megasamples/engines/    one subpackage per database engine (build server, load, dump, image)
    megasamples/sources/    translators and exporters for upstream formats (T-SQL, PL/SQL, .bak, ...)
    megasamples/port/       the MySQL corpus -> engine-neutral model -> other engines

ARCHITECTURE.md describes how the pieces fit; every path comes from megasamples/paths.py.
"""
__version__ = "2.0.0-dev"
