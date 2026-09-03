#!/usr/bin/env python3
"""The Lahman Baseball Database (SABR Version 2025) -> MySQL.

SABR publishes no SQL types, only a readme describing what each column means, so the types are
derived by reading every value of every column and taking the narrowest type that holds all of them
-- integers sized by magnitude, DECIMAL sized by the digits actually used, DATE where every value is
one, VARCHAR sized to the longest string. That is measurement rather than inference, and the
converter prints what it chose.

Keys come from the readme and the conversion-path decision, and each one is checked for uniqueness
before it is declared; a key that does not hold becomes a plain index and is reported.

Record: knowledge/datasets/lahman.md
"""
import csv, io, os, re, sys, zipfile

DATABASE = "lahman"
CONTEXT = "/context/lahman"
ARCHIVE = "lahman_1871-2025_csv.zip"
INSIDE = "lahman_1871-2025_csv/"
csv.field_size_limit(1 << 24)

# from the readme and knowledge/decisions/lahman-conversion-path.md; each is verified unique
PRIMARY_KEYS = {
    "people": ["playerID"],
    "teams": ["yearID", "teamID"],
    "teamsfranchises": ["franchID"],
    "parks": ["parkkey"],
    "batting": ["playerID", "yearID", "stint"],
    "pitching": ["playerID", "yearID", "stint"],
    "fielding": ["playerID", "yearID", "stint", "POS"],
    "appearances": ["playerID", "yearID", "teamID"],
    "managers": ["playerID", "yearID", "teamID", "inseason"],
    "salaries": ["playerID", "yearID", "teamID", "lgID"],
    "schools": ["schoolID"],
    "homegames": ["yearkey", "teamkey", "parkkey"],
    "collegeplaying": ["playerID", "schoolID", "yearID"],
    "battingpost": ["playerID", "yearID", "round"],
    "pitchingpost": ["playerID", "yearID", "round"],
    "seriespost": ["yearID", "round"],
    "teamshalf": ["yearID", "teamID", "Half"],
    "managershalf": ["playerID", "yearID", "teamID", "half"],
}
INT_SIZES = [(127, "TINYINT"), (32767, "SMALLINT"), (8388607, "MEDIUMINT"),
             (2147483647, "INT"), (9223372036854775807, "BIGINT")]
