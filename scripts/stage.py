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


@stager("smallsets")
def stage_smallsets(dest):
    _run_dir_converter("smallsets", os.path.join(ROOT, "downloads", "smallsets"),
                       os.path.join(dest, "smallsets.sql"))


@stager("jaffle_shop")
def stage_jaffle_shop(dest):
    _run_dir_converter("jaffle_shop", os.path.join(ROOT, "downloads", "jaffle_shop"),
                       os.path.join(dest, "jaffle_shop.sql"))


@stager("oracle_hr")
def stage_oracle_hr(dest):
    _run_dir_converter("oracle_hr", os.path.join(ROOT, "downloads", "oracle_hr"),
                       os.path.join(dest, "oracle_hr.sql"))


@stager("oracle_co")
def stage_oracle_co(dest):
    _run_dir_converter("oracle_co", os.path.join(ROOT, "downloads", "oracle_co"),
                       os.path.join(dest, "oracle_co.sql"))


@stager("employees")
def stage_employees(dest):
    _run_dir_converter("employees", os.path.join(ROOT, "downloads", "employees"),
                       os.path.join(dest, "employees.sql"))


@stager("adventureworks_lt")
def stage_adventureworks_lt(dest):
    _run_converter("adventureworks_lt",
                   os.path.join(ROOT, "downloads", "adventureworks_lt",
                                "adventure-works-2012-oltp-lt-script.zip"),
                   os.path.join(dest, "adventureworks_lt.sql"))


@stager("wikipedia_simple")
def stage_wikipedia_simple(dest):
    _run_dir_converter("wikipedia_simple",
                       os.path.join(ROOT, "downloads", "wikipedia_simple"),
                       os.path.join(dest, "wikipedia_simple.sql"))


@stager("enron")
def stage_enron(dest):
    _run_dir_converter("enron", os.path.join(ROOT, "downloads", "enron"),
                       os.path.join(dest, "enron.sql"))


@stager("wikipedia_simple_full")
def stage_wikipedia_simple_full(dest):
    """Every ns0 article, in its own database; the core ships the 5,000 lowest page_ids."""
    import subprocess
    conv = os.path.join(ROOT, "datasets", "wikipedia_simple", "convert.py")
    out = os.path.join(dest, "wikipedia_simple_full.sql")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if subprocess.run([sys.executable, conv, os.path.join(ROOT, "downloads", "wikipedia_simple"),
                       out, "--full"], text=True).returncode != 0:
        sys.exit("wikipedia_simple_full conversion failed")


@stager("enron_full")
def stage_enron_full(dest):
    """The whole 150-mailbox corpus, in its own database; the core ships 5 mailboxes."""
    import subprocess
    conv = os.path.join(ROOT, "datasets", "enron", "convert.py")
    out = os.path.join(dest, "enron_full.sql")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if subprocess.run([sys.executable, conv, os.path.join(ROOT, "downloads", "enron"), out,
                       "--full"], text=True).returncode != 0:
        sys.exit("enron_full conversion failed")


@stager("lahman")
def stage_lahman(dest):
    _run_dir_converter("lahman", os.path.join(ROOT, "downloads", "lahman"),
                       os.path.join(dest, "lahman.sql"))


@stager("stackexchange_beer")
def stage_stackexchange_beer(dest):
    _run_dir_converter("stackexchange_beer",
                       os.path.join(ROOT, "downloads", "stackexchange_beer"),
                       os.path.join(dest, "stackexchange_beer.sql"))


@stager("tpcds")
def stage_tpcds(dest):
    import subprocess
    conv = os.path.join(ROOT, "datasets", "tpcds", "convert.py")
    out = os.path.join(dest, "tpcds.sql")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if subprocess.run([sys.executable, conv, out, "--sf", os.environ.get("SF", "1")],
                      text=True).returncode != 0:
        sys.exit("tpcds generation failed")


@stager("tpch")
def stage_tpch(dest):
    """Generated, not downloaded: SF comes from the environment so `make gen-tpch SF=…` works."""
    import subprocess
    conv = os.path.join(ROOT, "datasets", "tpch", "convert.py")
    out = os.path.join(dest, "tpch.sql")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if subprocess.run([sys.executable, conv, out, "--sf", os.environ.get("SF", "1")],
                      text=True).returncode != 0:
        sys.exit("tpch generation failed")


@stager("stackexchange_dba")
def stage_stackexchange_dba(dest):
    """The same converter, a different site: dba.stackexchange.com in its own database."""
    import subprocess
    conv = os.path.join(ROOT, "datasets", "stackexchange_beer", "convert.py")
    out = os.path.join(dest, "stackexchange_dba.sql")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if subprocess.run([sys.executable, conv, os.path.join(ROOT, "downloads", "stackexchange_dba"),
                       out, "--site", "dba"], text=True).returncode != 0:
        sys.exit("stackexchange_dba conversion failed")


@stager("chicago_crimes")
def stage_chicago_crimes(dest):
    _run_dir_converter("chicago_crimes", os.path.join(ROOT, "downloads", "chicago_crimes"),
                       os.path.join(dest, "chicago_crimes.sql"))


@stager("nyc_taxi")
def stage_nyc_taxi(dest):
    _run_dir_converter("nyc_taxi", os.path.join(ROOT, "downloads", "nyc_taxi"),
                       os.path.join(dest, "nyc_taxi.sql"))


