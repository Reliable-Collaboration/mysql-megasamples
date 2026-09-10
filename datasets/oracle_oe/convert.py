#!/usr/bin/env python3
"""Oracle Order Entry -> MySQL.

The relational core of OE, with its object-relational parts flattened: the address object becomes
five columns, the phone VARRAY a child table, the two SDO_GEOMETRY points a longitude/latitude pair,
and the XMLType warehouse spec both the raw document and the eight elements it holds. OC (object
views), PM (LOB media) and IX (advanced queues) are not shipped; see the record.

Every INSERT in the data files is positional, so the converter checks the upstream CREATE TABLE
column order before using it, and stops rather than shifting rows into the wrong columns.

Record: knowledge/datasets/oracle-oe-pm-ix.md
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import oeparse, schema
from megasamples.sources import plsql  # noqa: E402

DATABASE = "oracle_oe"
HR = "oracle_hr"
DDL_FILES = ["coe_v3.sql", "ccus_v3.sql", "cwhs_v3.sql", "cord_v3.sql"]
DATA_FILES = ["oe_p_pi.sql", "pwhs_v3.sql", "pcus_v3.sql", "pord_v3.sql",
              "oe_p_itm.sql", "oe_p_inv.sql", "loe_v3.sql"]
LANGUAGES = ("us ar ca cs d dk e el esa f frc hu i iw ja ko n nl pl pt ptb ro ru s sf sk th tr "
             "zhs zht").split()
# Every object the installed scripts create, and what this build does with it. The converter checks
# the scripts against this list so an object added upstream stops the build rather than vanishing.
OBJECTS = {
    "type cust_address_typ": "flattened into five customers columns",
    "type phone_list_typ": "flattened into the customer_phone_numbers table",
    "trigger insert_ord_line": "objects.sql",
    "function get_phone_number_f": "dropped: it indexed into the VARRAY, now a child table",
    "view products": "objects.sql (fixed to language US)",
    "view sydney_inventory": "objects.sql",
    "view bombay_inventory": "objects.sql",
    "view toronto_inventory": "objects.sql",
    "view product_prices": "objects.sql",
    "view orders_view": "objects.sql",
    "view customers_view": "objects.sql (phone columns by join)",
    "view account_managers": "objects.sql (WITH ROLLUP)",
    "synonym countries": "dropped: queries name oracle_hr directly",
    "synonym locations": "dropped: queries name oracle_hr directly",
    "synonym departments": "dropped: queries name oracle_hr directly",
    "synonym jobs": "dropped: queries name oracle_hr directly",
    "synonym employees": "dropped: queries name oracle_hr directly",
    "synonym job_history": "dropped: queries name oracle_hr directly",
}
OBJECT_RE = re.compile(r"(?im)^\s*CREATE\s+(?:OR\s+REPLACE\s+)?(?:UNIQUE\s+)?"
                       r"(VIEW|TRIGGER|FUNCTION|PROCEDURE|TYPE|SYNONYM|INDEX)\s+(\w+)")

SPEC_ELEMENTS = [("building", "Building"), ("area", "Area"), ("docks", "Docks"),
                 ("dock_type", "DockType"), ("water_access", "WaterAccess"),
                 ("rail_access", "RailAccess"), ("parking", "Parking"),
                 ("v_clearance", "VClearance")]


def quote(value):
    if value is None:
        return "NULL"
    return "'" + str(value).replace("\\", "\\\\").replace("'", "''") + "'"


def number(expr):
    expr = expr.strip()
    if expr.upper() == "NULL":
        return "NULL"
    if not re.fullmatch(r"[-+]?\d+(\.\d+)?", expr):
        raise SystemExit(f"expected a number, got {expr[:60]!r}")
    return expr


def timestamp(expr):
    """`TO_TIMESTAMP('16-AUG-07 02.34.12.234359 PM', 'DD-MON-RR HH.MI.SS.FF AM', ...)`.

    TIMESTAMP WITH LOCAL TIME ZONE normalises to the database time zone and renders in the session
    zone; these literals carry no zone at all, so they are stored as the wall-clock time written in
    the script and the divergence is recorded rather than guessed at.
    """
    c = oeparse.call(expr)
    if not c or c[0] != "to_timestamp":
        raise SystemExit(f"expected TO_TIMESTAMP, got {expr[:60]!r}")
    return quote(plsql.oracle_date_literal(oeparse.sql_string(c[1][0]),
                                           oeparse.sql_string(c[1][1])))


def warranty_months(expr):
    """`to_yminterval('+00-03')` -> 3. MySQL has no interval type."""
    if expr.strip().upper() == "NULL":
        return "NULL"
    c = oeparse.call(expr)
    if not c or c[0] != "to_yminterval":
        raise SystemExit(f"expected to_yminterval, got {expr[:60]!r}")
    m = re.fullmatch(r"([-+])(\d+)-(\d+)", oeparse.sql_string(c[1][0]).strip())
    if not m:
        raise SystemExit(f"unparsed year-month interval {expr[:60]!r}")
    months = int(m.group(2)) * 12 + int(m.group(3))
    return str(-months if m.group(1) == "-" else months)


def point(expr):
    """`MDSYS.SDO_GEOMETRY(2001, 8307, MDSYS.SDO_POINT_TYPE(x, y, NULL), NULL, NULL)` -> (x, y)."""
    if expr.strip().upper() == "NULL":
        return "NULL", "NULL"
    c = oeparse.call(expr)
    if not c or not c[0].endswith("sdo_geometry"):
        raise SystemExit(f"expected SDO_GEOMETRY, got {expr[:60]!r}")
    gtype, srid, pt = c[1][0].strip(), c[1][1].strip(), oeparse.call(c[1][2])
    if gtype != "2001" or srid != "8307":
        raise SystemExit(f"unexpected geometry {gtype}/{srid}: only WGS84 points are handled")
    if not pt or not pt[0].endswith("sdo_point_type"):
        raise SystemExit(f"expected SDO_POINT_TYPE, got {c[1][2][:60]!r}")
    return number(pt[1][0]), number(pt[1][1])


def check_objects(downloads):
    """Compare the scripts' programmable objects and indexes against what this build accounts for."""
    files = DDL_FILES + ["poe_v3.sql", "oe_views.sql", "cidx_v3.sql"]
    found, indexes = set(), set()
    for name in files:
        text = oeparse.preprocess(open(os.path.join(downloads, name), encoding="utf-8").read())
        for kind, obj in OBJECT_RE.findall(text):
            if kind.lower() == "index":
                indexes.add(obj.lower())
            else:
                found.add(f"{kind.lower()} {obj.lower()}")
    if found != set(OBJECTS):
        raise SystemExit(f"OE objects changed upstream; missing {sorted(set(OBJECTS) - found)}, "
                         f"unaccounted {sorted(found - set(OBJECTS))}")
    # the primary-key and unique indexes are declared with their tables in schema.py
    declared = {n for n, _, _ in schema.INDEXES} | {
        "customers_pk", "warehouses_pk", "order_items_pk", "order_items_uk", "order_pk",
        "prd_desc_pk", "inventory_ix"}
    if indexes != declared:
        raise SystemExit(f"OE indexes changed upstream; missing {sorted(declared - indexes)}, "
                         f"unaccounted {sorted(indexes - declared)}")


