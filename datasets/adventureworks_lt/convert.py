#!/usr/bin/env python3
"""AdventureWorks LT: translate the 2012 install script and its tab-separated data files.

The script is UTF-16LE T-SQL; the data files are Windows-1252 (`CODEPAGE='ACP'`) except
ProductModel.csv, which is UTF-16LE and uses `~~\\t` / `~~\\n` terminators because its XML columns
contain tabs and newlines of their own. Rather than hard-coding any of that, the converter reads
each file's terminators and codepage out of the script's own BULK INSERT clauses, so a change
upstream shows up as a conversion failure instead of silent corruption.

Record: knowledge/datasets/adventureworks-lt.md
"""
import os, re, sys, zipfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from megasamples.sources import tsql, ddlutil  # noqa: E402

DATABASE = "adventureworks_lt"
# T-SQL infers a computed column's type; MySQL makes you declare it. SalesOrderDetail.LineTotal is
# numeric(38,6) upstream, and the data files carry the computed value, which the build compares
# against what MySQL generates (tests/smoke.yaml) rather than trusting the expression to agree.
COMPUTED_TYPES = {"salesorderdetail.linetotal": "DECIMAL(38,6)",     # numeric(38,6) upstream
                  "salesorderheader.salesordernumber": "VARCHAR(25)",
                  "salesorderheader.totaldue": "DECIMAL(19,4)"}       # money upstream
# MySQL refuses a generated column that reads an AUTO_INCREMENT column, and SalesOrderNumber is
# 'SO' + SalesOrderID. Keeping the identity is worth more than keeping the column generated, so this
# one is loaded from the data file, which carries the same value.
MATERIALIZE = {"salesorderheader.salesordernumber"}
# Every programmable object the upstream script defines, and what this build does with it. The
# converter checks the script against this list, so an object added or renamed upstream stops the
# build instead of disappearing from the image without anyone noticing.
OBJECTS = {
    "view vproductanddescription": "translated",
    "view vproductmodelcatalogdescription": "translated",     # XQuery -> ExtractValue
    "view vgetallcategories": "translated",                   # recursive CTE
    "trigger idusalesorderdetail": "objects.sql",             # split into three row triggers
    "trigger usalesorderheader": "objects.sql",               # AFTER -> BEFORE, writes NEW
    "function ufngetsalesorderstatustext": "objects.sql",
    "function ufngetcustomerinformation": "dropped: MySQL has no table-valued functions",
    "function ufngetallcategories": "dropped: superseded by the vgetallcategories view",
    "procedure usplogerror": "dropped: T-SQL error handling has no MySQL equivalent",
    "procedure uspprinterror": "dropped: T-SQL error handling has no MySQL equivalent",
}
OBJECT_RE = re.compile(r"(?im)^\s*CREATE\s+(VIEW|TRIGGER|FUNCTION|PROCEDURE)\s+"
                       r"(?:\[?\w+\]?\s*\.\s*)?\[?(\w+)\]?")
INSIDE = "AdventureWorks 2012 LT Script/"
BULK = re.compile(r"(?is)BULK INSERT\s+\[[^\]]+\]\.\[([^\]]+)\]\.\[([^\]]+)\]\s+FROM\s+N'[^']*?"
                  r"([\w.]+\.csv)'\s*WITH\s*\((.*?)\);")


def unescape(term):
    return term.replace("\\t", "\t").replace("\\n", "\n").replace("\\r", "\r")


def row_pattern(term):
    """A ROWTERMINATOR of '\\n' also matches '\\r\\n', which is what BULK INSERT itself does.

    The files are CRLF, so splitting on a bare newline would both fail on ProductModel's '~~\\n'
    and leave a stray CR on the last column of every row of every other file.
    """
    return re.compile(re.escape(term).replace(re.escape("\n"), r"\r?\n"))


def decode(raw):
    """UTF-16 when the file says so with a BOM, otherwise Windows-1252 (the script's 'ACP')."""
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16"), "utf-16"
    return raw.decode("cp1252"), "cp1252"