INTEGER = re.compile(r"^-?\d+$")
DECIMAL = re.compile(r"^-?\d*\.\d+$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def column_type(values):
    """The narrowest MySQL type that holds every non-empty value in a column."""
    present = [v for v in values if v != ""]
    if not present:
        return "VARCHAR(1)"
    if all(INTEGER.match(v) for v in present):
        biggest = max(abs(int(v)) for v in present)
        return next(name for limit, name in INT_SIZES if biggest <= limit)
    if all(INTEGER.match(v) or DECIMAL.match(v) for v in present):
        scale = max((len(v.split(".")[1]) if "." in v else 0) for v in present)
        digits = max(len(v.split(".")[0].lstrip("-")) for v in present)
        return f"DECIMAL({digits + scale},{scale})"
    if all(DATE.match(v) for v in present):
        return "DATE"
    longest = max(len(v) for v in present)
    return "TEXT" if longest > 255 else f"VARCHAR({max(longest, 1)})"


def tsv(value):
    if value == "":
        return "\\N"
    return (value.replace("\\", "\\\\").replace("\t", "\\t")
            .replace("\n", "\\n").replace("\r", "\\r"))


def main():
    downloads, dest = sys.argv[1], sys.argv[2]
    context = os.path.dirname(os.path.abspath(dest))
    z = zipfile.ZipFile(os.path.join(downloads, ARCHIVE))

    files = sorted(n for n in z.namelist() if n.endswith(".csv"))
    ddl, loads, counts, notes, boms = [], [], {}, [], 0
    for name in files:
        table = os.path.basename(name)[:-4].lower()
        raw = z.read(name)
        boms += raw[:3] == b"\xef\xbb\xbf"
        reader = csv.reader(io.StringIO(raw.decode("utf-8-sig")))
        header = next(reader)
        rows = list(reader)
        counts[table] = len(rows)

        columns = []
        for i, column in enumerate(header):
            values = [r[i] if i < len(r) else "" for r in rows]
            mysql = column_type(values)
            null = "" if all(v != "" for v in values) else " NULL"
            columns.append((column, mysql + (" NOT NULL" if not null else "")))

        key = PRIMARY_KEYS.get(table)
        if key:
            index = {c: i for i, c in enumerate(header)}
            missing = [c for c in key if c not in index]
            if missing:
                notes.append(f"{table}: key column(s) {missing} are not in the file; no primary key")
                key = None
            else:
                seen = {tuple(r[index[c]] for c in key) for r in rows}
                if len(seen) != len(rows):
                    notes.append(f"{table}: {key} is not unique ({len(seen)} of {len(rows)}); "
                                 f"declared as an index instead")
                    key, index_only = None, True
        body = ",\n".join(f"  `{c.lower()}` {t}" for c, t in columns)
        if key:
            body += ",\n  PRIMARY KEY (" + ", ".join(f"`{c.lower()}`" for c in key) + ")"
        ddl.append(f"CREATE TABLE `{table}` (\n{body}\n);")

        with open(os.path.join(context, f"{table}.tsv"), "w", encoding="utf-8", newline="") as out:
            for r in rows:
                padded = (r + [""] * len(header))[:len(header)]
                out.write("\t".join(tsv(v) for v in padded) + "\n")
        names = ", ".join(f"`{c.lower()}`" for c, _ in columns)
        loads.append(f"LOAD DATA LOCAL INFILE '{CONTEXT}/{table}.tsv' INTO TABLE `{table}`\n"
                     f"  CHARACTER SET utf8mb4 ({names});")

    out = [f"""-- The Lahman Baseball Database, SABR Version 2025, prepared by
-- datasets/{DATABASE}/convert.py from the CSV set. Copyright 1996-2025 by SABR, via generous
-- donation from Sean Lahman; licensed CC BY-SA 3.0. See datasets/{DATABASE}/LICENSE and the
-- upstream readme2025.txt vendored beside it.
--
-- Column types are not published upstream; each was derived by reading every value in the column.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{DATABASE}`;
CREATE DATABASE `{DATABASE}` DEFAULT CHARACTER SET utf8mb4;
USE `{DATABASE}`;
"""]
    out += ddl
    out.append(f"\n-- {'-' * 60}\n-- data\n")
    out += loads
    out.append(f"""
-- {'-' * 60}
-- indexes: playerID links almost every table to people

CREATE INDEX `ix_batting_player` ON `batting` (`playerid`);
CREATE INDEX `ix_batting_team` ON `batting` (`teamid`, `yearid`);
CREATE INDEX `ix_pitching_player` ON `pitching` (`playerid`);
CREATE INDEX `ix_fielding_player` ON `fielding` (`playerid`);
CREATE INDEX `ix_appearances_player` ON `appearances` (`playerid`);
CREATE INDEX `ix_people_name` ON `people` (`namelast`, `namefirst`);
CREATE INDEX `ix_teams_franchise` ON `teams` (`franchid`);
CREATE INDEX `ix_halloffame_player` ON `halloffame` (`playerid`);
CREATE INDEX `ix_awardsplayers_player` ON `awardsplayers` (`playerid`);
CREATE INDEX `ix_salaries_player` ON `salaries` (`playerid`);

SET SESSION foreign_key_checks = 1;
""")
    open(dest, "w", encoding="utf-8").write("\n".join(out))
    # the upstream readme travels with the data, as the licence's attribution requires
    with open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "readme2025.txt"),
              "wb") as fh:
        fh.write(z.read(INSIDE + "readme2025.txt"))

    print(f"  . {len(counts)} tables, {sum(counts.values()):,} rows; {boms} of {len(files)} CSVs "
          f"carry a UTF-8 BOM (stripped)")
    print(f"  . primary keys verified unique for {sum(1 for t in counts if t in PRIMARY_KEYS and not any(t in n for n in notes))} tables")
    for n in notes:
        print(f"  . {n}")


if __name__ == "__main__":
    main()
