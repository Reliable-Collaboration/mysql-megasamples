"""Port a database's views: each definition translated, created after what it depends on.

A view that selects from another view is created after it. A view the target cannot express --
one that reads another database, uses XML functions on SQLite, or ROLLUP on SQLite -- is dropped by
name with the reason, and the catalogue records it.
"""
from megasamples.port import sqltranslate


def ordered(views):
    out, seen = [], set()

    def place(v):
        if v.name in seen:
            return
        seen.add(v.name)
        for d in v.depends_on:
            dep = next((o for o in views if o.name == d), None)
            if dep:
                place(dep)
        out.append(v)

    for v in views:
        place(v)
    return out


def render(database, dialect):
    """([CREATE VIEW statements], dropped) for one database."""
    quote = '"'
    statements, dropped = [], []
    unavailable = set()
    names = sqltranslate.names_of(database)
    for v in ordered(database.views):
        missing = [d for d in v.depends_on if d in unavailable]
        if missing:
            unavailable.add(v.name)
            dropped.append(f"view {v.name}: depends on {', '.join(missing)}, which is not ported")
            continue
        try:
            body = sqltranslate.translate(v.definition, dialect, database.name,
                                          extra=[r.name for r in database.routines] if dialect == "postgres" else (),
                                          names=names)
        except sqltranslate.Unportable as exc:
            unavailable.add(v.name)
            dropped.append(f"view {v.name}: {exc}")
            continue
        cols = ", ".join(f'{quote}{c[0]}{quote}' for c in v.columns)
        statements.append(f"CREATE VIEW {quote}{v.name}{quote} ({cols}) AS\n{body};")
    return statements, dropped
