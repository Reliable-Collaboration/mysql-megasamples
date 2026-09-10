---
type: Tool
title: archive.org as a secondary mirror for upstream artifacts and release bundles
description: The ia CLI / IAS3 API let the project upload redistributable upstream archives and its own bundles to archive.org items; uploads must be non-infringing (Terms of Use not readable this session); throughput and availability are undocumented, so archive.org is a fallback URL in the manifest, never the only source.
resource: https://archive.org/developers/internetarchive/
tags:
- tool
- archive-org
- mirroring
- downloads
status: stable
trust: inferred
stale_after: "2027-03-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:49:47Z"
sources:
- resource: https://archive.org/developers/internetarchive/
  accessed: "2026-09-02"
- resource: https://archive.org/developers/internetarchive/cli.html
  accessed: "2026-09-02"
- resource: https://archive.org/developers/ias3.html
  accessed: "2026-09-02"
- resource: https://help.archive.org/help/rights/
  accessed: "2026-09-02"
- resource: https://help.archive.org/help/uploading-a-basic-guide/
  accessed: "2026-09-02"
- resource: /sources/build-machine-environment-2026-09-02.md
  title: Environment survey (archive.org has no AAAA record)
  accessed: "2026-09-02"
---

# Facts
* Tooling: `pip install internetarchive` provides the `ia` CLI and Python API ([AGPL-3](/licenses/agpl-3-0.md) licensed library); `ia configure` stores the IAS3 access/secret keys; `ia upload <identifier> file1 file2 --metadata="mediatype:texts" --metadata="blah:arg"`; "unless specified otherwise, items will be uploaded with a data mediatype. This cannot be changed afterwards."; `--retries` "to retry on errors (i.e. if IA-S3 is overloaded)"; `ia download <identifier> --glob="*.mp4"`; `ia metadata <identifier> --modify="foo:bar"` ([library](/sources/archive-org-developers-internetarchive.md), [CLI](/sources/archive-org-developers-cli.md)).
* IAS3 API: endpoint `s3.us.archive.org`, items are buckets; header `authorization: LOW :`; new items need `x-archive-auto-make-bucket:1` and `x-archive-meta-mediatype/collection/title`; `x-archive-queue-derive:0` prevents derivative generation; `x-archive-size-hint:` for large items; overload returns `503 SlowDown`; a limit check endpoint exists (`?check_limit=1`) ([IAS3](/sources/archive-org-developers-ias3.md)).
* Rights: "users make use of the Internet Archive's Collections at their own risk and ensure that such use is non-infringing and in accordance with all applicable laws"; the Archive "cannot guarantee information posted on item details or collection pages regarding copyright" and removes infringing content on notice ([rights](/sources/archive-org-help-rights.md)).
* Uploading guide: no size limits stated; post-upload tasks "can take seconds, hours or days depending on the amount and type of data uploaded"; test-collection items are deleted after ~30 days ([uploading guide](/sources/archive-org-help-uploading-guide.md)).
* Networking: `archive.org` resolves to IPv4 only on the build machine (no AAAA), so it is immune to the IPv6 hang described in the [runbook](/runbooks/ipv6-and-privileges.md) ([environment survey](/sources/build-machine-environment-2026-09-02.md)).
* Precedent in this bundle: the Stack Exchange data dump is itself distributed through archive.org (see [dataset-group question](/questions/stackexchange-archive-org-item-persistence.md)).

# Inferred
* **Inferred:** the Terms of Use page (https://archive.org/about/terms.php) renders only through JavaScript and the Wayback Machine is not reachable from this session, so the exact upload warranty wording is unverified; the help-centre rights page is the closest authoritative text. Treat the obligation as: upload only content whose license permits redistribution, carry the license and attribution in item metadata, and never upload click-through-licensed or "personal use only" material.
* **Inferred:** public download URLs follow `https://archive.org/download/<identifier>/<filename>`; download speed varies widely and items can be dark-listed after a takedown — hence "fallback, not primary".
* **Inferred:** one item per dataset+version (`sql-megasamples-<slug>-<version>`) with `mediatype:data`, `collection:opensource_media` (or whatever `ia upload` defaults to for new accounts), sha256 sidecars, and `x-archive-queue-derive:0`.

# Limits
1. Not a documented CDN: no SLA, no bandwidth guarantee, possible 503 SlowDown on upload; `megasamples/fetch.py` tries the canonical URL first, then a GitHub release asset, then archive.org, verifying sha256 each time.
2. Only redistributable datasets may be mirrored (CC0, CC BY, BSD/MIT-licensed samples, public-record data); datasets under click-through EULAs are never mirrored.
3. The AGPL-3 `internetarchive` package is a maintainer-side tool, never shipped in the image.

# Open questions
* Read the archive.org Terms of Use from a browser and record the upload warranty paragraph verbatim (5 minutes, maintainer task); until then the mirroring step stays behind a manual approval.
