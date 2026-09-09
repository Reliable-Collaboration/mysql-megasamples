"""Read the MySQL Shell dump's TSV chunks, and write them again in another engine's text format.

A dump directory (build/mysql/dumps/<dataset>/) holds, per table, `<schema>@<table>.json` with the
column order and the decode directives, and `<schema>@<table>@@N.tsv.zst` chunks. The chunks use
MySQL's LOAD DATA text format: tab-separated fields, newline-terminated rows, backslash escapes
(`\\N` is NULL; `\\t`, `\\n`, `\\r`, `\\\\`, `\\0`, `\\b`, `\\Z` are the characters), and binary columns
carried as base64 (`decodeColumns: {col: FROM_BASE64}`). The dump is taken with `tzUtc`, so every
timestamp is UTC text.

`rows()` yields each row as a list: `None` for NULL, `bytes` for a base64 column, `str` otherwise.
`postgres_line()` renders one row in PostgreSQL COPY text format; a row that carries no escape and no
binary column passes through unchanged, which is most of them.
"""
import base64, glob, json, os, re

from compression import zstd

UNESCAPE = {b"0": b"\x00", b"b": b"\b", b"n": b"\n", b"r": b"\r", b"t": b"\t", b"Z": b"\x1a", b"\\": b"\\"}


class TableDump:
    def __init__(self, dump_dir, schema, table):
        base = os.path.join(dump_dir, f"{schema}@{table}")
        with open(base + ".json", encoding="utf-8") as fh:
            meta = json.load(fh)
        opts = meta["options"]
        self.schema, self.table = schema, table
        self.columns = list(opts["columns"])
        self.base64 = {c for c, how in (opts.get("decodeColumns") or {}).items() if how == "FROM_BASE64"}
        assert opts.get("fieldsTerminatedBy", "\t") == "\t" and opts.get("linesTerminatedBy", "\n") == "\n"
        assert opts.get("fieldsEscapedBy", "\\") == "\\" and not opts.get("fieldsEnclosedBy")
        # a chunk is `<base>@@N.tsv.zst`; a table the dumper could not chunk by key (no primary or
        # unique key) gets `<base>@N.tsv.zst` as well -- both forms carry rows and both are read
        found = {}
        for path in glob.glob(base + "@*.tsv.zst"):
            m = re.match(r"^" + re.escape(base) + r"@@?(\d+)\.tsv\.zst$", path)
            if m:
                found[(int(m.group(1)), path)] = path
        self.chunks = [found[k] for k in sorted(found)]
        self.binary_index = [i for i, c in enumerate(self.columns) if c in self.base64]

    def lines(self):
        """Raw lines (bytes, without the newline) across every chunk, in order."""
        for chunk in self.chunks:
            with open(chunk, "rb") as fh:
                data = zstd.decompress(fh.read())
            for line in data.split(b"\n"):
                if line:
                    yield line

    def rows(self):
        for line in self.lines():
            yield decode_line(line, self.binary_index)


def unescape(field):
    """One field's bytes with MySQL's backslash escapes resolved; None for `\\N`."""
    if field == b"\\N":
        return None
    if b"\\" not in field:
        return field
    out = bytearray()
    i, n = 0, len(field)
    while i < n:
        c = field[i:i + 1]
        if c == b"\\" and i + 1 < n:
            nxt = field[i + 1:i + 2]
            out += UNESCAPE.get(nxt, nxt)
            i += 2
        else:
            out += c
            i += 1
    return bytes(out)


def decode_line(line, binary_index=()):
    fields = line.split(b"\t")
    row = []
    for i, f in enumerate(fields):
        v = unescape(f)
        if v is None:
            row.append(None)
        elif i in binary_index:
            row.append(base64.b64decode(v))
        else:
            row.append(v.decode("utf-8"))
    return row


PG_ESCAPE = {"\\": "\\\\", "\t": "\\t", "\n": "\\n", "\r": "\\r", "\b": "\\b", "\f": "\\f", "\v": "\\v"}


def postgres_field(value):
    if value is None:
        return "\\N"
    if isinstance(value, bytes):
        return "\\\\x" + value.hex()              # bytea input `\x..`, with COPY's own backslash doubled
    if any(ch in value for ch in PG_ESCAPE):
        return "".join(PG_ESCAPE.get(ch, ch) for ch in value)
    return value


def postgres_line(line, binary_index=()):
    """A dump line rendered for PostgreSQL COPY (FORMAT text), as bytes without the newline."""
    if b"\\" not in line and not binary_index:
        return line                                # nothing to translate: same tabs, same text
    row = decode_line(line, binary_index)
    return "\t".join(postgres_field(v) for v in row).encode("utf-8")


def write_postgres(dump, out_path, strip_srid=()):
    """Write a table's rows in COPY text format. Returns the row count.

    `strip_srid` names the geometry columns (by index): MySQL's dump carries its internal form, four
    bytes of SRID before the WKB, and only the WKB is stored."""
    n = 0
    strip_srid = set(strip_srid)
    with open(out_path, "wb") as fh:
        for line in dump.lines():
            if strip_srid:
                row = decode_line(line, dump.binary_index)
                for i in strip_srid:
                    if isinstance(row[i], bytes):
                        row[i] = row[i][4:]
                fh.write("\t".join(postgres_field(v) for v in row).encode("utf-8"))
            else:
                fh.write(postgres_line(line, dump.binary_index))
            fh.write(b"\n")
            n += 1
    return n
