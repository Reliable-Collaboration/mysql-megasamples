#!/usr/bin/env python3
"""Load one month of Citi Bike or Divvy trips, fetched by you rather than shipped by us.

  MEGASAMPLES_ACCEPT_BIKESHARE_LICENSE=1 python3 -m megasamples bikeshare citibike [--month JC-202602]

These two datasets are the only ones in the project whose data is **never** redistributed -- not in
the image, not as a release asset, not mirrored. Both licences grant a broad right to use and to
"distribute in your product or service", and then forbid you to

    "Host, stream, publish, distribute, sublicense, or sell the Data as a stand-alone dataset"

with a carve-out only for "analyses, reports, or studies ... for non-commercial purposes". A Docker
image whose entire value for this dataset *is* the dataset reads as the prohibited thing, so the
project takes the conservative reading and ships this loader instead. You fetch from Lyft's own
interface, which is where the licence attaches, and you accept it directly. That is safe under
either reading, which is why it is the design even though the question is unresolved
(knowledge/questions/citibike-divvy-redistribution.md).

Two things the records warn about and this respects:

* **The bucket is listed and matched, never templated.** Citi Bike's keys include
  `JC-201708 citibike-tripdata.csv.zip` (a space), `JC-202207-citbike-tripdata.csv.zip` (a typo),
  and months that drop the `.csv` infix. Constructing a name from a template finds nothing, or the
  wrong thing.
* **Archives are not one CSV.** Citi Bike's monthly zips hold several *stored* CSV parts, its yearly
  zips are zips of zips, and both systems' archives carry `__MACOSX/._*` members to skip.
"""
import argparse, csv, hashlib, io, os, re, subprocess, sys, zipfile
import xml.etree.ElementTree as ET

from megasamples.paths import ROOT, stage_dir
from megasamples.engines.mysql import server as db  # noqa: E402

ENV_FLAG = "MEGASAMPLES_ACCEPT_BIKESHARE_LICENSE"
S3_NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"

SYSTEMS = {
    "citibike": {
        "bucket": "https://s3.amazonaws.com/tripdata/",
        "database": "citibike",
        "default": "JC-202602",          # Jersey City: the smallest current-schema series
        "licence": "Citi Bike Data Use Policy",
        "url": "https://www.citibikenyc.com/data-sharing-policy",
        "attribution": "Citi Bike trip data, Lyft Bikes and Scooters, LLC.",
    },
    "divvy": {
        "bucket": "https://divvy-tripdata.s3.amazonaws.com/",
        "database": "divvy",
        "default": "202004",
        "licence": "Divvy Data License Agreement",
        "url": "https://divvybikes.com/data-license-agreement",
        "attribution": "Divvy trip data, Lyft Bikes and Scooters, LLC, "
                       "owned by the City of Chicago.",
    },
}

# The current 13-column layout, shared by both systems. Header spelling varies by era and series --
# Title Case with spaces in 2015, run-together lower case elsewhere -- so headers are matched after
# normalisation rather than literally.
COLUMNS = [
    ("ride_id", "VARCHAR(32) NOT NULL"),
    ("rideable_type", "VARCHAR(20)"),
    ("started_at", "DATETIME(3) NOT NULL"),
    ("ended_at", "DATETIME(3)"),
    ("start_station_name", "VARCHAR(120)"),
    ("start_station_id", "VARCHAR(32)"),
    ("end_station_name", "VARCHAR(120)"),
    ("end_station_id", "VARCHAR(32)"),
    ("start_lat", "DECIMAL(17,14)"),
    ("start_lng", "DECIMAL(17,14)"),
    ("end_lat", "DECIMAL(17,14)"),
    ("end_lng", "DECIMAL(17,14)"),
    ("member_casual", "VARCHAR(10)"),
]
WANTED = [c for c, _ in COLUMNS]


def notice(system):
    s = SYSTEMS[system]
    return f"""\
{s['licence']} ({s['url']})

  "Host, stream, publish, distribute, sublicense, or sell the Data as a stand-alone dataset;
   provided, however, you may include the Data as source material, as applicable, in analyses,
   reports, or studies published or distributed for non-commercial purposes"

This project never redistributes these trips: not in the published image, not as a release asset,
not mirrored. Running this downloads them from Lyft's own bucket to your machine, which is where the
licence attaches and how you accept it. What you then do with the loaded database is between you and
that agreement -- in particular, do not republish it as a dataset.

To accept and continue:

    {ENV_FLAG}=1 make load-{system}
"""


