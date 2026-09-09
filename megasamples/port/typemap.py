"""The one type-mapping table: how a MySQL column is declared in PostgreSQL and in SQLite.

Rules, and the reasons they are what they are (knowledge/decisions/engine-hub.md):

* Unsigned integers take the next wider signed type, so every MySQL value fits.
* `tinyint(1)` stays an integer: no boolean is inferred from a display width.
* Enum becomes text with a CHECK on its members; set becomes text (the comma-joined literal MySQL
  renders, which is also what the canonical digest sees).
* Decimals keep their precision and scale. SQLite has no decimal type: the declaration is kept for
  affinity and the digest re-renders the value at the declared scale.
* datetime and timestamp become `timestamp` without time zone (the dump and the digest are both
  rendered in UTC); SQLite stores the ISO-8601 text.
* Binary and blob kinds become bytea / BLOB; geometry is stored as its WKB bytes.
* JSON becomes PostgreSQL `json`, not `jsonb`, so the text is preserved as MySQL rendered it.

Anything not in the table raises, because a silent guess is the one kind of mapping error that
does not show up until someone's query is wrong.
"""

INT_PG = {  # data_type -> (signed, unsigned)
    "tinyint": ("smallint", "smallint"),
    "smallint": ("smallint", "integer"),
    "mediumint": ("integer", "integer"),
    "int": ("integer", "bigint"),
    "bigint": ("bigint", "numeric(20,0)"),
}
INT_SQLITE = {"tinyint": "TINYINT", "smallint": "SMALLINT", "mediumint": "MEDIUMINT", "int": "INTEGER", "bigint": "BIGINT"}
TEXT_KINDS = {"tinytext", "text", "mediumtext", "longtext"}
BLOB_KINDS = {"tinyblob", "blob", "mediumblob", "longblob", "binary", "varbinary"}
GEOMETRY_KINDS = {"geometry", "point", "linestring", "polygon", "multipoint", "multilinestring",
                  "multipolygon", "geometrycollection"}


class Unmapped(Exception):
    pass


def postgres(col):
    """The PostgreSQL declaration for a Column (type only; nullability and defaults are the emitter's)."""
    t = col.data_type
    if t in INT_PG:
        if col.auto_increment and col.unsigned and t == "bigint":
            # an identity column must be smallint, integer or bigint; a bigint unsigned key keeps
            # bigint (its values are far below 2^63) rather than the numeric(20,0) a plain unsigned
            # bigint gets
            return "bigint"
        return INT_PG[t][1 if col.unsigned else 0]
    if t == "decimal":
        return f"numeric({col.precision},{col.scale})"
    if t == "double":
        return "double precision"
    if t == "float":
        return "real"
    if t == "char":
        return f"character({col.char_len})"
    if t == "varchar":
        return f"character varying({col.char_len})"
    if t in TEXT_KINDS or t in ("enum", "set"):
        return "text"
    if t in BLOB_KINDS or t in GEOMETRY_KINDS:
        return "bytea"
    if t == "date":
        return "date"
    if t in ("datetime", "timestamp"):
        return f"timestamp({col.fsp}) without time zone" if col.fsp else "timestamp(0) without time zone"
    if t == "time":
        return f"time({col.fsp}) without time zone" if col.fsp else "time(0) without time zone"
    if t == "year":
        return "smallint"
    if t == "json":
        return "json"
    if t == "bit":
        return f"bit({col.precision or 1})"
    raise Unmapped(f"no PostgreSQL mapping for {col.column_type} ({col.name})")


def sqlite(col):
    """The SQLite declaration: MySQL-like names, chosen for the affinity SQLite derives from them."""
    t = col.data_type
    if t in INT_SQLITE:
        return INT_SQLITE[t]
    if t == "decimal":
        return f"DECIMAL({col.precision},{col.scale})"
    if t == "double":
        return "DOUBLE"
    if t == "float":
        return "FLOAT"
    if t == "char":
        return f"CHAR({col.char_len})"
    if t == "varchar":
        return f"VARCHAR({col.char_len})"
    if t in TEXT_KINDS or t in ("enum", "set", "json"):
        return "TEXT"
    if t in BLOB_KINDS or t in GEOMETRY_KINDS:
        return "BLOB"
    if t == "date":
        return "DATE"
    if t in ("datetime", "timestamp"):
        return "DATETIME"
    if t == "time":
        return "TIME"
    if t == "year":
        return "SMALLINT"
    if t == "bit":
        return "BLOB"
    raise Unmapped(f"no SQLite mapping for {col.column_type} ({col.name})")


def is_binary(col):
    return col.data_type in BLOB_KINDS or col.data_type in GEOMETRY_KINDS or col.data_type == "bit"


def is_textual(col):
    return col.data_type in TEXT_KINDS or col.data_type in ("char", "varchar", "enum", "set", "json")
