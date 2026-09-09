#!/usr/bin/env python3
"""Generate the browsing console's landing page from the running stack.

  python3 -m megasamples console-page [--out consoles/landing/index.html]

The page is generated rather than written because a hand-written one is wrong the first time a
dataset is added, an engine is switched on or a row count moves. For every engine megasamples.yaml
names it reads the provenance registry inside that engine's running container -- the same table
the image tests assert against -- so it lists the databases that are actually there, with the
counts they actually have and, for a port, what was not carried over.

It also states the credentials: Adminer's login form remains even with a default server set
(measured, not assumed), so a visitor needs them to get in. Both accounts are shown, the read-only
one first, and the passwords are read from .env if there is one, so the page says what is actually
configured rather than what the defaults were.
"""
import argparse, html, json, os, subprocess, sys

import yaml

from megasamples import config as stack, consoles as console_registry, engines as engine_registry
from megasamples.catalogue import shorten
from megasamples.paths import CONSOLES as CONSOLES_DIR, ROOT


def passwords():
    found = {}
    env_file = os.path.join(ROOT, ".env")
    if os.path.exists(env_file):
        for line in open(env_file, encoding="utf-8"):
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            found[k.strip()] = v.strip().strip('"\'')
    return (found.get("DEMO_PASSWORD") or os.environ.get("DEMO_PASSWORD") or "demo",
            found.get("ADMIN_PASSWORD") or os.environ.get("ADMIN_PASSWORD") or "admin")


def describe(record, blurb=""):
    """The dataset's one-line description, from its knowledge record (one trimming rule, shared
    with the catalogue, so the page and the catalogue cannot describe a dataset differently)."""
    if blurb:
        return blurb
    path = os.path.join(ROOT, record or "")
    if not record or not os.path.exists(path):
        return ""
    try:
        meta = yaml.safe_load(open(path, encoding="utf-8").read().split("---", 2)[1]) or {}
    except Exception:
        return ""
    return shorten((meta.get("description") or "").strip())


# Which consoles can be pointed at one database through a URL, per engine. DbGate and CloudBeaver
# read no database parameter, so they get no per-row link rather than one that opens their front page.
DEEP_LINKS = {
    "mysql": [("phpmyadmin", "P", "http://127.0.0.1:{port}/index.php?route=/database/structure&db={db}&server=1"),
              ("adminer", "A", "http://127.0.0.1:{port}/?server=mysql&username=demo&db={db}")],
    "postgres": [("adminer", "A", "http://127.0.0.1:{port}/?pgsql=postgres&username=demo&db={db}")],
    "sqlite": [],
}


def running(container):
    p = subprocess.run(["docker", "inspect", "-f", "{{.State.Running}}", container], capture_output=True, text=True)
    return p.returncode == 0 and p.stdout.strip() == "true"


def collect(cfg):
    """{engine: {database: {tier, licenses, counts, record, tables, mb, not_ported}}} for every running engine."""
    out = {}
    for name in cfg.engines:
        engine = engine_registry.get(name)
        if not running(engine.container):
            print(f"  ! {engine.container} is not running; {engine.title} is left off the page")
            continue
        rows = engine.registry_rows(engine.container)
        sizes = engine.sizes(engine.container)
        per = {}
        for r in rows:
            db, tier, licenses, counts, record = r[:5]
            try:
                per_table = json.loads(counts) if counts and counts != "NULL" else {}
            except ValueError:
                per_table = {}
            try:
                lic = ", ".join(json.loads(licenses)) if licenses else ""
            except ValueError:
                lic = licenses or ""
            tables, mb = sizes.get(db, (len(per_table), 0.0))
            per[db] = {"tier": tier, "licenses": lic, "rows": sum(v for v in per_table.values() if isinstance(v, int)),
                       "record": record, "tables": tables, "mb": mb, "not_ported": not_ported(engine, db)}
        out[name] = per
    return out


