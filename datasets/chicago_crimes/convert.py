#!/usr/bin/env python3
"""Chicago crimes, calendar year 2024, plus the IUCR code lookup -> MySQL.

The source moves daily, so the snapshot is identified by three things together -- the sha256 in
manifest.yaml, the row count, and `X-SODA2-Truth-Last-Modified` -- rather than by a checksum alone.
The converter records the count it saw so a later fetch that drifts is visible rather than silent.

The City's terms make one paragraph mandatory wherever this data is redistributed; it is written
into the generated SQL and into the table comment, not just into a licence file.

Record: knowledge/datasets/chicago-crimes.md
"""
import os, sys

import duckdb

DATABASE = "chicago_crimes"
CONTEXT = "/context/chicago_crimes"
CRIMES = "crimes_2024.csv"
IUCR = "iucr.csv"
DISCLAIMER = (
    "This site provides applications using data that has been modified for use from its original "
    "source, www.cityofchicago.org, the official website of the City of Chicago. The City of "
    "Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of "
    "the data provided at this site. The data provided at this site is subject to change at any "
    "time. It is understood that the data provided at this site is being used at one's own risk.")

# (MySQL column, MySQL type, DuckDB expression)
CRIME_COLUMNS = [
    ("id", "INT UNSIGNED NOT NULL", "id"),
    ("case_number", "VARCHAR(16)", "case_number"),
    ("date", "DATETIME", '"date"'),
    ("block", "VARCHAR(64)", "block"),
    ("iucr", "CHAR(4)", "iucr"),
    ("primary_type", "VARCHAR(40)", "primary_type"),
    ("description", "VARCHAR(80)", "description"),
    ("location_description", "VARCHAR(80)", "location_description"),
    ("arrest", "TINYINT(1)", "CAST(arrest AS TINYINT)"),
    ("domestic", "TINYINT(1)", "CAST(domestic AS TINYINT)"),
    ("beat", "SMALLINT", "CAST(beat AS SMALLINT)"),
    ("district", "TINYINT", "CAST(district AS TINYINT)"),
    ("ward", "TINYINT", "CAST(ward AS TINYINT)"),
    ("community_area", "TINYINT", "CAST(community_area AS TINYINT)"),
    ("fbi_code", "VARCHAR(4)", "fbi_code"),
    ("x_coordinate", "INT", "x_coordinate"),
    ("y_coordinate", "INT", "y_coordinate"),
    ("year", "SMALLINT", '"year"'),
    ("updated_on", "DATETIME", "updated_on"),
    ("latitude", "DECIMAL(9,6)", "latitude"),
    ("longitude", "DECIMAL(9,6)", "longitude"),
]
COPY_OPTIONS = "(FORMAT CSV, DELIMITER '\t', HEADER false, NULLSTR '\\N', QUOTE '', ESCAPE '')"


