#!/usr/bin/env python3
"""The MySQL shape of Oracle Order Entry, and the upstream shape it is derived from.

OE is object-relational: an address object, a phone VARRAY, two spatial points and an XMLType. None
of those survive into MySQL, so the target schema is written out here rather than translated, and
`UPSTREAM` records the column order the populate scripts rely on. The converter checks the upstream
CREATE TABLE statements against `UPSTREAM` and stops if they no longer agree, because every INSERT
in the data files is positional -- a column inserted upstream would otherwise shift 11,140 rows
silently into the wrong columns.

Record: knowledge/datasets/oracle-oe-pm-ix.md
"""

# what the OE install scripts declare, in the order the INSERT ... VALUES statements assume
UPSTREAM = {
    "customers": ["customer_id", "cust_first_name", "cust_last_name", "cust_address",
                  "phone_numbers", "nls_language", "nls_territory", "credit_limit", "cust_email",
                  "account_mgr_id", "cust_geo_location"],
    "warehouses": ["warehouse_id", "warehouse_spec", "warehouse_name", "location_id",
                   "wh_geo_location"],
    "orders": ["order_id", "order_date", "order_mode", "customer_id", "order_status",
               "order_total", "sales_rep_id", "promotion_id"],
    "order_items": ["order_id", "line_item_id", "product_id", "unit_price", "quantity"],
    "inventories": ["product_id", "warehouse_id", "quantity_on_hand"],
    "product_information": ["product_id", "product_name", "product_description", "category_id",
                            "weight_class", "warranty_period", "supplier_id", "product_status",
                            "list_price", "min_price", "catalog_url"],
    "product_descriptions": ["product_id", "language_id", "translated_name",
                             "translated_description"],
    "promotions": ["promo_id", "promo_name"],
}

# columns loe_v3.sql adds after the load ("OWB, BI additions"), appended to customers
UPSTREAM_ADDED = {"customers": ["date_of_birth", "marital_status", "gender", "income_level"]}

# The MySQL tables. Each column is (name, definition); the converter attaches the upstream
# COMMENT ON COLUMN text to any name that still exists.
TABLES = [
    ("customers", [
        ("customer_id", "INT NOT NULL"),
        ("cust_first_name", "VARCHAR(20) NOT NULL"),
        ("cust_last_name", "VARCHAR(20) NOT NULL"),
        ("cust_street_address", "VARCHAR(40)"),
        ("cust_postal_code", "VARCHAR(10)"),
        ("cust_city", "VARCHAR(30)"),
        ("cust_state_province", "VARCHAR(10)"),
        ("cust_country_id", "CHAR(2)"),
        ("nls_language", "VARCHAR(3)"),
        ("nls_territory", "VARCHAR(30)"),
        ("credit_limit", "DECIMAL(9,2)"),
        ("cust_email", "VARCHAR(40)"),
        ("account_mgr_id", "INT"),
        ("geo_longitude", "DECIMAL(9,6)"),
        ("geo_latitude", "DECIMAL(9,6)"),
        ("date_of_birth", "DATE"),
        ("marital_status", "VARCHAR(20)"),
        ("gender", "VARCHAR(1)"),
        ("income_level", "VARCHAR(20)"),
    ], ["PRIMARY KEY (customer_id)",
        "CONSTRAINT customer_credit_limit_max CHECK (credit_limit <= 5000)",
        "CONSTRAINT customer_id_min CHECK (customer_id > 0)"]),
    ("customer_phone_numbers", [
        ("customer_id", "INT NOT NULL"),
        ("phone_seq", "TINYINT NOT NULL"),
        ("phone_number", "VARCHAR(25) NOT NULL"),
    ], ["PRIMARY KEY (customer_id, phone_seq)",
        "CONSTRAINT cust_phone_customer_fk FOREIGN KEY (customer_id) "
        "REFERENCES customers (customer_id) ON DELETE CASCADE"]),
    ("warehouses", [
        ("warehouse_id", "INT NOT NULL"),
        ("warehouse_name", "VARCHAR(35)"),
        # NUMBER(4) upstream, but it carries a foreign key to oracle_hr.locations, whose key is
        # SMALLINT; MySQL requires the two sides to have the same type
        ("location_id", "SMALLINT"),
        ("geo_longitude", "DECIMAL(9,6)"),
        ("geo_latitude", "DECIMAL(9,6)"),
        ("warehouse_spec_xml", "TEXT"),
        ("building", "VARCHAR(20)"),
        ("area", "INT"),
        ("docks", "INT"),
        ("dock_type", "VARCHAR(20)"),
        ("water_access", "VARCHAR(1)"),
        ("rail_access", "VARCHAR(1)"),
        ("parking", "VARCHAR(10)"),
        ("v_clearance", "VARCHAR(10)"),
    ], ["PRIMARY KEY (warehouse_id)"]),
    ("product_information", [
        ("product_id", "INT NOT NULL"),
        ("product_name", "VARCHAR(50)"),
        ("product_description", "VARCHAR(2000)"),
        ("category_id", "SMALLINT"),
        ("weight_class", "TINYINT"),
        ("warranty_months", "SMALLINT"),
        ("supplier_id", "INT"),
        ("product_status", "VARCHAR(20)"),
        ("list_price", "DECIMAL(8,2)"),
        ("min_price", "DECIMAL(8,2)"),
        ("catalog_url", "VARCHAR(50)"),
    ], ["PRIMARY KEY (product_id)",
        "CONSTRAINT product_status_lov CHECK (product_status IN "
        "('orderable', 'planned', 'under development', 'obsolete'))"]),
    ("product_descriptions", [
        ("product_id", "INT NOT NULL"),
        ("language_id", "VARCHAR(3) NOT NULL"),
        ("translated_name", "VARCHAR(50) NOT NULL"),
        ("translated_description", "VARCHAR(2000) NOT NULL"),
    ], ["PRIMARY KEY (product_id, language_id)",
        "CONSTRAINT pd_product_id_fk FOREIGN KEY (product_id) "
        "REFERENCES product_information (product_id)"]),
    ("inventories", [
        ("product_id", "INT NOT NULL"),
        ("warehouse_id", "INT NOT NULL"),
        ("quantity_on_hand", "INT NOT NULL"),
    ], ["PRIMARY KEY (product_id, warehouse_id)",
        "CONSTRAINT inventories_warehouses_fk FOREIGN KEY (warehouse_id) "
        "REFERENCES warehouses (warehouse_id)",
        "CONSTRAINT inventories_product_id_fk FOREIGN KEY (product_id) "
        "REFERENCES product_information (product_id)"]),
    ("orders", [
        ("order_id", "INT NOT NULL"),
        ("order_date", "DATETIME(6) NOT NULL"),
        ("order_mode", "VARCHAR(8)"),
        ("customer_id", "INT NOT NULL"),
        ("order_status", "SMALLINT"),
        ("order_total", "DECIMAL(8,2)"),
        ("sales_rep_id", "INT"),
        ("promotion_id", "INT"),
    ], ["PRIMARY KEY (order_id)",
        "CONSTRAINT orders_customer_id_fk FOREIGN KEY (customer_id) "
        "REFERENCES customers (customer_id)",
        "CONSTRAINT order_mode_lov CHECK (order_mode IN ('direct', 'online'))",
        "CONSTRAINT order_total_min CHECK (order_total >= 0)"]),
    ("order_items", [
        ("order_id", "INT NOT NULL"),
        ("line_item_id", "SMALLINT NOT NULL"),
        ("product_id", "INT NOT NULL"),
        ("unit_price", "DECIMAL(8,2)"),
        ("quantity", "INT"),
    ], ["PRIMARY KEY (order_id, line_item_id)",
        "UNIQUE KEY order_items_uk (order_id, product_id)",
        "CONSTRAINT order_items_order_id_fk FOREIGN KEY (order_id) "
        "REFERENCES orders (order_id) ON DELETE CASCADE",
        "CONSTRAINT order_items_product_id_fk FOREIGN KEY (product_id) "
        "REFERENCES product_information (product_id)"]),
    ("promotions", [
        ("promo_id", "INT NOT NULL"),
        ("promo_name", "VARCHAR(20)"),
    ], ["PRIMARY KEY (promo_id)"]),
]

