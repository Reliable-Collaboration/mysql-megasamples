#!/usr/bin/env python3
"""Read the data files of a SQL Server `BULK INSERT` script the way BULK INSERT reads them.

Shared by the AdventureWorks OLTP and DW converters, which use the same install-script shape with
different terminators.

The one thing that matters here: **BULK INSERT does not split a file into lines and then into
fields.** It reads field by field, and only the *last* field of a row is delimited by the row
terminator. That is why a newline inside a non-final column is data, not a row break -- AdventureWorks
OLTP's ProductReview has 4 rows across 34 physical lines because of it. Two further details of the
format are handled here as well: a `ROWTERMINATOR` of `\\n` means `\\r\\n` in a CRLF file, and a field
holding a single NUL byte is the empty string rather than NULL.
"""
import re, sys

# the whitespace after INSERT is optional: AdventureWorks DW writes `BULK INSERT[dbo].[DimCustomer]`
# for one table, and requiring a space there silently skipped its largest dimension
BULK = re.compile(r"(?is)BULK\s+INSERT\s*\[?(\w+)\]?\.\[?(\w+)\]?(?:\.\[?(\w+)\]?)?\s*FROM\s+'[^']*?"
                  r"([\w.]+\.csv)'\s*WITH\s*\((.*?)\)")


def unescape(term):
    if term.lower().startswith("0x"):
        return bytes.fromhex(term[2:]).decode("latin-1")
    return term.replace("\\t", "\t").replace("\\n", "\n").replace("\\r", "\r")


def statements(script, schemas=None):
    """[(schema, table, csv name, field terminator, row terminator)] in load order.

    A qualified name may be `[db].[schema].[table]` or `[schema].[table]`; the last two parts are
    what matter. Every clause is checked for the codepage and datafiletype the callers assume.
    """
    out = []
    for m in BULK.finditer(script):
        parts = [p for p in (m.group(1), m.group(2), m.group(3)) if p]
        schema, table = (parts[-2], parts[-1]) if len(parts) > 1 else ("dbo", parts[-1])
        opts = {k.upper(): v.strip("'") for k, v in
                re.findall(r"(\w+)\s*=\s*('[^']*'|\w+)", m.group(5))}
        if opts.get("CODEPAGE") != "65001" or opts.get("DATAFILETYPE") != "char":
            sys.exit(f"{m.group(4)}: unexpected codepage/datafiletype {opts}")
        out.append((schema.lower(), table.lower(), m.group(4),
                    unescape(opts["FIELDTERMINATOR"]), unescape(opts["ROWTERMINATOR"])))
    return out


def row_terminator(term, text):
    """The terminator the file actually uses, which is not always the one the script names."""
    if term.endswith("\n") and (term[:-1] + "\r\n") in text:
        return term[:-1] + "\r\n"
    return term


def rows(text, field, row, ncols, filename, table):
    """Yield one list of raw field strings per row, reading field by field."""
    row = row_terminator(row, text)
    pos, n = 0, len(text)
    while pos < n:
        fields = []
        for _ in range(ncols - 1):
            j = text.find(field, pos)
            if j < 0:
                sys.exit(f"{filename}: ran out of fields for `{table}` after {len(fields)} of "
                         f"{ncols} -- upstream layout changed")
            fields.append(text[pos:j])
            pos = j + len(field)
        j = text.find(row, pos)
        if j < 0:
            j = n
        fields.append(text[pos:j])
        pos = j + len(row)
        yield fields


def escape(value):
    return (value.replace("\\", "\\\\").replace("\t", "\\t")
            .replace("\n", "\\n").replace("\r", "\\r"))


def tsv_value(value):
    """BULK INSERT's char format: an empty field is NULL, a single NUL byte is the empty string."""
    if value == "\x00":
        return ""
    if value == "":
        return "\\N"
    return escape(value)
