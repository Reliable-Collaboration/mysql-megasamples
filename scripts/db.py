#!/usr/bin/env python3
"""Lifecycle helpers for the throwaway `mysql-build` server used by every dataset build.

The build server is a plain container running the pinned image with the project's my.cnf plus the
loading options the plan requires (local_infile on, binary logging off). Datasets are loaded into it,
tested there, and dumped from it; the container is disposable.
"""
import json, os, shlex, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE = os.environ.get("MYSQL_IMAGE", "mysql:9.7.2")
NAME = os.environ.get("BUILD_SERVER", "mms-build")
PW = "build"


def run(cmd, **kw):
    kw.setdefault("capture_output", True)
    kw.setdefault("text", True)
    return subprocess.run(cmd if isinstance(cmd, list) else shlex.split(cmd), **kw)


def container_state():
    p = run(["docker", "inspect", "-f", "{{.State.Status}}", NAME])
    return p.stdout.strip() if p.returncode == 0 else None


def ready(timeout=180):
    """Wait until a real statement succeeds. `mysqladmin ping` answers on access-denied (P-02)."""
    for _ in range(int(timeout * 5)):
        if run(["docker", "exec", NAME, "mysql", f"-p{PW}", "-uroot", "-N", "-e", "SELECT 1"]).returncode == 0:
            return True
        time.sleep(0.2)
    return False


def start(fresh=False):
    if fresh and container_state():
        stop()
    if container_state() == "running":
        return
    if container_state():
        run(["docker", "rm", "-f", NAME])
    p = run(["docker", "run", "-d", "--name", NAME,
             "-e", f"MYSQL_ROOT_PASSWORD={PW}",
             "-v", f"{os.path.join(ROOT, 'docker', 'my.cnf')}:/etc/mysql/conf.d/megasamples.cnf:ro",
             "-v", f"{os.path.join(ROOT, 'datasets')}:/datasets:ro",
             # read-only: staged inputs are produced on the host. The context must NOT be the
             # secure_file_priv directory -- the entrypoint chowns that one to uid 999 at every
             # start, which takes it away from the host user (found at S-02).
             "-v", f"{os.path.join(ROOT, 'docker', 'context')}:/context:ro",
             IMAGE, "mysqld",
             "--local-infile=1", "--skip-log-bin"])
    if p.returncode != 0:
        sys.exit(f"could not start the build server: {p.stderr.strip()}")
    if not ready():
        logs = run(["docker", "logs", "--tail", "30", NAME])
        sys.exit(f"build server never became ready:\n{logs.stdout}{logs.stderr}")


def stop():
    run(["docker", "rm", "-f", NAME])


def sql(statement, database=None, table=False, check=True):
    cmd = ["docker", "exec", "-i", NAME, "mysql", f"-p{PW}", "-uroot",
           "--default-character-set=utf8mb4"]
    if not table:
        cmd += ["-N", "--batch", "--raw"]
    else:
        cmd += ["--table"]
    if database:
        cmd += ["-D", database]
    p = run(cmd, input=statement)
    if check and p.returncode != 0:
        raise RuntimeError(f"SQL failed: {p.stderr.strip()}\n--- statement ---\n{statement[:400]}")
    return p.stdout


def sql_file(path, database=None):
    """Stream a .sql file into the server (files can be large; never read them into argv)."""
    cmd = ["docker", "exec", "-i", NAME, "mysql", f"-p{PW}", "-uroot", "--default-character-set=utf8mb4"]
    if database:
        cmd += ["-D", database]
    with open(path, "rb") as fh:
        p = subprocess.run(cmd, stdin=fh, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"loading {path} failed: {p.stderr.strip()[:500]}")
    return p.stderr


def rows(statement, database=None):
    out = sql(statement, database=database)
    return [line.split("\t") for line in out.splitlines() if line]


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "start"
    if action == "start":
        start(); print(f"{NAME} ready ({IMAGE})")
    elif action == "fresh":
        start(fresh=True); print(f"{NAME} ready, fresh ({IMAGE})")
    elif action == "stop":
        stop(); print(f"{NAME} removed")
    elif action == "status":
        print(container_state() or "absent")
    else:
        sys.exit(f"unknown action {action}")
