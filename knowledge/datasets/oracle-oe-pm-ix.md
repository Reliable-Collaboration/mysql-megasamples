---
type: Dataset
title: Oracle OE (Order Entry) with the archived OC, PM and IX schemas
description: The object-relational Order Entry schema (7 relational tables, 11,140 rows incl. 8,640 multilingual product descriptions) is worth carrying in flattened form as oracle_oe; the OC object views, PM LOB/nested-table media schema and IX AQ queues are dropped.
resource: https://github.com/oracle-samples/db-sample-schemas/tree/v23.3/order_entry
tags: [tier-core, oracle, oe, oc, pm, ix, archived, object-relational, encoding-canary, mit]
status: stable
trust: verified
stale_after: 2027-03-01
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: /sources/github-oracle-samples-db-sample-schemas-releases-and-tree.md
    title: Releases, tags, tree sizes (where the archived schemas live)
    accessed: 2026-09-02
  - resource: /sources/github-oracle-samples-db-sample-schemas-oe-pm-ix-scripts.md
    title: OE/OC/PM scripts at v23.3, IX at v19.2
    accessed: 2026-09-02
  - resource: /sources/github-oracle-samples-db-sample-schemas-readme-and-license.md
    title: README (archived status), LICENSE.txt
    accessed: 2026-09-02
  - resource: /sources/oracle-docs-database-sample-schemas-guide-23-comsc.md
    title: Oracle Sample Schemas guide (OE/PM pages, IX/BI/QS removed)
    accessed: 2026-09-02
  - resource: /sources/oracle-docs-sql-language-reference-23-data-types.md
    title: Oracle data types (TSLTZ, NUMBER)
    accessed: 2026-09-02
  - resource: /sources/mysql-refman-9-7-spatial-type-overview.md
    title: MySQL spatial SRID attribute
    accessed: 2026-09-02
  - resource: /sources/mysql-refman-9-7-fractional-seconds.md
    title: MySQL fractional seconds
    accessed: 2026-09-02
---

# Identity
* **OE** "Order Entry" (with its **OC** "Online Catalog" object-relational sub-schema) — archived, "19c and lower", still shipped in v23.3 under `order_entry/`.
* **PM** "Product Media" — archived, shipped under `product_media/`.
* **IX** "Information Exchange" — **not in v23.3 at all**; last present at tag `v19.2`/`v21.1` under `info_exchange/`; the 26ai guide states "The Business Intelligence (bi), Information Exchange (ix), and Shipping (qs) schemas are no longer available."
* Proposed MySQL database name: **`oracle_oe`** (holding the flattened OE tables; OC/PM/IX are not shipped).

# Source artifact
* Same repo; the archived directories are **plain directories inside tag v23.3** (commit `e3325a8`), not a branch or separate tag. `order_entry/`: 216 files, 13,600,128 bytes (70 `.sql` = 3,572,146 B; 132 XML purchase orders in `2002/<Mon>/` = 484,971 B; `PurchaseOrders.dmp` 9,345,886 B; `POList.json` 64,658 B; `bi_oe_*.ctl/.dat` ≈ 100 KB; `purchaseOrder.xsd/.xsl`, `empdept.xsl`, `filelist.xml`). `product_media/`: 65 files, 2,763,923 B (54 media files = 2,720,743 B). IX at v19.2: `info_exchange/cix_v3.sql` 3,200 B, `dix_v3.sql`, `ix_main.sql`, `vix_v3.sql`.
* Files the converter needs (v23.3): `oe_cre.sql`, `ccus_v3.sql`, `cord_v3.sql`, `cwhs_v3.sql`, `oe_idx.sql`, `oe_views.sql`, `poe_v3.sql`, `loe_v3.sql`, `pcus_v3.sql` 99,139 B (the legacy `oe_p_cus.sql` 94,971 B is a near-duplicate not called by the installer), `pord_v3.sql` 21,518 B, `pwhs_v3.sql` 4,086 B, `oe_p_pi.sql` 91,524 B, `oe_p_itm.sql` 40,641 B, `oe_p_inv.sql` 50,918 B, `oe_p_pd.sql` 2,179 B and the 30 `oe_p_<lang>.sql` files (62–229 KB each, ≈ 2.9 MB). No auth/click-through.

