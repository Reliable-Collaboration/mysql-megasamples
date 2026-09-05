#!/usr/bin/env python3
"""S10: the browsing console starts and shows what is actually loaded.

  python3 tests/console_test.py

Deliberately shallow, as PLAN.md section 4 says: it catches a withdrawn image tag, a console that no
longer starts, and a landing page that has drifted from the registry. It does not try to drive three
web applications.
"""
import http.cookiejar, json, subprocess, sys, urllib.error, urllib.request

ENDPOINTS = [("landing page", "http://127.0.0.1:8080/"),
             ("phpMyAdmin", "http://127.0.0.1:8081/"),
             ("Adminer", "http://127.0.0.1:8082/"),
             ("DbGate", "http://127.0.0.1:8083/"),
             ("CloudBeaver", "http://127.0.0.1:8084/")]
CONTAINER = "megasamples-mysql"


def passwords():
    """Whatever compose is actually using: .env if there is one, else the environment, else the
    image's baked defaults. Mirrors scripts/console_page.py."""
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    found = {}
    env_file = os.path.join(root, ".env")
    if os.path.exists(env_file):
        for line in open(env_file, encoding="utf-8"):
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            found[k.strip()] = v.strip().strip('"\'')
    return (found.get("DEMO_PASSWORD") or os.environ.get("DEMO_PASSWORD") or "demo",
            found.get("ADMIN_PASSWORD") or os.environ.get("ADMIN_PASSWORD") or "admin")


PASSWORDS = passwords()


def cloudbeaver_ready(timeout=20):
    """CloudBeaver answers on 8084 even while it is showing its setup wizard, so HTTP 200 proves
    nothing. Ask it whether it is still in configuration mode and whether an anonymous visitor can
    actually see the connection -- the two things that silently regress."""
    gql = "http://127.0.0.1:8084/api/gql"
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def call(query):
        req = urllib.request.Request(gql, data=json.dumps({"query": query}).encode(),
                                     headers={"Content-Type": "application/json"})
        with opener.open(req, timeout=timeout) as r:
            return json.load(r).get("data") or {}

    def connect(conn_id):
        q = ('mutation{initConnection(projectId:"g_GlobalConfiguration",id:"%s"){connected}}' % conn_id)
        return (call(q).get("initConnection") or {}).get("connected")

    call("mutation{openSession{valid}}")
    d = call("{serverConfig{configurationMode} userConnections{id}}")
    problems = []
    if d.get("serverConfig", {}).get("configurationMode"):
        problems.append("CloudBeaver is in configuration mode: it is showing its setup wizard")

    ids = {c["id"] for c in d.get("userConnections") or []}
    for wanted in ("megasamples-demo", "megasamples-admin"):
        if wanted not in ids:
            problems.append(f"CloudBeaver does not offer the {wanted} connection anonymously")
        elif not connect(wanted):
            # a connection that lists but will not open is the caching_sha2 public-key trap:
            # the JDBC driver needs allowPublicKeyRetrieval on a cold server credential cache
            problems.append(f"CloudBeaver lists {wanted} but cannot connect with it")
    return problems


def get(url, timeout=20):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def main():
    failures, page = [], ""
    for name, url in ENDPOINTS:
        try:
            status, body = get(url)
            if status != 200:
                failures.append(f"{name}: HTTP {status}")
            else:
                print(f"  . {name:<14} HTTP 200 ({len(body):,} bytes)")
            if name == "landing page":
                page = body
        except (urllib.error.URLError, OSError) as exc:
            failures.append(f"{name}: {exc}")
            print(f"  x {name:<14} {exc}")

    p = subprocess.run(["docker", "exec", CONTAINER, "mysql", "-udemo", f"-p{PASSWORDS[0]}",
                        "-N", "--batch",
                        "-e", "SELECT name FROM megasamples.datasets ORDER BY name"],
                       capture_output=True, text=True)
    if p.returncode != 0:
        failures.append(f"could not read the registry: {p.stderr.strip()[:150]}")
    else:
        names = [n for n in p.stdout.split() if n]
        missing = [n for n in names if f">{n}<" not in page]
        if missing:
            failures.append(f"the landing page omits {len(missing)} database(s): "
                            + ", ".join(missing[:6]))
        else:
            print(f"  . the landing page names all {len(names)} databases in the registry")

    try:
        problems = cloudbeaver_ready()
        failures += problems
        if not problems:
            print("  . CloudBeaver is configured and shows the connection anonymously")
    except (urllib.error.URLError, OSError, ValueError, KeyError) as exc:
        failures.append(f"CloudBeaver: could not check its state: {exc}")

    # both accounts must be real, and must differ: read-only is a claim the page makes, so test it
    def mysql(user, password, sql):
        return subprocess.run(["docker", "exec", CONTAINER, "mysql", f"-u{user}", f"-p{password}",
                               "-N", "--batch", "-e", sql], capture_output=True, text=True)

    demo_pw, admin_pw = PASSWORDS
    if mysql("demo", demo_pw, "SELECT 1").returncode != 0:
        failures.append("the demo account cannot log in with the configured password")
    elif mysql("demo", demo_pw, "CREATE TABLE sakila.t_console_probe (i INT)").returncode == 0:
        mysql("admin", admin_pw, "DROP TABLE IF EXISTS sakila.t_console_probe")
        failures.append("the demo account can write: it is meant to be read-only")
    else:
        print("  . demo can read and cannot write")

    w = mysql("admin", admin_pw, "CREATE TABLE sakila.t_console_probe (i INT); "
                                 "DROP TABLE sakila.t_console_probe")
    if w.returncode != 0:
        failures.append(f"the admin account cannot write: {w.stderr.strip()[:120]}")
    else:
        print("  . admin can write")

    # the credentials have to be on the page: Adminer's login form is not preset
    for account in ("demo", "admin"):
        if account not in page:
            failures.append(f"the landing page does not state the {account} account, "
                            "and Adminer's login form needs it")

    for f in failures:
        print(f"  x {f}")
    print(f"console: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