def require_acceptance(system, accepted):
    if not (accepted or os.environ.get(ENV_FLAG) == "1"):
        print(notice(system), file=sys.stderr)
        sys.exit(f"refusing to download: the {SYSTEMS[system]['licence']} has not been accepted "
                 f"(set {ENV_FLAG}=1 or pass --accept-license)")
    print(f"  ! {SYSTEMS[system]['licence']} accepted; downloading from Lyft's bucket to this "
          f"machine only")
    print(f"  ! {SYSTEMS[system]['url']} -- the data is never redistributed by this project")


def listing(bucket):
    """[(key, size, last modified)] from an anonymous S3 ListBucket, following continuations."""
    out, marker = [], ""
    while True:
        url = bucket + (f"?marker={marker}" if marker else "")
        p = subprocess.run(["curl", "-sS", "--fail", "--connect-timeout", "20", url],
                           capture_output=True, timeout=180)
        if p.returncode != 0:
            sys.exit(f"could not list {bucket}: {p.stderr.decode('utf-8', 'replace')[:200]}")
        root = ET.fromstring(p.stdout)
        for c in root.findall(f"{S3_NS}Contents"):
            out.append((c.findtext(f"{S3_NS}Key"), int(c.findtext(f"{S3_NS}Size")),
                        c.findtext(f"{S3_NS}LastModified")))
        if root.findtext(f"{S3_NS}IsTruncated") != "true" or not out:
            return out
        marker = out[-1][0]


