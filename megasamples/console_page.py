#!/usr/bin/env python3
"""Generate the browsing console's landing page from the registry inside the running image.

  python3 -m megasamples console-page [--host 127.0.0.1] [--port 3306] [--out consoles/landing/index.html]

The page is generated rather than written because a hand-written one is wrong the first time a
dataset is added or a row count moves. It reads `megasamples.datasets` -- the same table
`tests/image_test.py` asserts against -- so it lists the databases that are actually present, with
the counts they actually have.

It also states the credentials, which is not laziness: Adminer's login form remains even with
`ADMINER_DEFAULT_SERVER` set (measured, not assumed), so a visitor needs them to get in. Both
accounts are shown -- the read-only `demo` one and the full-privilege `admin` one -- because every
console offers both and a visitor has to know which is which. The passwords are read from `.env` if
there is one, so the page says what is actually configured rather than what the defaults were.
"""
import argparse, html, json, os, subprocess, sys

import yaml

from megasamples.catalogue import shorten  # noqa: E402

from megasamples.paths import CONSOLES as CONSOLES_DIR, ROOT
CONSOLES = [
    ("phpMyAdmin", 8081, "Signed in already; the server menu switches account."),
    ("Adminer", 8082, "Its login form remains; use either account below."),
    ("DbGate", 8083, "Both connections are preconfigured; pick one in the sidebar."),
    ("CloudBeaver", 8084, "Open as a guest; both connections are in the sidebar."),
]


def passwords():
    """What the consoles are actually configured with: .env if present, else the environment, else
    the image's baked defaults. A page that states a stale password is worse than one that omits it."""
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
    """The dataset's one-line description, from its knowledge record.

    Written there once, by the research that produced the dataset, and reused here rather than
    rewritten: a hand-typed blurb on a landing page is the first thing to go stale, and inventing
    one would be the first thing to be wrong."""
    if blurb:
        return blurb
    if not record:
        return ""
    path = os.path.join(ROOT, record)
    if not os.path.exists(path):
        return ""
    try:
        text = open(path, encoding="utf-8").read()
        meta = yaml.safe_load(text.split("---", 2)[1]) or {}
    except Exception:
        return ""
    # one trimming rule, shared with megasamples/catalogue.py, so the page and the catalogue cannot
    # describe the same dataset differently
    return shorten((meta.get("description") or "").strip())


# Which consoles can actually be pointed at one database, measured rather than assumed. phpMyAdmin
# takes a route and a db; Adminer takes the db and lands on it once you are past its login form.
# DbGate and CloudBeaver have no such URL -- their front ends read no database parameter at all
# (DbGate's bundle reads only auth params; CloudBeaver's routing carries none) -- so no icon is
# offered for them rather than one that quietly opens the app at its front page.
DEEP_LINKS = (
    ("phpMyAdmin", "P", "http://127.0.0.1:8081/index.php?route=/database/structure&db={db}&server=1"),
    ("Adminer", "A", "http://127.0.0.1:8082/?server=mysql&username=demo&db={db}"),
)


def open_in(db):
    links = "".join(
        f'<a class="go" title="Open {db} in {name}" href="{html.escape(url.format(db=db), quote=True)}">{letter}</a>'
        for name, letter, url in DEEP_LINKS)
    return f'<span class="opens">{links}</span>'


