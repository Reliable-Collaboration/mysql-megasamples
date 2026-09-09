#!/usr/bin/env python3
"""Parsing helpers for the Oracle Order Entry install scripts.

Two things here are not shared with the other Oracle schemas. The scripts use SQL*Plus line
continuation, and their INSERT statements carry object constructors -- an address object, a phone
VARRAY, a spatial point and an XMLType -- which have to be taken apart before the rows can be
written to a relational schema.

Record: knowledge/datasets/oracle-oe-pm-ix.md
"""
import os, re, sys

from megasamples.sources import plsql  # noqa: E402

# `SET FEEDBACK OFF` is a SQL*Plus directive; `SET sales_rep_id = NULL` is the SET clause of an
# UPDATE, which happens to start its own line in pord_v3.sql. Requiring the SQL*Plus two-word form
# and no assignment keeps the second one.
DIRECTIVE = re.compile(r"(?i)^\s*(rem\b|prompt\b|set\s+\w+(\s+\w+)?\s*;?\s*$|define\b|@|--"
                       r"|/\s*$|alter\s+session\b|connect\b|commit\s*;?\s*$)")


def preprocess(text):
    """Drop SQL*Plus directives, then join continued lines with a single space.

    A `-` at the end of a line continues the statement, and the whole of the OE data is written
    that way to keep every line under 80 bytes -- including inside string literals, where the join
    decides what the text says. The continuation and its line break become **one space**: verified
    against an independent export of the same schema, where the source's
    `...virtually-flat,-\\nhigh-resolution...` reads `virtually-flat, high-resolution`. Joining with
    nothing instead would run 264 pairs of words together in the English descriptions alone.
    """
    lines = [l for l in text.split("\n") if not DIRECTIVE.match(l)]
    out = []
    for line in lines:
        stripped = line.rstrip("\r")
        if out and out[-1].endswith("-"):
            out[-1] = out[-1][:-1] + " " + stripped.lstrip()
        else:
            out.append(stripped)
    return "\n".join(out)


def statements(path):
    return plsql.split_statements(preprocess(open(path, encoding="utf-8").read()))


CALL = re.compile(r"(?is)^\s*([\w.]+)\s*\((.*)\)\s*$")


def call(expr):
    """`f(a, b)` -> ('f', ['a', 'b']); None when the expression is not a call."""
    m = CALL.match(expr.strip())
    if not m:
        return None
    return m.group(1).lower(), [a.strip() for a in plsql.split_top_level(m.group(2))]


def values_of(statement):
    """The top-level expressions of an `INSERT INTO t VALUES (...)` statement."""
    m = re.match(r"(?is)^\s*INSERT\s+INTO\s+(\w+)\s*(\([^)]*\))?\s*VALUES\s*\((.*)\)\s*$",
                 statement.strip().rstrip(";").strip())
    if not m:
        return None, None, None
    columns = [c.strip().lower() for c in m.group(2)[1:-1].split(",")] if m.group(2) else None
    return m.group(1).lower(), columns, [v.strip() for v in plsql.split_top_level(m.group(3))]


UNISTR_ESCAPE = re.compile(r"\\([0-9a-fA-F]{4})")


def sql_string(expr):
    """The text of a string expression: a literal, a `||` concatenation, or a UNISTR() call."""
    parts = plsql.split_top_level(expr, "|")
    if len(parts) > 1:                      # split_top_level on '|' halves each '||'
        parts = [p for p in parts if p.strip()]
        return "".join(sql_string(p) for p in parts)
    expr = expr.strip()
    c = call(expr)
    if c and c[0] == "unistr":
        # UNISTR turns \XXXX into a UCS-2 code unit; surrogate pairs are written as two escapes
        text = sql_string(c[1][0])
        return UNISTR_ESCAPE.sub(lambda m: chr(int(m.group(1), 16)), text).encode(
            "utf-16", "surrogatepass").decode("utf-16")
    if c and c[0] in ("sys.xmltype.createxml", "xmltype.createxml", "sys.xmltype", "xmltype"):
        return sql_string(c[1][0])
    if expr.upper() == "NULL":
        return None
    if expr.startswith("'") and expr.endswith("'"):
        return expr[1:-1].replace("''", "'")
    raise ValueError(f"not a string expression: {expr[:80]!r}")