def check_upstream(downloads):
    """Fail if the upstream CREATE TABLE column order no longer matches what the data assumes."""
    text = "\n".join(oeparse.preprocess(open(os.path.join(downloads, f), encoding="utf-8").read())
                     for f in DDL_FILES)
    found = {}
    for m in re.finditer(r"(?is)CREATE\s+TABLE\s+(\w+)\s*\((.*?)\)\s*;", text):
        columns = []
        for item in plsql.split_top_level(m.group(2)):
            item = item.strip()
            if re.match(r"(?i)^(CONSTRAINT|PRIMARY|FOREIGN|UNIQUE|CHECK)\b", item):
                continue
            columns.append(item.split()[0].lower())
        found[m.group(1).lower()] = columns
    for table, expected in schema.UPSTREAM.items():
        if table not in found:
            raise SystemExit(f"{table} is no longer created by the OE scripts")
        if found[table] != expected:
            raise SystemExit(f"{table} column order changed upstream:\n"
                             f"  expected {expected}\n  found    {found[table]}")
    return found


def create_tables(comments):
    out = []
    for table, columns, extras in schema.TABLES:
        lines = []
        for name, definition in columns:
            comment = comments.get((table, name))
            lines.append(f"  `{name}` {definition}" + (f" COMMENT {quote(comment)}" if comment else ""))
        lines += [f"  {e}" for e in extras]
        table_comment = comments.get((table, None))
        suffix = f" COMMENT = {quote(table_comment)}" if table_comment else ""
        out.append(f"CREATE TABLE `{table}` (\n" + ",\n".join(lines) + f"\n){suffix};")
    return out


