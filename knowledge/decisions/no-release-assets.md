---
type: Decision
title: "No release assets: the repository is what is published, and every byte of data comes from its upstream to the user's machine"
description: The maintainer publishes only the repository -- no data-v1 mirror of upstream artifacts, no SQLite file set -- so nothing the project builds is redistributed by it; what a script cannot fetch (the lahman zip behind a share link) the user obtains by hand, and an upstream that has moved since it was pinned (the Chicago 2024 extract) is accepted explicitly with MEGASAMPLES_ACCEPT_DRIFT=1, which re-pins the manifest, after which the dataset's expectations are re-pinned from the MySQL build.
resource: /decisions/no-release-assets.md
tags:
- decision
- release
- licensing
- downloads
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-10T02:40:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-10T02:40:00Z"
sources:
- resource: /runbooks/clean-room-build.md
  title: the first-time build that found the two artifacts a script cannot verify
  accessed: "2026-09-10"
- resource: /datasets/chicago-crimes.md
  title: the Chicago extract and its re-pinning to the 2026-09-09 snapshot
  accessed: "2026-09-10"
---

# Question
Two core artifacts cannot be fetched and verified by a script from their upstream: the lahman zip
sits behind a SABR share link with no static URL, and the City of Chicago amends its 2024 crimes
extract, so the bytes the manifest pinned on 2026-09-03 were no longer what the portal served on
2026-09-09. Until now the project staged a `data-v1` set of "release assets" that would mirror
such artifacts, plus a `sqlite` set of the ported files, for the maintainer to publish. Should
anything be published beside the repository?

# Options considered
1. Publish the `data-v1` mirror and the `sqlite` set as GitHub release assets, with the manifest
   carrying the release URLs as mirrors -- rejected by the maintainer on 2026-09-10: nothing but
   the repository will be published.
2. **Publish only the repository. What a script cannot fetch, the user obtains by hand; what has
   moved since it was pinned, the user accepts explicitly, and the pins follow** (chosen).

# Evidence
* The clean-room build ([runbook](/runbooks/clean-room-build.md)) showed what a first-time user
  meets: the fetch names both artifacts, the build goes on without them, and the README says what
  to do.
* `megasamples/fetch.py`: a `manual` artifact's message names the URL to download from and the path
  to put the file at; a size or digest mismatch on any artifact names `MEGASAMPLES_ACCEPT_DRIFT=1`,
  which accepts the bytes, re-pins `sha256` and `size_bytes` in `manifest.yaml`, and says that the
  dataset's own expectations must be re-pinned with `megasamples verify <dataset> --pin` after the
  MySQL build; `tests/test_fetch.py` covers both paths with `file://` sources.
* `chicago_crimes` re-pinned to the 2026-09-09 extract (259,607 rows, up from 259,267): verified on
  MySQL, PostgreSQL and SQLite with 0 failures ([record](/datasets/chicago-crimes.md)).

# Outcome
Option 2. `megasamples/release.py`, `release/` and the `make release` targets are gone; the audit
and the pre-publication checklist cover the repository and the images. The five manifest mirrors
that pointed at the never-published release are removed (the `mirrors` mechanism stays for any
artifact that has a second upstream). The SQLite files remain under `build/sqlite/<database>/`
and inside `sql-megasamples-sqlite`, where `docker cp` takes one out. Reproducibility is per
snapshot: the manifest and the tests pin one extract, an accepted drift moves both, and the log
records when they moved.

# Status
accepted
