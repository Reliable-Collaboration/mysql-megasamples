"""The engine registry. An engine is a database product the datasets are built for.

MySQL is the hub: every dataset's converter emits MySQL SQL, the MySQL build server is where the
data is loaded and verified, and every other engine is a port of that verified corpus
(ARCHITECTURE.md section 3). Engines register here by name; the stack configuration names them.
"""
import importlib

from megasamples.engines.base import Engine  # noqa: F401  (re-exported)

_MODULES = {"mysql": "megasamples.engines.mysql"}
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