def query(container, sql):
    p = subprocess.run(["docker", "exec", container, "mysql", "-udemo", f"-p{passwords()[0]}",
                        "-N", "--batch", "-e", sql], capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"could not read the registry from {container}: {p.stderr.strip()[:200]}")
    return [line.split("\t") for line in p.stdout.splitlines() if line.strip()]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--container", default="megasamples-mysql")
    ap.add_argument("--out", default=os.path.join(CONSOLES_DIR, "landing", "index.html"))
    a = ap.parse_args(argv)

    rows = query(a.container, "SELECT name, tier, licenses, row_counts, record "
                              "FROM megasamples.datasets ORDER BY name")
    sizes = {r[0]: (int(r[1]), float(r[2])) for r in query(
        a.container,
        "SELECT table_schema, COUNT(*), ROUND(SUM(data_length+index_length)/1048576,1) "
        "FROM information_schema.tables WHERE table_type='BASE TABLE' "
        "AND table_schema NOT IN ('mysql','information_schema','performance_schema','sys') "
        "GROUP BY table_schema")}

    blurbs = {}
    for d in os.listdir(os.path.join(ROOT, "datasets")):
        spec_path = os.path.join(ROOT, "datasets", d, "dataset.yaml")
        if os.path.exists(spec_path):
            spec = yaml.safe_load(open(spec_path, encoding="utf-8")) or {}
            if spec.get("blurb"):
                blurbs[d] = spec["blurb"]

    items, total_rows, total_tables = [], 0, 0
    for name, tier, licenses, counts, record in rows:
        try:
            per_table = json.loads(counts) if counts and counts != "NULL" else {}
        except ValueError:
            per_table = {}
        n = sum(v for v in per_table.values() if isinstance(v, int))
        tables, mb = sizes.get(name, (len(per_table), 0.0))
        total_rows += n
        total_tables += tables
        try:
            lic = ", ".join(json.loads(licenses)) if licenses else ""
        except ValueError:
            lic = licenses or ""
        items.append((name, tier, tables, n, mb, lic, describe(record, blurbs.get(name, ""))))

    cards = "\n".join(
        f'      <tr><td><code>{html.escape(n)}</code>{open_in(n)}'
        f'<div class="what">{html.escape(what)}</div></td><td>{t}</td>'
        f'<td class="n">{tab:,}</td><td class="n">{rc:,}</td><td class="n">{mb:,.1f}</td>'
        f'<td>{html.escape(lic)}</td></tr>'
        for n, t, tab, rc, mb, lic, what in items)
    demo_pw, admin_pw = passwords()
    demo_pw, admin_pw = html.escape(demo_pw), html.escape(admin_pw)
    links = "\n".join(
        f'      <a class="console" href="http://127.0.0.1:{port}/"><b>{name}</b>'
        f'<span>{html.escape(note)}</span></a>' for name, port, note in CONSOLES)

    page = f"""<!doctype html>
<meta charset="utf-8"><title>sql-megasamples</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
 :root {{ color-scheme: light dark; --line:#8883; }}
 body {{ font:15px/1.5 system-ui,sans-serif; margin:0 auto; padding:2rem 1.25rem; max-width:60rem; }}
 h1 {{ font-size:1.5rem; margin:0 0 .25rem; }}
 p.sub {{ margin:0 0 1.5rem; opacity:.7; }}
 .consoles {{ display:grid; gap:.75rem; grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));
              margin-bottom:1.5rem; }}
 a.console {{ display:block; padding:.85rem 1rem; border:1px solid var(--line); border-radius:.5rem;
              text-decoration:none; color:inherit; }}
 a.console:hover {{ border-color:#69f; }}
 a.console span {{ display:block; font-size:.85em; opacity:.7; margin-top:.2rem; }}
 table {{ border-collapse:collapse; width:100%; font-size:.9em; }}
 th,td {{ text-align:left; padding:.35rem .6rem; border-bottom:1px solid var(--line); }}
 td.n, th.n {{ text-align:right; font-variant-numeric:tabular-nums; }}
 code {{ font-size:.95em; }}
 .what {{ font-size:.88em; opacity:.72; margin-top:.15rem; max-width:46rem; }}
 .opens {{ margin-left:.45rem; white-space:nowrap; }}
 a.go {{ display:inline-block; width:1.25rem; height:1.25rem; line-height:1.25rem; text-align:center;
         border:1px solid var(--line); border-radius:.25rem; font-size:.72em; font-weight:600;
         text-decoration:none; color:inherit; opacity:.65; margin-left:.15rem; }}
 a.go:hover {{ opacity:1; border-color:#69f; }}
 .creds {{ border:1px solid var(--line); border-radius:.5rem; padding:.75rem 1rem; margin:1.5rem 0;
           font-size:.9em; }}
 footer {{ margin-top:2rem; font-size:.85em; opacity:.7; }}
</style>
<h1>sql-megasamples</h1>
<p class="sub">{len(items)} databases · {total_tables:,} tables · {total_rows:,} rows · MySQL 9.7.2</p>

<div class="consoles">
{links}
</div>

<div class="creds">
  <b>Two accounts</b>, both reachable from every console on host <code>127.0.0.1</code>, port
  <code>3306</code>.
  <br>
  <code>demo</code> / <code>{demo_pw}</code> — <b>read only</b>: <code>SELECT</code> and
  <code>SHOW VIEW</code> everywhere, no write privilege anywhere. Each console opens on this one.
  <br>
  <code>admin</code> / <code>{admin_pw}</code> — <b>full privileges</b>, so anything you change here
  stays changed. In phpMyAdmin and DbGate and CloudBeaver it is the second entry; in Adminer, type it
  into the login form.
  <br>
  Both passwords are boilerplate for a disposable test database. Change them by copying
  <code>.env.example</code> to <code>.env</code>: the same value reaches the server and every
  console.
</div>

<table>
  <thead><tr><th>database — <b>P</b> opens it in phpMyAdmin, <b>A</b> in Adminer</th>
  <th>tier</th><th class="n">tables</th><th class="n">rows</th>
  <th class="n">MB</th><th>licence</th></tr></thead>
  <tbody>
{cards}
  </tbody>
</table>

<footer>
  Generated from <code>megasamples.datasets</code> inside the running image, so it cannot drift from
  what is actually loaded. Each dataset keeps its own upstream licence — see
  <code>datasets/&lt;name&gt;/PROVENANCE.md</code> in the repository, and each database's description
  comes from its own research record rather than being written here. Every console starts configured;
  none asks you to set anything up first. The <b>P</b> and <b>A</b> links open a single database
  directly — only phpMyAdmin and Adminer accept one in a URL, so DbGate and CloudBeaver have no
  per-row link rather than one that would just open their front page.
</footer>
"""
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(page)
    print(f"  . wrote {os.path.relpath(a.out, ROOT)}: {len(items)} databases, "
          f"{total_tables:,} tables, {total_rows:,} rows")


if __name__ == "__main__":
    sys.exit(main())