# Native format and friendlier forms
SQL*Plus scripts written for the pre-v23 `oe_main.sql` driver: 9 positional parameters (incl. **HR password and SYS password**), `perl` substitution of `__SUB__CWD__`, grants from HR, XML DB privileges (`xdbadmin`), `sqlldr` for PM, `DBMS_XMLSCHEMA.registerSchema` for the purchase-order table. The relational data is nevertheless plain text: `INSERT INTO customers VALUES (101,'Constantin','Welles',cust_address_typ('514 W Superior St','46901','Kokomo','IN','US'),PHONE_LIST_TYP('+1 317 123 4104'),'us','AMERICA','100','...@ANHINGA.EXAMPLE.COM',149, MDSYS.SDO_GEOMETRY(2001, 8307, MDSYS.SDO_POINT_TYPE(-86.13631, 40.485424,NULL),NULL,NULL))`, `TO_TIMESTAMP('16-AUG-07 02.34.12.234359 PM','DD-MON-RR HH.MI.SS.FF AM')`, `to_yminterval('+00-03')`, `UNISTR('LCD\30e2\30cb\30bf\30fc11/PM')`, `sys.xmltype.createxml('<?xml ...')`. A Python parser handles all of these; the XML purchase orders are separate `.xml` files. Only `PurchaseOrders.dmp` (Data Pump) is unreadable without Oracle — and no install script references it.

# Shape (OE relational core, verified counts from the populate scripts)
| upstream table | rows | MySQL target |
|---|---|---|
| customers | 319 | `customers` with `cust_address` flattened to `cust_street_address VARCHAR(40)`, `cust_postal_code VARCHAR(10)`, `cust_city VARCHAR(30)`, `cust_state_province VARCHAR(10)`, `cust_country_id CHAR(2)`; `cust_geo_location` → `geo_longitude DECIMAL(9,6)`, `geo_latitude DECIMAL(9,6)`; plus `date_of_birth DATE`, `marital_status`, `gender`, `income_level` (added/updated post-load upstream); `credit_limit DECIMAL(9,2)` CHECK ≤ 5000; `account_mgr_id` FK → `oracle_hr.employees` |
| customer_phone_numbers (new) | ≈ 319–400 (**inferred**; VARRAY(5), most customers have one) | `(customer_id INT, phone_seq TINYINT, phone_number VARCHAR(25))` PK (customer_id, phone_seq) — the `phone_list_typ` VARRAY flattened |
| warehouses | 9 | `warehouse_spec` XMLType → `warehouse_spec_xml TEXT` (raw XML kept; MySQL `ExtractValue()` still works) and, for convenience, the 8 known child elements as nullable columns `building, area, docks, dock_type, water_access, rail_access, parking, v_clearance` (**recommended**, cheap: 9 rows); `wh_geo_location` → lon/lat DECIMAL; `location_id` FK → `oracle_hr.locations` |
| orders | 105 | `order_date TIMESTAMP WITH LOCAL TIME ZONE` → `DATETIME(6)` (values have 6 fractional digits; treat the literals as UTC — upstream had no zone information); `order_mode` CHECK; `order_total DECIMAL(8,2)`; `sales_rep_id` FK → `oracle_hr.employees`; `promotion_id` |
| order_items | 665 | as is; PK (order_id, line_item_id); trigger `insert_ord_line` ported |
| product_information | 288 | `warranty_period INTERVAL YEAR TO MONTH` → `warranty_months SMALLINT` (values like `+00-03`; converter asserts the year part is 0 or folds it into months); `product_status` CHECK |
| product_descriptions | **8,640** (288 × 30 languages) | `translated_name VARCHAR(50)`, `translated_description VARCHAR(2000)` utf8mb4; `language_id` in {US, AR, CA, CS, D, DK, E, EL, ESA, F, FRC, HU, I, IW, JA, KO, N, NL, PL, PT, PTB, RO, RU, S, SF, SK, TH, TR, ZHS, ZHT}; text decoded from `UNISTR` `\XXXX` escapes — Arabic, Hebrew, Thai, Greek, Cyrillic, CJK: **the best encoding canary in the whole image** |
| inventories | 1,112 | as is |
| promotions | 2 | as is (`promo_id`, `promo_name`) |

