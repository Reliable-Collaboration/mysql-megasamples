---
type: Source
title: Sakila Sample Database manual (dev.mysql.com, revision 84779)
description: The Oracle-hosted Sakila manual; sections read - index, installation, structure (tables, views, procedures, functions, triggers, address table), history, preface/legal notices.
resource: https://dev.mysql.com/doc/sakila/en/
tags:
- sakila
- mysql
- manual
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/sakila/en/
  title: Sakila Sample Database (index)
  accessed: "2026-09-02"
  version: "Document generated on: 2026-08-04 (revision: 84779)"
- resource: https://dev.mysql.com/doc/sakila/en/sakila-installation.html
  title: 4 Installation
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/sakila/en/sakila-structure-tables.html
  title: 5.1 Tables
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/sakila/en/sakila-structure-tables-address.html
  title: 5.1.2 The address Table
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/sakila/en/sakila-structure-views.html
  title: 5.2 Views
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/sakila/en/sakila-structure-procedures.html
  title: 5.3 Stored Procedures
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/sakila/en/sakila-structure-functions.html
  title: 5.4 Stored Functions
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/sakila/en/sakila-structure-triggers.html
  title: 5.5 Triggers
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/sakila/en/sakila-history.html
  title: 3 History
  accessed: "2026-09-02"
- resource: https://dev.mysql.com/doc/sakila/en/sakila-preface.html
  title: Preface and Legal Notices
  accessed: "2026-09-02"
---

# What was read
The HTML manual for the Sakila sample database, all sections listed in `sources`, accessed 2026-09-02. The index page states "Document generated on: 2026-08-04 (revision: 84779)".

# Relevant excerpt
* Installation: the archive "contains three files": `sakila-schema.sql` ("contains all the CREATE statements required to create the structure of the Sakila database including tables, views, stored procedures, and triggers"), `sakila-data.sql` ("contains the INSERT statements required to populate the structure ... along with definitions for triggers that must be created after the initial data load"), and `sakila.mwb` ("a MySQL Workbench data model"). "Sakila contains MySQL version specific comments, in that the sakila schema and data depends on the version of your MySQL server. For example, MySQL server 5.7.5 added support for spatial data indexing to InnoDB, so the address table will include a spatial-aware location column for MySQL 5.7.5 and higher." No checksum is published.
* Tables (16, alphabetical): actor, address, category, city, country, customer, film, film_actor, film_category, film_text, inventory, language, payment, rental, staff, store.
* Views (7): actor_info, customer_list, film_list, nicer_but_slower_film_list, sales_by_film_category, sales_by_store, staff_list.
* Stored procedures (3): film_in_stock, film_not_in_stock, rewards_report. Stored functions (3): get_customer_balance, inventory_held_by_customer, inventory_in_stock. Triggers (6): customer_create_date (customer), payment_date (payment), rental_date (rental), ins_film / upd_film / del_film (film, maintain film_text).
* address.location: "A Geometry column with a spatial index on it", "supported as of MySQL 5.7.5", `SPATIAL KEY idx_location`.
* History: development began early 2005, first official release March 2006; borrows film and actor names from the Dell DVD Store sample ("Three Approaches to MySQL Applications on Dell PowerEdge Servers").
* Legal notices (preface): documentation is Copyright Oracle and/or its affiliates and "is NOT distributed under a GPL license"; redistribution of the documentation is restricted (paraphrase). The .sql files are covered by the separate license page.

# What it was used to decide
[Sakila dataset record](/datasets/sakila.md) (object inventory, file list, spatial column); [Sakila conversion decision](/decisions/sakila-conversion-path.md).
