#!/usr/bin/env python3
"""Read a MediaWiki `mysqldump` file: its CREATE TABLE, and its INSERT rows one tuple at a time.

The dumps are MariaDB `mysqldump` output and MySQL 9.7 accepts them unchanged -- the
[DDL question](../../knowledge/questions/mediawiki-sql-dump-ddl-compatibility-mysql-9-7.md) was
answered by trying every construct on the target server. What this module adds is the ability to
keep only some rows, which needs the multi-row INSERT split into tuples, and that has to respect
quoting: titles are `varbinary` and contain commas, quotes and backslashes.
"""
import gzip, re

CREATE = re.compile(r"(?is)^CREATE TABLE .*?;$", re.M)
INSERT = re.compile(r"(?i)^INSERT INTO `(\w+)` VALUES ")


def create_table(path):
    """The CREATE TABLE statement, verbatim."""
    with gzip.open(path, "rt", encoding="utf-8", errors="surrogateescape") as fh:
        buffer = []
        for line in fh:
            if line.startswith("CREATE TABLE"):
                buffer = [line]
            elif buffer:
                buffer.append(line)
                if line.rstrip().endswith(";"):
                    return "".join(buffer).rstrip()
    raise ValueError(f"no CREATE TABLE in {path}")


def split_tuples(values):
    """`(1,'a'),(2,'b\\'c')` -> ["(1,'a')", "(2,'b\\'c')"], respecting quotes and backslashes."""
    out, depth, start, in_str, i, n = [], 0, None, False, 0, len(values)
    while i < n:
        ch = values[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == "'":
                in_str = False
        elif ch == "'":
            in_str = True
        elif ch == "(":
            if depth == 0:
                start = i
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                out.append(values[start:i + 1])
        i += 1
    return out


def fields(row):
    """The top-level fields of one `(...)` tuple, as raw SQL text."""
    body = row[1:-1]
    out, current, in_str, i, n = [], [], False, 0, len(body)
    while i < n:
        ch = body[i]
        if in_str:
            current.append(ch)
            if ch == "\\" and i + 1 < n:
                current.append(body[i + 1]); i += 2; continue
            if ch == "'":
                in_str = False
        elif ch == "'":
            in_str = True; current.append(ch)
        elif ch == ",":
            out.append("".join(current)); current = []
        else:
            current.append(ch)
        i += 1
    out.append("".join(current))
    return out


def rows(path):
    """Yield (table, tuple text) for every row of every INSERT in the dump."""
    with gzip.open(path, "rt", encoding="utf-8", errors="surrogateescape") as fh:
        for line in fh:
            m = INSERT.match(line)
            if not m:
                continue
            for row in split_tuples(line[m.end():].rstrip().rstrip(";")):
                yield m.group(1), row