def read_comments(path):
    """`COMMENT ON TABLE oe.customers IS '...'` -> {(table, column or None): text}."""
    comments, text = {}, oeparse.preprocess(open(path, encoding="utf-8").read())
    for m in re.finditer(r"(?is)COMMENT\s+ON\s+(TABLE|COLUMN)\s+(?:oe\.)?([\w.]+)\s+IS\s+"
                         r"('(?:[^']|'')*')\s*;", text):
        target = m.group(2).lower().split(".")
        key = (target[0], target[1] if len(target) > 1 else None)
        comments[key] = m.group(3)[1:-1].replace("''", "'")
    return comments


def rows_from(downloads):
    """Parse every INSERT and UPDATE in the data files into rows keyed by MySQL table."""
    rows = {t: [] for t, _, _ in schema.TABLES}
    customers, warehouses, orders = {}, {}, {}
    seen = {}
    for filename in DATA_FILES + [f"oe_p_{l}.sql" for l in LANGUAGES]:
        for statement in oeparse.statements(os.path.join(downloads, filename)):
            table, columns, values = oeparse.values_of(statement)
            if table:
                seen[table] = seen.get(table, 0) + 1
                add_row(table, columns, values, rows, customers, warehouses, orders)
                continue
            apply_update(statement, customers, warehouses, orders)
    rows["customers"] = [customers[k] for k in sorted(customers)]
    rows["warehouses"] = [warehouses[k] for k in sorted(warehouses)]
    rows["orders"] = [orders[k] for k in sorted(orders)]
    return rows, seen


def add_row(table, columns, values, rows, customers, warehouses, orders):
    if table == "customers":
        cid = number(values[0])
        street, postal, city, state, country = ["NULL"] * 5
        address = oeparse.call(values[3])
        if address:
            street, postal, city, state, country = [
                quote(oeparse.sql_string(a)) if a.upper() != "NULL" else "NULL" for a in address[1]]
        phones = oeparse.call(values[4])
        if phones:
            for seq, phone in enumerate(phones[1], start=1):
                rows["customer_phone_numbers"].append([cid, str(seq), quote(oeparse.sql_string(phone))])
        lon, lat = point(values[10])
        customers[int(cid)] = [
            cid, quote(oeparse.sql_string(values[1])), quote(oeparse.sql_string(values[2])),
            street, postal, city, state, country,
            quote(oeparse.sql_string(values[5])), quote(oeparse.sql_string(values[6])),
            number(values[7].strip("'")), quote(oeparse.sql_string(values[8])),
            number(values[9].strip("'")), lon, lat, "NULL", "NULL", "NULL", "NULL"]
    elif table == "warehouses":
        wid = number(values[0])
        lon, lat = point(values[4])
        warehouses[int(wid)] = [wid, quote(oeparse.sql_string(values[2])), number(values[3]),
                                lon, lat, "NULL"] + ["NULL"] * len(SPEC_ELEMENTS)
    elif table == "orders":
        orders[int(number(values[0]))] = [
            number(values[0]), timestamp(values[1]), quote(oeparse.sql_string(values[2])),
            number(values[3]), number(values[4]), number(values[5]),
            number(values[6]), number(values[7])]
    elif table == "order_items":
        rows["order_items"].append([number(v) for v in values])
    elif table == "inventories":
        rows["inventories"].append([number(v) for v in values])
    elif table == "product_information":
        rows["product_information"].append([
            number(values[0]), quote(oeparse.sql_string(values[1])),
            quote(oeparse.sql_string(values[2])), number(values[3]), number(values[4]),
            warranty_months(values[5]), number(values[6]), quote(oeparse.sql_string(values[7])),
            number(values[8]), number(values[9]), quote(oeparse.sql_string(values[10]))])
    elif table == "product_descriptions":
        rows["product_descriptions"].append([
            number(values[0]), quote(oeparse.sql_string(values[1])),
            quote(oeparse.sql_string(values[2])), quote(oeparse.sql_string(values[3]))])
    elif table == "promotions":
        rows["promotions"].append([number(values[0]), quote(oeparse.sql_string(values[1]))])
    else:
        raise SystemExit(f"unhandled INSERT into {table}")