Total ≈ 11,140 rows + phone rows; loaded size < 10 MB (**inferred**; scripts ≈ 3.6 MB of which ≈ 2.9 MB are the descriptions). Source files are pure ASCII (non-Latin text is escaped), so no file-encoding hazard; the *output* is heavily non-ASCII.

# What is dropped and why
* **OC**: object types (`customer_typ`, `order_typ`, `category_typ` hierarchy, …), object table `categories_tab` (22 rows with nested `product_ref_list`/`subcategory_ref_list`) and object views `oc_customers`, `oc_orders`, `oc_inventories`, `oc_product_information`, `oc_corporate_customers` with `INSTEAD OF` triggers — they are alternative object views over the same relational rows; no MySQL equivalent. Optional later: flatten `categories_tab` into `categories(category_id, category_name, category_description, category_type)`, `category_products`, `category_subcategories` (22 + ≈ 300 rows) — cheap but not needed for v1.
* **XML purchase orders** (`purchaseorder` XMLType table, 132 XML files, `xdbpo_*` types, XDB repository folders, `PurchaseOrders.dmp`, `POList.json`): dropped in v1; see [question](/questions/oracle-oe-xml-purchase-orders-scope.md) for an optional `purchase_orders(reference, requestor, ..., xml_doc LONGTEXT, json_doc JSON)` table built directly from the 132 files.
* **PM**: `print_media` has only **4 rows** (+ 12 nested `textdoc` rows) of BLOB/CLOB/NCLOB/BFILE/nested-table/object-column data loaded by `sqlldr` from 2.7 MB of media files; `online_media` (ORDSYS types) was already removed upstream in 2018; BFILE needs a filesystem directory. Dropped entirely — zero teaching value beyond LOB syntax that MySQL demonstrates elsewhere (Sakila `film_text`, etc.).
* **IX**: only an AQ queue table/queue (`orders_queuetable`, `orders_queue`) and `DBMS_STREAMS_ADM`; no rows; removed upstream. Dropped.
* HR synonyms (`employees`, `locations`, …) → not created; queries use `oracle_hr.employees` explicitly.
* `oe_analz` stats, `NOLOGGING`, OIDs on types, `coe_*` public synonyms → nothing.

# Conversion path
Path (a): Python parser over the populate scripts listed above (see [decision](/decisions/oracle-conversion-path.md)); Oracle is **not** required, and the archived scripts might not even run on 26ai Free (they target "19c and lower" and need `xdbadmin`, `sqlldr`, `perl` path substitution) — so path (b) is *less* reliable here, not more.

