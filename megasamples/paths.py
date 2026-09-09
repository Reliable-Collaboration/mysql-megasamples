"""Where everything lives. Every path the package uses comes from here, so a directory moves once.

Build outputs are git-ignored and live under build/, one subdirectory per engine plus the shared
staging area that holds each dataset's converted SQL.
"""
import os

PACKAGE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(PACKAGE)

DATASETS = os.path.join(ROOT, "datasets")          # one directory per dataset: contract, converter, tests
ENGINES = os.path.join(ROOT, "engines")            # per-engine Dockerfiles, server configuration, init SQL
CONSOLES = os.path.join(ROOT, "consoles")          # per-console configuration and the generated landing page
KNOWLEDGE = os.path.join(ROOT, "knowledge")        # the OKF evidence bundle
DOWNLOADS = os.path.join(ROOT, "downloads")        # sha256-verified upstream artifacts (git-ignored)
BUILD = os.path.join(ROOT, "build")                # everything a build produces (git-ignored)
STAGE = os.path.join(BUILD, "stage")               # converted SQL per dataset: the build server's input
RELEASE = os.path.join(ROOT, "release")            # staged release assets and their checksums

MANIFEST = os.path.join(ROOT, "manifest.yaml")     # every downloadable artifact
CONFIG = os.path.join(ROOT, "megasamples.yaml")    # the stack: engines x datasets, consoles, ports
CONFIG_EXAMPLE = os.path.join(ROOT, "megasamples.example.yaml")
COMPOSE = os.path.join(ROOT, "compose.yaml")       # generated from CONFIG by `megasamples compose`


def dataset_dir(name):
    return os.path.join(DATASETS, name)


def stage_dir(name):
    return os.path.join(STAGE, name)


def engine_build_dir(engine):
    """Per-engine build outputs: dumps, registry SQL, port files."""
    return os.path.join(BUILD, engine)


def engine_dir(engine):
    """The engine's committed assets: Dockerfile, configuration, init scripts."""
    return os.path.join(ENGINES, engine)


def rel(path):
    """A path as the documentation writes it: relative to the repository root, or absolute when
    it lies outside it."""
    inside = os.path.commonpath([os.path.abspath(path), ROOT]) == ROOT
    return os.path.relpath(path, ROOT) if inside else os.path.abspath(path)
