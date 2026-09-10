"""The MySQL corpus, read back as an engine-neutral model and rewritten for other engines.

    model.py    information_schema of a loaded database -> Table, Column, Index, ForeignKey, Check
    typemap.py  the ONE mapping table: a MySQL column -> its PostgreSQL and SQLite declarations
    tsv.py      the MySQL Shell dump's TSV chunks, decoded row by row

Every engine that is not the hub is built through these three modules, so a type decision is made
once and shows up in every target the same way (knowledge/decisions/engine-hub.md).
"""
