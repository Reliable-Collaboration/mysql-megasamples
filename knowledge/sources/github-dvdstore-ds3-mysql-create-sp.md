---
type: Source
title: ds3/mysqlds3/build/mysqlds3_create_sp.sql (MySQL stored procedures)
description: Only four procedures exist in the MySQL kit - NEW_CUSTOMER, NEW_MEMBER, NEW_PROD_REVIEW, NEW_REVIEW_HELPFULNESS; the browse/login/purchase logic lives in the PHP pages and the Oracle kit.
resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/build/mysqlds3_create_sp.sql
tags:
- dvdstore
- ds3
- mysql
- procedures
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/build/mysqlds3_create_sp.sql
  title: mysqlds3_create_sp.sql (5/27/15)
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/build/mysqlds3_create_trigger2.sql
  title: mysqlds3_create_trigger2.sql
  accessed: "2026-09-02"
---

# What was read
Both scripts in full, accessed 2026-09-02.

# Relevant excerpt
* `Delimiter $` then `CREATE PROCEDURE DS3.NEW_CUSTOMER(IN firstname_in varchar(50), ... IN gender_in varchar(1), OUT customerid_out INT)` - inserts if USERNAME unused, returns `last_insert_id()` else 0.
* `DS3.NEW_MEMBER(IN customerid_in int, IN membershiplevel_in int, OUT customerid_out int)` - inserts MEMBERSHIP with `SYSDATE()` as EXPIREDATE.
* `DS3.NEW_PROD_REVIEW(prod_id_in, stars_in, customerid_in, review_summary_in VARCHAR(50), review_text_in VARCHAR(1000), OUT review_id_out)` - INSERT then `COMMIT;`.
* `DS3.NEW_REVIEW_HELPFULNESS(review_id_in, customerid_in, review_helpfulness_in, OUT review_helpfulness_id_out)` - INSERT then `COMMIT;`.
* mysqlds3_create_trigger2.sql begins with the comment "// Doesn't work yet!!!" and defines `CREATE TRIGGER RESTOCK BEFORE UPDATE ON DS3.INVENTORY ... INSERT INTO DS3.REORDER(PROD_ID, DATE_LOW, QUAN_LOW) VALUES(60, CURDATE(), 8);` (hard-coded values). It is not called by mysqlds3_create_all.sh.

# What it was used to decide
Programmable-object plan in [Dell DVD Store](/datasets/dell-dvd-store.md): port 4 procedures, drop the broken trigger.
