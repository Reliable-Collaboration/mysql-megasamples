"""stage.py plans: every kind of `stage:` block produces the right converter invocation."""
import os

from megasamples import stage
from megasamples.paths import DATASETS, DOWNLOADS, STAGE


def argv_of(name):
    steps = [s for _, s in stage.plan(name) if s[0] == "run"]
    assert len(steps) == 1
    return steps[0][1]


def test_extract_kind():
    steps = stage.plan("sakila")
    assert steps[0][1][0] == "extract"
    assert steps[0][1][2] == ["sakila-db/sakila-schema.sql", "sakila-db/sakila-data.sql"]


def test_artifact_kind_passes_artifact_output_and_name_map():
    argv = argv_of("chinook")
    assert argv[2] == os.path.join(DOWNLOADS, "chinook", "Chinook_MySql.sql")
    assert argv[3] == os.path.join(STAGE, "chinook", "chinook.sql")
    assert argv[4] == os.path.join(DATASETS, "chinook", "name_map.yaml")


def test_dir_kind_with_shared_converter_source_and_args():
    argv = argv_of("contoso_1m")
    assert argv[1] == os.path.join(DATASETS, "contoso", "convert.py")
    assert argv[2] == os.path.join(DOWNLOADS, "contoso")
    assert argv[3] == os.path.join(STAGE, "contoso_1m", "contoso_1m.sql")
    assert argv[4:] == ["--size", "1m"]
    assert argv_of("stackexchange_dba")[2] == os.path.join(DOWNLOADS, "stackexchange_dba")


def test_generator_kind_takes_the_scale_factor(monkeypatch):
    monkeypatch.setenv("SF", "0.01")
    assert argv_of("tpch")[2:] == [os.path.join(STAGE, "tpch", "tpch.sql"), "--sf", "0.01"]


def test_export_kind_requires_the_export():
    steps = stage.plan("wideworldimporters")
    assert steps[0][1][0] == "require" and steps[0][1][1].endswith("export/meta.json")


def test_nothing_to_stage():
    assert stage.plan("citibike") == []
