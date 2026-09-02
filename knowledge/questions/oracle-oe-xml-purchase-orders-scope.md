---
type: Open Question
title: OE extras — carry the 132 XML purchase orders, add POINT SRID 4326 columns, flatten categories_tab?
description: Three optional enrichments of oracle_oe whose value depends on cheap checks (XML structure, MySQL 4326 axis order, OC category data) not performed during research.
resource: /questions/oracle-oe-xml-purchase-orders-scope.md
tags: [question, oracle, oe, xml, spatial]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: /sources/github-oracle-samples-db-sample-schemas-oe-pm-ix-scripts.md
    title: OE/OC scripts, XML loading
    accessed: 2026-09-02
  - resource: /sources/mysql-refman-9-7-spatial-type-overview.md
    title: MySQL SRID attribute (axis order not covered)
    accessed: 2026-09-02
---

# Question
1. The 132 `order_entry/2002/<Mon>/<USER>-<timestamp>.xml` files (485 KB) conform to `purchaseOrder.xsd` (Reference, Actions, Requestor, User, CostCenter, ShippingInstructions, SpecialInstructions, LineItems …). Is a `purchase_orders(reference, requestor, user_name, cost_center, ship_to_name, ship_to_address, special_instructions, po_date, xml_doc LONGTEXT, json_doc JSON)` + `purchase_order_lines` pair worth adding (it would be the image's only XML/JSON-from-XML example)? `PurchaseOrders.dmp` (Data Pump) is ignored either way.
2. Should `customers`/`warehouses` get a generated `POINT SRID 4326` column from the `SDO_POINT_TYPE(x=lon, y=lat)` values? Requires confirming MySQL's axis order for SRID 4326 (`ST_SRID(ST_GeomFromText('POINT(40.48 -86.13)',4326))`, `ST_Latitude()`), which the spatial overview page does not state.
3. Is the OC `categories_tab` (22 rows, nested product/subcategory REF lists in `oc_popul.sql`) worth flattening into `categories`, `category_products`, `category_subcategories`?
4. Does the archived `oe_main.sql` run at all on Oracle 26ai Free (needed only if OE is to be included in the verification profile)?

# Cheapest experiment
* (1) `python3 -c "import xml.etree.ElementTree as E,glob;[print(f, [c.tag for c in E.parse(f).getroot()]) for f in glob.glob('order_entry/2002/*/*.xml')[:3]]"` plus `xmllint --schema purchaseOrder.xsd` on one file; decide by the coordinator's appetite for a 132-row XML table.
* (2) On `mysql:9.7`: `SELECT ST_Latitude(ST_GeomFromText('POINT(40.485424 -86.13631)', 4326)), ST_Longitude(ST_GeomFromText('POINT(40.485424 -86.13631)', 4326, 'axis-order=lat-long'));`.
* (3) `grep -c "INSERT INTO categories_tab" oc_popul.sql` (22) and read the 22 constructor calls (≈ 7 KB).
* (4) Run `oe_main.sql` inside `gvenzl/oracle-free:23.26.3-full` with HR installed; record the first error.

# Resolves
[OE dataset record](/datasets/oracle-oe-pm-ix.md) optional scope; nothing blocks the core relational conversion.
