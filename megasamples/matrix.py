"""What exists: the engines, the datasets with their tiers and sizes, the consoles.

  python3 -m megasamples list [--engines | --datasets | --consoles] [--names]

`--names` prints bare dataset names, one per line, which is how the Makefile learns its targets.
"""
import argparse, os, sys

import yaml

from megasamples import consoles as console_registry, datasets as inventory, engines as engine_registry
from megasamples.paths import DATASETS


def counts(name):
    path = os.path.join(DATASETS, name, "tests", "expected_counts.yaml")
    if not os.path.exists(path):
        return None, None
    with open(path, encoding="utf-8") as fh:
        c = yaml.safe_load(fh) or {}
    return len(c), sum(v for v in c.values() if isinstance(v, int))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--engines", action="store_true")
    ap.add_argument("--datasets", action="store_true")
    ap.add_argument("--consoles", action="store_true")
    ap.add_argument("--names", action="store_true", help="dataset names only, one per line")
    ap.add_argument("--select", default="all", help="with --names: core | quick | all | a tier")
    a = ap.parse_args(argv)
    if a.names:
        print("\n".join(inventory.select(a.select)))
        return 0
    show_all = not (a.engines or a.datasets or a.consoles)

    if show_all or a.engines:
        print("ENGINES")
        for e in engine_registry.all():
            print(f"  {e.name:<10} {e.title} {e.version:<8} image {e.image}" + ("   (hub)" if e.hub else ""))
        print()
    if show_all or a.datasets:
        print("DATASETS — download is the upstream bytes fetched; tables and rows are the pinned expectations")
        print(f"  {'dataset':<24}{'tier':<13}{'quick':<7}{'download MB':>12}{'tables':>8}{'rows':>12}")
        for name, cfg in inventory.inventory().items():
            t, r = counts(name)
            print(f"  {name:<24}{cfg.get('tier', '?'):<13}{'yes' if cfg.get('quick') else '':<7}"
                  f"{inventory.download_bytes(name) / 1e6:>12.1f}"
                  f"{(t if t is not None else '—'):>8}{(f'{r:,}' if r else '—'):>12}")
        core = inventory.core()
        print(f"\n  core: {len(core)} datasets, {sum(inventory.download_bytes(n) for n in core) / 1e6:,.0f} MB of downloads;"
              f" quick: {len(inventory.quick())} datasets, "
              f"{sum(inventory.download_bytes(n) for n in inventory.quick()) / 1e6:,.0f} MB")
        print()
    if show_all or a.consoles:
        print("CONSOLES")
        for c in console_registry.CONSOLES:
            print(f"  {c.name:<12} {c.title:<14} {', '.join(c.engines) or '(no database; the index page)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
