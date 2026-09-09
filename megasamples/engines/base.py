"""What every engine provides. The pipeline talks to engines only through this interface, so the
commands (build, image, test-image, verify, up) read the same for MySQL, PostgreSQL and SQLite.
"""


class Engine:
    name = ""            # the key in megasamples.yaml and the build/<name>/ directory
    title = ""           # how documentation names it
    version = ""         # the pinned server version the image is built from
    image = ""           # the local image tag `megasamples image` produces
    container = ""       # the stack container name (docker compose)
    port = 0             # the server port inside the container
    hub = False          # True for the engine the datasets are converted into first

    # --- building --------------------------------------------------------------------------------
    def build(self, dataset, fresh=False):
        """Get one dataset into the engine's build server or file: stage/load/port as the engine needs."""
        raise NotImplementedError

    def verify(self, dataset, stages=None, pin=False):
        """Run the verification stages against the built dataset. Returns the number of failures."""
        raise NotImplementedError

    def image_build(self, datasets, keep=False, threads=4, from_dumps=False):
        """Bake the named datasets into the engine's image. `from_dumps` skips the build server and
        uses the dumps already under build/<engine>/, which is how a finished corpus is re-baked."""
        raise NotImplementedError

    def image_test(self, datasets):
        """Run the image-level tests. Returns the number of failures."""
        raise NotImplementedError

    # --- running ---------------------------------------------------------------------------------
    def compose_service(self, config):
        """The service definition for the stack, as a dict compose.yaml will carry."""
        raise NotImplementedError

    def registry_rows(self, container):
        """[(name, tier, licenses_json, row_counts_json, record)] from the running image's registry."""
        raise NotImplementedError

    def sizes(self, container):
        """{database: (tables, megabytes)} from the running image."""
        raise NotImplementedError

    def connection_hint(self, config):
        """The one-line client hint the landing page shows, e.g. a mysql or psql command."""
        raise NotImplementedError
