"""Read a loaded MySQL database back as an engine-neutral table model.

Everything comes from information_schema on the build server, not from parsing SHOW CREATE TABLE:
columns in ordinal order with their types, nullability, defaults and generated expressions; every
index with its columns, uniqueness and type; foreign keys with their actions; check constraints.
Views, routines and triggers are listed by name only, so the catalogue can say what was not ported.
"""
from dataclasses import dataclass, field
import re

from megasamples.engines.mysql import server as db


@dataclass
class Column:
    name: str
    data_type: str            # information_schema DATA_TYPE: int, varchar, enum, ...
    column_type: str          # the full declaration: int unsigned, varchar(45), enum('a','b')
    nullable: bool
    default: str | None       # COLUMN_DEFAULT as MySQL reports it (a literal, or an expression)
    extra: str                # auto_increment, DEFAULT_GENERATED, STORED GENERATED, on update ...
    generation: str | None    # GENERATION_EXPRESSION for a generated column
    char_len: int | None
    precision: int | None
    scale: int | None
    fsp: int | None           # fractional seconds for datetime/time/timestamp
    charset: str | None
    collation: str | None
    ordinal: int

    @property
    def unsigned(self):
        return "unsigned" in self.column_type

    @property
    def auto_increment(self):
        return "auto_increment" in self.extra

    @property
    def generated(self):
        return "GENERATED" in self.extra and "DEFAULT_GENERATED" not in self.extra

    @property
    def default_is_expression(self):
        return "DEFAULT_GENERATED" in self.extra

    @property
    def on_update_now(self):
        return "on update CURRENT_TIMESTAMP" in self.extra

    @property
    def enum_values(self):
        """The members of an enum or set, unescaped."""
        m = re.match(r"^(enum|set)\((.*)\)$", self.column_type, re.S)
        if not m:
            return []
        return [v.replace("''", "'") for v in re.findall(r"'((?:[^']|'')*)'", m.group(2))]


@dataclass
class Index:
    name: str
    unique: bool
    type: str                 # BTREE, FULLTEXT, SPATIAL
    columns: list             # [(column, sub_part or None)]
    primary: bool = False


@dataclass
class ForeignKey:
    name: str
    columns: list
    ref_schema: str
    ref_table: str
    ref_columns: list
    on_update: str
    on_delete: str


@dataclass
class Check:
    name: str
    clause: str               # MySQL's rendering: backticked identifiers, _utf8mb4'x' literals


@dataclass
class Table:
    schema: str
    name: str
    columns: list = field(default_factory=list)
    indexes: list = field(default_factory=list)
    foreign_keys: list = field(default_factory=list)
    checks: list = field(default_factory=list)
    comment: str = ""

    @property
    def primary_key(self):
        for i in self.indexes:
            if i.primary:
                return i
        return None

    def column(self, name):
        for c in self.columns:
            if c.name == name:
                return c
        raise KeyError(f"{self.schema}.{self.name} has no column {name}")


@dataclass
class Database:
    name: str
    tables: list
    views: list
    routines: list
    triggers: list

    def table(self, name):
        for t in self.tables:
            if t.name == name:
                return t
        raise KeyError(f"{self.name} has no table {name}")


def _int(v):
    return int(v) if v not in (None, "", "NULL") else None


def _str(v):
    return None if v in (None, "NULL") else v


