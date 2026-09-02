---
type: Source
title: Oracle Database Sample Schemas guide (docs.oracle.com /23/comsc/, now serving the 26ai edition)
description: Official schema overview, install prerequisites (SQLcl mandatory for SH), and the per-table column descriptions for HR, CO, SH, OE and PM.
resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/comsc/
tags: [oracle, sample-schemas, documentation]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/comsc/index.html
    title: Title page — "Database Sample Schemas, 26ai, G43102-02, March 2026"
    accessed: "2026-09-02"
  - resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/comsc/toc.htm
    title: Table of contents
    accessed: "2026-09-02"
  - resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/comsc/introduction-to-sample-schemas.html
    title: Introduction to Sample Schemas
    accessed: "2026-09-02"
  - resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/comsc/installing-sample-schemas.html
    title: Installation of the Sample Schemas
    accessed: "2026-09-02"
  - resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/comsc/HR-sample-schema-table-descriptions.html
    title: HR table descriptions (+ HR-sample-schema-scripts-and-objects.html)
    accessed: "2026-09-02"
  - resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/comsc/co-table-desciptions.html
    title: CO table descriptions (+ co-schema.html)
    accessed: "2026-09-02"
  - resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/comsc/SH-sample-schema-table-descriptions.html
    title: SH table descriptions (+ SH-sample-schema-scripts-and-objects.html)
    accessed: "2026-09-02"
  - resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/comsc/OE-sample-schema-table-descriptions.html
    title: OE table descriptions (+ OE-sample-schema-scripts-and-objects.html)
    accessed: "2026-09-02"
  - resource: https://docs.oracle.com/en/database/oracle/oracle-database/23/comsc/PM-sample-schema-table-descriptions.html
    title: PM table descriptions
    accessed: "2026-09-02"
---

# What was read
The pages listed above, 2026-09-02. Note: the `/23/comsc/` path currently serves the **26ai** edition of the guide (title page "Database Sample Schemas 26ai, G43102-02, March 2026"); the content matches the v23.3 scripts.

# Relevant excerpt
* Introduction: "Schema Human Resources (`hr`) is useful for introducing basic topics." / "Schema Customer Orders (`co`) is a modern schema useful for demos of e-commerce transactions. It allows the storage of semi-structured data using JSON." / "Schema Sales History (`sh`) is designed to allow for demos with large amounts of data." / "**Note:** The `oe` schema is no longer updated, but is still available." (same note for `oc` and `pm`) / "**Note:** The Business Intelligence (`bi`), Information Exchange (`ix`), and Shipping (`qs`) schemas are no longer available."
* Installation: latest release at `https://github.com/oracle/db-sample-schemas/releases/latest` (old org name; redirects to oracle-samples); "To install or uninstall the `sh` schema, you must use SQLcl, SQL Developer, or Visual Studio Code with the Oracle SQL Developer extension. You cannot use SQL*Plus to install the `sh` schema."; the `*_install.sql` scripts drop and recreate the user (reset = re-install).
* HR objects page: tables countries, departments, employees, jobs, job_history, locations, regions; sequences departments_seq, employees_seq, locations_seq; procedures add_job_history, secure_dml; triggers secure_employees, update_job_history; view emp_details_view; 19 indexes. Column types as in hr_create.sql (e.g. EMPLOYEES.SALARY NUMBER(8,2), COMMISSION_PCT NUMBER(2,2), HIRE_DATE DATE, COUNTRIES.COUNTRY_ID CHAR(2), COUNTRY_NAME VARCHAR2(60)).
* CO pages: tables customers, stores, products, orders, order_items, shipments, inventory; views customer_order_products, store_orders, product_reviews, product_orders; column types: `CUSTOMER_ID INTEGER` "Primary Key (auto-generated if NULL)", `ORDER_TMS TIMESTAMP(6)`, `PRODUCT_DETAILS BLOB`, `LOGO BLOB`, `LATITUDE/LONGITUDE NUMBER(9,6)`, `UNIT_PRICE NUMBER(10,2)`, `EMAIL_ADDRESS VARCHAR2(255 CHAR)`. (No `TIMESTAMP WITH TIME ZONE` column exists in CO.)
* SH pages: tables channels, countries, customers, products, promotions, times; partitioned tables costs, sales; view profits; materialized views cal_month_sales_mv, fweek_pscat_sales_mv; dimensions channels_dim, customers_dim, products_dim, promotions_dim, times_dim; partitioned (bitmap) indexes costs_prod_bix, costs_time_bix, sales_channel_bix, sales_cust_bix, sales_prod_bix, sales_promo_bix, sales_time_bix; other indexes incl. `dr$sup_text_idx$x`, `sup_text_idx`, `customers_gender_bix`, `customers_marital_bix`, `customers_yob_bix`, `products_prod_status_bix`, `fw_psc_s_mv_*_bix`. Column types: SALES(PROD_ID NUMBER(6), CUST_ID NUMBER, TIME_ID DATE, CHANNEL_ID NUMBER(1), PROMO_ID NUMBER(6), QUANTITY_SOLD NUMBER(3), AMOUNT_SOLD NUMBER(10,2)); COSTS(UNIT_COST/UNIT_PRICE NUMBER(10,2)); CUSTOMERS.CUST_GENDER CHAR(1), CUST_YEAR_OF_BIRTH NUMBER(4), CUST_CREDIT_LIMIT NUMBER; TIMES.CALENDAR_QUARTER_DESC CHAR(7). The docs pages state no row counts.
* OE pages: tables customers, inventories, orders, order_items, product_descriptions, product_information, warehouses and "Table `OE.purchaseorder` is an object-relational table with `XMLType` data. The data conforms to XML schema `purchaseOrder.xsd`."; `CUST_ADDRESS CUST_ADDRESS_TYP`, `PHONE_NUMBERS PHONE_LIST_TYP`, `CUST_GEO_LOCATION MDSYS.SDO_GEOMETRY`, `ORDER_DATE TIMESTAMP(6) WITH LOCAL TIME ZONE`, `TRANSLATED_NAME NVARCHAR2(50)`, `WARRANTY_PERIOD INTERVAL YEAR(2) TO MONTH`, `WAREHOUSE_SPEC SYS.XMLTYPE` ("top-level element `Warehouse` and child elements: `Building`, `Area`, `Docks`, `DockType`, `WaterAccess`, `RailAccess`, `Parking`, and `VClearance`"), `WH_GEO_LOCATION MDSYS.SDO_GEOMETRY`. OE object list includes function `get_phone_number_f`, sequence `orders_seq`, triggers `insert_ord_line, orders_items_trg, orders_trg`, 28 object types (incl. `xdbpo_*`), views `account_managers, bombay_inventory, customers_view, deptview, oc_corporate_customers, oc_customers, oc_inventories, oc_orders, oc_product_information, orders_view, products, product_prices, sydney_inventory, toronto_inventory`.
* PM page: PRINT_MEDIA columns PRODUCT_ID NUMBER(6), AD_ID NUMBER(6), AD_COMPOSITE BLOB, AD_SOURCETEXT CLOB, AD_FINALTEXT CLOB, AD_FLTEXTN NCLOB, AD_TEXTDOCS_NTAB TEXTDOC_TAB, AD_PHOTO BLOB, AD_GRAPHIC BFILE, AD_HEADER ADHEADER_TYP.

# What it was used to decide
Current-vs-archived status and column types in all four Oracle dataset records; the "SH needs SQLcl" fact in the [conversion path decision](/decisions/oracle-conversion-path.md).