# cidx_v3.sql, which is what the installer runs. The legacy oe_idx.sql additionally creates
# inv_warehouse_ix; there it is commented out, so it is not created here either.
INDEXES = [
    ("whs_location_ix", "warehouses", "(location_id)"),
    ("inv_product_ix", "inventories", "(product_id)"),
    ("item_order_ix", "order_items", "(order_id)"),
    ("item_product_ix", "order_items", "(product_id)"),
    ("ord_sales_rep_ix", "orders", "(sales_rep_id)"),
    ("ord_customer_ix", "orders", "(customer_id)"),
    ("ord_order_date_ix", "orders", "(order_date)"),
    ("cust_account_manager_ix", "customers", "(account_mgr_id)"),
    ("cust_lname_ix", "customers", "(cust_last_name)"),
    ("cust_email_ix", "customers", "(cust_email)"),
    ("prod_name_ix", "product_descriptions", "(translated_name)"),
    ("prod_supplier_ix", "product_information", "(supplier_id)"),
    # the upstream index is on UPPER(cust_last_name), UPPER(cust_first_name); under MySQL's
    # accent- and case-insensitive default collation an index on the columns serves the same
    # queries, so this is the plain composite rather than a functional index
    ("cust_upper_name_ix", "customers", "(cust_last_name, cust_first_name)"),
]

# Two indexes this image adds beyond the upstream set, per PLAN.md section 3.14: the language filter
# every multilingual query starts with, and a FULLTEXT index over the descriptions. The FULLTEXT one
# is there to show what MySQL's default parser does with 30 languages at once. Measured on this data:
# `monitor` matches 237 rows and the German `Auflösung` 12, while the Japanese `モニター` matches only
# 8 -- the parser splits on whitespace and punctuation, so it finds a Japanese word only where the
# text happens to set it off with punctuation, and misses it inside a run of kana and kanji. The
# `ngram` parser would fix the CJK languages at the cost of the European ones.
ADDED_INDEXES = [
    ("prod_desc_language_ix", "product_descriptions", "(language_id)", ""),
    ("prod_desc_ft", "product_descriptions", "(translated_description)", "FULLTEXT "),
]