def not_ported(engine, db):
    if engine.name == "mysql":
        return []
    try:
        rows = engine.query(engine.container, f"SELECT not_ported FROM datasets WHERE name = '{db}'")
        return json.loads(rows[0][0]) if rows and rows[0][0] not in ("", "NULL") else []
    except Exception:
        return []


def render(cfg, data):
    demo_pw, admin_pw = (html.escape(p) for p in passwords())
    engines = [engine_registry.get(n) for n in data]
    blurbs = {}
    for d in os.listdir(os.path.join(ROOT, "datasets")):
        p = os.path.join(ROOT, "datasets", d, "dataset.yaml")
        if os.path.exists(p):
            spec = yaml.safe_load(open(p, encoding="utf-8")) or {}
            if spec.get("blurb"):
                blurbs[spec.get("database", d)] = spec["blurb"]

    databases = sorted({db for per in data.values() for db in per})
    consoles = [console_registry.get(n) for n in cfg.consoles if n != "landing" and n in cfg.ports]
    console_cards = "\n".join(
        f'      <a class="console" href="http://127.0.0.1:{cfg.ports[c.name]}/"><b>{html.escape(c.title)}</b>'
        f'<span>{html.escape(c.note)}</span><em>browses {html.escape(", ".join(engine_registry.get(e).title for e in c.engines if e in data) or "—")}</em></a>'
        for c in consoles)

    head_cells = "".join(f'<th colspan="3" class="eng">{html.escape(e.title)} {html.escape(e.version)}</th>' for e in engines)
    sub_cells = "".join('<th class="n">tables</th><th class="n">rows</th><th class="n">MB</th>' for _ in engines)
    rows_html = []
    for db in databases:
        first = next((per[db] for per in data.values() if db in per), {})
        what = describe(first.get("record", ""), blurbs.get(db, ""))
        cells = []
        for e in engines:
            info = data[e.name].get(db)
            if not info:
                cells.append('<td class="n" colspan="3">—</td>')
                continue
            links = "".join(
                f'<a class="go" title="Open {html.escape(db)} in {html.escape(console_registry.get(cn).title)}" '
                f'href="{html.escape(url.format(port=cfg.ports.get(cn, 0), db=db), quote=True)}">{letter}</a>'
                for cn, letter, url in DEEP_LINKS.get(e.name, []) if cn in cfg.consoles)
            np = info["not_ported"]
            note = (f' <span class="np" title="{html.escape(chr(10).join(np))}">{len(np)} not ported</span>' if np else "")
            cells.append(f'<td class="n">{info["tables"]:,}{links}</td><td class="n">{info["rows"]:,}</td>'
                         f'<td class="n">{info["mb"]:,.1f}{note}</td>')
        rows_html.append(f'      <tr><td><code>{html.escape(db)}</code><div class="what">{html.escape(what)}</div></td>'
                         f'<td>{html.escape(first.get("tier", ""))}</td>{"".join(cells)}<td>{html.escape(first.get("licenses", ""))}</td></tr>')

    connect = "\n".join(
        f'  <div><b>{html.escape(e.title)}</b> on <code>127.0.0.1:{cfg.ports.get(e.name, e.port)}</code>'
        + (f' — <code>{html.escape(e.connection_hint(cfg))}</code>' if e.port else f' — <code>{html.escape(e.connection_hint(cfg))}</code>')
        + "</div>" for e in engines)
    totals = " · ".join(f"{html.escape(e.title)}: {len(data[e.name])} databases, "
                        f"{sum(i['rows'] for i in data[e.name].values()):,} rows" for e in engines)
    page = f"""<!doctype html>
<meta charset="utf-8"><title>sql-megasamples</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
 :root {{ color-scheme: light dark; --line:#8883; }}
 body {{ font:15px/1.5 system-ui,sans-serif; margin:0 auto; padding:2rem 1.25rem; max-width:72rem; }}
 h1 {{ font-size:1.5rem; margin:0 0 .25rem; }}
 p.sub {{ margin:0 0 1.5rem; opacity:.7; }}
 .consoles {{ display:grid; gap:.75rem; grid-template-columns:repeat(auto-fit,minmax(15rem,1fr)); margin-bottom:1.5rem; }}
 a.console {{ display:block; padding:.85rem 1rem; border:1px solid var(--line); border-radius:.5rem; text-decoration:none; color:inherit; }}
 a.console:hover {{ border-color:#69f; }}
 a.console span, a.console em {{ display:block; font-size:.85em; opacity:.7; margin-top:.2rem; font-style:normal; }}
 table {{ border-collapse:collapse; width:100%; font-size:.9em; }}
 th,td {{ text-align:left; padding:.35rem .6rem; border-bottom:1px solid var(--line); vertical-align:top; }}
 th.eng {{ text-align:center; border-left:1px solid var(--line); }}
 td.n, th.n {{ text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }}
 code {{ font-size:.95em; }}
 .what {{ font-size:.88em; opacity:.72; margin-top:.15rem; max-width:34rem; }}
 a.go {{ display:inline-block; width:1.25rem; height:1.25rem; line-height:1.25rem; text-align:center; border:1px solid var(--line);
         border-radius:.25rem; font-size:.72em; font-weight:600; text-decoration:none; color:inherit; opacity:.65; margin-left:.25rem; }}
 a.go:hover {{ opacity:1; border-color:#69f; }}
 .np {{ font-size:.75em; opacity:.6; cursor:help; }}
 .creds {{ border:1px solid var(--line); border-radius:.5rem; padding:.75rem 1rem; margin:1.5rem 0; font-size:.9em; }}
 footer {{ margin-top:2rem; font-size:.85em; opacity:.7; }}
</style>
<h1>sql-megasamples</h1>
<p class="sub">{totals}</p>

<div class="consoles">
{console_cards}
</div>

<div class="creds">
  <b>Two accounts</b>, offered by every console and usable from any client:
  <code>demo</code> / <code>{demo_pw}</code> — <b>read only</b>, no write privilege anywhere; each console opens on this one.
  <code>admin</code> / <code>{admin_pw}</code> — <b>full privileges</b>, so anything you change here stays changed.
  SQLite files have no accounts. Both passwords are boilerplate for a disposable test database; change them by copying
  <code>.env.example</code> to <code>.env</code>, and the same value reaches every engine and every console.
{connect}
</div>

<table>
  <thead><tr><th rowspan="2">database — <b>P</b> opens it in phpMyAdmin, <b>A</b> in Adminer</th><th rowspan="2">tier</th>{head_cells}<th rowspan="2">licence</th></tr>
  <tr>{sub_cells}</tr></thead>
  <tbody>
{chr(10).join(rows_html)}
  </tbody>
</table>

<footer>
  Generated from the provenance registry inside each running engine, so it cannot drift from what is actually loaded.
  PostgreSQL and SQLite are ports of the verified MySQL corpus: the same rows, checked by the same content digests;
  "not ported" counts the views, routines, triggers, indexes and columns that engine cannot carry, lists them with the
  reason when you hover, and <code>knowledge/decisions/programmable-object-parity.md</code> in the repository explains
  each kind. Each dataset keeps its own upstream licence — see <code>datasets/&lt;name&gt;/PROVENANCE.md</code>
  in the repository — and each description comes from its research record rather than being written here.
</footer>
"""
    return page, len(databases)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=os.path.join(CONSOLES_DIR, "landing", "index.html"))
    a = ap.parse_args(argv)
    cfg = stack.load()
    data = collect(cfg)
    if not data:
        print("  x no engine of the stack is running; nothing to write")
        return 1
    page, n = render(cfg, data)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(page)
    print(f"  . wrote {os.path.relpath(a.out, ROOT)}: {n} databases across {', '.join(data)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
