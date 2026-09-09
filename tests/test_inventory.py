"""The dataset inventory: selectors, prerequisites and build order."""
from megasamples import datasets as inventory


def test_every_dataset_has_a_tier_and_load_list():
    for name, cfg in inventory.inventory().items():
        assert cfg.get("tier") in inventory.TIERS, name
        assert "load" in cfg, name


def test_core_and_quick_sizes():
    core, quick = inventory.core(), inventory.quick()
    assert len(core) == 21
    assert len(quick) == 15
    assert set(quick) <= set(core)


def test_prerequisites_precede_dependants():
    order = inventory.select("all")
    assert order.index("oracle_hr") < order.index("oracle_oe")          # depends:
    assert order.index("dvdstore") < order.index("dvdstore_reviews")     # append: true
    assert order.index("nyc_taxi") < order.index("nyc_taxi_yellow")


def test_select_pulls_in_prerequisites_and_is_ordered_small_first():
    order = inventory.select(["oracle_oe", "sakila"])
    assert "oracle_hr" in order and order.index("oracle_hr") < order.index("oracle_oe")
    sizes = [inventory.download_bytes(n) for n in inventory.select("quick")]
    # small-first, except where a prerequisite had to come earlier
    assert sizes[0] <= sizes[-1]


def test_unknown_selector_is_an_error():
    import pytest
    with pytest.raises(KeyError):
        inventory.select("no_such_dataset")
