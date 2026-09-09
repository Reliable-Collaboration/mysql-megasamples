"""The verification adapter for SQLite: the file is opened with the stdlib driver, and the
canonical digest is rendered in Python from the MySQL types the port's model.json records."""
import decimal, json, os, sqlite3

from megasamples import canon, datasets as inventory
from megasamples.paths import engine_build_dir
from megasamples.port import typemap
from megasamples.port.ddl import physical_index_name


def pad_fraction(text):
    """MySQL renders date-times with six fractional digits; the file holds what the dump wrote."""
    if "." in text:
        head, frac = text.split(".", 1)
        return f"{head}.{frac.ljust(6, '0')}"
    return text + ".000000"


def canonical(value, mysql_type, scale):
    if value is None:
        return None
    t = mysql_type.lower()
    if isinstance(value, bytes):
        return value.hex()
    if t == "decimal":
        d = decimal.Decimal(str(value))
        return str(d.quantize(decimal.Decimal(1).scaleb(-(scale or 0))))
    if t in typemap.INT_PG or t == "year":
        return str(int(value))
    if t in ("datetime", "timestamp", "time"):
        return pad_fraction(str(value))
    if t == "char":
        return str(value).rstrip(" ")
    return str(value)


class SQLiteAdapter:
    name = "sqlite"

    def __init__(self, dataset):
        base = os.path.join(engine_build_dir("sqlite"), dataset)
        self.path = os.path.join(base, f"{inventory.load(dataset)['database']}.sqlite")
        if not os.path.exists(self.path):
            raise SystemExit(f"{dataset}: no SQLite port at {self.path}; run: megasamples sqlite-port {dataset}")
        with open(os.path.join(base, "model.json"), encoding="utf-8") as fh:
            self.model = json.load(fh)
        self.tables_by_name = {t["name"]: t for t in self.model["tables"]}
        self.logical = {physical_index_name(t["name"], i["name"]): i["name"]
                        for t in self.model["tables"] for i in t["indexes"] if not i["primary"]}
        self.con = sqlite3.connect(self.path)

    def supports(self, stage):
        return stage in ("counts", "digests", "fks", "indexes")

    def tables(self, schema):
        return [r[0] for r in self.con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]

    def columns(self, schema, table):
        return [(c["name"], c["data_type"]) for c in self.tables_by_name[table]["columns"]]

    def count(self, schema, table):
        return self.con.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0]

    def fingerprint(self, schema, table, cols):
        meta = {c["name"]: c for c in self.tables_by_name[table]["columns"]}
        kept = [(c, t) for c, t in cols if t.lower() not in canon.EXCLUDED]
        digests = []
        if kept:
            names = ", ".join(f'"{c}"' for c, _ in kept)
            for row in self.con.execute(f'SELECT {names} FROM "{table}"'):
                digests.append(canon.row_digest([canonical(v, t, meta[c].get("scale")) for v, (c, t) in zip(row, kept)]))
        else:
            digests = [canon.row_digest([]) for _ in range(self.count(schema, table))]
        f = canon.fold(digests)
        return f["n"], f["x"], f["s"]

    def foreign_keys(self, schema):
        out = []
        for t in self.model["tables"]:
            for fk in t["foreign_keys"]:
                if fk["ref_schema"] != schema:
                    continue                       # dropped by the port: another database
                for col, rcol in zip(fk["columns"], fk["ref_columns"]):
                    out.append((fk["name"], t["name"], col, schema, fk["ref_table"], rcol))
        return out

    def orphans(self, schema, table, col, rschema, rtable, rcol):
        return self.con.execute(
            f'SELECT count(*) FROM "{table}" c LEFT JOIN "{rtable}" p ON c."{col}" = p."{rcol}" '
            f'WHERE c."{col}" IS NOT NULL AND p."{rcol}" IS NULL').fetchone()[0]

    def indexes(self, schema):
        out = {}
        for table in self.tables(schema):
            pk = [r[1] for r in sorted(self.con.execute(f'PRAGMA table_info("{table}")'), key=lambda r: r[5]) if r[5]]
            idx = {}
            if pk:
                idx["PRIMARY"] = {"unique": True, "type": "BTREE", "columns": pk}
            for _, name, unique, origin, _partial in self.con.execute(f'PRAGMA index_list("{table}")'):
                if origin == "pk":
                    continue
                cols = [r[2] for r in sorted(self.con.execute(f'PRAGMA index_info("{name}")'), key=lambda r: r[0])]
                short = self.logical.get(name, name)
                idx[short] = {"unique": bool(unique), "type": "BTREE", "columns": cols}
            out[table] = idx
        return out

    def carries_index(self, spec):
        return spec.get("type") == "BTREE"

    def explain_json(self, schema, query):
        raise NotImplementedError

    def query_text(self, schema, query):
        raise NotImplementedError
