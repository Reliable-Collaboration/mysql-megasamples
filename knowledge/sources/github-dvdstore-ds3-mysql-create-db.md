---
type: Source
title: ds3/mysqlds3/build/mysqlds3_create_db.sql (MySQL DDL)
description: The MySQL build script - CREATE DATABASE DS3 and 11 tables with engines and types; PRODUCTS is MyISAM; CATEGORIES seeded with 16 rows.
resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/build/mysqlds3_create_db.sql
tags:
- dvdstore
- ds3
- mysql
- ddl
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/build/mysqlds3_create_db.sql
  title: mysqlds3_create_db.sql ("Last updated 5/27/15")
  accessed: "2026-09-02"
---

# What was read
The whole script (4,038 bytes), accessed 2026-09-02.

# Relevant excerpt
* `DROP DATABASE IF EXISTS DS3; CREATE DATABASE DS3; USE DS3;` - no character set.
* CUSTOMERS: CUSTOMERID INT AUTO_INCREMENT PK, FIRSTNAME/LASTNAME/ADDRESS1/ADDRESS2/CITY/STATE VARCHAR(50), ZIP INT, COUNTRY VARCHAR(50), REGION TINYINT, EMAIL/PHONE VARCHAR(50), CREDITCARDTYPE INT, CREDITCARD VARCHAR(50), CREDITCARDEXPIRATION VARCHAR(50), USERNAME/PASSWORD VARCHAR(50), AGE TINYINT, INCOME INT, GENDER VARCHAR(1) - ENGINE=InnoDB.
* CUST_HIST(CUSTOMERID, ORDERID, PROD_ID) InnoDB; MEMBERSHIP(CUSTOMERID, MEMBERSHIPTYPE INT, EXPIREDATE DATE) InnoDB; ORDERS(ORDERID AUTO_INCREMENT PK, ORDERDATE DATE, CUSTOMERID INT NULL, NETAMOUNT/TAX/TOTALAMOUNT NUMERIC(12,2)) InnoDB; ORDERLINES(ORDERLINEID SMALLINT, ORDERID INT, PROD_ID INT, QUANTITY SMALLINT, ORDERDATE DATE) InnoDB; **PRODUCTS(PROD_ID AUTO_INCREMENT PK, CATEGORY TINYINT, TITLE VARCHAR(50), ACTOR VARCHAR(50), PRICE NUMERIC(12,2), SPECIAL TINYINT, COMMON_PROD_ID INT, MEMBERSHIP_ITEM INT) ENGINE = MyISAM**; REVIEWS(REVIEW_ID AUTO_INCREMENT PK, PROD_ID, REVIEW_DATE DATE, STARS INT, CUSTOMERID INT, REVIEW_SUMMARY VARCHAR(50), REVIEW_TEXT VARCHAR(1000)) InnoDB; REVIEWS_HELPFULNESS(REVIEWS_HELPFULNESS_ID AUTO_INCREMENT PK, REVIEW_ID, CUSTOMERID, HELPFULNESS INT) InnoDB; INVENTORY(PROD_ID PK, QUAN_IN_STOCK, SALES) InnoDB; CATEGORIES(CATEGORY TINYINT AUTO_INCREMENT PK, CATEGORYNAME VARCHAR(50)) InnoDB with 16 INSERTs (Action, Animation, Children, Classics, Comedy, Documentary, Drama, Family, Foreign, Games, Horror, Music, New, Sci-Fi, Sports, Travel); REORDER(PROD_ID, DATE_LOW, QUAN_LOW, DATE_REORDERED, QUAN_REORDERED, DATE_EXPECTED) InnoDB.

# What it was used to decide
DDL hazards (MyISAM, uppercase names, no charset) in [Dell DVD Store](/datasets/dell-dvd-store.md).
