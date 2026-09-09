# sqlite release assets

Staged by `python3 -m megasamples release stage --set sqlite`. **Not published**: creating the
release, uploading these files and making them public is the maintainer's decision.

One SQLite file per core database, ported from the verified MySQL corpus and checked against the
same counts, content digests, foreign keys and indexes (`knowledge/decisions/sqlite-file-conventions.md`),
plus `megasamples.sqlite`, the provenance registry. Each database keeps its own upstream licence,
named below and in full in `datasets/<name>/LICENSE`; the share-alike ones stay under their terms.

Verify with `sha256sum -c SHA256SUMS`, or `python3 -m megasamples release check --set sqlite`.

| file | size | dataset | licence |
|---|---:|---|---|
| `adventureworks.sqlite` | 127.6 MB | `adventureworks` | mit |
| `adventureworks_lt.sqlite` | 2.9 MB | `adventureworks_lt` | mit |
| `chicago_crimes.sqlite` | 70.4 MB | `chicago_crimes` | chicago-data-portal-terms |
| `chinook.sqlite` | 1.0 MB | `chinook` | mit |
| `contoso.sqlite` | 84.7 MB | `contoso` | mit |
| `dvdstore.sqlite` | 10.0 MB | `dvdstore` | gpl-2-0 |
| `employees.sqlite` | 244.4 MB | `employees` | cc-by-sa-3-0 |
| `enron.sqlite` | 31.0 MB | `enron` | enron-public-record |
| `jaffle_shop.sqlite` | 0.0 MB | `jaffle_shop` | apache-2-0 |
| `lahman.sqlite` | 64.8 MB | `lahman` | cc-by-sa-3-0 |
| `megasamples.sqlite` | 0.1 MB | `-` | - |
| `northwind.sqlite` | 1.0 MB | `northwind` | mit |
| `nyc_taxi.sqlite` | 8.8 MB | `nyc_taxi` | nyc-open-data-terms |
| `oracle_co.sqlite` | 0.7 MB | `oracle_co` | mit |
| `oracle_hr.sqlite` | 0.2 MB | `oracle_hr` | mit |
| `oracle_oe.sqlite` | 2.5 MB | `oracle_oe` | mit |
| `oracle_sh.sqlite` | 114.1 MB | `oracle_sh` | mit |
| `pubs.sqlite` | 0.2 MB | `pubs` | mit |
| `sakila.sqlite` | 5.1 MB | `sakila` | bsd-3-clause-sakila |
| `smallsets.sqlite` | 0.2 MB | `smallsets` | hbiostat-data-permission, cc-by-4-0, cc0-1-0 |
| `stackexchange_beer.sqlite` | 17.4 MB | `stackexchange_beer` | cc-by-sa-4-0 |
| `wikipedia_simple.sqlite` | 122.6 MB | `wikipedia_simple` | cc-by-sa-4-0, gfdl-1-3 |
