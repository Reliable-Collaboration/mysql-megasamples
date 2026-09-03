
-- ------------------------------------------------------------
-- view
--
-- The seven OE views, hand-translated from oe_views.sql and poe_v3.sql. Four constructs have no
-- MySQL equivalent and are handled here rather than by a general translator:
--
--  * Oracle's `(+)` outer-join marker becomes a LEFT JOIN.
--  * `products` selects the description for `sys_context('USERENV','LANG')`, the session language.
--    MySQL has no such setting, so the view is fixed to 'US' and falls back to the untranslated
--    name and description, which is what the Oracle view does when a language is missing.
--    `TRANSLATE(x USING NCHAR_CS)` was the conversion to NCHAR and is simply dropped: every column
--    here is already utf8mb4.
--  * `customers_view` called get_phone_number_f(n, phone_numbers) to index into the VARRAY. With
--    the VARRAY flattened into customer_phone_numbers, each position is a LEFT JOIN instead, and
--    the function is not recreated.
--  * `account_managers` groups by ROLLUP, which MySQL spells `WITH ROLLUP`, and it reads countries
--    from the HR schema, which here is a second database.

CREATE VIEW `products` AS
SELECT i.`product_id`,
       d.`language_id`,
       COALESCE(d.`translated_name`, i.`product_name`) AS `product_name`,
       i.`category_id`,
       COALESCE(d.`translated_description`, i.`product_description`) AS `product_description`,
       i.`weight_class`,
       i.`warranty_months`,
       i.`supplier_id`,
       i.`product_status`,
       i.`list_price`,
       i.`min_price`,
       i.`catalog_url`
FROM   `product_information` i
LEFT JOIN `product_descriptions` d
       ON d.`product_id` = i.`product_id` AND d.`language_id` = 'US';

CREATE VIEW `sydney_inventory` AS
SELECT p.`product_id`, p.`product_name`, i.`quantity_on_hand`
FROM   `inventories` i
JOIN   `warehouses` w ON i.`warehouse_id` = w.`warehouse_id`
JOIN   `products` p ON p.`product_id` = i.`product_id`
WHERE  w.`warehouse_name` = 'Sydney';

CREATE VIEW `bombay_inventory` AS
SELECT p.`product_id`, p.`product_name`, i.`quantity_on_hand`
FROM   `inventories` i
JOIN   `warehouses` w ON i.`warehouse_id` = w.`warehouse_id`
JOIN   `products` p ON p.`product_id` = i.`product_id`
WHERE  w.`warehouse_name` = 'Bombay';

CREATE VIEW `toronto_inventory` AS
SELECT p.`product_id`, p.`product_name`, i.`quantity_on_hand`
FROM   `inventories` i
JOIN   `warehouses` w ON i.`warehouse_id` = w.`warehouse_id`
JOIN   `products` p ON p.`product_id` = i.`product_id`
WHERE  w.`warehouse_name` = 'Toronto';

CREATE VIEW `product_prices` AS
SELECT `category_id`,
       COUNT(*)          AS `#_of_products`,
       MIN(`list_price`) AS `low_price`,
       MAX(`list_price`) AS `high_price`
FROM   `product_information`
GROUP BY `category_id`;

-- the Oracle view casts the timestamp down to a DATE, losing the time of day
CREATE VIEW `orders_view` AS
SELECT `order_id`,
       DATE(`order_date`) AS `order_date`,
       `order_mode`, `customer_id`, `order_status`, `order_total`, `sales_rep_id`, `promotion_id`
FROM   `orders`;

CREATE VIEW `customers_view` AS
SELECT c.`customer_id`,
       c.`cust_first_name`,
       c.`cust_last_name`,
       c.`cust_street_address`   AS `street_address`,
       c.`cust_postal_code`      AS `postal_code`,
       c.`cust_city`             AS `city`,
       c.`cust_state_province`   AS `state_province`,
       co.`country_id`,
       co.`country_name`,
       co.`region_id`,
       c.`nls_language`,
       c.`nls_territory`,
       c.`credit_limit`,
       c.`cust_email`,
       p1.`phone_number` AS `primary_phone_number`,
       p2.`phone_number` AS `phone_number_2`,
       p3.`phone_number` AS `phone_number_3`,
       p4.`phone_number` AS `phone_number_4`,
       p5.`phone_number` AS `phone_number_5`,
       c.`account_mgr_id`,
       c.`geo_longitude` AS `location_x`,
       c.`geo_latitude`  AS `location_y`
FROM   `customers` c
LEFT JOIN `oracle_hr`.`countries` co ON c.`cust_country_id` = co.`country_id`
LEFT JOIN `customer_phone_numbers` p1 ON p1.`customer_id` = c.`customer_id` AND p1.`phone_seq` = 1
LEFT JOIN `customer_phone_numbers` p2 ON p2.`customer_id` = c.`customer_id` AND p2.`phone_seq` = 2
LEFT JOIN `customer_phone_numbers` p3 ON p3.`customer_id` = c.`customer_id` AND p3.`phone_seq` = 3
LEFT JOIN `customer_phone_numbers` p4 ON p4.`customer_id` = c.`customer_id` AND p4.`phone_seq` = 4
LEFT JOIN `customer_phone_numbers` p5 ON p5.`customer_id` = c.`customer_id` AND p5.`phone_seq` = 5;

CREATE VIEW `account_managers` AS
SELECT c.`account_mgr_id`      AS `acct_mgr`,
       cr.`region_id`          AS `region`,
       c.`cust_country_id`     AS `country`,
       c.`cust_state_province` AS `province`,
       COUNT(*)                AS `num_customers`
FROM   `customers` c
JOIN   `oracle_hr`.`countries` cr ON c.`cust_country_id` = cr.`country_id`
GROUP BY c.`account_mgr_id`, cr.`region_id`, c.`cust_country_id`, c.`cust_state_province`
WITH ROLLUP;

-- ------------------------------------------------------------
-- trigger
--
-- SalesLT's insert_ord_line numbers each new line within its order. The Oracle original assigns
-- :new.line_item_id from a SELECT over the same table; MySQL allows a BEFORE trigger to read its
-- own table and to write NEW, so this is a direct port. Created after the load, because it would
-- otherwise renumber the 665 rows the data files carry.
DELIMITER $$
CREATE TRIGGER `insert_ord_line` BEFORE INSERT ON `order_items`
FOR EACH ROW
BEGIN
    SET NEW.`line_item_id` = (SELECT COALESCE(MAX(`line_item_id`), 0) + 1
                              FROM `order_items` WHERE `order_id` = NEW.`order_id`);
END$$
DELIMITER ;
