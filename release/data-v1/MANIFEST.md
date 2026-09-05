# data-v1 release assets

Staged by `python3 scripts/release.py stage`. **Not published**: creating the GitHub release,
uploading these files and making them public is the maintainer's decision (PLAN.md task R-02).

Each file here is an *upstream source artifact*, not a converted database. It is mirrored
because a third party cannot otherwise obtain and verify it — either upstream has no stable
URL, or its content changes underneath the recorded checksum. Everything else the build
downloads has a stable URL with a pinned sha256 in `manifest.yaml` and is deliberately absent.

Verify with `sha256sum -c SHA256SUMS`, or `python3 scripts/release.py check`.

| asset | size | licence | mirrored because |
|---|---:|---|---|
| `beer.stackexchange.com.7z` | 4.3 MB | [cc-by-sa-4-0](../../knowledge/licenses/cc-by-sa-4-0.md) | the archive.org item could be taken down |
| `chicago-crimes-2024.csv` | 74.8 MB | [chicago-data-portal-terms](../../knowledge/licenses/chicago-data-portal-terms.md) | the portal's data changes daily |
| `chicago-iucr.csv` | 0.0 MB | [chicago-data-portal-terms](../../knowledge/licenses/chicago-data-portal-terms.md) | the portal's data changes daily |
| `dba.stackexchange.com.7z` | 319.3 MB | [cc-by-sa-4-0](../../knowledge/licenses/cc-by-sa-4-0.md) | the archive.org item could be taken down |
| `lahman_1871-2025_csv.zip` | 42.2 MB | [cc-by-sa-3-0](../../knowledge/licenses/cc-by-sa-3-0.md) | SABR publishes it through a Box share with no static URL |

## Attribution travels with these files

* **Lahman** is CC BY-SA 3.0: the SABR notice in `datasets/lahman/LICENSE` must accompany any
  redistribution, and a modified database must be offered under the same licence.
* **Chicago** data carries a **mandatory verbatim disclaimer**, reproduced in `NOTICE.md` and
  `README.md`; the City also reserves the right to require distribution to stop.
* **Stack Exchange** content is CC BY-SA 4.0 with per-post attribution requirements; the
  `contentlicense` column is preserved per row. The project sources the 2024-04 archive.org
  snapshot, which predates the current click-through — a contract it has never accepted.

No Citi Bike or Divvy data is here, and none may be added: both licences prohibit
redistribution as a stand-alone dataset. No TPC-generated data is here either.
`scripts/release.py` refuses either regardless of what its asset list says.
