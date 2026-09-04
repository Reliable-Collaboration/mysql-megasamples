#!/usr/bin/env python3
"""NYC TLC taxi trips (January 2025) + the zone lookup -> MySQL.

Two modes, because the two colours are two tiers of the same database:

  convert.py <downloads> <out.sql>            green trips + the zone lookup (core, 48,326 rows)
  convert.py <downloads> <out.sql> --yellow   yellow trips only, appended (extended, 3,475,226)

The trips are Parquet, read with DuckDB and written as contract TSV. Three things the record calls
out are done deliberately rather than by default: the timestamps are local wall-clock
(`isAdjustedToUTC=false`), so they become `DATETIME(6)` and are never passed through a session time
zone; the money columns become `DECIMAL(10,2)`, and the converter checks the totals against DuckDB's
own sum of the source so the narrowing cannot go unnoticed; and the dirty rows the archive is known
for are kept, because the TLC makes no accuracy claim about data it did not create.

The two colours have different columns *in a different order* (record hazard 7), so every projection
here is by name. Yellow's fee column is `Airport_fee` with a capital A in 2025+ files and lower case
before that, while the data dictionary spells it lower case (hazard 2) -- it is normalised to
`airport_fee` on the way in.

Record: knowledge/datasets/nyc-tlc.md
"""
import os, sys

import duckdb

DATABASE = "nyc_taxi"
ZONES = "taxi_zone_lookup.csv"
MONTH = ("2025-01-01", "2025-01-31")

# (MySQL column, MySQL type, the DuckDB expression that produces it)
GREEN_COLUMNS = [
    ("vendorid", "SMALLINT", '"VendorID"'),
    ("pickup_datetime", "DATETIME(6) NOT NULL", '"lpep_pickup_datetime"'),
    ("dropoff_datetime", "DATETIME(6) NOT NULL", '"lpep_dropoff_datetime"'),
    ("store_and_fwd_flag", "CHAR(1)", '"store_and_fwd_flag"'),
    ("ratecodeid", "SMALLINT", '"RatecodeID"'),
    ("pulocationid", "SMALLINT", '"PULocationID"'),
    ("dolocationid", "SMALLINT", '"DOLocationID"'),
    ("passenger_count", "SMALLINT", '"passenger_count"'),
    ("trip_distance", "DOUBLE", '"trip_distance"'),
    ("fare_amount", "DECIMAL(10,2)", '"fare_amount"'),
    ("extra", "DECIMAL(10,2)", '"extra"'),
    ("mta_tax", "DECIMAL(10,2)", '"mta_tax"'),
    ("tip_amount", "DECIMAL(10,2)", '"tip_amount"'),
    ("tolls_amount", "DECIMAL(10,2)", '"tolls_amount"'),
    ("ehail_fee", "DECIMAL(10,2)", '"ehail_fee"'),
    ("improvement_surcharge", "DECIMAL(10,2)", '"improvement_surcharge"'),
    ("total_amount", "DECIMAL(10,2)", '"total_amount"'),
    ("payment_type", "SMALLINT", '"payment_type"'),
    ("trip_type", "SMALLINT", '"trip_type"'),
    ("congestion_surcharge", "DECIMAL(10,2)", '"congestion_surcharge"'),
    ("cbd_congestion_fee", "DECIMAL(10,2)", '"cbd_congestion_fee"'),
]
YELLOW_COLUMNS = [
    ("vendorid", "SMALLINT", '"VendorID"'),
    ("pickup_datetime", "DATETIME(6) NOT NULL", '"tpep_pickup_datetime"'),
    ("dropoff_datetime", "DATETIME(6) NOT NULL", '"tpep_dropoff_datetime"'),
    ("store_and_fwd_flag", "CHAR(1)", '"store_and_fwd_flag"'),
    ("ratecodeid", "SMALLINT", '"RatecodeID"'),
    ("pulocationid", "SMALLINT", '"PULocationID"'),
    ("dolocationid", "SMALLINT", '"DOLocationID"'),
    ("passenger_count", "SMALLINT", '"passenger_count"'),
    ("trip_distance", "DOUBLE", '"trip_distance"'),
    ("fare_amount", "DECIMAL(10,2)", '"fare_amount"'),
    ("extra", "DECIMAL(10,2)", '"extra"'),
    ("mta_tax", "DECIMAL(10,2)", '"mta_tax"'),
    ("tip_amount", "DECIMAL(10,2)", '"tip_amount"'),
    ("tolls_amount", "DECIMAL(10,2)", '"tolls_amount"'),
    ("improvement_surcharge", "DECIMAL(10,2)", '"improvement_surcharge"'),
    ("total_amount", "DECIMAL(10,2)", '"total_amount"'),
    ("payment_type", "SMALLINT", '"payment_type"'),
    ("congestion_surcharge", "DECIMAL(10,2)", '"congestion_surcharge"'),
    # hazard 2: the file says `Airport_fee`, the data dictionary says `airport_fee`
    ("airport_fee", "DECIMAL(10,2)", '"Airport_fee"'),
    ("cbd_congestion_fee", "DECIMAL(10,2)", '"cbd_congestion_fee"'),
]

