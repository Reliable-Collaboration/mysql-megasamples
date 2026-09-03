-- Programmable objects for AdventureWorks LT, hand-translated from instawltdb.sql.
--
-- The T-SQL originals are statement-level triggers wrapped in TRY/CATCH, using the `inserted`
-- pseudo-table, `UPDATE(column)` and `@@ROWCOUNT`. None of that exists in MySQL, so these are
-- rewritten as row triggers that reproduce the same effect. Two divergences are worth knowing:
--
--  * `UPDATE(col)` in T-SQL means "the column appeared in the SET list", whether or not its value
--    changed. MySQL cannot see the statement, so these compare values instead.
--  * The upstream triggers do not fire during the install, because BULK INSERT does not fire
--    triggers unless asked to. These are created after the data is loaded, for the same reason.
--
-- ufnGetCustomerInformation and ufnGetAllCategories are table-valued functions, which MySQL does not
-- have. The second one returns exactly what the vGetAllCategories view returns, and the first is a
-- single-row lookup on customer; neither is recreated. See datasets/adventureworks_lt/convert.py.

DELIMITER $$

-- dbo.ufnGetSalesOrderStatusText
CREATE FUNCTION `ufngetsalesorderstatustext`(`status` TINYINT UNSIGNED)
RETURNS VARCHAR(15)
DETERMINISTIC
BEGIN
    RETURN CASE `status`
        WHEN 1 THEN 'In process'
        WHEN 2 THEN 'Approved'
        WHEN 3 THEN 'Backordered'
        WHEN 4 THEN 'Rejected'
        WHEN 5 THEN 'Shipped'
        WHEN 6 THEN 'Cancelled'
        ELSE '** Invalid **'
    END;
END$$

-- SalesLT.uSalesOrderHeader: bump RevisionNumber unless Status or RevisionNumber is being set.
-- The original is an AFTER UPDATE trigger that updates its own table, which MySQL forbids; a BEFORE
-- UPDATE trigger writing NEW has the same result and is the idiomatic form.
CREATE TRIGGER `usalesorderheader` BEFORE UPDATE ON `salesorderheader`
FOR EACH ROW
BEGIN
    IF NEW.`status` <=> OLD.`status` AND NEW.`revisionnumber` <=> OLD.`revisionnumber` THEN
        SET NEW.`revisionnumber` = OLD.`revisionnumber` + 1;
    END IF;
END$$

-- SalesLT.iduSalesOrderDetail: keep SalesOrderHeader.SubTotal equal to the sum of its line totals.
-- One T-SQL trigger covers INSERT, DELETE and UPDATE; MySQL needs one trigger per event.
CREATE TRIGGER `idusalesorderdetail_insert` AFTER INSERT ON `salesorderdetail`
FOR EACH ROW
BEGIN
    UPDATE `salesorderheader` SET `subtotal` =
        (SELECT COALESCE(SUM(`linetotal`), 0) FROM `salesorderdetail`
         WHERE `salesorderid` = NEW.`salesorderid`)
    WHERE `salesorderid` = NEW.`salesorderid`;
END$$

CREATE TRIGGER `idusalesorderdetail_delete` AFTER DELETE ON `salesorderdetail`
FOR EACH ROW
BEGIN
    UPDATE `salesorderheader` SET `subtotal` =
        (SELECT COALESCE(SUM(`linetotal`), 0) FROM `salesorderdetail`
         WHERE `salesorderid` = OLD.`salesorderid`)
    WHERE `salesorderid` = OLD.`salesorderid`;
END$$

CREATE TRIGGER `idusalesorderdetail_update` AFTER UPDATE ON `salesorderdetail`
FOR EACH ROW
BEGIN
    UPDATE `salesorderheader` SET `subtotal` =
        (SELECT COALESCE(SUM(`linetotal`), 0) FROM `salesorderdetail`
         WHERE `salesorderid` = NEW.`salesorderid`)
    WHERE `salesorderid` = NEW.`salesorderid`;
    IF OLD.`salesorderid` <> NEW.`salesorderid` THEN
        UPDATE `salesorderheader` SET `subtotal` =
            (SELECT COALESCE(SUM(`linetotal`), 0) FROM `salesorderdetail`
             WHERE `salesorderid` = OLD.`salesorderid`)
        WHERE `salesorderid` = OLD.`salesorderid`;
    END IF;
END$$

DELIMITER ;
