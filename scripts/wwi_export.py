#!/usr/bin/env python3
"""Open the WideWorldImporters backups in SQL Server once, and export everything MySQL will need.

  MEGASAMPLES_ACCEPT_MSSQL_EULA=1 python3 scripts/wwi_export.py

This is the only step in the project that runs proprietary software, and it runs it once: the two
`.bak` files are restored, the catalogue and the data are written to `downloads/<dataset>/export/`,
and the container is deleted. Everything after this point reads the export, so a rebuild -- and
anyone who takes the published export -- never needs SQL Server at all. The EULA gate lives in
scripts/mssql.py.

The export format is deliberately boring, because `bcp` never quotes and never escapes:

  field terminator  0x1f    row terminator  0x1e 0x0a    NULL  0x00    value  0x01 then the text

Those are not arbitrary. 0x1f and 0x1e are the ASCII unit and record separators, which no WWI value
contains -- and rather than trust that, the converter re-counts the fields in every row, so a value
that did contain one would be caught instead of silently splitting a row. The tag byte is what makes
NULL distinguishable from an empty string, which `bcp -c` alone does not (it writes both as nothing),
and tagging *values* rather than only NULLs is what makes it safe against data that is itself a NUL
-- which this database has.

Every value is rendered to text by an explicit expression per type (`render()`), and the same
expression feeds the row export and the per-column baseline aggregates, so the two cannot disagree
about what a value is.
"""
import argparse, json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import mssql  # noqa: E402

DATABASES = [
    # (SQL Server database, .bak under downloads/, dataset directory)
    ("WideWorldImporters", "wideworldimporters/WideWorldImporters-Standard.bak",
     "wideworldimporters"),
    ("WideWorldImportersDW", "wideworldimporters_dw/WideWorldImportersDW-Standard.bak",
     "wideworldimporters_dw"),
]

# How each SQL Server type becomes text. `{c}` is the bracketed column reference.
#   datetime2 style 121 gives all 7 fractional digits ("2013-01-01 00:00:00.0000000"), which is more
#     precision than MySQL DATETIME(6) can hold; the converter truncates and says so.
#   varbinary style 2 is hex without the 0x prefix, lower-cased to match MySQL's HEX() in canon.py.
#   geography goes out as WKT; MySQL reads it back with ST_GeomFromText(..., 4326, 'axis-order=long-lat').
RENDER = {
    "int": "CONVERT(NVARCHAR(20),{c})", "bigint": "CONVERT(NVARCHAR(24),{c})",
    "smallint": "CONVERT(NVARCHAR(10),{c})", "tinyint": "CONVERT(NVARCHAR(5),{c})",
    "bit": "CONVERT(NVARCHAR(1),CONVERT(TINYINT,{c}))",
    "decimal": "CONVERT(NVARCHAR(45),{c})", "numeric": "CONVERT(NVARCHAR(45),{c})",
    "money": "CONVERT(NVARCHAR(45),{c})", "smallmoney": "CONVERT(NVARCHAR(45),{c})",
    "float": "CONVERT(NVARCHAR(35),{c},3)", "real": "CONVERT(NVARCHAR(35),{c},3)",
    "date": "CONVERT(NVARCHAR(10),{c},23)",
    "datetime2": "CONVERT(NVARCHAR(27),{c},121)", "datetime": "CONVERT(NVARCHAR(23),{c},121)",
    "smalldatetime": "CONVERT(NVARCHAR(23),{c},121)", "time": "CONVERT(NVARCHAR(16),{c},114)",
    "datetimeoffset": "CONVERT(NVARCHAR(34),{c},127)",
    "nvarchar": "{c}", "varchar": "{c}", "nchar": "{c}", "char": "{c}", "sysname": "{c}",
    "ntext": "CONVERT(NVARCHAR(MAX),{c})", "text": "CONVERT(NVARCHAR(MAX),{c})",
    "xml": "CONVERT(NVARCHAR(MAX),{c})",
    "varbinary": "LOWER(CONVERT(NVARCHAR(MAX),{c},2))",
    "binary": "LOWER(CONVERT(NVARCHAR(MAX),{c},2))",
    "image": "LOWER(CONVERT(NVARCHAR(MAX),{c},2))",
    "uniqueidentifier": "LOWER(CONVERT(NVARCHAR(36),{c}))",
    "geography": "{c}.STAsText()", "geometry": "{c}.STAsText()",
    "hierarchyid": "{c}.ToString()",
}