def sql_value(value):
    if value == "":
        return "NULL"
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def main():
    src, dest, mapfile = sys.argv[1], sys.argv[2], sys.argv[3]
    z = zipfile.ZipFile(src)
    script = z.read(INSIDE + "instawltdb.sql").decode("utf-16")

    # SalesLT and dbo collapse into one MySQL database: their table names do not collide,
    # so the prefix is dropped rather than folded in (knowledge/decisions/schema-to-database-mapping.md)
    statements, name_map, notes = tsql.translate(script, keep_objects=True, schemas=("dbo", "SalesLT"),
                                                 computed_types=COMPUTED_TYPES,
                                                 materialize=MATERIALIZE)
    buckets = {k: [] for k in ("table", "index", "constraint", "view", "procedure", "function")}
    for st in statements:
        if st["kind"] in buckets:
            buckets[st["kind"]].append(st["sql"])
        elif st["kind"] == "other" and re.match(r"(?i)^\s*create\s+(unique\s+)?index", st["sql"].strip()):
            buckets["index"].append(st["sql"])

    out = [f"""-- AdventureWorks LT, translated by datasets/{DATABASE}/convert.py from the 2012 install
-- script. Upstream: microsoft/sql-server-samples (MIT). See datasets/{DATABASE}/LICENSE.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{DATABASE}`;
CREATE DATABASE `{DATABASE}` DEFAULT CHARACTER SET utf8mb4;
USE `{DATABASE}`;
"""]
    columns, generated = {}, {}
    for st in statements:
        if st["kind"] == "table":
            name = re.search(r"(?is)^\s*CREATE\s+TABLE\s+`([^`]+)`", st["sql"]).group(1)
            columns[name] = ddlutil.columns_of(st["sql"])
            generated[name] = set(st["generated"])
    for sql in buckets["table"]:
        out.append(tsql.terminate(sql))

    loaded, encodings = {}, {}
    out.append(f"\n-- {'-' * 60}\n-- data\n")
    for schema, table, filename, options in BULK.findall(script):
        opts = {k.upper(): v.strip("'") for k, v in re.findall(r"(\w+)\s*=\s*('[^']*'|\w+)", options)}
        field = unescape(opts.get("FIELDTERMINATOR", "\\t"))
        row = unescape(opts.get("ROWTERMINATOR", "\\n"))
        text, encoding = decode(z.read(INSIDE + filename))
        encodings[filename] = encoding
        target = tsql.ident(table)
        # the data files carry every column including the computed one, which MySQL will not accept
        # a value for, so name the columns explicitly and drop the generated fields
        keep = [i for i, c in enumerate(columns[target]) if c not in generated[target]]
        names = ", ".join(f"`{columns[target][i]}`" for i in keep)
        rows = [r for r in row_pattern(row).split(text) if r.strip("\r\n") != ""]
        values = []
        for line in rows:
            fields = line.lstrip("\r\n").split(field)
            if any(f.endswith("\r") for f in fields):
                sys.exit(f"{filename}: a field ends with CR -- the row terminator did not match")
            if len(fields) != len(columns[target]):
                sys.exit(f"{filename}: {len(fields)} fields but `{target}` has "
                         f"{len(columns[target])} columns -- upstream layout changed")
            values.append("(" + ", ".join(sql_value(fields[i]) for i in keep) + ")")
        loaded[target] = len(values)
        for i in range(0, len(values), 200):
            chunk = ",\n".join(values[i:i + 200])
            out.append(f"INSERT INTO `{target}` ({names}) VALUES\n{chunk};")

    found = {f"{kind.lower()} {name.lower()}" for kind, name in OBJECT_RE.findall(script)}
    if found != set(OBJECTS):
        missing, extra = sorted(set(OBJECTS) - found), sorted(found - set(OBJECTS))
        sys.exit(f"programmable objects changed upstream; missing {missing}, unaccounted {extra}")
    # only the views come from the translator; the rest are hand-written or deliberately dropped
    buckets["procedure"], buckets["function"] = [], []

    for phase in ("index", "constraint", "view", "function", "procedure"):
        if buckets[phase]:
            out.append(f"\n-- {'-' * 60}\n-- {phase}\n")
            out += [tsql.terminate(s) for s in buckets[phase]]
    out.append(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "objects.sql"),
                    encoding="utf-8").read())
    out.append("SET SESSION foreign_key_checks = 1;\n")
    open(dest, "w", encoding="utf-8").write("\n".join(out))
    with open(mapfile, "w", encoding="utf-8") as fh:
        fh.write("# Generated by datasets/adventureworks_lt/convert.py.\n")
        for old, new in sorted(name_map.items()):
            fh.write(f"{old}: {new}\n")
    print(f"  . translated {len(buckets['table'])} tables, {sum(loaded.values()):,} rows from "
          f"{len(loaded)} files; encodings {sorted(set(encodings.values()))}")
    for name, action in sorted(OBJECTS.items()):
        if action.startswith("dropped"):
            print(f"  . {name}: {action}")


if __name__ == "__main__":
    main()
