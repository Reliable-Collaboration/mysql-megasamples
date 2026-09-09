#!/usr/bin/env python3
"""Turn a CSV file into MySQL DDL plus INSERT statements, from an explicit column specification.

The specification is always explicit: nothing infers types from the data, because an inferred type
is a silent decision that only shows up as truncation or a coercion much later. Each table declares
its columns, the tokens that mean NULL, and any renaming needed to make an upstream header a legal
MySQL identifier.
"""
import csv, io, os


def sql_literal(value, column_type):
    if value is None:
        return "NULL"
    t = column_type.upper()
    if any(k in t for k in ("INT", "DECIMAL", "DOUBLE", "FLOAT")):
        return value
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def emit_table(path, table, columns, null_tokens=("", "NA", "NULL"), surrogate=None,
               header="named", transform=None, batch=200):
    """Return SQL for one table.

    columns      [(source_header_or_index, mysql_name, mysql_type)]
    header       "named"   -> first row holds column names, matched by name
                 "skip"    -> first row is not column names; columns are matched by position
                 "none"    -> the file has no header row
    surrogate    name of an AUTO_INCREMENT primary key to add (the file supplies no key)
    transform    optional fn(dict) -> dict applied to each row before emitting
    """
    with open(path, encoding="utf-8", newline="") as fh:
        text = fh.read()
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if header in ("named", "skip"):
        head, rows = rows[0], rows[1:]
    else:
        head = None

    def value_of(row, key):
        if isinstance(key, int):
            return row[key] if key < len(row) else None
        return row[head.index(key)] if head and key in head else None

    defs = []
    if surrogate:
        defs.append(f"  `{surrogate}` INT UNSIGNED NOT NULL AUTO_INCREMENT")
    defs += [f"  `{name}` {ctype}" for _, name, ctype in columns]
    if surrogate:
        defs.append(f"  PRIMARY KEY (`{surrogate}`)")
    out = [f"DROP TABLE IF EXISTS `{table}`;",
           f"CREATE TABLE `{table}` (\n" + ",\n".join(defs) + "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"]

    names = ", ".join(f"`{name}`" for _, name, _ in columns)
    values, emitted = [], 0
    for row in rows:
        if not row or all(c.strip() == "" for c in row):
            continue
        record = {}
        for key, name, ctype in columns:
            raw = value_of(row, key)
            record[name] = None if raw is None or raw.strip() in null_tokens else raw.strip()
        if transform:
            record = transform(record)
        tuple_sql = ", ".join(sql_literal(record[name], ctype) for _, name, ctype in columns)
        values.append(f"({tuple_sql})")
        emitted += 1
        if len(values) >= batch:
            out.append(f"INSERT INTO `{table}` ({names}) VALUES\n" + ",\n".join(values) + ";")
            values = []
    if values:
        out.append(f"INSERT INTO `{table}` ({names}) VALUES\n" + ",\n".join(values) + ";")
    return "\n".join(out) + "\n", emitted
