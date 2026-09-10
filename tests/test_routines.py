"""The routine port (megasamples/port/routines.py): the scanner that keeps blocks whole, the
branch splitter, the type synonyms, and one procedure translated end to end without a server."""
from megasamples.port import model, routines, sqltranslate


def col(name, data_type, column_type=None, **kw):
    base = dict(name=name, data_type=data_type, column_type=column_type or data_type, nullable=True, default=None,
                extra="", generation=None, char_len=None, precision=None, scale=None, fsp=None, charset=None,
                collation=None, ordinal=0)
    base.update(kw)
    return model.Column(**base)


def database(routine):
    t = model.Table("s", "customers", columns=[col("customerid", "int"), col("username", "varchar", "varchar(50)", char_len=50)],
                    indexes=[])
    return model.Database("s", [t], [], [routine], [])


def test_scanner_splits_statements_only_at_block_depth_zero():
    body = "SET v = CONCAT(REPEAT('0', 8 - LENGTH(v)), v); DROP TABLE IF EXISTS a; IF a = 1 THEN SET b = IF(c, 1, 2); END IF; RETURN v"
    assert routines.split_statements(body) == [
        "SET v = CONCAT(REPEAT('0', 8 - LENGTH(v)), v)", "DROP TABLE IF EXISTS a",
        "IF a = 1 THEN SET b = IF(c, 1, 2); END IF", "RETURN v"]
    handler = "DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN IF 0 > 0 THEN ROLLBACK; END IF; CALL `p`(); END; START TRANSACTION; COMMIT"
    assert routines.split_statements(handler)[0].startswith("DECLARE EXIT HANDLER") and len(routines.split_statements(handler)) == 3
    assert routines.split_statements("SELECT 'a; b'; SELECT 2") == ["SELECT 'a; b'", "SELECT 2"]


def test_branches_are_found_below_nested_blocks_and_case_expressions():
    body = "x := 1; ELSEIF a = 2 THEN SET v = CASE p WHEN 1 THEN 'a' ELSE 'b' END; ELSE IF b THEN y := 2; ELSE y := 3; END IF;"
    branches = routines.split_branches(body)
    assert [c for c, _ in branches] == [None, "a = 2", None]
    assert "CASE p WHEN 1 THEN 'a' ELSE 'b' END" in branches[1][1] and "IF b THEN" in branches[2][1]


def test_type_synonyms_and_boolean_results():
    assert routines.pg_type("INTEGER") == "integer"
    assert routines.pg_type("DECIMAL(5,2)") == "numeric(5,2)"
    assert routines.pg_type("tinyint unsigned") == "smallint"
    assert routines.pg_type("tinyint(1)") == "smallint"
    assert routines.pg_type("tinyint(1)", boolean_for_tinyint1=True) == "boolean"
    assert routines.pg_type("datetime(3)") == "timestamp(3) without time zone"


def test_procedure_with_out_parameter_becomes_a_plpgsql_procedure():
    r = model.Routine(name="new_customer", kind="PROCEDURE",
                      params=[("IN", "username_in", "varchar(50)"), ("OUT", "customerid_out", "int")], returns=None,
                      body="begin\n  declare rows_returned int;\n  select count(*) into rows_returned from customers where username = username_in;\n"
                           "  if rows_returned = 0 then\n    insert into customers (username) values (username_in);\n"
                           "    select last_insert_id() into customerid_out;\n  else set customerid_out = 0;\n  end if;\nend",
                      deterministic=False, data_access="CONTAINS SQL")
    stmt, notes = routines.translate_routine(r, database(r), {})
    assert stmt.startswith('CREATE PROCEDURE "new_customer"(IN username_in character varying(50), OUT customerid_out integer) LANGUAGE plpgsql AS $body$')
    assert "DECLARE\n  rows_returned integer;" in stmt
    assert 'SELECT COUNT(*) FROM "customers" WHERE "username" = username_in INTO rows_returned;' in stmt
    assert "IF rows_returned = 0 THEN" in stmt and "SELECT LASTVAL() INTO customerid_out;" in stmt
    assert "  ELSE\n    customerid_out := 0;\n  END IF;" in stmt and notes == []


def test_function_with_handler_user_variable_and_returns():
    r = model.Routine(name="f", kind="FUNCTION", params=[("IN", "p", "int")], returns="tinyint(1)",
                      body="BEGIN\n  DECLARE v INT;\n  DECLARE EXIT HANDLER FOR NOT FOUND RETURN NULL;\n"
                           "  SELECT customerid INTO v FROM customers WHERE customerid = p;\n  SET @last = v;\n"
                           "  IF v > 0 THEN RETURN TRUE; ELSE RETURN FALSE; END IF;\nEND",
                      deterministic=False, data_access="READS SQL DATA")
    stmt, notes = routines.translate_routine(r, database(r), {})
    assert 'CREATE FUNCTION "f"(p integer) RETURNS boolean LANGUAGE plpgsql STABLE AS $body$' in stmt
    assert "PERFORM set_config('megasamples.last', (v)::text, false);" in stmt
    assert any("NOT FOUND" in n for n in notes) and any("set_config" in n for n in notes)


def test_result_set_procedure_needs_its_columns_measured_once():
    r = model.Routine(name="p", kind="PROCEDURE", params=[("IN", "p_id", "int"), ("OUT", "p_count", "int")], returns=None,
                      body="BEGIN\n SELECT username FROM customers WHERE customerid = p_id;\n"
                           " SELECT COUNT(*) FROM customers WHERE customerid = p_id INTO p_count;\nEND",
                      deterministic=False, data_access="READS SQL DATA")
    try:
        routines.translate_routine(r, database(r), {})
        assert False
    except routines.NotProbed:
        pass
    probed = {}
    stmt, notes = routines.translate_routine(r, database(r), probed, probe=lambda tr: [("username", "character varying(50)")])
    assert probed == {"p": [("username", "character varying(50)")]}
    assert 'RETURNS TABLE("username" character varying(50))' in stmt and "#variable_conflict use_column" in stmt
    assert "INTO p_count" not in stmt and any("OUT parameter" in n for n in notes)
    # the same statement comes out of the recorded columns without a probe
    again, _ = routines.translate_routine(r, database(r), probed)
    assert again == stmt


def test_unportable_statement_is_dropped_by_name():
    r = model.Routine(name="w", kind="PROCEDURE", params=[], returns=None,
                      body="BEGIN\n WHILE 1 = 1 DO SET @x = 1; END WHILE;\nEND", deterministic=False, data_access="CONTAINS SQL")
    statements, dropped, notes = routines.render(database(r), {})
    assert statements == [] and dropped == ["procedure w: statement outside the census: 'WHILE 1 = 1 DO SET @x = 1; END WHILE'"]