CUSTOMER_COLUMN = {c: i for i, (c, _) in enumerate(schema.TABLES[0][1])}
WAREHOUSE_COLUMN = {c: i for i, (c, _) in enumerate(schema.TABLES[2][1])}
ADDRESS_ATTRIBUTE = {"street_address": "cust_street_address", "postal_code": "cust_postal_code",
                     "city": "cust_city", "state_province": "cust_state_province",
                     "country_id": "cust_country_id"}


def apply_update(statement, customers, warehouses, orders):
    """Apply the scripts' post-load UPDATEs to the parsed rows.

    They are applied here rather than emitted as SQL because two of them read the address object
    (`c.cust_address.country_id`), which no longer exists as such once the address is flattened.
    """
    text = " ".join(statement.split())
    if not re.match(r"(?i)^UPDATE\b", text):
        if text and not re.match(r"(?i)^(COMMIT|ALTER\s+TABLE)\b", text):
            raise SystemExit(f"unhandled statement: {text[:90]}")
        return
    m = re.match(r"(?i)^UPDATE\s+(\w+)\s+(?:(?!SET\b)\w+\s+)?SET\s+(.*)$", text)
    if not m:
        raise SystemExit(f"unparsed UPDATE: {text[:90]}")
    table, rest = m.group(1).lower(), m.group(2).rstrip(";")
    split = re.split(r"(?i)\s+WHERE\s+", rest, maxsplit=1)
    assignments, where = split[0], (split[1] if len(split) > 1 else "")
    sets = {}
    for part in plsql.split_top_level(assignments):
        key, _, value = part.partition("=")
        sets[key.strip().split(".")[-1].lower()] = value.strip()
    if table == "warehouses":
        wid = int(re.search(r"warehouse_id\s*=\s*(\d+)", where).group(1))
        spec = oeparse.sql_string(sets["warehouse_spec"])
        row = warehouses[wid]
        row[WAREHOUSE_COLUMN["warehouse_spec_xml"]] = quote(spec)
        for column, element in SPEC_ELEMENTS:
            found = re.search(rf"<{element}>(.*?)</{element}>", spec, re.S)
            row[WAREHOUSE_COLUMN[column]] = quote(found.group(1).strip()) if found else "NULL"
    elif table == "orders":
        # "SET sales_rep_id = NULL WHERE order_mode = 'online'"
        mode = re.search(r"order_mode\s*=\s*'(\w+)'", where).group(1)
        for row in orders.values():
            if row[2] == quote(mode):
                row[6] = "NULL"
    elif table == "customers":
        target = re.search(r"customer_id\s*=\s*(\d+)", where)
        if target:
            chosen = [customers[int(target.group(1))]]
        else:
            chosen = [r for r in customers.values() if matches_address(r, where)]
            if not chosen:
                raise SystemExit(f"UPDATE matched no customers: {where[:80]}")
        for row in chosen:
            for column, value in sets.items():
                if column in ("date_of_birth",):
                    value = quote(plsql.oracle_date_literal(oeparse.sql_string(value), "DD-MON-RR"))
                elif value.startswith("'"):
                    value = quote(oeparse.sql_string(value))
                row[CUSTOMER_COLUMN[column]] = value
    else:
        raise SystemExit(f"unhandled UPDATE of {table}")