# Type-mapping hazards
* `NUMBER(12)` order_id → `BIGINT`; `NUMBER(6)`/`NUMBER(3)`/`NUMBER(2)`/`NUMBER(1)` → `INT`/`SMALLINT`/`TINYINT`; `NUMBER(8,2)`/`NUMBER(9,2)` → `DECIMAL`.
* `TIMESTAMP WITH LOCAL TIME ZONE`: Oracle normalises to the DB zone and renders in the session zone ([data types](/sources/oracle-docs-sql-language-reference-23-data-types.md)); the literals carry no zone, so the converter stores them verbatim as `DATETIME(6)` and documents "wall-clock as written in the script (2007–2008 dates)". `orders_view` (which casts to DATE) ports as `DATE(order_date)`.
* `NVARCHAR2` → `VARCHAR` utf8mb4 (**Inferred:** MySQL's `NVARCHAR` is a `VARCHAR` synonym tied to utf8mb3 — from memory, avoid it either way).
* `INTERVAL YEAR TO MONTH` → `SMALLINT` months (no interval type in MySQL).
* `SDO_GEOMETRY` points (SRID 8307 = WGS84 lon/lat) → `DECIMAL(9,6)` lon/lat columns; a generated `POINT SRID 4326` column is optional but MySQL's 4326 axis order (lat-long) was not verified in this research ([spatial source](/sources/mysql-refman-9-7-spatial-type-overview.md)) — keep it out of v1.
* `XMLType` → `TEXT` + scalar columns (above).
* VARRAY → child table; `get_phone_number_f(n, phone_numbers)` → `SELECT phone_number FROM customer_phone_numbers WHERE customer_id=? AND phone_seq=n`; `customers_view` ports with LEFT JOINs to phone_seq 1..5.
* Function-based index `cust_upper_name_ix ON customers (UPPER(cust_last_name), UPPER(cust_first_name))` → functional index `((UPPER(cust_last_name)), (UPPER(cust_first_name)))` (**Inferred:** supported since MySQL 8.0.13 — from memory, verify) or simply an index on the case-insensitive collated columns (redundant under `utf8mb4_0900_ai_ci`) — recommend the plain composite index and note the difference.
* `sequence orders_seq START WITH 1000` while existing order_ids go up to 2458 → `AUTO_INCREMENT` continues from 2459 (upstream would collide; documented quirk).
* Cross-database FKs to `oracle_hr` (`orders.sales_rep_id`, `customers.account_mgr_id`, `warehouses.location_id` with `ON DELETE SET NULL`): MySQL allows them; keep them (both databases are core, HR must load first) with a documented fallback of index-only if the coordinator prefers database independence ([naming decision](/decisions/database-naming-convention.md) notes tooling displays them poorly).
* `products` view uses `sys_context('USERENV','LANG')` and `TRANSLATE(... USING NCHAR_CS)` → port as a view fixed to `language_id = 'US'` falling back to `product_information` names (or parameterise with `@lang` session variable defaulting to 'US').

# Programmable objects
| object | action |
|---|---|
| views `sydney_inventory`, `bombay_inventory`, `toronto_inventory`, `product_prices`, `orders_view`, `account_managers` (ROLLUP over flattened address columns), `customers_view` (flattened), `products` (fixed language) | port |
| function `get_phone_number_f` | drop (replaced by child table) or trivial re-implementation |
| trigger `insert_ord_line` | port (`BEFORE INSERT` sets `line_item_id = COALESCE(MAX)+1`) |
| triggers `orders_trg`, `orders_items_trg` (INSTEAD OF on object views) | drop with OC |
| CHECK constraints (`order_mode_lov`, `order_total_min`, `product_status_lov`, `customer_credit_limit_max`, `customer_id_min`) | port |
| `COMMENT ON` (cmnt_v3.sql, oe_comnt.sql) | port |
| object types, OC views, XML schema, XDB resources, AQ queues, PM LOB tables | drop |

# Indexing
`oe_idx.sql` indexes (whs_location_ix, inv_product_ix, inv_warehouse_ix, item_order_ix, item_product_ix, ord_sales_rep_ix, ord_customer_ix, ord_order_date_ix, cust_account_manager_ix, cust_lname_ix, cust_email_ix, prod_name_ix on translated_name, prod_supplier_ix) plus the composite name index; PK/UNIQUE as declared.

# Tests and expected values
* Row counts: customers 319, warehouses 9, orders 105, order_items 665, product_information 288, product_descriptions 8,640 (288 per language × 30), inventories 1,112, promotions 2; phone rows = number of VARRAY elements (computed by the converter and stored in the baseline).
* Encoding canaries: `SELECT translated_name FROM product_descriptions WHERE product_id=1726 AND language_id='JA'` = `LCDモニター11/PM` (decoded from `UNISTR('LCD\30e2\30cb\30bf\30fc11/PM')`); `language_id='D'` description contains `Auflösung für optimale Bildqualität` (from `\00f6`, `\00fc`, `\00e4`).
* `order_id 2458`: order_date `2007-08-16 14:34:12.234359`, customer 101, total 78279.6, sales_rep 153.
* Cross-DB FK: every `orders.sales_rep_id` exists in `oracle_hr.employees`.

# Tier assignment
**core** — < 10 MB loaded (**inferred** from 3.6 MB of scripts; [tier model](/decisions/tier-model.md)). PM media (2.7 MB) and XML (0.5 MB) are not shipped.

# License and attribution
MIT — [MIT record](/licenses/mit.md); archived scripts carry "Copyright (c) 2001, 2018, Oracle" headers with the same MIT text.

# Open questions
* [XML purchase orders and spatial columns scope](/questions/oracle-oe-xml-purchase-orders-scope.md) — carry the 132 XML documents as a table? add `POINT SRID 4326` columns (axis order check)? flatten `categories_tab`?
* Whether the archived `oe_main.sql` still installs on 26ai Free is unknown (only matters for the optional verification profile; the answer does not affect path (a)).
