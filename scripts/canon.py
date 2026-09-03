#!/usr/bin/env python3
"""The canonical row digest: one definition, generated for SQL and computable in Python.

Rules and rationale: knowledge/decisions/test-checksum-method.md. Two separators matter and both are
written as character codes, never as backslash escapes, because MySQL drops the backslash before an
unrecognised escape (`'a\\x1fb'` is the text `ax1fb`, verified at P-02):

    field separator  U+001F   SQL CHAR(31)    Python "\\x1f"
    NULL sentinel    U+0000   SQL CHAR(0)     Python "\\x00"

Float/double and JSON columns are excluded from the digest: their text rendering is not stable across
the two sides. They are compared through per-column aggregates and the deterministic samples instead.
"""
import hashlib

SEP, NUL = "\x1f", "\x00"
EXCLUDED = {"float", "double", "json"}


def column_sql(name, data_type):
    """The SQL expression rendering one column into its canonical text."""
    q = f"`{name}`"
    t = data_type.lower()
    if t in ("datetime", "timestamp"):
        expr = f"DATE_FORMAT({q}, '%Y-%m-%d %H:%i:%s.%f')"
    elif t == "time":
        expr = f"DATE_FORMAT({q}, '%H:%i:%s.%f')"
    elif t in ("binary", "varbinary", "blob", "tinyblob", "mediumblob", "longblob", "bit"):
        expr = f"LOWER(HEX({q}))"
    elif t in ("geometry", "point", "linestring", "polygon", "multipoint",
               "multilinestring", "multipolygon", "geometrycollection"):
        expr = f"LOWER(HEX(ST_AsBinary({q})))"
    elif t == "char":
        expr = f"RTRIM({q})"          # CHAR is space-padded on the source side
    else:
        expr = f"CAST({q} AS CHAR)"   # ints, decimals, dates, text, enum, set, year
    return f"COALESCE({expr}, CHAR(0))"


def row_text_sql(columns):
    """CONCAT_WS over the canonical column expressions. `columns` is [(name, data_type)]."""
    parts = ", ".join(column_sql(n, t) for n, t in columns if t.lower() not in EXCLUDED)
    return f"CONCAT_WS(CHAR(31), {parts})"


def digest_sql(columns):
    """The unsigned 64-bit per-row digest. The CAST is load-bearing: CONV returns a string, and an
    uncast SUM over it evaluates as DOUBLE and loses precision above 2^53 (verified at P-02)."""
    return f"CAST(CONV(SUBSTRING(SHA2({row_text_sql(columns)}, 256), 1, 16), 16, 10) AS UNSIGNED)"


def fingerprint_sql(schema, table, columns):
    """(count, bit_xor, sum mod 2^64). COALESCE matters: both aggregates are NULL over zero rows."""
    d = digest_sql(columns)
    return (f"SELECT COUNT(*) AS n, "
            f"COALESCE(BIT_XOR({d}), 0) AS x, "
            f"CAST(COALESCE(SUM({d}), 0) % 18446744073709551616 AS UNSIGNED) AS s "
            f"FROM `{schema}`.`{table}`")


def row_digest(values):
    """The Python side, for baselines computed by a converter before MySQL is involved."""
    text = SEP.join(NUL if v is None else v for v in values)
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


def fold(digests):
    x, s = 0, 0
    n = 0
    for d in digests:
        x ^= d
        s = (s + d) % (2 ** 64)
        n += 1
    return {"n": n, "x": x, "s": s}