GREEN = {"table": "green_trips", "parquet": "green_tripdata_2025-01.parquet",
         "columns": GREEN_COLUMNS, "colour": "green (boro)"}
YELLOW = {"table": "yellow_trips", "parquet": "yellow_tripdata_2025-01.parquet",
          "columns": YELLOW_COLUMNS, "colour": "yellow (medallion)"}


def quoted(path):
    return path.replace("'", "''")


def measure(con, spec, parquet, zones):
    """The three source sums, the row count, and the precondition for the foreign keys."""
    money = [c for c, t, _ in spec["columns"] if t.startswith("DECIMAL")]
    rows = con.execute(f"SELECT COUNT(*) FROM read_parquet('{parquet}')").fetchone()[0]
    totals = con.execute(
        f"SELECT ROUND(SUM(total_amount), 2), ROUND(SUM(fare_amount), 2), "
        f"ROUND(SUM(trip_distance), 2) FROM read_parquet('{parquet}')").fetchone()
    # DECIMAL(10,2) is only lossless if no source value needs a third decimal; MySQL would round
    # each value on the way in and the totals would then disagree for a reason nothing reports
    over = con.execute(
        "SELECT " + " + ".join(
            f'SUM(CASE WHEN {expr} IS NOT NULL AND ROUND({expr}, 2) <> {expr} THEN 1 ELSE 0 END)'
            for c, t, expr in spec["columns"] if c in money)
        + f" FROM read_parquet('{parquet}')").fetchone()[0]
    if over:
        sys.exit(f"{spec['parquet']}: {over} money value(s) need more than two decimals; "
                 f"DECIMAL(10,2) would round them and the pinned sums would not match the source")
    outside = con.execute(
        f"SELECT COUNT(*) FROM read_parquet('{parquet}') t WHERE "
        f't."PULocationID" NOT IN (SELECT "LocationID" FROM read_csv(\'{zones}\', header=true)) '
        f'OR t."DOLocationID" NOT IN (SELECT "LocationID" FROM read_csv(\'{zones}\', header=true))'
    ).fetchone()[0]
    return rows, totals, outside


def write_tsv(con, spec, parquet, context):
    projection = ", ".join(f"{expr} AS {name}" for name, _, expr in spec["columns"])
    con.execute(f"COPY (SELECT {projection} FROM read_parquet('{parquet}')) "
                f"TO '{quoted(os.path.join(context, spec['table'] + '.tsv'))}' "
                "(FORMAT CSV, DELIMITER '\t', HEADER false, NULLSTR '\\N', QUOTE '', ESCAPE '')")


