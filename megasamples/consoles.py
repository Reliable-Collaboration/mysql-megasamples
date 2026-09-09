"""The console registry: the web UIs the stack can start beside the databases.

Each console says which engines it can browse, the image it runs (pinned by digest), the memory it
is allowed, and how it is pointed at the databases. compose.py turns these into services,
console_page.py into landing-page links, console_test.py into endpoints to probe.
"""
from dataclasses import dataclass, field


@dataclass
class Console:
    name: str
    title: str
    engines: tuple                 # engines it can browse; () means it needs none (the landing page)
    image: str
    container_port: int
    mem_limit: str
    note: str                      # how a visitor gets in, shown on the landing page
    deep_link: str = ""            # URL template opening one database, {port} and {db}; "" if none
    letter: str = ""               # the one-letter badge the landing page uses for the deep link
    volumes: list = field(default_factory=list)

    @property
    def container(self):
        return f"megasamples-{self.name}"


CONSOLES = [
    Console("landing", "Console index", (),
            "nginx@sha256:3bcf852aed06467cf075c6105892e4d5a6ebbbafa0ce22d35062db9e90ddef4c", 80, "32m",
            "Start here: every database with its size, licence and provenance.",
            volumes=["./consoles/landing:/usr/share/nginx/html:ro"]),
    Console("phpmyadmin", "phpMyAdmin", ("mysql",),
            "phpmyadmin@sha256:20fa6f724ba77d41abc25b1aeb4d97692ce344c7ace305594e57c5893f60f0f7", 80, "256m",
            "Signed in already; the server menu switches account.",
            "http://127.0.0.1:{port}/index.php?route=/database/structure&db={db}&server=1", "P",
            volumes=["./consoles/phpmyadmin/config.user.inc.php:/etc/phpmyadmin/config.user.inc.php:ro"]),
    Console("adminer", "Adminer", ("mysql", "postgres"),
            "adminer@sha256:f1e2ba27b10a565ac77b2d8555d803be4ddb3232f4216dcf0ea85bcd8f2f1343", 8080, "160m",
            "Its login form remains; use either account below.",
            "http://127.0.0.1:{port}/?server=mysql&username=demo&db={db}", "A"),
    Console("dbgate", "DbGate", ("mysql", "postgres", "sqlite"),
            "dbgate/dbgate@sha256:14fce4ece52df514e0d320dc82cbfbca5e8f18f98464a6389b1c126f783a6b7e", 3000, "320m",
            "Both connections are preconfigured; pick one in the sidebar."),
    Console("cloudbeaver", "CloudBeaver", ("mysql", "postgres", "sqlite"),
            "dbeaver/cloudbeaver@sha256:3b4bf82287cf4febe0d335873f1346a01100f3951d266cd6a78c27fe30429cbc", 8978, "640m",
            "Open as a guest; both connections are in the sidebar.",
            volumes=["./consoles/cloudbeaver/.cloudbeaver.auto.conf:/opt/cloudbeaver/conf/.cloudbeaver.auto.conf:ro",
                     "./consoles/cloudbeaver/generated/cloudbeaver.conf:/opt/cloudbeaver/conf/cloudbeaver.conf:ro",
                     "./consoles/cloudbeaver/generated/initial-data-sources.conf:/opt/cloudbeaver/conf/initial-data-sources.conf:ro"]),
]
_BY_NAME = {c.name: c for c in CONSOLES}


def names():
    return list(_BY_NAME)


def get(name):
    if name not in _BY_NAME:
        raise KeyError(f"unknown console {name!r}; known: {', '.join(_BY_NAME)}")
    return _BY_NAME[name]


def usable(engines):
    """The consoles that can browse at least one of the given engines, plus the landing page."""
    return [c for c in CONSOLES if not c.engines or any(e in engines for e in c.engines)]
