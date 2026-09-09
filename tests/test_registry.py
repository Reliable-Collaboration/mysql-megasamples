"""The provenance registry: one row per database, an `append: true` dataset folded into its base's row."""
from megasamples import registry
from megasamples.engines import unique_databases


def test_append_dataset_shares_its_base_row():
    assert unique_databases(["dvdstore", "dvdstore_reviews", "sakila"]) == ["dvdstore", "sakila"]
    sql = registry.render(["dvdstore", "dvdstore_reviews", "sakila"], "test")
    rows = [l for l in sql.splitlines() if l.startswith("  ('")]
    assert len(rows) == 2 and rows[0].startswith("  ('dvdstore'") and rows[1].startswith("  ('sakila'")
    assert "reviews" in rows[0]                      # the appended table's pinned count joins the row


def test_by_database_orders_and_groups():
    groups = registry.by_database(["sakila", "dvdstore_reviews", "dvdstore"])
    assert list(groups) == ["dvdstore", "sakila"] and groups["dvdstore"] == ["dvdstore", "dvdstore_reviews"]
