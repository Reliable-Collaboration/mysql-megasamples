"""The verification adapter for PostgreSQL.

Counts, foreign keys and indexes are read from the ported database itself; the canonical digest is
computed in Python from a `COPY ... TO STDOUT` of each table rendered column by column in the
canonical text form (megasamples/canon.py), because PostgreSQL text cannot hold the U+0000 NULL
sentinel the SQL form uses. The MySQL types every column had come from the port's model.json, so the
same digest rules apply to the same columns.
"""
import json, os

from megasamples import canon
from megasamples.engines.postgres import server as pg
from megasamples.paths import engine_build_dir
from megasamples.port import typemap
from megasamples.port.ddl import physical_index_name

PG_UNESCAPE = {b"\\": b"\\", b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b", b"f": b"\f", b"v": b"\v"}


def canonical_expr(name, mysql_type):
    q = '"' + name + '"'
    t = mysql_type.lower()
    if t in ("datetime", "timestamp"):
        return f"to_char({q}, 'YYYY-MM-DD HH24:MI:SS.US')"
    if t == "time":
        return f"to_char({q}::interval, 'HH24:MI:SS.US')"
    if t in typemap.BLOB_KINDS or t in typemap.GEOMETRY_KINDS or t == "bit":
        return f"encode({q}, 'hex')"
    if t == "char":
        return f"rtrim({q})"
    return f"{q}::text"


def unescape_field(field):
    if field == b"\\N":
        return None
    if b"\\" not in field:
        return field.decode("utf-8")
    out, i, n = bytearray(), 0, len(field)
    while i < n:
        c = field[i:i + 1]
        if c == b"\\" and i + 1 < n:
            out += PG_UNESCAPE.get(field[i + 1:i + 2], field[i + 1:i + 2])
            i += 2
        else:
            out += c
            i += 1
    return out.decode("utf-8")


class PostgresAdapter:
    name = "postgres"

    def __init__(self, dataset):
        path = os.path.join(engine_build_dir("postgres"), dataset, "model.json")
        if not os.path.exists(path):
            raise SystemExit(f"{dataset}: no PostgreSQL port under build/postgres/; run: megasamples pg-port {dataset}")
        with open(path, encoding="utf-8") as fh:
            self.model = json.load(fh)
        self.types = {t["name"]: {c["name"]: c["data_type"] for c in t["columns"]} for t in self.model["tables"]}
        self.logical = {physical_index_name(t["name"], i["name"]): i["name"]
                        for t in self.model["tables"] for i in t["indexes"] if not i["primary"]}

    def supports(self, stage):
        return stage in ("counts", "digests", "fks", "indexes")

    def tables(self, schema):
        return [r[0] for r in pg.rows(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public' "
            "AND table_type='BASE TABLE' ORDER BY table_name", schema)]

    def columns(self, schema, table):
        types = self.types.get(table, {})
        return [(c["name"], types[c["name"]]) for t in self.model["tables"] if t["name"] == table for c in t["columns"]]

    def count(self, schema, table):
        return int(pg.rows(f'SELECT count(*) FROM "{table}"', schema)[0][0])

    def fingerprint(self, schema, table, cols):
        kept = [(c, t) for c, t in cols if t.lower() not in canon.EXCLUDED]
        exprs = ", ".join(canonical_expr(c, t) for c, t in kept) or "1"
        data = pg.copy_out(f'SELECT {exprs} FROM "{table}"', schema)
        digests = []
        for line in data.split(b"\n"):
            if not line:
                continue
            values = [unescape_field(f) for f in line.split(b"\t")] if kept else []
            digests.append(canon.row_digest(values))
        f = canon.fold(digests)
        return f["n"], f["x"], f["s"]

    def foreign_keys(self, schema):
        return [(r[0], r[1], r[2], schema, r[3], r[4]) for r in pg.rows(
            "SELECT con.conname, rel.relname, att.attname, frel.relname, fatt.attname "
            "FROM pg_constraint con JOIN pg_class rel ON rel.oid = con.conrelid "
            "JOIN pg_class frel ON frel.oid = con.confrelid "
            "JOIN LATERAL unnest(con.conkey, con.confkey) AS k(a, f) ON true "
            "JOIN pg_attribute att ON att.attrelid = con.conrelid AND att.attnum = k.a "
            "JOIN pg_attribute fatt ON fatt.attrelid = con.confrelid AND fatt.attnum = k.f "
            "WHERE con.contype = 'f' AND rel.relnamespace = 'public'::regnamespace ORDER BY 1, 3", schema)]

    def orphans(self, schema, table, col, rschema, rtable, rcol):
        return int(pg.rows(
            f'SELECT count(*) FROM "{table}" c LEFT JOIN "{rtable}" p ON c."{col}" = p."{rcol}" '
            f'WHERE c."{col}" IS NOT NULL AND p."{rcol}" IS NULL', schema)[0][0])

    def indexes(self, schema):
        """Indexes by MySQL's names: the `<table>_` prefix stripped, the primary key as PRIMARY."""
        out = {}
        for table, index, unique, primary, cols in pg.rows(
                "SELECT t.relname, i.relname, ix.indisunique, ix.indisprimary, "
                "string_agg(a.attname, ',' ORDER BY k.ord) "
                "FROM pg_index ix JOIN pg_class t ON t.oid = ix.indrelid JOIN pg_class i ON i.oid = ix.indexrelid "
                "JOIN LATERAL unnest(ix.indkey) WITH ORDINALITY AS k(attnum, ord) ON true "
                "JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = k.attnum "
                "WHERE t.relnamespace = 'public'::regnamespace AND t.relkind = 'r' "
                "GROUP BY t.relname, i.relname, ix.indisunique, ix.indisprimary ORDER BY 1, 2", schema):
            name = "PRIMARY" if primary == "t" else self.logical.get(index, index)
            out.setdefault(table, {})[name] = {"unique": unique == "t", "type": "BTREE", "columns": cols.split(",")}
        return out

    def carries_index(self, spec):
        return spec.get("type") == "BTREE"

    def explain_json(self, schema, query):
        raise NotImplementedError

    def query_text(self, schema, query):
        raise NotImplementedError
