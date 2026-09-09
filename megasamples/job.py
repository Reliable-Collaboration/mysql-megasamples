"""The commands that read megasamples.yaml and drive the engines.

  python3 -m megasamples build [--engine E] [--fresh] [--no-fetch] [dataset ...]
  python3 -m megasamples image [--engine E] [--keep] [--from-dumps] [dataset ...]
  python3 -m megasamples test-image [--engine E] [dataset ...]
  python3 -m megasamples run [--up]              fetch, build, image for every configured engine
  python3 -m megasamples up | down               the stack, from compose.yaml (regenerated first)
  python3 -m megasamples check                   the local gate

Datasets default to what megasamples.yaml names for the engine; naming some on the command line
narrows the job to those. MySQL is the hub, so building a dataset for any engine first builds it
there (ARCHITECTURE.md section 3).
"""
import argparse, os, subprocess, sys

from megasamples import compose, config as stack, console_page, fetch as fetcher, engines as engine_registry
from megasamples.paths import COMPOSE, ROOT


def _engines(cfg, chosen):
    names = [chosen] if chosen else list(cfg.engines)
    for n in names:
        if n not in cfg.engines and chosen:
            print(f"  ! {n} is not in {cfg.source}; building it anyway")
    return [engine_registry.get(n) for n in names]


def _datasets(cfg, engine, named):
    return list(named) if named else cfg.datasets(engine.name)


def build(argv=None):
    ap = argparse.ArgumentParser(description="fetch, stage, load and verify datasets on an engine")
    ap.add_argument("datasets", nargs="*")
    ap.add_argument("--engine")
    ap.add_argument("--fresh", action="store_true", help="recreate the build server first")
    ap.add_argument("--no-fetch", action="store_true", help="assume the downloads are present")
    a = ap.parse_args(argv)
    cfg = stack.load()
    failures = 0
    for engine in _engines(cfg, a.engine):
        datasets = _datasets(cfg, engine, a.datasets)
        if not datasets:
            print(f"  . {engine.name}: no datasets configured")
            continue
        if not a.no_fetch:
            print(f"== fetch: {' '.join(datasets)}")
            if fetcher.main(datasets):
                return 1
        for i, d in enumerate(datasets):
            print(f"== {engine.name} {d} ({i + 1}/{len(datasets)})")
            failures += engine.build(d, fresh=a.fresh and i == 0) or 0
    print(f"build: {failures} failure(s)")
    return 1 if failures else 0


def image(argv=None):
    ap = argparse.ArgumentParser(description="bake the configured datasets into an engine's image")
    ap.add_argument("datasets", nargs="*")
    ap.add_argument("--engine")
    ap.add_argument("--keep", action="store_true", help="keep the build server afterwards")
    ap.add_argument("--from-dumps", action="store_true",
                    help="bake from the dumps already in build/<engine>/ instead of dumping the build server")
    a = ap.parse_args(argv)
    cfg = stack.load()
    keep = a.keep or bool(cfg.build.get("keep_build_server"))
    for engine in _engines(cfg, a.engine):
        datasets = _datasets(cfg, engine, a.datasets)
        print(f"== image: {engine.image} <- {' '.join(datasets)}")
        rc = engine.image_build(datasets, keep=keep, threads=int(cfg.build.get("threads", 4)),
                                from_dumps=a.from_dumps)
        if rc:
            return rc
    return 0


def test_image(argv=None):
    ap = argparse.ArgumentParser(description="run the image-level tests against a built image")
    ap.add_argument("datasets", nargs="*")
    ap.add_argument("--engine")
    a = ap.parse_args(argv)
    cfg = stack.load()
    failures = 0
    for engine in _engines(cfg, a.engine):
        print(f"== test-image: {engine.image}")
        failures += engine.image_test(_datasets(cfg, engine, a.datasets)) or 0
    return 1 if failures else 0


def main(argv=None):
    """`run`: the whole job from the configuration."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--up", action="store_true", help="start the stack when the images are built")
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args(argv)
    cfg = stack.load()
    problems = cfg.validate()
    for p in problems:
        print(f"  x {p}")
    if problems:
        return 2
    print(f"run: {cfg.source}")
    for name, datasets in cfg.engines.items():
        print(f"  {name}: {len(datasets)} dataset(s)")
    print(f"  consoles: {', '.join(cfg.consoles)}\n")
    if build(["--no-fetch"] if a.no_fetch else []):
        return 1
    if image([]):
        return 1
    if a.up:
        return up([])
    return 0


def up(argv=None):
    ap = argparse.ArgumentParser(description="regenerate compose.yaml and the landing page, start the stack")
    ap.parse_args(argv)
    cfg = stack.load()
    if compose.main([]):
        return 2
    print("  . docker compose up -d --wait")
    if subprocess.run(["docker", "compose", "-f", COMPOSE, "up", "-d", "--wait"], cwd=ROOT).returncode != 0:
        return 1
    if "landing" in cfg.consoles:
        rc = console_page.main([])
        if rc:
            return rc
    print("  . the stack is up:")
    for name in cfg.engines:
        e = engine_registry.get(name)
        print(f"      {e.title:<14} 127.0.0.1:{cfg.ports.get(name, e.port)}   {e.connection_hint(cfg)}")
    for name in cfg.consoles:
        if name in cfg.ports:
            print(f"      {name:<14} http://127.0.0.1:{cfg.ports[name]}/")
    return 0


def down(argv=None):
    ap = argparse.ArgumentParser(description="stop the stack")
    ap.parse_args(argv)
    if not os.path.exists(COMPOSE):
        compose.main([])
    return subprocess.run(["docker", "compose", "-f", COMPOSE, "down"], cwd=ROOT).returncode


def check(argv=None):
    """The local gate: everything that needs no build."""
    ap = argparse.ArgumentParser(description="the local gate: bundle validation and generated files")
    ap.parse_args(argv)
    from megasamples import catalogue, okf_check, okf_fix_quotes, provenance
    steps = [("knowledge bundle", lambda: okf_check.main(["--bundle", "knowledge"])),
             ("frontmatter quoting", lambda: okf_fix_quotes.main(["--bundle", "knowledge", "--check"])),
             ("licence and provenance files", lambda: provenance.main(["--check"])),
             ("catalogue and README table", lambda: catalogue.main(["--check"])),
             ("unit tests", lambda: subprocess.run([sys.executable, "-m", "pytest", "-q", "tests"], cwd=ROOT).returncode)]
    failed = []
    for label, fn in steps:
        print(f"== {label}")
        try:
            rc = fn()
        except SystemExit as exc:
            rc = exc.code
        if rc:
            failed.append(label)
    print(f"check: {len(failed)} failure(s)" + (f" -- {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