META_SQL = """SET NOCOUNT ON;
SELECT CAST((SELECT
 (SELECT s.name AS [schema], t.name, t.temporal_type,
         OBJECT_SCHEMA_NAME(t.history_table_id) AS history_schema,
         OBJECT_NAME(t.history_table_id) AS history_table,
         CAST(ep.value AS NVARCHAR(MAX)) AS description
  FROM sys.tables t JOIN sys.schemas s ON s.schema_id=t.schema_id
  LEFT JOIN sys.extended_properties ep ON ep.class=1 AND ep.major_id=t.object_id
       AND ep.minor_id=0 AND ep.name='Description'
  ORDER BY s.name, t.name FOR JSON PATH) AS [tables],
 (SELECT s.name AS [schema], t.name AS [table], c.column_id, c.name, ty.name AS type,
         c.max_length, c.precision, c.scale, c.is_nullable, c.is_identity, c.is_computed,
         c.generated_always_type, c.collation_name, cc.definition AS computed, cc.is_persisted,
         dc.definition AS [default], CAST(ep.value AS NVARCHAR(MAX)) AS description
  FROM sys.columns c JOIN sys.tables t ON t.object_id=c.object_id
  JOIN sys.schemas s ON s.schema_id=t.schema_id
  JOIN sys.types ty ON ty.user_type_id=c.user_type_id
  LEFT JOIN sys.computed_columns cc ON cc.object_id=c.object_id AND cc.column_id=c.column_id
  LEFT JOIN sys.default_constraints dc ON dc.object_id=c.default_object_id
  LEFT JOIN sys.extended_properties ep ON ep.class=1 AND ep.major_id=c.object_id
       AND ep.minor_id=c.column_id AND ep.name='Description'
  ORDER BY s.name, t.name, c.column_id FOR JSON PATH) AS [columns],
 (SELECT s.name AS [schema], t.name AS [table], i.name AS [index], i.is_primary_key, i.is_unique,
         i.is_unique_constraint, i.type_desc, i.filter_definition, ic.key_ordinal,
         ic.index_column_id, ic.is_descending_key, ic.is_included_column, c.name AS [column]
  FROM sys.indexes i JOIN sys.tables t ON t.object_id=i.object_id
  JOIN sys.schemas s ON s.schema_id=t.schema_id
  JOIN sys.index_columns ic ON ic.object_id=i.object_id AND ic.index_id=i.index_id
  JOIN sys.columns c ON c.object_id=ic.object_id AND c.column_id=ic.column_id
  WHERE i.type <> 0
  ORDER BY s.name, t.name, i.name, ic.is_included_column, ic.key_ordinal, ic.index_column_id
  FOR JSON PATH) AS [indexes],
 (SELECT fk.name, sp.name AS [schema], tp.name AS [table], cp.name AS [column],
         sr.name AS ref_schema, tr.name AS ref_table, cr.name AS ref_column,
         fk.delete_referential_action_desc AS on_delete,
         fk.update_referential_action_desc AS on_update, fkc.constraint_column_id
  FROM sys.foreign_keys fk
  JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id=fk.object_id
  JOIN sys.tables tp ON tp.object_id=fk.parent_object_id
  JOIN sys.schemas sp ON sp.schema_id=tp.schema_id
  JOIN sys.columns cp ON cp.object_id=fkc.parent_object_id AND cp.column_id=fkc.parent_column_id
  JOIN sys.tables tr ON tr.object_id=fk.referenced_object_id
  JOIN sys.schemas sr ON sr.schema_id=tr.schema_id
  JOIN sys.columns cr ON cr.object_id=fkc.referenced_object_id
       AND cr.column_id=fkc.referenced_column_id
  ORDER BY fk.name, fkc.constraint_column_id FOR JSON PATH) AS [fks],
 (SELECT cc.name, s.name AS [schema], t.name AS [table], cc.definition
  FROM sys.check_constraints cc JOIN sys.tables t ON t.object_id=cc.parent_object_id
  JOIN sys.schemas s ON s.schema_id=t.schema_id ORDER BY cc.name FOR JSON PATH) AS [checks],
 (SELECT s.name AS [schema], sq.name, CAST(sq.start_value AS BIGINT) AS start_value,
         CAST(sq.increment AS BIGINT) AS increment,
         CAST(sq.current_value AS BIGINT) AS current_value
  FROM sys.sequences sq JOIN sys.schemas s ON s.schema_id=sq.schema_id
  ORDER BY s.name, sq.name FOR JSON PATH) AS [sequences],
 (SELECT s.name AS [schema], o.name, o.type_desc,
         OBJECT_DEFINITION(o.object_id) AS definition
  FROM sys.objects o JOIN sys.schemas s ON s.schema_id=o.schema_id
  WHERE o.type IN ('P','FN','IF','TF','V','TR') AND o.is_ms_shipped=0
  ORDER BY o.type_desc, s.name, o.name FOR JSON PATH) AS [routines]
 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER) AS NVARCHAR(MAX))"""


