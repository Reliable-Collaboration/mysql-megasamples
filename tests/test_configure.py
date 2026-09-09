"""The chooser's model: what it writes for each kind of selection."""
from megasamples import config as stack, configure, datasets as inventory


def test_selection_writes_selectors_when_they_match_exactly():
    sel = configure.Selection(stack.Config({}))
    assert sel.to_raw()["engines"]["mysql"] == {"datasets": "core"}
    sel.set_column("mysql", inventory.quick())
    assert sel.to_raw()["engines"]["mysql"] == {"datasets": "quick"}
    sel.set_column("mysql", inventory.names())
    assert sel.to_raw()["engines"]["mysql"] == {"datasets": "all"}


def test_selection_writes_an_ordered_list_otherwise():
    sel = configure.Selection(stack.Config({}))
    sel.set_column("mysql", [])
    sel.toggle("mysql", "oracle_oe")
    sel.toggle("mysql", "sakila")
    raw = sel.to_raw()["engines"]["mysql"]["datasets"]
    assert raw == inventory.build_order(["oracle_oe", "sakila"])
    assert raw.index("oracle_hr") < raw.index("oracle_oe")


def test_consoles_are_filtered_to_what_the_engines_support():
    sel = configure.Selection(stack.Config({}))
    assert "phpmyadmin" in sel.to_raw()["consoles"]
    sel.toggle_console("phpmyadmin")
    assert "phpmyadmin" not in sel.to_raw()["consoles"]


def test_toggling_the_last_engine_off_is_refused():
    sel = configure.Selection(stack.Config({}))
    sel.toggle_engine("mysql")
    assert sel.engines == ["mysql"]
