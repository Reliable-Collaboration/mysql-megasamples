"""Generate the console configuration files that depend on which engines are in the stack.

  python3 -m megasamples console-config

CloudBeaver reads its connections from conf/initial-data-sources.conf at first start, so the file
is written from megasamples.yaml: one read-only and one full-access connection per server engine,
and one connection per SQLite file. The generated file lives under consoles/cloudbeaver/generated/
(git-ignored) and compose.yaml mounts it. phpMyAdmin's configuration is static (MySQL only) and
DbGate and Adminer are configured through environment variables by compose.py.
"""
import argparse, json, os, sys

from megasamples import config as stack, datasets as inventory
from megasamples.paths import CONSOLES, rel

GENERATED = os.path.join(CONSOLES, "cloudbeaver", "generated")


def cloudbeaver_connections(cfg):
    conns = {}
    first = {e: (inventory.load(cfg.datasets(e)[0])["database"] if cfg.datasets(e) else "megasamples") for e in cfg.engines}
    if "mysql" in cfg.engines:
        for account, label, desc in (("demo", "read-only", "SELECT and SHOW VIEW only, no write privilege anywhere."),
                                     ("admin", "full access", "ALL PRIVILEGES. Anything you change here, stays changed.")):
            conns[f"mysql-{account}"] = {
                "provider": "mysql", "driver": "mysql8", "name": f"MySQL ({label})",
                "description": f"Connected as {account}: {desc}", "save-password": True,
                "configuration": {"host": "mysql", "port": "3306", "database": first["mysql"],
                                  "url": f"jdbc:mysql://mysql:3306/{first['mysql']}", "type": "dev",
                                  "auth-model": "native",
                                  "properties": {"allowPublicKeyRetrieval": "true", "useSSL": "false"},
                                  "user": account, "password": "${%s_PASSWORD:%s}" % (account.upper(), account)}}
    if "postgres" in cfg.engines:
        for account, label, desc in (("demo", "read-only", "SELECT only, on every database."),
                                     ("admin", "full access", "Can create, alter and drop. Anything you change here, stays changed.")):
            conns[f"postgres-{account}"] = {
                "provider": "postgresql", "driver": "postgres-jdbc", "name": f"PostgreSQL ({label})",
                "description": f"Connected as {account}: {desc}", "save-password": True,
                "configuration": {"host": "postgres", "port": "5432", "database": first["postgres"],
                                  "url": f"jdbc:postgresql://postgres:5432/{first['postgres']}", "type": "dev",
                                  "auth-model": "native",
                                  "provider-properties": {"@dbeaver-show-non-default-db@": "true",
                                                          "@dbeaver-show-template-db@": "false"},
                                  "user": account, "password": "${%s_PASSWORD:%s}" % (account.upper(), account)}}
    if "sqlite" in cfg.engines:
        for d in cfg.datasets("sqlite"):
            db = inventory.load(d)["database"]
            conns[f"sqlite-{db}"] = {
                "provider": "sqlite", "driver": "sqlite_jdbc", "name": f"SQLite {db}",
                "description": f"The {db} database as a SQLite file (/data/{db}.sqlite).", "save-password": True,
                "configuration": {"database": f"/data/{db}.sqlite", "url": f"jdbc:sqlite:/data/{db}.sqlite",
                                  "type": "dev", "auth-model": "native"}}
    return {"folders": {}, "connections": conns}


DRIVERS = {"mysql": "mysql:mysql8", "postgres": "postgresql:postgres-jdbc", "sqlite": "sqlite:sqlite_jdbc"}


def cloudbeaver_server_conf(cfg):
    """The image's own cloudbeaver.conf with the drivers the stack needs enabled.

    CloudBeaver disables file-based drivers such as SQLite by default, and its shipped
    configuration names no drivers at all, so the file is taken from the pinned image (`docker run
    ... cat`) and the `enabledDrivers` list inserted into its `app` block; every other setting,
    including the environment references, stays as the image wrote it."""
    import subprocess
    from megasamples import consoles as console_registry
    image = console_registry.get("cloudbeaver").image
    p = subprocess.run(["docker", "run", "--rm", "--label", "megasamples.transient=true", "--entrypoint", "cat",
                        image, "/opt/cloudbeaver/conf/cloudbeaver.conf"], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"could not read cloudbeaver.conf from {image}: {p.stderr.strip()[:200]}")
    text = p.stdout
    drivers = ", ".join(f'"{DRIVERS[e]}"' for e in cfg.engines if e in DRIVERS)
    marker = "    app: {\n"
    if marker not in text:
        raise SystemExit("cloudbeaver.conf from the image has no `app: {` block; the generator needs updating")
    return text.replace(marker, marker + f"        enabledDrivers: [ {drivers} ],\n", 1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.parse_args(argv)
    cfg = stack.load()
    os.makedirs(GENERATED, exist_ok=True)
    path = os.path.join(GENERATED, "initial-data-sources.conf")
    doc = cloudbeaver_connections(cfg)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    print(f"  . {rel(path)}: {len(doc['connections'])} CloudBeaver connection(s) for {', '.join(cfg.engines)}")
    if "cloudbeaver" in cfg.consoles:
        conf = os.path.join(GENERATED, "cloudbeaver.conf")
        with open(conf, "w", encoding="utf-8") as fh:
            fh.write(cloudbeaver_server_conf(cfg))
        print(f"  . {rel(conf)}: the image's server configuration with drivers enabled for {', '.join(e for e in cfg.engines if e in DRIVERS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
