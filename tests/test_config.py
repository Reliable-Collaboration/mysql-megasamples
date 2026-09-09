"""megasamples.yaml: defaults, expansion, validation, round trip."""
import os

from megasamples import config as stack


def test_default_is_mysql_core_four_consoles():
    cfg = stack.Config({})
    assert list(cfg.engines) == ["mysql"]
    assert len(cfg.engines["mysql"]) == 21
    assert cfg.consoles == ["landing", "phpmyadmin", "adminer", "dbgate", "cloudbeaver"]
    assert cfg.validate() == []


def test_selectors_and_lists_expand():
    cfg = stack.Config({"engines": {"mysql": {"datasets": "quick"}}})
    assert len(cfg.engines["mysql"]) == 15
    cfg = stack.Config({"engines": {"mysql": {"datasets": ["oracle_oe"]}}})
    assert cfg.engines["mysql"] == ["oracle_hr", "oracle_oe"]


def test_validation_names_the_problem():
    problems = stack.Config({"engines": {"mysql": {"datasets": "core"}, "oracle": {}}}).validate()
    assert any("unknown engine 'oracle'" in p for p in problems)
    problems = stack.Config({"consoles": ["landing", "pgweb"]}).validate()
    assert any("unknown console 'pgweb'" in p for p in problems)
    problems = stack.Config({"ports": {"mysql": 8080}}).validate()
    assert any("port 8080 is used by both" in p for p in problems)


def test_write_then_load_round_trip(tmp_path):
    path = tmp_path / "megasamples.yaml"
    stack.write({"engines": {"mysql": {"datasets": "quick"}}, "consoles": ["landing", "adminer"]}, str(path))
    cfg = stack.load(str(path))
    assert cfg.source.endswith("megasamples.yaml")
    assert len(cfg.engines["mysql"]) == 15
    assert cfg.consoles == ["landing", "adminer"]
    assert cfg.ports["mysql"] == 3306          # defaults fill what the file leaves out


def test_missing_file_means_defaults(tmp_path):
    cfg = stack.load(str(tmp_path / "absent.yaml"))
    assert cfg.path is None and "default" in cfg.source