def trip_table(spec, outside):
    """The CREATE TABLE for one colour. Same shape for both; only the column list differs."""
    table = spec["table"]
    columns = ",\n".join(f"  `{name}` {mysql}" for name, mysql, _ in spec["columns"])
    fk = ("" if outside else
          f",\n  CONSTRAINT `fk_{table}_pu` FOREIGN KEY (`pulocationid`) "
          f"REFERENCES `taxi_zone` (`locationid`),\n"
          f"  CONSTRAINT `fk_{table}_do` FOREIGN KEY (`dolocationid`) "
          f"REFERENCES `taxi_zone` (`locationid`)")
    return f"""-- The trip archive has no natural key: two identical trips by one vendor in the same second are
-- indistinguishable and no trip identifier is published, so the primary key is a surrogate.
-- Timestamps are local wall-clock (the Parquet says isAdjustedToUTC=false), which is why they are
-- DATETIME and not TIMESTAMP.
CREATE TABLE `{table}` (
  `trip_id` INT NOT NULL AUTO_INCREMENT,
{columns},
  PRIMARY KEY (`trip_id`),
  KEY `ix_{table}_pickup` (`pickup_datetime`),
  KEY `ix_{table}_pu` (`pulocationid`),
  KEY `ix_{table}_do` (`dolocationid`){fk}
) COMMENT = '{spec["colour"]} taxi trips for 2025-01; dirty rows are kept deliberately';"""


def load_statement(spec, context):
    """The container path follows the staging directory, which differs between the two tiers:
    the core dataset stages into /context/nyc_taxi, the yellow tier into /context/nyc_taxi_yellow."""
    names = ", ".join(f"`{c}`" for c, _, _ in spec["columns"])
    inside = f"/context/{os.path.basename(context)}"
    return (f"LOAD DATA LOCAL INFILE '{inside}/{spec['table']}.tsv' INTO TABLE `{spec['table']}`\n"
            f"  CHARACTER SET utf8mb4 ({names});")


def suspect_view(spec, name):
    return f"""-- The archive is well known for out-of-range rows. They are kept -- the TLC states the data was not
-- created by the TLC and makes no representation as to its accuracy -- and this view names them.
CREATE SQL SECURITY INVOKER VIEW `{name}` AS
SELECT * FROM `{spec['table']}`
WHERE `passenger_count` = 0 OR `total_amount` <= 0 OR `trip_distance` <= 0
   OR `trip_distance` > 100 OR `dropoff_datetime` < `pickup_datetime`
   OR DATE(`pickup_datetime`) NOT BETWEEN '{MONTH[0]}' AND '{MONTH[1]}';"""


def zone_view(spec, name):
    return f"""CREATE SQL SECURITY INVOKER VIEW `{name}` AS
SELECT t.`trip_id`, t.`pickup_datetime`, t.`dropoff_datetime`, t.`trip_distance`,
       t.`total_amount`,
       pu.`borough` AS `pickup_borough`, pu.`zone` AS `pickup_zone`,
       do_.`borough` AS `dropoff_borough`, do_.`zone` AS `dropoff_zone`
FROM `{spec['table']}` t
LEFT JOIN `taxi_zone` pu ON pu.`locationid` = t.`pulocationid`
LEFT JOIN `taxi_zone` do_ ON do_.`locationid` = t.`dolocationid`;"""


def daily_view(spec, name):
    return f"""CREATE SQL SECURITY INVOKER VIEW `{name}` AS
SELECT DATE(`pickup_datetime`) AS `trip_date`, COUNT(*) AS `trips`,
       ROUND(SUM(`total_amount`), 2) AS `revenue`,
       ROUND(AVG(`trip_distance`), 4) AS `avg_distance`
FROM `{spec['table']}` GROUP BY DATE(`pickup_datetime`);"""


def report(spec, rows, totals, outside):
    print(f"  . {rows:,} {spec['colour']} trips from Parquet via DuckDB")
    print(f"  . source sums: total_amount {totals[0]:,}, fare_amount {totals[1]:,}, "
          f"trip_distance {totals[2]:,}")
    print(f"  . zone ids outside the lookup: {outside} -> foreign keys "
          f"{'enabled' if not outside else 'omitted'}")


