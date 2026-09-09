"""The engine registry. An engine is a database product the datasets are built for.

MySQL is the hub: every dataset's converter emits MySQL SQL, the MySQL build server is where the
data is loaded and verified, and every other engine is a port of that verified corpus
(ARCHITECTURE.md section 3). Engines register here by name; the stack configuration names them.
"""
import importlib, os

from megasamples.engines.base import Engine  # noqa: F401  (re-exported)

_MODULES = {"mysql": "megasamples.engines.mysql", "postgres": "megasamples.engines.postgres",
            "sqlite": "megasamples.engines.sqlite"}
_instances = {}


def names():
    return list(_MODULES)


def get(name):
    if name not in _MODULES:
        raise KeyError(f"unknown engine {name!r}; known: {', '.join(_MODULES)}")
    if name not in _instances:
        module = importlib.import_module(_MODULES[name])
        _instances[name] = module.ENGINE
    return _instances[name]


def all():
    return [get(n) for n in _MODULES]


def first_database(cfg, engine):
    """The database a connection hint names: sakila when configured, else the first configured dataset's."""
    from megasamples import datasets as inventory
    names = cfg.datasets(engine)
    chosen = "sakila" if "sakila" in names else (names[0] if names else "sakila")
    return inventory.load(chosen)["database"] if names else chosen


def unique_databases(datasets):
    """The databases the datasets live in, once each, in order: an `append: true` dataset shares its
    base's, and everything built per database (dumps, ports, images, registry rows) is keyed by it."""
    from megasamples import datasets as inventory
    out = []
    for d in datasets:
        s = inventory.load(d)["database"]
        if s not in out:
            out.append(s)
    return out


def expected_tables(dataset):
    """The tables a dataset's tests/expected_counts.yaml names (its own tables, for an append dataset)."""
    import yaml
    from megasamples.paths import DATASETS
    path = os.path.join(DATASETS, dataset, "tests", "expected_counts.yaml")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return list(yaml.safe_load(fh) or {})