def normalise(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def pick(keys, want):
    """The key matching `want`, compared with punctuation and case removed.

    This is why the bucket is listed: `JC-202207-citbike-tripdata.csv.zip` is a typo upstream and
    `JC-201708 citibike-tripdata.csv.zip` has a space, so neither is reachable from a template.
    """
    target = normalise(want)
    hits = [k for k in keys if target in normalise(k[0]) and k[0].lower().endswith(".zip")]
    if not hits:
        sample = ", ".join(k[0] for k in keys[:4])
        sys.exit(f"no archive matches '{want}'. The bucket holds {len(keys)} keys, e.g. {sample}")
    return min(hits, key=lambda k: k[1])          # the smallest match, if a prefix hits several


def fetch(bucket, key, dest):
    path = os.path.join(dest, os.path.basename(key).replace(" ", "_"))
    if not os.path.exists(path):
        url = bucket + key.replace(" ", "%20")
        p = subprocess.run(["curl", "-sS", "--fail", "--location", "--retry", "3",
                            "--connect-timeout", "20", "-o", path, url], capture_output=True)
        if p.returncode != 0:
            sys.exit(f"download failed: {p.stderr.decode('utf-8', 'replace')[:200]}")
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return path, h.hexdigest()


def csv_members(path, depth=0):
    """Every CSV inside the archive, recursing into inner zips and skipping macOS junk."""
    with zipfile.ZipFile(path) as z:
        for info in sorted(z.infolist(), key=lambda i: i.filename):
            name = info.filename
            if info.is_dir() or name.startswith("__MACOSX/") or os.path.basename(name).startswith("._"):
                continue
            if name.lower().endswith(".zip"):
                if depth > 2:
                    sys.exit(f"{name}: archives nested more than three deep")
                inner = io.BytesIO(z.read(name))
                yield from csv_members(inner, depth + 1)
            elif name.lower().endswith(".csv"):
                yield name, z.read(name)


def column_map(header, source):
    """Position of each wanted column in this file's header, matched after normalisation.

    A legacy file is refused rather than half-loaded: the 2015-era layout is 15 different columns
    (Trip Duration, Bike ID, Birth Year, Gender and no ride_id), which is a different table, not a
    spelling variation.
    """
    seen = {normalise(h): i for i, h in enumerate(header)}
    missing = [c for c in WANTED if normalise(c) not in seen]
    if missing:
        sys.exit(f"{source}: this file predates the current 13-column layout (missing "
                 f"{', '.join(missing)}). Choose a month from 2021-02 onward for Citi Bike or "
                 f"2020-04 onward for Divvy; the legacy layout is a different table and is not "
                 f"loaded into this one.")
    return [seen[normalise(c)] for c in WANTED]


def write_tsv(archive, out_path):
    """Every CSV part into one contract TSV. Returns (rows, files, empty station counts)."""
    rows = files = blank_start = blank_end = 0
    with open(out_path, "w", encoding="utf-8", newline="") as out:
        for name, blob in csv_members(archive):
            files += 1
            reader = csv.reader(io.StringIO(blob.decode("utf-8-sig", "replace")))
            order = column_map(next(reader), name)
            for row in reader:
                if not row or len(row) < len(order):
                    continue
                values = [row[i].strip() for i in order]
                blank_start += not values[4]
                blank_end += not values[6]
                out.write("\t".join(
                    "\\N" if v == "" else v.replace("\\", "\\\\").replace("\t", " ")
                    for v in values) + "\n")
                rows += 1
    return rows, files, blank_start, blank_end


def load(system, month, accepted, keep):
    s = SYSTEMS[system]
    require_acceptance(system, accepted)
    downloads = os.path.join(ROOT, "downloads", system)
    context = stage_dir(system)
    os.makedirs(downloads, exist_ok=True)
    os.makedirs(context, exist_ok=True)

    keys = listing(s["bucket"])
    key, size, modified = pick(keys, month or s["default"])
    print(f"  . {len(keys)} keys in the bucket; chose {key} ({size:,} bytes, {modified})")
    archive, digest = fetch(s["bucket"], key, downloads)
    print(f"  . sha256 {digest}")

    tsv = os.path.join(context, f"{system}_trips.tsv")
    rows, files, blank_start, blank_end = write_tsv(archive, tsv)
    print(f"  . {rows:,} trips from {files} CSV part(s); {blank_start:,} have no start station "
          f"and {blank_end:,} no end station (dockless trips)")

    columns = ",\n".join(f"  `{c}` {t}" for c, t in COLUMNS)
    names = ", ".join(f"`{c}`" for c, _ in COLUMNS)
    sql = f"""SET NAMES utf8mb4;
DROP DATABASE IF EXISTS `{s['database']}`;
CREATE DATABASE `{s['database']}` DEFAULT CHARACTER SET utf8mb4;
USE `{s['database']}`;

-- {s['attribution']} Source: {key}, sha256 {digest}, LastModified {modified}.
-- Licensed under the {s['licence']} ({s['url']}). NOT redistributable as a stand-alone dataset:
-- this database was downloaded to this machine by whoever ran the loader, and this project
-- neither ships nor mirrors it.
CREATE TABLE `trips` (
{columns},
  PRIMARY KEY (`ride_id`),
  KEY `ix_trips_started_at` (`started_at`),
  KEY `ix_trips_start_station` (`start_station_id`),
  KEY `ix_trips_end_station` (`end_station_id`)
) COMMENT = '{s["attribution"]} {s["licence"]}; not redistributable as a stand-alone dataset';

LOAD DATA LOCAL INFILE '/context/{system}/{system}_trips.tsv' INTO TABLE `trips`
  CHARACTER SET utf8mb4 ({names});
"""
    out_sql = os.path.join(context, f"{system}.sql")
    open(out_sql, "w", encoding="utf-8").write(sql)
    db.start()
    db.sql_file(out_sql)
    db.sql(f"ANALYZE TABLE `{s['database']}`.`trips`")
    loaded = int(db.rows(f"SELECT COUNT(*) FROM `{s['database']}`.`trips`")[0][0])
    mb = db.rows("SELECT ROUND(SUM(data_length+index_length)/1048576,1) FROM "
                 f"information_schema.tables WHERE table_schema='{s['database']}'")[0][0]
    print(f"  . loaded {loaded:,} of {rows:,} rows into `{s['database']}`, {mb} MB in InnoDB")
    if loaded != rows:
        print(f"  ! {rows - loaded:,} rows were not loaded -- LOAD DATA LOCAL implies IGNORE, so a "
              f"duplicate ride_id is dropped silently; the archive repeats some")
    if not keep:
        os.remove(tsv)
    return loaded


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("system", choices=sorted(SYSTEMS))
    ap.add_argument("--month", help="a key fragment, e.g. 202602 or JC-202602; matched, not templated")
    ap.add_argument("--accept-license", action="store_true")
    ap.add_argument("--keep-tsv", action="store_true", help="leave the staged TSV in place")
    a = ap.parse_args(argv)
    load(a.system, a.month, a.accept_license, a.keep_tsv)


if __name__ == "__main__":
    main()