def main():
    downloads, dest = sys.argv[1], sys.argv[2]
    yellow = "--yellow" in sys.argv[3:]
    spec = YELLOW if yellow else GREEN
    context = os.path.dirname(os.path.abspath(dest))
    zones = quoted(os.path.join(downloads, ZONES))
    parquet = quoted(os.path.join(downloads, spec["parquet"]))
    con = duckdb.connect()

    rows, totals, outside = measure(con, spec, parquet, zones)
    write_tsv(con, spec, parquet, context)

    if yellow:
        # the extended tier: the database, the zone lookup and green are already there
        out = f"""-- NYC TLC yellow taxi trips, January 2025, prepared by datasets/{DATABASE}/convert.py.
-- Extended tier: appended to an existing `{DATABASE}`, never baked into the image.
-- Upstream: NYC Taxi & Limousine Commission. See datasets/{DATABASE}/LICENSE.
SET NAMES utf8mb4;
USE `{DATABASE}`;
DROP VIEW IF EXISTS `v_yellow_zone`, `v_yellow_daily`, `v_suspect_yellow_trips`;
DROP TABLE IF EXISTS `yellow_trips`;

{trip_table(spec, outside)}

{load_statement(spec, context)}

{zone_view(spec, 'v_yellow_zone')}

{daily_view(spec, 'v_yellow_daily')}

{suspect_view(spec, 'v_suspect_yellow_trips')}
"""
        open(dest, "w", encoding="utf-8").write(out)
        with open(os.path.join(context, "baseline_yellow.txt"), "w") as fh:
            fh.write(f"total_amount={totals[0]}\nfare_amount={totals[1]}\n"
                     f"trip_distance={totals[2]}\n")
        report(spec, rows, totals, outside)
        return

    zone_rows = con.execute(f"SELECT COUNT(*) FROM read_csv('{zones}', header=true)").fetchone()[0]
    con.execute(f"""COPY (SELECT "LocationID", "Borough", "Zone", "service_zone"
                          FROM read_csv('{zones}', header=true) ORDER BY "LocationID")
                    TO '{quoted(os.path.join(context, 'taxi_zone.tsv'))}'
                    (FORMAT CSV, DELIMITER '\t', HEADER false, NULLSTR '\\N', QUOTE '', ESCAPE '')""")

    out = f"""-- NYC TLC green taxi trips, January 2025, prepared by datasets/{DATABASE}/convert.py.
-- Upstream: NYC Taxi & Limousine Commission. See datasets/{DATABASE}/LICENSE.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{DATABASE}`;
CREATE DATABASE `{DATABASE}` DEFAULT CHARACTER SET utf8mb4;
USE `{DATABASE}`;

CREATE TABLE `taxi_zone` (
  `locationid` SMALLINT NOT NULL,
  `borough` VARCHAR(30) NOT NULL,
  `zone` VARCHAR(60),
  `service_zone` VARCHAR(20),
  PRIMARY KEY (`locationid`),
  KEY `ix_taxi_zone_borough` (`borough`)
) COMMENT = 'TLC taxi zone lookup, 1..265 plus the unknown zones';

{trip_table(spec, outside)}

-- {'-' * 60}
-- data

LOAD DATA LOCAL INFILE '/context/{os.path.basename(context)}/taxi_zone.tsv' INTO TABLE `taxi_zone`
  CHARACTER SET utf8mb4 (`locationid`, `borough`, `zone`, `service_zone`);
{load_statement(spec, context)}

-- {'-' * 60}
-- view

{zone_view(spec, 'v_trip_zone')}

{daily_view(spec, 'v_green_daily')}

{suspect_view(spec, 'v_suspect_trips')}

SET SESSION foreign_key_checks = 1;
"""
    open(dest, "w", encoding="utf-8").write(out)
    with open(os.path.join(context, "baseline.txt"), "w") as fh:
        fh.write(f"total_amount={totals[0]}\nfare_amount={totals[1]}\ntrip_distance={totals[2]}\n")
    report(spec, rows, totals, outside)
    print(f"  . {zone_rows} taxi zones")


if __name__ == "__main__":
    main()
