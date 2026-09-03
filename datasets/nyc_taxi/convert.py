#!/usr/bin/env python3
"""NYC TLC green taxi trips (January 2025) + the zone lookup -> MySQL.

The trips are Parquet, read with DuckDB and written as contract TSV. Three things the record calls
out are done deliberately rather than by default: the timestamps are local wall-clock
(`isAdjustedToUTC=false`), so they become `DATETIME(6)` and are never passed through a session time
zone; the money columns become `DECIMAL(10,2)`, and the converter checks the totals against DuckDB's
own sum of the source so the narrowing cannot go unnoticed; and the dirty rows the archive is known
for are kept, because the TLC makes no accuracy claim about data it did not create.

Record: knowledge/datasets/nyc-tlc.md
"""
import os, sys

import duckdb

DATABASE = "nyc_taxi"
CONTEXT = "/context/nyc_taxi"
TRIPS = "green_tripdata_2025-01.parquet"
ZONES = "taxi_zone_lookup.csv"

# (MySQL column, MySQL type, the DuckDB expression that produces it)
TRIP_COLUMNS = [
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
MONEY = [c for c, t, _ in TRIP_COLUMNS if t.startswith("DECIMAL")]


def main():
    downloads, dest = sys.argv[1], sys.argv[2]
    context = os.path.dirname(os.path.abspath(dest))
    parquet = os.path.join(downloads, TRIPS).replace("'", "''")
    con = duckdb.connect()

    trips = con.execute(f"SELECT COUNT(*) FROM read_parquet('{parquet}')").fetchone()[0]
    # the sums are taken from the source before any narrowing, and compared after the load
    totals = con.execute(
        f"SELECT ROUND(SUM(total_amount), 2), ROUND(SUM(fare_amount), 2), "
        f"ROUND(SUM(trip_distance), 2) FROM read_parquet('{parquet}')").fetchone()

    projection = ", ".join(f"{expr} AS {name}" for name, _, expr in TRIP_COLUMNS)
    con.execute(f"COPY (SELECT {projection} FROM read_parquet('{parquet}')) "
                f"TO '{os.path.join(context, 'green_trips.tsv')}' "
                "(FORMAT CSV, DELIMITER '\t', HEADER false, NULLSTR '\\N', QUOTE '', ESCAPE '')")

    zones = os.path.join(downloads, ZONES).replace("'", "''")
    zone_rows = con.execute(f"SELECT COUNT(*) FROM read_csv('{zones}', header=true)").fetchone()[0]
    con.execute(f"""COPY (SELECT "LocationID", "Borough", "Zone", "service_zone"
                          FROM read_csv('{zones}', header=true) ORDER BY "LocationID")
                    TO '{os.path.join(context, 'taxi_zone.tsv')}'
                    (FORMAT CSV, DELIMITER '\t', HEADER false, NULLSTR '\\N', QUOTE '', ESCAPE '')""")

    # the record asks for this before a foreign key is defensible
    outside = con.execute(
        f"SELECT COUNT(*) FROM read_parquet('{parquet}') t WHERE "
        f't."PULocationID" NOT IN (SELECT "LocationID" FROM read_csv(\'{zones}\', header=true)) '
        f'OR t."DOLocationID" NOT IN (SELECT "LocationID" FROM read_csv(\'{zones}\', header=true))'
    ).fetchone()[0]

    columns = ",\n".join(f"  `{name}` {mysql}" for name, mysql, _ in TRIP_COLUMNS)
    fk = ("" if outside else
          ",\n  CONSTRAINT `fk_green_trips_pu` FOREIGN KEY (`pulocationid`) "
          "REFERENCES `taxi_zone` (`locationid`),\n"
          "  CONSTRAINT `fk_green_trips_do` FOREIGN KEY (`dolocationid`) "
          "REFERENCES `taxi_zone` (`locationid`)")
    names = ", ".join(f"`{c}`" for c, _, _ in TRIP_COLUMNS)

    out = [f"""-- NYC TLC green taxi trips, January 2025, prepared by datasets/{DATABASE}/convert.py.
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

-- The trip archive has no natural key: two identical trips by one vendor in the same second are
-- indistinguishable and no trip identifier is published, so the primary key is a surrogate.
-- Timestamps are local wall-clock (the Parquet says isAdjustedToUTC=false), which is why they are
-- DATETIME and not TIMESTAMP.
CREATE TABLE `green_trips` (
  `trip_id` INT NOT NULL AUTO_INCREMENT,
{columns},
  PRIMARY KEY (`trip_id`),
  KEY `ix_green_trips_pickup` (`pickup_datetime`),
  KEY `ix_green_trips_pu` (`pulocationid`),
  KEY `ix_green_trips_do` (`dolocationid`){fk}
) COMMENT = 'green (boro) taxi trips for 2025-01; dirty rows are kept deliberately';

-- {'-' * 60}
-- data

LOAD DATA LOCAL INFILE '{CONTEXT}/taxi_zone.tsv' INTO TABLE `taxi_zone`
  CHARACTER SET utf8mb4 (`locationid`, `borough`, `zone`, `service_zone`);
LOAD DATA LOCAL INFILE '{CONTEXT}/green_trips.tsv' INTO TABLE `green_trips`
  CHARACTER SET utf8mb4 ({names});

-- {'-' * 60}
-- view

CREATE SQL SECURITY INVOKER VIEW `v_trip_zone` AS
SELECT t.`trip_id`, t.`pickup_datetime`, t.`dropoff_datetime`, t.`trip_distance`,
       t.`total_amount`,
       pu.`borough` AS `pickup_borough`, pu.`zone` AS `pickup_zone`,
       do_.`borough` AS `dropoff_borough`, do_.`zone` AS `dropoff_zone`
FROM `green_trips` t
LEFT JOIN `taxi_zone` pu ON pu.`locationid` = t.`pulocationid`
LEFT JOIN `taxi_zone` do_ ON do_.`locationid` = t.`dolocationid`;

CREATE SQL SECURITY INVOKER VIEW `v_green_daily` AS
SELECT DATE(`pickup_datetime`) AS `trip_date`, COUNT(*) AS `trips`,
       ROUND(SUM(`total_amount`), 2) AS `revenue`,
       ROUND(AVG(`trip_distance`), 4) AS `avg_distance`
FROM `green_trips` GROUP BY DATE(`pickup_datetime`);

-- The archive is well known for out-of-range rows. They are kept -- the TLC states the data was not
-- created by the TLC and makes no representation as to its accuracy -- and this view names them.
CREATE SQL SECURITY INVOKER VIEW `v_suspect_trips` AS
SELECT * FROM `green_trips`
WHERE `passenger_count` = 0 OR `total_amount` <= 0 OR `trip_distance` <= 0
   OR `trip_distance` > 100 OR `dropoff_datetime` < `pickup_datetime`
   OR DATE(`pickup_datetime`) NOT BETWEEN '2025-01-01' AND '2025-01-31';

SET SESSION foreign_key_checks = 1;
"""]
    open(dest, "w", encoding="utf-8").write("\n".join(out))
    with open(os.path.join(context, "baseline.txt"), "w") as fh:
        fh.write(f"total_amount={totals[0]}\nfare_amount={totals[1]}\ntrip_distance={totals[2]}\n")

    print(f"  . {trips:,} green trips and {zone_rows} taxi zones from Parquet via DuckDB")
    print(f"  . source sums: total_amount {totals[0]:,}, fare_amount {totals[1]:,}, "
          f"trip_distance {totals[2]:,}")
    print(f"  . zone ids outside the lookup: {outside} -> foreign keys "
          f"{'enabled' if not outside else 'omitted'}")


if __name__ == "__main__":
    main()