def _stage_contoso_size(dest, size):
    """The extended tier: the same eight tables at 1 M or 10 M orders, in their own database."""
    import subprocess
    conv = os.path.join(ROOT, "datasets", "contoso", "convert.py")
    out = os.path.join(dest, f"contoso_{size}.sql")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if subprocess.run([sys.executable, conv, os.path.join(ROOT, "downloads", "contoso"), out,
                       "--size", size], text=True).returncode != 0:
        sys.exit(f"contoso_{size} conversion failed")


@stager("contoso_1m")
def stage_contoso_1m(dest):
    _stage_contoso_size(dest, "1m")


@stager("contoso_10m")
def stage_contoso_10m(dest):
    _stage_contoso_size(dest, "10m")


@stager("chicago_crimes_full")
def stage_chicago_crimes_full(dest):
    """The extended tier: 2001..2024 appended to an existing chicago_crimes."""
    import subprocess
    conv = os.path.join(ROOT, "datasets", "chicago_crimes", "convert.py")
    out = os.path.join(dest, "chicago_crimes_full.sql")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if subprocess.run([sys.executable, conv, os.path.join(ROOT, "downloads", "chicago_crimes"),
                       out, "--full"], text=True).returncode != 0:
        sys.exit("chicago_crimes_full conversion failed")


@stager("bts_ontime")
def stage_bts_ontime(dest):
    _run_dir_converter("bts_ontime", os.path.join(ROOT, "downloads", "bts_ontime"),
                       os.path.join(dest, "bts_ontime.sql"))


@stager("nyc_taxi_yellow")
def stage_nyc_taxi_yellow(dest):
    """The extended tier: yellow trips appended to an existing nyc_taxi, never baked in."""
    import subprocess
    conv = os.path.join(ROOT, "datasets", "nyc_taxi", "convert.py")
    out = os.path.join(dest, "nyc_taxi_yellow.sql")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if subprocess.run([sys.executable, conv, os.path.join(ROOT, "downloads", "nyc_taxi"), out,
                       "--yellow"], text=True).returncode != 0:
        sys.exit("nyc_taxi_yellow conversion failed")


@stager("contoso")
def stage_contoso(dest):
    _run_dir_converter("contoso", os.path.join(ROOT, "downloads", "contoso"),
                       os.path.join(dest, "contoso.sql"))


@stager("dvdstore_reviews")
def stage_dvdstore_reviews(dest):
    """The extended tier: loaded into an existing dvdstore, never baked into the image."""
    import subprocess
    conv = os.path.join(ROOT, "datasets", "dvdstore", "convert.py")
    out = os.path.join(dest, "dvdstore_reviews.sql")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if subprocess.run([sys.executable, conv, os.path.join(ROOT, "downloads", "dvdstore"), out,
                       "--reviews"], text=True).returncode != 0:
        sys.exit("dvdstore_reviews conversion failed")


@stager("dvdstore")
def stage_dvdstore(dest):
    _run_dir_converter("dvdstore", os.path.join(ROOT, "downloads", "dvdstore"),
                       os.path.join(dest, "dvdstore.sql"))


@stager("adventureworks_dw")
def stage_adventureworks_dw(dest):
    _run_converter("adventureworks_dw",
                   os.path.join(ROOT, "downloads", "adventureworks_dw",
                                "AdventureWorksDW-data-warehouse-install-script.zip"),
                   os.path.join(dest, "adventureworks_dw.sql"))


@stager("adventureworks")
def stage_adventureworks(dest):
    _run_converter("adventureworks",
                   os.path.join(ROOT, "downloads", "adventureworks",
                                "AdventureWorks-oltp-install-script.zip"),
                   os.path.join(dest, "adventureworks.sql"))


@stager("oracle_sh")
def stage_oracle_sh(dest):
    _run_dir_converter("oracle_sh", os.path.join(ROOT, "downloads", "oracle_sh"),
                       os.path.join(dest, "oracle_sh.sql"))


@stager("wideworldimporters")
def stage_wideworldimporters(dest):
    """Reads downloads/wideworldimporters/export/, which `make wwi-export` produced once."""
    _run_export_converter("wideworldimporters", os.path.join(dest, "wideworldimporters.sql"))


@stager("wideworldimporters_dw")
def stage_wideworldimporters_dw(dest):
    _run_export_converter("wideworldimporters_dw",
                          os.path.join(dest, "wideworldimporters_dw.sql"))


@stager("oracle_oe")
def stage_oracle_oe(dest):
    _run_dir_converter("oracle_oe", os.path.join(ROOT, "downloads", "oracle_oe"),
                       os.path.join(dest, "oracle_oe.sql"))


def _run_export_converter(name, out):
    """WideWorldImporters converts from the SQL Server export, not from a downloaded archive."""
    import subprocess
    export = os.path.join(ROOT, "downloads", name, "export")
    if not os.path.exists(os.path.join(export, "meta.json")):
        sys.exit(f"{name}: no export in {export}. It is produced once, by:\n"
                 f"    MEGASAMPLES_ACCEPT_MSSQL_EULA=1 make wwi-export\n"
                 f"which runs SQL Server under Microsoft's Developer EULA -- see "
                 f"knowledge/licenses/microsoft-sql-server-developer-eula.md")
    conv = os.path.join(ROOT, "datasets", name, "convert.py")
    if subprocess.run([sys.executable, conv, export, out], text=True).returncode != 0:
        sys.exit(f"{name} conversion failed")


def _run_dir_converter(name, src_dir, out):
    """Converters that read a directory of files rather than a single artifact."""
    import subprocess
    conv = os.path.join(ROOT, "datasets", name, "convert.py")
    if subprocess.run([sys.executable, conv, src_dir, out], text=True).returncode != 0:
        sys.exit(f"{name} conversion failed")


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
