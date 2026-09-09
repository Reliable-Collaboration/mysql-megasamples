"""What every engine's adapter prints for a routine call or a trigger scenario, in one comparable
form: the lines of the output, each value normalised, sorted.

Sorting the lines makes the comparison independent of row order (a procedure without ORDER BY
returns rows in whatever order the engine reads them, and collations order text differently),
and of the client: a value holding a newline is compared line by line on every engine. The
normalisation covers the renderings that differ between clients for the same value:

    t / f            PostgreSQL's booleans -> 1 / 0, MySQL's tinyint(1) rendering
    12.3600          a decimal rounded to four places, then its trailing zeros dropped: MySQL gives
                     an AVG four more places than its argument, PostgreSQL sixteen; both agree to four
    'abc   '         trailing blanks dropped: PostgreSQL pads CHAR(n) on output, MySQL strips it
    ...:59.500       a date-time's fractional zeros dropped: MySQL prints DATETIME(3) as .000, psql prints none
    NULL             every client is asked to print NULL that way
"""
import decimal, re

DECIMAL = re.compile(r"^-?\d+\.\d+$")
FRACTION = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|\d{2}:\d{2}:\d{2})\.(\d+)$")
PLACES = decimal.Decimal("0.0001")


def cell(text):
    text = text.rstrip(" ")
    if text in ("t", "f"):
        return "1" if text == "t" else "0"
    m = FRACTION.match(text)
    if m:                                   # MySQL prints a DATETIME(3) as .000, PostgreSQL prints nothing
        frac = m.group(2).rstrip("0")
        return m.group(1) + (f".{frac}" if frac else "")
    if DECIMAL.match(text):
        d = decimal.Decimal(text).quantize(PLACES, rounding=decimal.ROUND_HALF_UP).normalize()
        return "0" if d == 0 else format(d, "f")
    return text


def lines(text):
    """The normalised, sorted lines of a client's tab-separated output."""
    out = []
    for line in text.split("\n"):
        if line == "":
            continue
        out.append("\t".join(cell(c) for c in line.split("\t")))
    return sorted(out)


def value(v):
    """A driver value (SQLite, Python) rendered as the clients render it."""
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, bytes):
        return v.hex()
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return str(v)


def rows_text(rows):
    return "\n".join("\t".join(value(v) for v in row) for row in rows)