def extract(schema):
    """The model of one database on the build server."""
    tables = {}
    for (name, comment) in db.rows_escaped(
            "SELECT table_name, table_comment FROM information_schema.tables "
            f"WHERE table_schema='{schema}' AND table_type='BASE TABLE' ORDER BY table_name"):
        tables[name] = Table(schema, name, comment=comment or "")

    for r in db.rows_escaped(
            "SELECT table_name, column_name, data_type, column_type, is_nullable, column_default, extra, "
            "generation_expression, character_maximum_length, numeric_precision, numeric_scale, "
            "datetime_precision, character_set_name, collation_name, ordinal_position "
            "FROM information_schema.columns "
            f"WHERE table_schema='{schema}' ORDER BY table_name, ordinal_position"):
        if r[0] not in tables:
            continue
        tables[r[0]].columns.append(Column(
            name=r[1], data_type=r[2], column_type=r[3], nullable=(r[4] == "YES"),
            default=_str(r[5]), extra=r[6] or "", generation=_str(r[7]) or None,
            char_len=_int(r[8]), precision=_int(r[9]), scale=_int(r[10]), fsp=_int(r[11]),
            charset=_str(r[12]), collation=_str(r[13]), ordinal=int(r[14])))

    current = {}
    for r in db.rows(
            "SELECT table_name, index_name, non_unique, index_type, column_name, sub_part, seq_in_index "
            "FROM information_schema.statistics "
            f"WHERE table_schema='{schema}' ORDER BY table_name, index_name, seq_in_index"):
        if r[0] not in tables:
            continue
        key = (r[0], r[1])
        if key not in current:
            current[key] = Index(name=r[1], unique=(r[2] == "0"), type=r[3], columns=[],
                                 primary=(r[1] == "PRIMARY"))
            tables[r[0]].indexes.append(current[key])
        current[key].columns.append((r[4], _int(r[5])))

    fks = {}
    for r in db.rows(
            "SELECT rc.table_name, rc.constraint_name, kcu.column_name, kcu.referenced_table_schema, "
            "rc.referenced_table_name, kcu.referenced_column_name, rc.update_rule, rc.delete_rule "
            "FROM information_schema.referential_constraints rc "
            "JOIN information_schema.key_column_usage kcu ON kcu.constraint_schema=rc.constraint_schema "
            "AND kcu.constraint_name=rc.constraint_name AND kcu.table_name=rc.table_name "
            f"WHERE rc.constraint_schema='{schema}' ORDER BY rc.table_name, rc.constraint_name, kcu.ordinal_position"):
        if r[0] not in tables:
            continue
        key = (r[0], r[1])
        if key not in fks:
            fks[key] = ForeignKey(name=r[1], columns=[], ref_schema=r[3], ref_table=r[4],
                                  ref_columns=[], on_update=r[6], on_delete=r[7])
            tables[r[0]].foreign_keys.append(fks[key])
        fks[key].columns.append(r[2])
        fks[key].ref_columns.append(r[5])

    for r in db.rows_escaped(
            "SELECT tc.table_name, cc.constraint_name, cc.check_clause "
            "FROM information_schema.check_constraints cc "
            "JOIN information_schema.table_constraints tc ON tc.constraint_schema=cc.constraint_schema "
            "AND tc.constraint_name=cc.constraint_name AND tc.constraint_type='CHECK' "
            f"WHERE cc.constraint_schema='{schema}' ORDER BY tc.table_name, cc.constraint_name"):
        if r[0] in tables:
            tables[r[0]].checks.append(Check(name=r[1], clause=r[2]))

    views = [r[0] for r in db.rows(
        f"SELECT table_name FROM information_schema.views WHERE table_schema='{schema}' ORDER BY table_name")]
    routines = [f"{r[1].lower()} {r[0]}" for r in db.rows(
        "SELECT routine_name, routine_type FROM information_schema.routines "
        f"WHERE routine_schema='{schema}' ORDER BY routine_name")]
    triggers = [r[0] for r in db.rows(
        f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_schema='{schema}' ORDER BY trigger_name")]
    return Database(schema, list(tables.values()), views, routines, triggers)


def load_order(database):
    """Tables with their foreign-key targets first, so constraints can be created as tables are.

    Cycles and self-references are broken by falling back to name order; foreign keys are created
    after all data is loaded anyway (ARCHITECTURE.md section 4), so this only helps readability.
    """
    names = [t.name for t in database.tables]
    deps = {t.name: {fk.ref_table for fk in t.foreign_keys if fk.ref_schema == database.name and fk.ref_table != t.name}
            for t in database.tables}
    out, seen = [], set()

    def place(n, stack=()):
        if n in seen or n in stack:
            return
        for d in sorted(deps.get(n, ())):
            if d in deps:
                place(d, stack + (n,))
        if n not in seen:
            seen.add(n)
            out.append(n)

    for n in names:
        place(n)
    return [database.table(n) for n in out]
