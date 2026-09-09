"""The verification adapter for MySQL: every stage's questions, answered with information_schema
and the canonical digest in SQL (megasamples/canon.py)."""
from megasamples import canon
from megasamples.engines.mysql import server as db


class MySQLAdapter:
    name = "mysql"

    def supports(self, stage):
        return True

    def tables(self, schema):
        return [r[0] for r in db.rows(
            "SELECT table_name FROM information_schema.tables "
            f"WHERE table_schema='{schema}' AND table_type='BASE TABLE' ORDER BY table_name")]

    def columns(self, schema, table):
        return [(r[0], r[1]) for r in db.rows(
            "SELECT column_name, data_type FROM information_schema.columns "
            f"WHERE table_schema='{schema}' AND table_name='{table}' ORDER BY ordinal_position")]

    def count(self, schema, table):
        return int(db.rows(f"SELECT COUNT(*) FROM `{schema}`.`{table}`")[0][0])

    def fingerprint(self, schema, table, cols):
        row = db.rows(canon.fingerprint_sql(schema, table, cols))[0]
        return int(row[0]), int(row[1]), int(row[2])

    def foreign_keys(self, schema):
        # kcu.referenced_table_schema, not the constraint's own schema: Oracle OE's orders and
        # customers reference oracle_hr, and joining against the wrong database finds no table
        return db.rows(
            "SELECT rc.constraint_name, rc.table_name, kcu.column_name, "
            "kcu.referenced_table_schema, rc.referenced_table_name, "
            "kcu.referenced_column_name FROM information_schema.referential_constraints rc "
            "JOIN information_schema.key_column_usage kcu ON kcu.constraint_name=rc.constraint_name "
            "AND kcu.constraint_schema=rc.constraint_schema "
            f"WHERE rc.constraint_schema='{schema}' ORDER BY 1,3")

    def orphans(self, schema, table, col, rschema, rtable, rcol):
        return int(db.rows(
            f"SELECT COUNT(*) FROM `{schema}`.`{table}` c LEFT JOIN `{rschema}`.`{rtable}` p "
            f"ON c.`{col}` = p.`{rcol}` WHERE c.`{col}` IS NOT NULL AND p.`{rcol}` IS NULL")[0][0])

    def indexes(self, schema):
        out = {}
        for table, index, nonuniq, itype, cols in db.rows(
                "SELECT table_name, index_name, MAX(non_unique), MAX(index_type), "
                "GROUP_CONCAT(column_name ORDER BY seq_in_index) "
                f"FROM information_schema.statistics WHERE table_schema='{schema}' "
                "GROUP BY table_name, index_name ORDER BY table_name, index_name"):
            out.setdefault(table, {})[index] = {
                "unique": nonuniq == "0", "type": itype, "columns": cols.split(",")}
        return out

    def carries_index(self, spec):
        return True

    def explain_json(self, schema, query):
        return db.sql(f"EXPLAIN FORMAT=JSON {query}", database=schema)

    def query_text(self, schema, query):
        return db.sql(query, database=schema).strip()