def scalar(sql, database, out_root, inside):
    """Run a query returning one NVARCHAR(MAX) value and return it, via a temporary bcp file."""
    mssql.bcp(sql, database, f"{inside}/scalar.tmp")
    path = os.path.join(out_root, "scalar.tmp")
    raw = open(path, "rb").read()
    os.remove(path)
    return raw.rstrip(b"\x1e\n").decode("utf-8")


def render(col):
    """The text rendering of one column, used identically by the export and the baseline."""
    template = RENDER.get(col["type"])
    if template is None:
        sys.exit(f"no rendering for type {col['type']} "
                 f"({col['schema']}.{col['table']}.{col['name']})")
    return template.format(c=f"[{col['name']}]")


def exported(expr):
    """Every field is tagged: 0x00 alone means NULL, 0x01 introduces a value.

    A bare NUL for NULL is not enough, and the per-column baselines proved it: four of
    `Purchasing.Suppliers.DeliveryAddressLine1`'s thirteen rows hold a single NUL *as their value*,
    so a lone-NUL convention read four real values as NULL. Prefixing every non-null value with 0x01
    removes the ambiguity for any value at all, including that one. `+` yields NULL when either side
    is NULL, so the ISNULL still fires exactly on real NULLs."""
    return f"ISNULL(NCHAR(1)+{expr},NCHAR(0))"


# a LOB or a spatial value cannot be sorted on, and does not need to be: the columns that can are
# enough to fix the order
UNSORTABLE = {"nvarchar_max", "varbinary", "binary", "image", "text", "ntext", "xml",
              "geography", "geometry"}


def key_order(meta, schema, table, cols):
    """Column list to ORDER BY so that re-exporting produces the same bytes.

    The primary key when there is one. The 18 `_Archive` history tables have none -- SQL Server
    keeps history in a clustered index it manages -- so they fall back to every sortable column,
    which fixes the order just as well: two rows that tie on all of them are identical rows, and
    swapping identical rows does not change the file.
    """
    for idx in meta["indexes"]:
        if idx["schema"] == schema and idx["table"] == table and idx.get("is_primary_key") \
                and not idx.get("is_included_column"):
            keys = [i for i in meta["indexes"]
                    if i["schema"] == schema and i["table"] == table
                    and i["index"] == idx["index"] and not i.get("is_included_column")]
            return [c["column"] for c in sorted(keys, key=lambda c: c["key_ordinal"])]
    return [c["name"] for c in cols
            if not (c["type"] in UNSORTABLE
                    or (c["type"] in ("nvarchar", "varchar") and c["max_length"] == -1))]


