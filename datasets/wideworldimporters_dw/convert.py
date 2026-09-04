#!/usr/bin/env python3
"""WideWorldImportersDW -> MySQL.

A far simpler schema than the OLTP database: no temporal tables, no computed columns, no JSON, two
geography columns. What it does have is names with spaces -- five tables and 314 columns -- which the
mapping decision resolves by removing spaces from table names (`dimension_stockitem`) and replacing
them with underscores in column names (`total_including_tax`).

Record: knowledge/datasets/wideworldimporters-dw.md
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import wwi  # noqa: E402

EXPORT = os.path.abspath(os.path.join(HERE, "..", "..", "downloads", "wideworldimporters_dw",
                                      "export"))

# The Integration schema's staging tables exist for the SSIS package that populates the warehouse.
# All 13 are empty in the shipped backup and none is reachable from the star schema, so they are
# dropped; `ETL Cutoff` and `Lineage`, which do carry rows, are kept.
def staging_tables():
    meta = json.load(open(os.path.join(EXPORT, "meta.json"), encoding="utf-8"))
    return {(t["schema"], t["name"]) for t in meta["tables"]
            if t["schema"] == "Integration" and t["name"].endswith("_Staging")}


CONFIG = {
    "dataset": "wideworldimporters_dw",
    "database": "wideworldimporters_dw",
    "title": "WideWorldImportersDW, v1.0",
    "context": "/context/wideworldimporters_dw",
    "prefix": True,
    "json_columns": set(),
    "computed": {},
    "unported": [
        "the Sequences schema: 8 sequence objects become AUTO_INCREMENT columns",
        "datetime2(7) -> DATETIME(6): the 7th fractional digit is dropped",
        "Integration.*_Staging: 13 empty SSIS staging tables, dropped",
    ],
}


def main():
    CONFIG["drop_tables"] = staging_tables()
    wwi.convert(CONFIG, EXPORT, sys.argv[2], os.path.join(HERE, "name_map.yaml"))


if __name__ == "__main__":
    main()