def main():
    downloads, dest = sys.argv[1], sys.argv[2]
    context = os.path.dirname(os.path.abspath(dest))
    crimes = os.path.join(downloads, CRIMES).replace("'", "''")
    iucr = os.path.join(downloads, IUCR).replace("'", "''")
    con = duckdb.connect()
    source = f"read_csv('{crimes}', header=true)"

    rows = con.execute(f"SELECT COUNT(*) FROM {source}").fetchone()[0]
    distinct_ids = con.execute(f"SELECT COUNT(DISTINCT id) FROM {source}").fetchone()[0]
    if rows != distinct_ids:
        sys.exit(f"id is not unique: {rows} rows, {distinct_ids} distinct")
    # case_number is documented as non-unique, so it is not a key; record what this snapshot holds
    distinct_cases = con.execute(f"SELECT COUNT(DISTINCT case_number) FROM {source}").fetchone()[0]

    projection = ", ".join(f"{expr} AS {name}" for name, _, expr in CRIME_COLUMNS)
    con.execute(f"COPY (SELECT {projection} FROM {source} ORDER BY id) "
                f"TO '{os.path.join(context, 'crimes.tsv')}' {COPY_OPTIONS}")

    codes = f"read_csv('{iucr}', header=true)"
    code_rows = con.execute(f"SELECT COUNT(*) FROM {codes}").fetchone()[0]
    con.execute(f"""COPY (SELECT "IUCR" AS iucr, "PRIMARY DESCRIPTION" AS primary_description,
                                 "SECONDARY DESCRIPTION" AS secondary_description,
                                 "INDEX CODE" AS index_code,
                                 CAST("ACTIVE" AS TINYINT) AS active
                          FROM {codes} ORDER BY "IUCR")
                    TO '{os.path.join(context, 'iucr.tsv')}' {COPY_OPTIONS}""")

    # a foreign key onto the lookup is only defensible if every code in the data is present
    orphans = con.execute(
        f'SELECT COUNT(*) FROM {source} c WHERE c.iucr NOT IN (SELECT "IUCR" FROM {codes})'
    ).fetchone()[0]
    fk = ("" if orphans else
          ",\n  CONSTRAINT `fk_crimes_iucr` FOREIGN KEY (`iucr`) REFERENCES `iucr` (`iucr`)")

    columns = ",\n".join(f"  `{name}` {mysql}" for name, mysql, _ in CRIME_COLUMNS)
    names = ", ".join(f"`{c}`" for c, _, _ in CRIME_COLUMNS)
    comment = DISCLAIMER.replace("'", "''")

    out = [f"""-- Chicago crimes (calendar year 2024), prepared by datasets/{DATABASE}/convert.py.
--
-- The City of Chicago requires this paragraph wherever the data is redistributed:
--
--   {DISCLAIMER}
--
-- The Chicago Police Department adds that the data reflects reported incidents that have not been
-- verified, and that attempts to derive specific addresses from it are strictly prohibited: the
-- block column is deliberately truncated to the hundred block for that reason.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{DATABASE}`;
CREATE DATABASE `{DATABASE}` DEFAULT CHARACTER SET utf8mb4;
USE `{DATABASE}`;

CREATE TABLE `iucr` (
  `iucr` CHAR(4) NOT NULL,
  `primary_description` VARCHAR(40) NOT NULL,
  `secondary_description` VARCHAR(80) NOT NULL,
  `index_code` CHAR(1),
  `active` TINYINT(1),
  PRIMARY KEY (`iucr`)
) COMMENT = 'Illinois Uniform Crime Reporting codes';

CREATE TABLE `crimes` (
{columns},
  PRIMARY KEY (`id`),
  KEY `ix_crimes_date` (`date`),
  KEY `ix_crimes_iucr` (`iucr`),
  KEY `ix_crimes_primary_type` (`primary_type`),
  KEY `ix_crimes_beat` (`beat`),
  KEY `ix_crimes_district` (`district`),
  KEY `ix_crimes_community_area` (`community_area`){fk}
) COMMENT = '{comment[:900]}';

-- {'-' * 60}
-- data

LOAD DATA LOCAL INFILE '{CONTEXT}/iucr.tsv' INTO TABLE `iucr`
  CHARACTER SET utf8mb4 (`iucr`, `primary_description`, `secondary_description`, `index_code`,
  `active`);
LOAD DATA LOCAL INFILE '{CONTEXT}/crimes.tsv' INTO TABLE `crimes`
  CHARACTER SET utf8mb4 ({names});

SET SESSION foreign_key_checks = 1;
"""]
    open(dest, "w", encoding="utf-8").write("\n".join(out))

    print(f"  . {rows:,} crimes for 2024 and {code_rows} IUCR codes")
    print(f"  . id is unique across all {distinct_ids:,} rows; case_number has "
          f"{distinct_cases:,} distinct values, so it is not a key")
    print(f"  . IUCR codes absent from the lookup: {orphans} -> foreign key "
          f"{'enabled' if not orphans else 'omitted'}")


if __name__ == "__main__":
    main()