def group_columns(meta):
    by_table = {}
    for c in meta["columns"]:
        by_table.setdefault((c["schema"], c["table"]), []).append(c)
    return by_table


def export_database(database, dataset, accepted_via):
    out_root = os.path.join(ROOT, "downloads", dataset, "export")
    data_dir = os.path.join(out_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    inside = f"/export/{dataset}"

    print(f"\n== {database}: catalogue")
    meta = json.loads(scalar(META_SQL, database, out_root, inside))
    meta["database"] = database
    for key in ("tables", "columns", "indexes", "fks", "checks", "sequences", "routines"):
        meta.setdefault(key, [])
    print(f"  . {len(meta['tables'])} tables, {len(meta['columns'])} columns, "
          f"{len({(i['schema'], i['table'], i['index']) for i in meta['indexes']})} indexes, "
          f"{len({f['name'] for f in meta['fks']})} foreign keys, "
          f"{len(meta['sequences'])} sequences, {len(meta['routines'])} programmable objects")

    by_table = group_columns(meta)
    baseline, total_rows = {}, 0
    print(f"== {database}: rows and per-column baselines")
    for schema, table in sorted(by_table):
        cols = sorted(by_table[(schema, table)], key=lambda c: c["column_id"])
        baseline[f"{schema}.{table}"] = table_baseline(database, schema, table, cols,
                                                       out_root, inside)
        total_rows += baseline[f"{schema}.{table}"]["n"]
    print(f"  . {total_rows:,} rows in {len(baseline)} tables")

    print(f"== {database}: data")
    for schema, table in sorted(by_table):
        cols = sorted(by_table[(schema, table)], key=lambda c: c["column_id"])
        name = f"{schema}.{table}.dat"
        order = key_order(meta, schema, table, cols)
        select = ("SELECT " + ", ".join(exported(render(c)) for c in cols)
                  + f" FROM [{schema}].[{table}]"
                  + (" ORDER BY " + ", ".join(f"[{c}]" for c in order) if order else ""))
        copied = mssql.bcp(select, database, f"{inside}/data/{name}")
        want = baseline[f"{schema}.{table}"]["n"]
        if copied != want:
            sys.exit(f"{name}: bcp copied {copied} rows, the catalogue says {want}")
        baseline[f"{schema}.{table}"]["file"] = name
        baseline[f"{schema}.{table}"]["bytes"] = os.path.getsize(os.path.join(data_dir, name))
        baseline[f"{schema}.{table}"]["ordered_by"] = order
        print(f"  . {name:<52} {copied:>9,} rows  "
              f"{baseline[f'{schema}.{table}']['bytes']:>12,} bytes"
              + ("" if order else "   (nothing sortable: row order is not stable)"))

    write(os.path.join(out_root, "meta.json"), meta)
    write(os.path.join(out_root, "baseline.json"), baseline)
    return meta, baseline


def table_baseline(database, schema, table, cols, out_root, inside):
    """Row count plus, per column, the three numbers a lossy export would change.

    non_null   catches a NULL/'' confusion or a dropped column
    units      total UTF-16 code units, which catches truncation
    non_ascii  rows holding any character outside printable ASCII, which catches the `?`
               substitution a wrong client encoding would produce -- that one keeps the length,
               so length alone would not see it
    """
    parts = ["COUNT_BIG(*) AS n"]
    for i, c in enumerate(cols):
        expr = render(c)
        parts.append(f"SUM(CASE WHEN {expr} IS NULL THEN 0 ELSE 1 END) AS nn{i}")
        parts.append(f"SUM(CAST(DATALENGTH({expr})/2 AS BIGINT)) AS cu{i}")
        parts.append(f"SUM(CASE WHEN {expr} COLLATE Latin1_General_BIN2 LIKE "
                     f"'%[^ -~]%' THEN 1 ELSE 0 END) AS nx{i}")
    sql = (f"SET NOCOUNT ON; SELECT CAST((SELECT {', '.join(parts)} "
           f"FROM [{schema}].[{table}] FOR JSON PATH, WITHOUT_ARRAY_WRAPPER) AS NVARCHAR(MAX))")
    # through bcp, not sqlcmd: sqlcmd 18 refuses `-y 0` (unlimited column width) alongside either
    # `-h` or `-W`, and without it a value longer than 256 characters is silently cut
    row = json.loads(scalar(sql, database, out_root, inside))
    return {"n": int(row["n"]),
            "columns": {c["name"]: {"non_null": int(row.get(f"nn{i}") or 0),
                                    "units": int(row.get(f"cu{i}") or 0),
                                    "non_ascii": int(row.get(f"nx{i}") or 0)}
                        for i, c in enumerate(cols)}}


def write(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(f"  . wrote {os.path.relpath(path, ROOT)} ({os.path.getsize(path):,} bytes)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--accept-eula", action="store_true",
                    help="accept the Microsoft SQL Server Developer EULA for this run")
    ap.add_argument("--keep", action="store_true", help="leave the container running afterwards")
    a = ap.parse_args()
    via = mssql.require_acceptance(a.accept_eula)

    for _, bak, dataset in DATABASES:
        path = os.path.join(ROOT, "downloads", bak)
        if not os.path.exists(path):
            sys.exit(f"missing {path}; run: python3 scripts/fetch.py {dataset}")

    # the server runs as uid 10001 inside the container, so the directories it writes into have
    # to be writable by it; nothing outside downloads/<dataset>/export/ is made writable
    mounts = []
    for _, bak, dataset in DATABASES:
        out = os.path.join(ROOT, "downloads", dataset, "export")
        os.makedirs(os.path.join(out, "data"), exist_ok=True)
        os.chmod(out, 0o777)
        os.chmod(os.path.join(out, "data"), 0o777)
        mounts.append((out, f"/export/{dataset}", "rw"))
        mounts.append((os.path.dirname(os.path.join(ROOT, "downloads", bak)),
                       f"/bak/{dataset}", "ro"))

    started = time.time()
    print(f"starting {mssql.NAME} from {mssql.IMAGE}")
    mssql.start(mounts)
    facts = mssql.server_facts(via)
    print(f"  . {facts['version'].splitlines()[0].strip()}")
    print(f"  . bcp {facts['bcp']}")

    for database, bak, dataset in DATABASES:
        name = os.path.basename(bak)
        print(f"\n== restoring {database} from {name}")
        files = mssql.sqlcmd(f"SET NOCOUNT ON; RESTORE FILELISTONLY FROM DISK='/bak/{dataset}/{name}'")
        moves = []
        for line in files.stdout.splitlines():
            parts = line.split()
            if parts and parts[0] in ("WWI_Primary", "WWI_UserData", "WWI_Log"):
                ext = {"WWI_Primary": ".mdf", "WWI_UserData": "_UserData.ndf", "WWI_Log": ".ldf"}
                moves.append(f"MOVE '{parts[0]}' TO '/var/opt/mssql/data/{database}{ext[parts[0]]}'")
        if len(moves) != 3:
            sys.exit(f"{name}: expected 3 logical files, found {len(moves)}:\n{files.stdout}")
        mssql.sqlcmd(f"RESTORE DATABASE [{database}] FROM DISK='/bak/{dataset}/{name}' WITH "
                     + ", ".join(moves) + ", RECOVERY, NOUNLOAD")
        print(f"  . restored")

    for database, bak, dataset in DATABASES:
        meta, baseline = export_database(database, dataset, via)
        out = os.path.join(ROOT, "downloads", dataset, "export")
        artifact = os.path.join(ROOT, "downloads", bak)
        write(os.path.join(out, "server.json"),
              dict(facts, database=database, backup=os.path.basename(bak),
                   backup_bytes=os.path.getsize(artifact)))

    if not a.keep:
        mssql.stop()
        print(f"\nremoved {mssql.NAME}; nothing licensed under the EULA remains")
    print(f"export finished in {time.time() - started:.0f}s")


if __name__ == "__main__":
    main()
