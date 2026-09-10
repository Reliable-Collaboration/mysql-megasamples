"""The stack configuration: megasamples.yaml.

It answers three questions -- which engines, which datasets on each, which consoles -- plus the
ports and build knobs. `megasamples configure` writes it interactively; every other command reads
it. Without the file the built-in default applies: MySQL with the core tier and the four consoles.

    engines:
      mysql:      {datasets: core}          # a selector (core | quick | all | a tier) or a list
      postgres:   {datasets: [sakila, chinook]}
      sqlite:     {datasets: quick}
    consoles: [landing, cloudbeaver, dbgate, adminer, phpmyadmin]
    ports:    {mysql: 3306, landing: 8080, ...}   # host ports; every one binds to 127.0.0.1
    build:    {threads: 4, keep_build_server: false, scale_factor: 1}
    downloads: {concurrency: 3}
"""
import copy, os

import yaml

from megasamples import datasets as inventory
from megasamples.paths import CONFIG, rel

DEFAULT = {
    "engines": {"mysql": {"datasets": "core"}},
    "consoles": ["landing", "cloudbeaver", "dbgate", "adminer", "phpmyadmin"],
    "ports": {"mysql": 3306, "postgres": 5432, "landing": 8080, "phpmyadmin": 8081,
              "adminer": 8082, "dbgate": 8083, "cloudbeaver": 8084, "pgadmin": 8085,
              "sqlite-web": 8086},
    "build": {"threads": 4, "keep_build_server": False, "scale_factor": 1},
    "downloads": {"concurrency": 3},
}


class Config:
    def __init__(self, raw, path=None):
        merged = copy.deepcopy(DEFAULT)
        for key, value in (raw or {}).items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict) and key != "engines":
                merged[key].update(value)
            else:
                merged[key] = value
        self.raw = merged
        self.path = path
        # engine name -> ordered dataset list, selectors expanded
        self.engines = {}
        for name, spec in (merged.get("engines") or {}).items():
            spec = spec or {}
            self.engines[name] = inventory.select(spec.get("datasets", "core"))
        self.consoles = list(merged.get("consoles") or [])
        self.ports = dict(merged.get("ports") or {})
        self.build = dict(merged.get("build") or {})
        self.downloads = dict(merged.get("downloads") or {})

    @property
    def source(self):
        return rel(self.path) if self.path else "built-in default (no megasamples.yaml)"

    def datasets(self, engine=None):
        """The datasets for one engine, or the union across engines in build order."""
        if engine:
            return list(self.engines.get(engine, []))
        union = [d for names in self.engines.values() for d in names]
        return inventory.build_order(union)

    def hub_datasets(self):
        """Everything that has to exist in the MySQL build server: MySQL's own datasets plus every
        dataset another engine is ported from."""
        return self.datasets()

    def validate(self):
        from megasamples import consoles as console_registry, engines as engine_registry
        problems = []
        for name in self.engines:
            if name not in engine_registry.names():
                problems.append(f"unknown engine {name!r}; known: {', '.join(engine_registry.names())}")
        for name in self.consoles:
            if name not in console_registry.names():
                problems.append(f"unknown console {name!r}; known: {', '.join(console_registry.names())}")
            else:
                needs = console_registry.get(name).engines
                if needs and not any(e in self.engines for e in needs):
                    problems.append(f"console {name} needs one of {', '.join(needs)}, none selected")
        for name, chosen in self.engines.items():
            if not chosen:
                problems.append(f"engine {name} has no datasets; choose at least one or drop the engine")
        seen = {}
        for what, port in self.ports.items():
            if what in self.engines or what in self.consoles:
                if port in seen:
                    problems.append(f"port {port} is used by both {seen[port]} and {what}")
                seen[port] = what
        return problems


def load(path=None):
    path = path or CONFIG
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return Config(yaml.safe_load(fh) or {}, path)
    return Config({}, None)


def write(raw, path=None):
    """Write a configuration the way `configure` does: commented, keys in a fixed order."""
    path = path or CONFIG
    lines = ["# megasamples.yaml -- the stack this checkout builds and runs.",
             "# Written by `make configure`; edit freely. Selectors: core | quick | all | a tier name.",
             "# Every command reads it; without it the built-in default is MySQL + core + four consoles.",
             ""]
    ordered = {k: raw[k] for k in ("engines", "consoles", "ports", "build", "downloads") if k in raw}
    for k, v in raw.items():
        ordered.setdefault(k, v)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
        yaml.safe_dump(ordered, fh, sort_keys=False, default_flow_style=None, allow_unicode=True)
    return path
