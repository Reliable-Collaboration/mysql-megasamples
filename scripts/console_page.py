#!/usr/bin/env python3
"""Generate the browsing console's landing page from the registry inside the running image.

  python3 scripts/console_page.py [--host 127.0.0.1] [--port 3306] [--out docker/console/index.html]

The page is generated rather than written because a hand-written one is wrong the first time a
dataset is added or a row count moves. It reads `megasamples.datasets` -- the same table
`tests/image_test.py` asserts against -- so it lists the databases that are actually present, with
the counts they actually have.

It also states the credentials, which is not laziness: Adminer's login form remains even with
`ADMINER_DEFAULT_SERVER` set (measured, not assumed), so a visitor needs them to get in. They are the
read-only `demo` account, and saying so is better than leaving someone guessing.
"""
import argparse, html, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONSOLES = [
    ("phpMyAdmin", 8081, "Signed in already — it opens straight into the data."),
    ("Adminer", 8082, "Its login form remains; use the credentials below."),
    ("DbGate", 8083, "The connection is preconfigured; pick it in the sidebar."),
]


def query(container, sql):
    p = subprocess.run(["docker", "exec", container, "mysql", "-udemo", "-pdemo", "-N", "--batch",
                        "-e", sql], capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"could not read the registry from {container}: {p.stderr.strip()[:200]}")
    return [line.split("\t") for line in p.stdout.splitlines() if line.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--container", default="mms-console-db")
    ap.add_argument("--out", default=os.path.join(ROOT, "docker", "console", "index.html"))
    a = ap.parse_args()

    rows = query(a.container, "SELECT name, tier, licenses, row_counts FROM megasamples.datasets "
                              "ORDER BY name")
    sizes = {r[0]: (int(r[1]), float(r[2])) for r in query(
        a.container,
        "SELECT table_schema, COUNT(*), ROUND(SUM(data_length+index_length)/1048576,1) "
        "FROM information_schema.tables WHERE table_type='BASE TABLE' "
        "AND table_schema NOT IN ('mysql','information_schema','performance_schema','sys') "
        "GROUP BY table_schema")}

    items, total_rows, total_tables = [], 0, 0
    for name, tier, licenses, counts in rows:
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
        items.append((name, tier, tables, n, mb, lic))

    cards = "\n".join(
        f'      <tr><td><code>{html.escape(n)}</code></td><td>{t}</td>'
        f'<td class="n">{tab:,}</td><td class="n">{rc:,}</td><td class="n">{mb:,.1f}</td>'
        f'<td>{html.escape(lic)}</td></tr>'
        for n, t, tab, rc, mb, lic in items)
    links = "\n".join(
        f'      <a class="console" href="http://127.0.0.1:{port}/"><b>{name}</b>'
        f'<span>{html.escape(note)}</span></a>' for name, port, note in CONSOLES)

    page = f"""<!doctype html>
<meta charset="utf-8"><title>mysql-megasamples</title>
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
 .creds {{ border:1px solid var(--line); border-radius:.5rem; padding:.75rem 1rem; margin:1.5rem 0;
           font-size:.9em; }}
 footer {{ margin-top:2rem; font-size:.85em; opacity:.7; }}
</style>
<h1>mysql-megasamples</h1>
<p class="sub">{len(items)} databases · {total_tables:,} tables · {total_rows:,} rows · MySQL 9.7.2</p>

<div class="consoles">
{links}
</div>

<div class="creds">
  <b>Credentials</b> — host <code>127.0.0.1</code>, port <code>3306</code>,
  user <code>demo</code>, password <code>demo</code>. This account is <b>read only</b>: it can
  select and it cannot change anything, which is deliberate. An <code>admin</code> account exists for
  writing; <code>compose.yaml</code> has a commented block that switches the consoles over to it.
</div>

<table>
  <thead><tr><th>database</th><th>tier</th><th class="n">tables</th><th class="n">rows</th>
  <th class="n">MB</th><th>licence</th></tr></thead>
  <tbody>
{cards}
  </tbody>
</table>

<footer>
  Generated from <code>megasamples.datasets</code> inside the running image, so it cannot drift from
  what is actually loaded. Each dataset keeps its own upstream licence — see
  <code>datasets/&lt;name&gt;/PROVENANCE.md</code> in the repository. CloudBeaver is deliberately
  absent: version 25.2.0 cannot be brought up without its first-launch wizard, and the console ships
  nothing that needs a manual step.
</footer>
"""
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(page)
    print(f"  . wrote {os.path.relpath(a.out, ROOT)}: {len(items)} databases, "
          f"{total_tables:,} tables, {total_rows:,} rows")


if __name__ == "__main__":
    main()
