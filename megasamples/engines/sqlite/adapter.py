"""The verification adapter for SQLite: the file is opened with the stdlib driver, and the
canonical digest is rendered in Python from the MySQL types the port's model.json records."""
import decimal, json, os, sqlite3

from megasamples import canon, datasets as inventory
from megasamples.paths import engine_build_dir
from megasamples.port import typemap
from megasamples.port.ddl import fulltext_table_name, physical_index_name


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
    exact_decimals = False

    def __init__(self, dataset):
        base = os.path.join(engine_build_dir("sqlite"), inventory.load(dataset)["database"])
        self.path = os.path.join(base, f"{inventory.load(dataset)['database']}.sqlite")
        if not os.path.exists(self.path):
            raise SystemExit(f"{dataset}: no SQLite port at {self.path}; run: megasamples sqlite-port {dataset}")
        with open(os.path.join(base, "model.json"), encoding="utf-8") as fh:
            self.model = json.load(fh)
        self.tables_by_name = {t["name"]: t for t in self.model["tables"]}
        self.view_types = {v["name"]: v["columns"] for v in self.model.get("views", [])}
        self.ported_views = set(self.model.get("ported_views", []))
        self.logical = {physical_index_name(t["name"], i["name"]): i["name"]
                        for t in self.model["tables"] for i in t["indexes"] if not i["primary"]}
        self.ported_triggers = set(self.model.get("ported_triggers", []))
        self.fulltext = {fulltext_table_name(t["name"], i["name"]): (t["name"], i["name"])
                         for t in self.model["tables"] for i in t["indexes"] if i["type"] == "FULLTEXT"}
        self.con = sqlite3.connect(self.path)
        self.con.execute("PRAGMA foreign_keys=ON")
        self.names = None

    def supports(self, stage):
        return stage in ("counts", "digests", "fks", "indexes", "views", "triggers")

    def tables(self, schema):
        """The base tables: not the FTS5 tables of the FULLTEXT indexes, nor their shadow tables."""
        shadows = {f"{fts}_{suffix}" for fts in self.fulltext for suffix in ("data", "idx", "docsize", "config", "content")}
        return [r[0] for r in self.con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
            "AND sql NOT LIKE 'CREATE VIRTUAL TABLE%' ORDER BY name") if r[0] not in shadows]

    # --- triggers ---------------------------------------------------------------------------------
    def routines_not_ported(self, schema):
        return {r["name"] for r in self.model.get("routines", [])}

    def triggers_not_ported(self, schema):
        return {t["name"] for t in self.model.get("triggers", [])} - self.ported_triggers

    def translate(self, sql):
        from megasamples.port import sqltranslate
        if self.names is None:
            self.names = sqltranslate.names_of(self.model)
        return sqltranslate.translate(sql, "sqlite", self.model["name"], names=self.names)

    def run_scenario(self, schema, case):
        """The scenario's statements and probe, translated to SQLite, inside a rolled-back transaction."""
        from megasamples import probe
        con = sqlite3.connect(self.path, isolation_level=None)
        con.execute("PRAGMA foreign_keys=ON")
        con.execute("BEGIN")
        try:
            for st in case["statements"]:
                con.execute(self.translate(st))
            rows = con.execute(self.translate(case["probe"])).fetchall()
        except sqlite3.Error as exc:
            con.execute("ROLLBACK"); con.close()
            if case.get("error"):
                return ["ERROR"]
            raise RuntimeError(f"scenario {case['name']} failed on SQLite: {exc}") from None
        con.execute("ROLLBACK"); con.close()
        if case.get("error"):
            raise RuntimeError(f"scenario {case['name']} was expected to fail on SQLite and did not")
        return probe.lines(probe.rows_text(rows))

    def columns(self, schema, table):
        return [(c["name"], c["data_type"]) for c in self.tables_by_name[table]["columns"]]

    def count(self, schema, table):
        return self.con.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0]

    def views(self, schema):
        return sorted(self.ported_views)

    def view_columns(self, schema, view):
        return [(c[0], c[1]) for c in self.view_types.get(view, [])]

    def view_has_unordered_aggregate(self, schema, view):
        from megasamples.engines.mysql.adapter import has_unordered_group_concat
        v = next((v for v in self.model.get("views", []) if v["name"] == view), None)
        return bool(v) and has_unordered_group_concat(v["definition"])

    def views_not_ported(self, schema):
        return set(self.view_types) - self.ported_views

    def fingerprint(self, schema, table, cols):
        if table in self.view_types:
            meta = {c[0]: {"scale": c[3]} for c in self.view_types[table]}
        else:
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
        for fts, (table, index) in self.fulltext.items():          # a FULLTEXT index became an FTS5 table
            if self.con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", (fts,)).fetchone()[0]:
                cols = [r[1] for r in self.con.execute(f'PRAGMA table_info("{fts}")')]
                out.setdefault(table, {})[index] = {"unique": False, "type": "FULLTEXT", "columns": cols}
        return out

    def carries_index(self, spec):
        return spec.get("type") in ("BTREE", "FULLTEXT")

    def explain_json(self, schema, query):
        raise NotImplementedError

    def query_text(self, schema, query):
        raise NotImplementedError
