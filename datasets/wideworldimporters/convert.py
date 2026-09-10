#!/usr/bin/env python3
"""WideWorldImporters (OLTP) -> MySQL.

Everything general lives in megasamples/sources/wwi.py; this file holds the decisions that are specific to this
database and should be visible rather than inferred: which text columns are really JSON, and what
each of the eight computed columns becomes.

Record: knowledge/datasets/wideworldimporters.md
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from megasamples.sources import wwi  # noqa: E402

# Columns SQL Server stores as nvarchar(max) but that hold JSON. Only `ReturnedDeliveryData` carries
# an `isjson` CHECK upstream; the rest are named as JSON by the sample's own documentation and by the
# computed columns that read them with json_query/json_value. The converter parses every value in
# these columns while writing the TSV, so the claim is checked rather than trusted.
JSON_COLUMNS = {
    ("Application", "People", "UserPreferences"),
    ("Application", "People", "CustomFields"),
    ("Application", "People", "OtherLanguages"),
    ("Application", "People_Archive", "UserPreferences"),
    ("Application", "People_Archive", "CustomFields"),
    ("Application", "People_Archive", "OtherLanguages"),
    ("Application", "SystemParameters", "ApplicationSettings"),
    ("Sales", "Invoices", "ReturnedDeliveryData"),
    ("Warehouse", "StockItems", "CustomFields"),
    ("Warehouse", "StockItems", "Tags"),
    ("Warehouse", "StockItems_Archive", "CustomFields"),
    ("Warehouse", "StockItems_Archive", "Tags"),
}

# The eight computed columns, translated by hand. Two of them need COALESCE that the T-SQL does not:
# SQL Server's concat() renders NULL as an empty string, MySQL's CONCAT returns NULL for the whole
# expression, and `MarketingComments` and `PreferredName` are both nullable.
COMPUTED = {
    ("Sales", "CustomerTransactions", "IsFinalized"):
        "CASE WHEN `finalizationdate` IS NULL THEN 0 ELSE 1 END",
    ("Purchasing", "SupplierTransactions", "IsFinalized"):
        "CASE WHEN `finalizationdate` IS NULL THEN 0 ELSE 1 END",
    ("Application", "People", "SearchName"):
        "CONCAT(COALESCE(`preferredname`,''),' ',COALESCE(`fullname`,''))",
    ("Application", "People", "OtherLanguages"):
        "JSON_EXTRACT(`customfields`,'$.OtherLanguages')",
    ("Warehouse", "StockItems", "Tags"):
        "JSON_EXTRACT(`customfields`,'$.Tags')",
    ("Warehouse", "StockItems", "SearchDetails"):
        "CONCAT(COALESCE(`stockitemname`,''),' ',COALESCE(`marketingcomments`,''))",
    ("Sales", "Invoices", "ConfirmedDeliveryTime"):
        "CAST(JSON_UNQUOTE(JSON_EXTRACT(`returneddeliverydata`,'$.DeliveredWhen')) AS DATETIME(6))",
    ("Sales", "Invoices", "ConfirmedReceivedBy"):
        "JSON_UNQUOTE(JSON_EXTRACT(`returneddeliverydata`,'$.ReceivedBy'))",
}

CONFIG = {
    "dataset": "wideworldimporters",
    "database": "wideworldimporters",
    "title": "WideWorldImporters (OLTP), v1.0",
    "context": "/context/wideworldimporters",
    "prefix": True,
    "json_columns": JSON_COLUMNS,
    "computed": COMPUTED,
    "unported": [
        "system versioning: 18 tables are temporal; both the current table and its `_archive` "
        "partner are plain tables here, and ValidFrom/ValidTo are plain DATETIME(6) columns",
        "the Sequences schema: 26 sequence objects become AUTO_INCREMENT columns, so the "
        "TransactionID sequence no longer keeps customer, supplier and stock transactions from "
        "reusing a value between them",
        "datetime2(7) -> DATETIME(6): the 7th fractional digit is dropped",
    ],
}


def main():
    export = os.path.join(HERE, "..", "..", "downloads", "wideworldimporters", "export")
    wwi.convert(CONFIG, os.path.abspath(export), sys.argv[2],
                os.path.join(HERE, "name_map.yaml"))


if __name__ == "__main__":
    main()
