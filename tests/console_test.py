#!/usr/bin/env python3
"""S10: the browsing console starts and shows what is actually loaded.

  python3 tests/console_test.py

Deliberately shallow, as PLAN.md section 4 says: it catches a withdrawn image tag, a console that no
longer starts, and a landing page that has drifted from the registry. It does not try to drive three
web applications.
"""
import json, subprocess, sys, urllib.error, urllib.request

ENDPOINTS = [("landing page", "http://127.0.0.1:8080/"),
             ("phpMyAdmin", "http://127.0.0.1:8081/"),
             ("Adminer", "http://127.0.0.1:8082/"),
             ("DbGate", "http://127.0.0.1:8083/")]
CONTAINER = "megasamples-mysql"


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

    p = subprocess.run(["docker", "exec", CONTAINER, "mysql", "-udemo", "-pdemo", "-N", "--batch",
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

    # the credentials have to be on the page: Adminer's login form is not preset
    if "demo" not in page:
        failures.append("the landing page does not state the credentials, and Adminer needs them")

    for f in failures:
        print(f"  x {f}")
    print(f"console: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