def matches_address(row, where):
    """Evaluate the address predicates of the account-manager UPDATEs against a flattened row."""
    for m in re.finditer(r"(?i)cust_address\.(\w+)\s*(=|IN)\s*(\([^)]*\)|'[^']*')", where):
        column = CUSTOMER_COLUMN[ADDRESS_ATTRIBUTE[m.group(1).lower()]]
        wanted = {v.strip() for v in m.group(3).strip("()").split(",")}
        if row[column] not in wanted:
            return False
    return True


def main():
    downloads, dest = sys.argv[1], sys.argv[2]
    check_upstream(downloads)
    check_objects(downloads)
    comments = read_comments(os.path.join(downloads, "cmnt_v3.sql"))
    rows, seen = rows_from(downloads)

    out = [f"""-- Oracle Order Entry, translated by datasets/{DATABASE}/convert.py.
-- Upstream: oracle-samples/db-sample-schemas (MIT). See datasets/{DATABASE}/LICENSE.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{DATABASE}`;
CREATE DATABASE `{DATABASE}` DEFAULT CHARACTER SET utf8mb4;
USE `{DATABASE}`;
"""]
    out += create_tables(comments)
    out.append(f"\n-- {'-' * 60}\n-- data\n")
    for table, columns, _ in schema.TABLES:
        names = ", ".join(f"`{c}`" for c, _ in columns)
        data = rows[table]
        for i in range(0, len(data), 200):
            chunk = ",\n".join("(" + ", ".join(r) + ")" for r in data[i:i + 200])
            out.append(f"INSERT INTO `{table}` ({names}) VALUES\n{chunk};")
    out.append(f"\n-- {'-' * 60}\n-- index\n")
    out += [f"CREATE INDEX `{name}` ON `{table}` {cols};" for name, table, cols in schema.INDEXES]
    out += [f"CREATE {kind}INDEX `{name}` ON `{table}` {cols};"
            for name, table, cols, kind in schema.ADDED_INDEXES]
    out.append(f"\n-- {'-' * 60}\n-- cross-database foreign keys to {HR}\n")
    out += [f"ALTER TABLE `orders` ADD CONSTRAINT `orders_sales_rep_fk` FOREIGN KEY (`sales_rep_id`)"
            f" REFERENCES `{HR}`.`employees` (`employee_id`) ON DELETE SET NULL;",
            f"ALTER TABLE `customers` ADD CONSTRAINT `customers_account_manager_fk` "
            f"FOREIGN KEY (`account_mgr_id`) REFERENCES `{HR}`.`employees` (`employee_id`) "
            f"ON DELETE SET NULL;",
            f"ALTER TABLE `warehouses` ADD CONSTRAINT `warehouses_location_fk` "
            f"FOREIGN KEY (`location_id`) REFERENCES `{HR}`.`locations` (`location_id`) "
            f"ON DELETE SET NULL;"]
    out.append(open(os.path.join(HERE, "objects.sql"), encoding="utf-8").read())
    out.append("SET SESSION foreign_key_checks = 1;\n")
    open(dest, "w", encoding="utf-8").write("\n".join(out))

    total = sum(len(v) for v in rows.values())
    print(f"  . translated {len(schema.TABLES)} tables, {total:,} rows "
          f"from {len(DATA_FILES) + len(LANGUAGES)} scripts")
    print(f"  . flattened {len(rows['customer_phone_numbers'])} phone numbers out of the "
          f"phone_list_typ VARRAY, and {len(rows['product_descriptions']):,} descriptions "
          f"in {len(LANGUAGES)} languages")
    print(f"  . applied {len(comments)} upstream comments")
    for name, action in sorted(OBJECTS.items()):
        if action.startswith("dropped"):
            print(f"  . {name}: {action}")


if __name__ == "__main__":
    main()
