"""megasamples/probe.py: one comparable form for what every engine's client prints."""
from megasamples import probe


def test_cells_are_normalised_and_lines_sorted():
    assert probe.lines("business    \t7369.8333333333333333\tt\nALL\t4988.2000\tf\n") == ["ALL\t4988.2\t0", "business\t7369.8333\t1"]
    assert probe.cell("12.34495") == "12.345" and probe.cell("-0.00001") == "0" and probe.cell("abc") == "abc"
    assert probe.cell("NULL") == "NULL" and probe.cell("2004-06-30 23:59:59.998") == "2004-06-30 23:59:59.998"


def test_driver_values_render_like_the_clients():
    assert probe.rows_text([(None, True, 3.0, b"\x01", "x")]) == "NULL\t1\t3\t01\tx"
